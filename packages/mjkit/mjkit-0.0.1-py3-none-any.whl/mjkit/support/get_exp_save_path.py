import os
import uuid
from datetime import datetime


def get_exp_save_path(
        base_dir="experiments",
        experiments_name="optimization",
        cateogory_dir="optuna",
        trial_id=None
):
    current_dir = os.getcwd()

    # 날짜 기반 경로 생성
    date_str = datetime.now().strftime("%Y-%m-%d")
    save_dir = os.path.join(current_dir, base_dir, date_str, cateogory_dir)

    # trial_id 생성 및 포맷
    cut_uuid = uuid.uuid4().hex[:8]
    if trial_id is None:
        trial_id = f"{cut_uuid}"
    elif isinstance(trial_id, int):
        trial_id = f"{cut_uuid}_{trial_id:05d}"
    else:
        trial_id = f"{cut_uuid}_{str(trial_id)}"

    # 디렉토리 생성
    trial_path = os.path.join(save_dir, experiments_name)
    os.makedirs(trial_path, exist_ok=True)

    # 전체 경로 반환
    filename = f"best_model_{trial_id}.pt"
    model_path = os.path.join(trial_path, filename)
    return model_path


if __name__ == "__main__":
    # 테스트용 코드
    model_path = get_exp_save_path(trial_id=1)
    print(f"Model will be saved at: {model_path}")

    print({type(model_path)})

    model_path = get_exp_save_path()
    print(f"Model will be saved at: {model_path}")