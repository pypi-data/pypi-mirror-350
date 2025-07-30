import logging
import sys


# 로그 레벨별 이모지 태그
class EmojiFormatter(logging.Formatter):
    """
    로그 메시지 앞에 이모지와 태그를 붙여서 가독성을 높이는 Formatter
    """

    @property
    def level_tags(self):
        return {
            "DEBUG": "🔍 [DEBUG]",
            "INFO": "ℹ️ [INFO]",
            "WARNING": "⚠️ [WARNING]",
            "ERROR": "❌ [ERROR]",
            "CRITICAL": "🔥 [CRITICAL]"
        }

    def format(self, record):
        level_tag = self.level_tags.get(record.levelname, f"[{record.levelname}]")
        original_msg = super().format(record)
        # 기존 메시지에서 레벨명 앞에 이모지 태그 추가
        return original_msg.replace(f"[{record.levelname}]", level_tag)


def get_logger(
        name: str,
        level=logging.DEBUG
) -> logging.Logger:
    """
    모듈별 독립 로거를 생성하고 반환합니다.

    Args:
        name (str): 로거 이름 (일반적으로 __name__)
        level (int): 로그 레벨 (기본값: logging.INFO)

    Returns:
        logging.Logger: 설정된 로거 인스턴스
    """
    logger = logging.getLogger(name)
    logger.setLevel(level)

    if not logger.handlers:
        handler = logging.StreamHandler(sys.stderr)
        handler.setLevel(level)

        formatter = EmojiFormatter(
            fmt="[%(asctime)s][%(name)s] [%(levelname)s] %(message)s",
            datefmt="%y-%m-%d %H:%M:%S"
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        logger.propagate = False

    return logger


# 테스트용 실행 예시
if __name__ == "__main__":
    def some_function():
        logger.info("함수가 실행되었습니다.")
        logger.debug("디버깅 정보입니다.")
        logger.warning("경고 발생")
        logger.error("에러 발생")
        logger.critical("심각한 문제 발생")

    logger = get_logger(__name__, level=logging.DEBUG)
    some_function()

    print()

    logger = get_logger("__test__", level=logging.DEBUG)
    some_function()

