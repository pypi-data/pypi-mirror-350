import pickle
from typing import Any, Optional

import traceback
from contextvars import copy_context

from dash.background_callback.managers import BaseBackgroundCallbackManager
from dash.background_callback._proxy_set_props import ProxySetProps
from dash._callback_context import context_value
from dash._utils import AttributeDict
from dash.exceptions import PreventUpdate


class RedisCache:
    def __init__(self, redis_url: str, prefix: str = 'cache:', expire: Optional[int] = None, **kwargs):
        """Initialize Redis cache.

        Args:
            redis_url: Redis connection URL (e.g., 'redis://localhost:6379/0')
            prefix: Key prefix for cache entries
            expire: Default expiration time in seconds
        """
        try:
            import redis
        except ImportError:
            raise ImportError("redis-py required: pip install redis")

        self.redis = redis.from_url(redis_url, **kwargs)
        self.prefix = prefix
        self.expire = expire

    def _key(self, key: str) -> str:
        return f"{self.prefix}{key}"

    def set(self, key: str, value: Any, expire: Optional[int] = None,
        retry: bool = False, **kwargs) -> bool:
        try:
            data = pickle.dumps(value)
            exp = expire if expire is not None else self.expire
            return bool(self.redis.set(self._key(key), data, ex=exp))
        except Exception:
            if retry: raise
            return False

    def get(self, key: str, default: Any = None, retry: bool = False, **kwargs) -> Any:
        try:
            data = self.redis.get(self._key(key))
            return pickle.loads(data) if data else default
        except Exception:
            if retry: raise
            return default

    def delete(self, key: str, retry: bool = False) -> bool:
        try:
            return bool(self.redis.delete(self._key(key)))
        except Exception:
            if retry: raise
            return False

    def touch(self, key: str, expire: Optional[int] = None, retry: bool = False) -> bool:
        try:
            exp = expire if expire is not None else self.expire
            if exp is None: return True
            return bool(self.redis.expire(self._key(key), exp))
        except Exception:
            if retry: raise
            return False

    def clear(self, retry: bool = False) -> int:
        try:
            keys = self.redis.keys(f"{self.prefix}*")
            return self.redis.delete(*keys) if keys else 0
        except Exception:
            if retry: raise
            return 0

    def close(self):
        try:
            self.redis.close()
        except Exception:
            pass

    def __setitem__(self, key: str, value: Any):
        self.set(key, value, retry=True)

    def __getitem__(self, key: str) -> Any:
        ENOVAL = object()  # sentinel value
        val = self.get(key, ENOVAL, retry=True)
        if val is ENOVAL: raise KeyError(key)
        return val

    def __delitem__(self, key: str):
        if not self.delete(key, retry=True): raise KeyError(key)

    def __contains__(self, key: str) -> bool:
        try:
            return bool(self.redis.exists(self._key(key)))
        except Exception:
            return False


    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.close()


