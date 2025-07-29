# === ПУТЬ К ФАЙЛУ: temporal_redis.py ===
"""
temporal_redis — утилиты для хранения/чтения результатов Temporal workflow
в Redis Hash с обязательным TTL (по умолчанию сутки), возможностью
программной настройки, встроенной retry-политикой и пакетными операциями.

Batch-функции:
  - store_results
  - get_results
  - exists_results
  - delete_results
"""

import os
import logging
from typing import Any, Optional, List, Dict

import orjson
from pydantic import BaseModel
from redis.asyncio import Redis
from redis.exceptions import RedisError, ConnectionError
from tenacity import (
    retry,
    stop_after_attempt,
    wait_exponential,
    retry_if_exception_type,
)

__all__ = [
    "configure",
    "store_result",
    "store_results",
    "get_result",
    "get_results",
    "exists_result",
    "exists_results",
    "delete_result",
    "delete_results",
    "ResultNotFoundError",
]

logger = logging.getLogger(__name__)

class ResultNotFoundError(Exception):
    """Поднимается, когда в Redis нет результата для данного workflow_id."""
    pass

# internal state (можно переопределить через configure)
_REDIS_URL: str = os.getenv("REDIS_URL", "redis://localhost:6379")
_DEFAULT_PREFIX: str = os.getenv("TEMPORAL_REDIS_PREFIX", "temporal:result:")
try:
    _DEFAULT_TTL: int = int(os.getenv("TEMPORAL_REDIS_TTL", str(24 * 3600)))
except ValueError:
    _DEFAULT_TTL = 24 * 3600

_redis_client: Optional[Redis] = None


def configure(
    *,
    redis_url: Optional[str] = None,
    prefix: Optional[str] = None,
    default_ttl: Optional[int] = None,
) -> None:
    """
    Программно настраивает:
      - redis_url: куда подключаться
      - prefix: префикс ключей
      - default_ttl: TTL по умолчанию (в секундах)

    Вызывать до первого использования store/get/etc.
    """
    global _REDIS_URL, _DEFAULT_PREFIX, _DEFAULT_TTL, _redis_client
    if redis_url is not None:
        _REDIS_URL = redis_url
        _redis_client = None
        logger.debug("Configured REDIS_URL=%s", redis_url)
    if prefix is not None:
        _DEFAULT_PREFIX = prefix
        logger.debug("Configured PREFIX=%s", prefix)
    if default_ttl is not None:
        _DEFAULT_TTL = default_ttl
        logger.debug("Configured DEFAULT_TTL=%ds", default_ttl)


def _get_redis() -> Redis:
    """
    Ленивая инициализация Redis-клиента.
    При первом вызове сверяет _REDIS_URL.
    """
    global _redis_client
    if _redis_client is None:
        try:
            _redis_client = Redis.from_url(_REDIS_URL)
            logger.debug("Connected to Redis at %s", _REDIS_URL)
        except ConnectionError as e:
            logger.error("Не удалось подключиться к Redis по %s: %s", _REDIS_URL, e)
            raise
    return _redis_client


def _key(workflow_id: str) -> str:
    """Собирает ключ вида <prefix><workflow_id>."""
    return f"{_DEFAULT_PREFIX}{workflow_id}"


# Общая retry-политика: до 5 попыток, экспоненциальный бэкофф
_retry_params = {
    "stop": stop_after_attempt(5),
    "wait": wait_exponential(multiplier=0.5, min=0.5, max=8),
    "retry": retry_if_exception_type((ConnectionError, RedisError)),
    "reraise": True,
}


@retry(**_retry_params)
async def store_result(
    workflow_id: str,
    result: Any,
    *,
    ttl: Optional[int] = None,
) -> None:
    """
    Сохраняет один result в Redis.
    """
    redis = _get_redis()
    key = _key(workflow_id)
    blob = result.json().encode() if isinstance(result, BaseModel) else orjson.dumps(result)
    logger.debug("Store [%s] → %d bytes", key, len(blob))
    await redis.hset(key, mapping={"data": blob})
    expire = ttl if ttl is not None else _DEFAULT_TTL
    await redis.expire(key, expire)
    logger.debug("Set TTL=%ds for key %s", expire, key)


@retry(**_retry_params)
async def store_results(
    mapping: Dict[str, Any],
    *,
    ttl: Optional[int] = None,
) -> None:
    """
    Пакетно сохраняет несколько результатов.
    :param mapping: workflow_id → result
    """
    redis = _get_redis()
    pipe = redis.pipeline()
    for workflow_id, result in mapping.items():
        key = _key(workflow_id)
        blob = result.json().encode() if isinstance(result, BaseModel) else orjson.dumps(result)
        logger.debug("Pipelining store [%s] → %d bytes", key, len(blob))
        pipe.hset(key, mapping={"data": blob})
        expire = ttl if ttl is not None else _DEFAULT_TTL
        pipe.expire(key, expire)
    await pipe.execute()


@retry(**_retry_params)
async def get_result(workflow_id: str) -> Any:
    """
    Получить один результат.
    :raises ResultNotFoundError если нет.
    """
    redis = _get_redis()
    key = _key(workflow_id)
    raw = await redis.hget(key, "data")
    if raw is None:
        logger.info("No result for %s in Redis", key)
        raise ResultNotFoundError(f"No data for workflow_id={workflow_id}")
    return orjson.loads(raw)


@retry(**_retry_params)
async def get_results(workflow_ids: List[str]) -> Dict[str, Optional[Any]]:
    """
    Пакетно получить сразу несколько результатов.
    Возвращает словарь workflow_id → result или None (если не найдено).
    """
    redis = _get_redis()
    pipe = redis.pipeline()
    for wf_id in workflow_ids:
        pipe.hget(_key(wf_id), "data")
    raws = await pipe.execute()
    results: Dict[str, Optional[Any]] = {}
    for wf_id, raw in zip(workflow_ids, raws):
        if raw is None:
            results[wf_id] = None
            logger.debug("Missing result for %s", wf_id)
        else:
            results[wf_id] = orjson.loads(raw)
    return results


@retry(**_retry_params)
async def exists_result(workflow_id: str) -> bool:
    """
    Проверить один workflow_id.
    """
    redis = _get_redis()
    return bool(await redis.hexists(_key(workflow_id), "data"))


@retry(**_retry_params)
async def exists_results(workflow_ids: List[str]) -> Dict[str, bool]:
    """
    Пакетно проверить сразу несколько workflow_id.
    Возвращает workflow_id → bool.
    """
    redis = _get_redis()
    pipe = redis.pipeline()
    for wf_id in workflow_ids:
        pipe.hexists(_key(wf_id), "data")
    flags = await pipe.execute()
    return {wf_id: bool(flag) for wf_id, flag in zip(workflow_ids, flags)}


@retry(**_retry_params)
async def delete_result(workflow_id: str) -> bool:
    """
    Удалить один ключ.
    Возвращает True, если удалено.
    """
    redis = _get_redis()
    key = _key(workflow_id)
    deleted = await redis.delete(key)
    logger.debug("Deleted key=%s count=%d", key, deleted)
    return deleted == 1


@retry(**_retry_params)
async def delete_results(workflow_ids: List[str]) -> Dict[str, bool]:
    """
    Пакетно удалить сразу несколько ключей.
    Возвращает workflow_id → True/False.
    """
    redis = _get_redis()
    pipe = redis.pipeline()
    for wf_id in workflow_ids:
        pipe.delete(_key(wf_id))
    counts = await pipe.execute()
    return {wf_id: (cnt == 1) for wf_id, cnt in zip(workflow_ids, counts)}
