import hashlib
import json
from functools import cached_property
from typing import Any, Dict, Iterable, Optional, Tuple

import redis
from celery import Task


__all__ = (
    'LimitedTask',
)


class LockManager:
    """
    Manages Redis-backed counters for queue and concurrency locks.
    """

    def __init__(self, url: str, prefix: str) -> None:
        self._prefix = prefix
        self._client = redis.Redis.from_url(url)

    def _key(self, slot_type: str, task_name: str, signature: str) -> str:
        # e.g. celery-limited-tasks:queue:myapp.tasks.add:abc123
        return f"{self._prefix}:{slot_type}:{task_name}:{signature}"

    def acquire(
        self,
        slot_type: str,
        task_name: str,
        signature: str,
        limit: int,
        ttl: int,
    ) -> bool:
        key = self._key(slot_type, task_name, signature)
        pipe = self._client.pipeline()
        pipe.incr(key)
        pipe.ttl(key)
        new_count, current_ttl = pipe.execute()

        if new_count == 1:
            self._client.expire(key, ttl)
        elif new_count > limit:
            self._client.decr(key)
            return False
        else:
            if current_ttl < ttl:
                self._client.expire(key, ttl)
        return True

    def release(self, slot_type: str, task_name: str, signature: str) -> None:
        key = self._key(slot_type, task_name, signature)
        new_value = self._client.decr(key)
        if new_value <= 0:
            self._client.delete(key)

    def acquire_queue(self, task_name: str, signature: str, limit: int, ttl: int) -> bool:
        return self.acquire("queue", task_name, signature, limit, ttl)

    def release_queue(self, task_name: str, signature: str) -> None:
        self.release("queue", task_name, signature)

    def acquire_run(self, task_name: str, signature: str, limit: int, ttl: int) -> bool:
        return self.acquire("run", task_name, signature, limit, ttl)

    def release_run(self, task_name: str, signature: str) -> None:
        self.release("run", task_name, signature)


class LimitedTask(Task):
    """
    Celery Task base that enforces per-signature limits on queue size
    and concurrent execution.

    Usage in @app.task decorator via 'uts' dict:
      - queue_limit: max pending in queue (default 1)
      - concurrency_limit: max simultaneous runs (default 1)
      - lock_ttl: seconds before lock expiry (default 3600)
      - key_by: list of kwarg names to derive signature
    """
    abstract = True

    def __init__(self) -> None:
        super().__init__()
        broker_url = self.app.conf.broker_url
        prefix = self.app.conf.get(
            "LIMITED_TASKS_PREFIX", "celery-limited-tasks"
        )
        self._lock_manager = LockManager(url=broker_url, prefix=prefix)

    @cached_property
    def _uts(self) -> Dict[str, Any]:
        return getattr(self, "uts", {}) or {}

    def _get_queue_limit(self) -> int:
        return int(
            self._uts.get(
                "queue_limit",
                self.app.conf.get("LIMITED_TASKS_DEFAULT_QUEUE_LIMIT", 1),
            )
        )

    def _get_concurrency_limit(self) -> int:
        return int(
            self._uts.get(
                "concurrency_limit",
                self.app.conf.get("LIMITED_TASKS_DEFAULT_CONCURRENCY_LIMIT", 1),
            )
        )

    def _get_ttl(self) -> int:
        return int(
            self._uts.get(
                "lock_ttl",
                self.app.conf.get("LIMITED_TASKS_DEFAULT_TTL", 3600),
            )
        )

    def _get_key_by(self) -> Optional[Iterable[str]]:
        return self._uts.get("key_by")

    def _make_signature(
        self, args: Tuple[Any, ...], kwargs: Dict[str, Any]
    ) -> str:
        key_by = self._get_key_by()
        if key_by:
            subset = {k: kwargs[k] for k in key_by if k in kwargs}
        else:
            subset = {"args": args, "kwargs": kwargs}
        raw = json.dumps(subset, sort_keys=True, default=str)
        return hashlib.sha256(raw.encode()).hexdigest()

    def apply_async(
        self,
        args: Optional[Tuple[Any, ...]] = None,
        kwargs: Optional[Dict[str, Any]] = None,
        **options: Any,
    ):
        args = args or ()
        kwargs = kwargs or {}
        sig = self._make_signature(args, kwargs)
        queue_limit = self._get_queue_limit()
        ttl = self._get_ttl()

        if not self._lock_manager.acquire_queue(self.name, sig, queue_limit, ttl):
            return None

        hdrs = options.get("headers")
        if not isinstance(hdrs, dict):
            hdrs = {}
            options["headers"] = hdrs
        hdrs.setdefault("_limited_sig", sig)

        return super().apply_async(args=args, kwargs=kwargs, **options)

    def __call__(
        self, *args: Any, **kwargs: Any
    ) -> Any:
        # Safely retrieve headers dict
        hdrs = getattr(self.request, "headers", None)
        headers = hdrs if isinstance(hdrs, dict) else {}
        sig = headers.get("_limited_sig")

        if sig:
            self._lock_manager.release_queue(self.name, sig)
            concurrency_limit = self._get_concurrency_limit()
            ttl = self._get_ttl()
            if not self._lock_manager.acquire_run(
                self.name, sig, concurrency_limit, ttl
            ):
                queue_limit = self._get_queue_limit()
                if queue_limit > 0:
                    super().apply_async(
                        args=args,
                        kwargs=kwargs,
                        headers={"_limited_sig": sig},
                    )
                return None
            self.request._limited_run_acquired = True

        return super().__call__(*args, **kwargs)

    def after_return(
        self,
        status: str,
        retval: Any,
        task_id: str,
        args: Tuple[Any, ...],
        kwargs: Dict[str, Any],
        einfo: Any,
    ) -> None:
        if getattr(self.request, "_limited_run_acquired", False):
            hdrs = getattr(self.request, "headers", None)
            headers = hdrs if isinstance(hdrs, dict) else {}
            sig = headers.get("_limited_sig")
            if sig:
                self._lock_manager.release_run(self.name, sig)
        return super().after_return(
            status, retval, task_id, args, kwargs, einfo
        )
