import time
from functools import wraps
from mjkit.utiles.format_elapsed_time import format_elapsed_time
from mjkit.utiles.get_logger import get_logger, logging

def timeit(name: str):
    """
    실행 시간을 측정해 로깅하는 데코레이터를 생성합니다.

    :param name: 단계 이름 (로그 메시지에 사용) 예: "Clustering", "DB Save", etc.

    사용 예:
        @timeit("Clustering")
        def cluster_data(self, data):
            ...
    """
    # decorator 클로저: func를 인자로 받아 wrapper를 반환
    def decorator(func):
        # wraps를 통해 원본 함수의 __name__, __doc__ 유지
        @wraps(func)
        def wrapper(*args, **kwargs):
            # 1) 시작 시간 기록
            start = time.time()
            # 2) 원본 함수 실행
            result = func(*args, **kwargs)
            # 3) 경과 시간 계산
            elapsed = time.time() - start
            # 4) 로그 기록: 인스턴스에 logger가 있으면 logger 사용,
            #    없으면 print로 대체
            logger = None
            if args:
                first = args[0]
                if hasattr(first, "logger") and isinstance(first.logger, logging.Logger):
                    logger = first.logger
            if logger is None:
                logger = get_logger(func.__module__, logging.INFO)

            message = f"[Timing] {name} took {format_elapsed_time(elapsed)}"
            logger.info(message)

            return result
        return wrapper
    return decorator

# ------------------------------------
# 실제 실행 예시
# ------------------------------------
if __name__ == "__main__":
    def standalone_function(n: int):
        """독립 실행 함수 예시"""
        total = 0
        for i in range(n):
            total += i
            time.sleep(0.001)
        return total


    @timeit("Standalone Process")
    def processed_sum(n: int) -> int:
        return standalone_function(n)


    class Processor:
        """메서드 예시용 클래스"""

        def __init__(self):
            self.logger = logging.getLogger(self.__class__.__name__)

        @timeit("Instance Process")
        def compute(self, n: int) -> int:
            return processed_sum(n)
    logging.basicConfig(level=logging.INFO)

    ##############
    result1 = processed_sum(100)
    print(f"Standalone result: {result1}\n")
    proc = Processor()
    result2 = proc.compute(100)
    print(f"Instance result: {result2}")