class RedisBgManager(BaseBackgroundCallbackManager):
    """Redis-based background callback manager for dash background_callback_manager usage"""

    UNDEFINED = object()

    def __init__(self, cache: RedisCache = None, cacheBy=None, expire=None):
        """
        Long callback manager using Redis as backend

        :param cache:
            RedisCache instance is required
        :param cacheBy:
            List of zero-parameter functions. When provided, caching is enabled,
            and the return values of these functions are combined with callback function
            input parameters and source code to generate cache keys.
        :param expire:
            If provided, cache entries will be removed after expire seconds of no access.
            If not provided, cache entry lifecycle is determined by the cache instance's default behavior.
        """
        try:
            import psutil
            import multiprocess
        except ImportError as missing_imports:
            raise ImportError("please install: psutil multiprocess redis\n") from missing_imports

        if cache is None: raise ValueError("cache must be a RdsCacher")
        else:
            if not isinstance(cache, RedisCache): raise ValueError("cache must be a RdsCacher")
            self.handle = cache

        if cacheBy is not None and not isinstance(cacheBy, list): cacheBy = [cacheBy]

        self.expire = expire
        super().__init__(cacheBy)

    def terminate_job(self, job):
        import psutil

        if job is None: return

        job = int(job)

        if psutil.pid_exists(job):
            proc = psutil.Process(job)

            for child in proc.children(recursive=True):
                try:
                    child.kill()
                except psutil.NoSuchProcess:
                    pass

            try:
                proc.kill()
            except psutil.NoSuchProcess:
                pass

            try:
                proc.wait(1)
            except (psutil.TimeoutExpired, psutil.NoSuchProcess):
                pass

    def terminate_unhealthy_job(self, job):
        import psutil

        job = int(job)
        if job and psutil.pid_exists(job):
            if not self.job_running(job):
                self.terminate_job(job)
                return True

        return False

    def job_running(self, job):
        import psutil

        job = int(job)
        if job and psutil.pid_exists(job):
            proc = psutil.Process(job)
            return proc.status() != psutil.STATUS_ZOMBIE
        return False

    def make_job_fn(self, fn, progress, key=None):
        return _make_job_fn(fn, self.handle, progress)

    def clear_cache_entry(self, key):
        self.handle.delete(key)

    # noinspection PyUnresolvedReferences
    def call_job_fn(self, key, job_fn, args, ctx):
        from multiprocess import Process
        proc = Process(
            target=job_fn,
            args=(key, self._make_progress_key(key), args, ctx)
        )
        proc.start()
        return proc.pid

    def get_progress(self, key):
        progress_key = self._make_progress_key(key)
        progress_data = self.handle.get(progress_key)
        if progress_data: self.handle.delete(progress_key)

        return progress_data

    def result_ready(self, key):
        return key in self.handle

    def get_result(self, key, job):
        result = self.handle.get(key, self.UNDEFINED)
        if result is self.UNDEFINED: return self.UNDEFINED

        if self.cache_by is None: self.clear_cache_entry(key)
        else:
            if self.expire: self.handle.touch(key, expire=self.expire)

        self.clear_cache_entry(self._make_progress_key(key))

        if job:
            self.terminate_job(job)
        return result

    def get_updated_props(self, key):
        set_props_key = self._make_set_props_key(key)
        result = self.handle.get(set_props_key, self.UNDEFINED)
        if result is self.UNDEFINED: return {}

        self.clear_cache_entry(set_props_key)

        return result


    def register(self, key, fn, progress):
        self.func_registry[key] = self.make_job_fn(fn, progress, key)


def _make_job_fn(fn, cache, progress):
    def job_fn(result_key, progress_key, user_callback_args, context):
        def _set_progress(progress_value):
            if not isinstance(progress_value, (list, tuple)):
                progress_value = [progress_value]

            cache.set(progress_key, progress_value)

        maybe_progress = [_set_progress] if progress else []

        def _set_props(_id, props):
            cache.set(f"{result_key}-set_props", {_id: props})

        ctx = copy_context()

        def run():
            c = AttributeDict(**context)
            c.ignore_register_page = False
            c.updated_props = ProxySetProps(_set_props)
            context_value.set(c)
            errored = False
            user_callback_output = None
            try:
                if isinstance(user_callback_args, dict):
                    user_callback_output = fn(*maybe_progress, **user_callback_args)
                elif isinstance(user_callback_args, (list, tuple)):
                    user_callback_output = fn(*maybe_progress, *user_callback_args)
                else:
                    user_callback_output = fn(*maybe_progress, user_callback_args)
            except PreventUpdate:
                errored = True
                cache.set(result_key, {"_dash_no_update": "_dash_no_update"})
            except Exception as err:
                errored = True
                cache.set(
                    result_key,
                    {
                        "background_callback_error": {
                            "msg": str(err),
                            "tb": traceback.format_exc(),
                        }
                    },
                )

            if not errored:
                cache.set(result_key, user_callback_output)

        ctx.run(run)

    return job_fn


def NewRedisBgManager(redisUrl=None, prefix='app:', expire=3600, cacheBy=None, **kwargs):
    if redisUrl is None: raise ValueError("redisUrl is required")

    resc = RedisCache(redisUrl, prefix, expire, **kwargs)
    try:
        resc.redis.ping()
    except Exception as e:
        raise ConnectionError(f"Failed to connect to Redis url[{redisUrl}]: {e}")

    return RedisBgManager(resc, cacheBy=cacheBy, expire=expire)
