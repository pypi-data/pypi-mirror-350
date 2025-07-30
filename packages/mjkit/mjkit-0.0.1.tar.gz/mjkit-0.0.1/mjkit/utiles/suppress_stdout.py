import os
import sys
import contextlib


@contextlib.contextmanager
def suppress_stdout():
    """
    표준 출력(stdout)을 일시적으로 비활성화하는 컨텍스트 매니저입니다.

    이 함수는 코드 블록 실행 중 생성되는 모든 print 출력이나 기타 stdout 로그를 억제합니다.
    내부적으로 운영체제의 null 장치(os.devnull)를 사용하여 출력이 폐기되도록 합니다.

    예:
        with suppress_stdout():
            print("이 메시지는 출력되지 않습니다")
    """
    # 운영체제에 따라 자동으로 null 출력 장치 경로를 선택 (Linux/Mac: /dev/null, Windows: nul)
    with open(os.devnull, "w", encoding="utf-8") as devnull:
        old_stdout = sys.stdout  # 현재 stdout 백업
        sys.stdout = devnull  # stdout을 null 장치로 리디렉션하여 출력 억제
        try:
            yield  # suppress_stdout 내부에서 실행되는 블록
        finally:
            sys.stdout = old_stdout  # 블록 종료 후 stdout 원래대로 복원