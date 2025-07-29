from functools import wraps
from threading import Lock
from typing import Callable, TypeVar, ParamSpec
from diskcache import Cache

CACHE_DIR = ".cache"

cache = Cache(CACHE_DIR)


def cache_result(func):
    @wraps(func)
    def wrapper(latex_str: str):
        result = cache.get(latex_str)
        if result is not None:
            return result
        result = func(latex_str)
        try:
            cache.set(latex_str, result)
        except Exception as e:
            # TODO: 캐시저장 실패시 로그처리
            pass
        return result

    return wrapper


P = ParamSpec("P")
R = TypeVar("R")


class RunOnceRegistry:
    def __init__(self):
        self._executed_funcs = set()
        self._lock = Lock()

    def mark_executed(self, func_name: str) -> None:
        with self._lock:
            self._executed_funcs.add(func_name)

    def is_executed(self, func_name: str) -> bool:
        with self._lock:
            return func_name in self._executed_funcs

    def reset(self) -> None:
        with self._lock:
            self._executed_funcs.clear()


_registry = RunOnceRegistry()


def run_only_once(
    func: Callable[P, R] = None,
    *,
    verbose: bool = False,
    registry: RunOnceRegistry = _registry,
) -> Callable[P, R]:
    """
    함수를 한 번만 실행하도록 보장하는 데코레이터

    Args:
        func: 데코레이트할 함수
        silent: True일 경우 로깅을 비활성화
        registry: 실행 상태를 추적할 레지스트리 인스턴스

    Returns:
        데코레이트된 함수
    """

    def decorator(func: Callable[P, R]) -> Callable[P, R]:
        @wraps(func)
        def wrapper(*args: P.args, **kwargs: P.kwargs) -> R | None:
            if verbose:
                print(f"run_only_once: {func.__name__}")

            if registry.is_executed(func.__name__):
                if verbose:
                    print(f"run_only_once: {func.__name__} already done")
                return None

            result = func(*args, **kwargs)
            registry.mark_executed(func.__name__)
            return result

        return wrapper

    return decorator(func) if func else decorator


def reset_run_once_registry() -> None:
    """모든 함수의 실행 상태를 초기화합니다."""
    _registry.reset()
