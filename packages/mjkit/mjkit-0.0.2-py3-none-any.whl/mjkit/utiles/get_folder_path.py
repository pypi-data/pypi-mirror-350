import os
from typing import Optional

def find_project_root(start_path: Optional[str] = None) -> str:
    """
    현재 파일에서 시작하여 루트 디렉토리까지 올라가며,
    .venv, .git, pyproject.toml, .gitignore 중 하나라도 존재하는 폴더를 루트 디렉토리로 판단합니다.

    단, 반환 경로가 `.venv` 폴더일 경우, `.venv` 상위 폴더를 루트로 간주합니다.

    Args:
        start_path (str, optional): 탐색을 시작할 경로 (기본값은 현재 파일 경로)

    Returns:
        str: 탐색된 루트 디렉토리 경로

    Raises:
        RuntimeError: 루트 디렉토리를 찾을 수 없을 경우
    """
    if start_path is None:
        start_path = os.path.dirname(os.path.abspath(__file__))

    root_indicators = {".venv", ".git", "pyproject.toml", ".gitignore"}

    current_path = start_path

    while True:
        entries = set(os.listdir(current_path))
        if root_indicators & entries:
            # 만약 current_path가 .venv 경로라면 상위 폴더 반환
            if os.path.basename(current_path) == ".venv":
                return os.path.dirname(current_path)
            return current_path

        parent_path = os.path.dirname(current_path)
        if parent_path == current_path:
            # 루트 디렉토리까지 올라왔는데도 못 찾음
            raise RuntimeError("루트 디렉토리(.venv, .git, pyproject.toml 등)를 찾을 수 없습니다.")

        current_path = parent_path


# 기존 함수에 적용
def get_root_dir() -> str:
    """
    프로젝트의 루트 디렉토리를 반환합니다.
    (.venv, .git, pyproject.toml, .gitignore 등을 기준으로 탐색)
    """
    return find_project_root()

def _ensure_directory_exists(path: str) -> None:
    """
    주어진 경로에 폴더가 없으면 생성합니다.
    """
    os.makedirs(path, exist_ok=True)

def get_assets_folder_path() -> str:
    """
    루트 디렉토리 기준으로 'assets' 폴더의 절대 경로를 반환합니다.
    폴더가 없으면 생성합니다.
    """
    assets_path = os.path.join(get_root_dir(), "assets")
    _ensure_directory_exists(assets_path)
    return assets_path

def get_assets_subfolder_path(subfolder_name: str) -> str:
    """
    'assets' 디렉토리 내부의 하위 폴더 경로를 반환합니다.
    폴더가 없으면 생성합니다.

    Args:
        subfolder_name (str): 하위 폴더명 (예: "market", "data", "logs")

    Returns:
        str: 절대 경로
    """
    path = os.path.join(get_assets_folder_path(), subfolder_name)
    _ensure_directory_exists(path)
    return path

# 하위 폴더별 전용 함수 정의
def get_market_folder_path() -> str:
    """
    assets/market 경로 반환
    """
    return get_assets_subfolder_path("market")

def get_data_folder_path() -> str:
    """
    assets/data 경로 반환
    """
    return get_assets_subfolder_path("data")

def get_logs_folder_path() -> str:
    """
    assets/logs 경로 반환
    """
    return get_assets_subfolder_path("logs")


# 예시 실행
if __name__ == "__main__":
    print("Project root:", get_root_dir())
    print("assets:", get_assets_folder_path())
    print("market:", get_market_folder_path())
    print("data:", get_data_folder_path())
    print("logs:", get_logs_folder_path())


