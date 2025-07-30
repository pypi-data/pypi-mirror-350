from dataclasses import dataclass
from typing import List, Optional
from datetime import datetime


@dataclass
class ReadmeConfig:
    tags: Optional[List[str]] = None
    datasets: Optional[List[str]] = None
    languages: Optional[List[str]] = None
    license: str = "apache-2.0"
    pretty_name: Optional[str] = None
    description: Optional[str] = None


def create_readme(msg: str, config: ReadmeConfig) -> str:
    """
    Hugging Face Dataset/Card용 README.md 파일을 생성합니다.

    :param msg: 본문 설명 (README의 메인 텍스트, 필수)
    :param config: README에 포함될 메타 정보 설정
    :return: README.md 형식의 문자열 (YAML 헤더 + 본문)
    :raises ValueError: msg가 없거나 비어있을 경우
    """
    # Validation
    if not isinstance(msg, str) or not msg.strip():
        raise ValueError("`msg`는 필수이며, 비어있을 수 없습니다.")

    # Default fallback values
    tags = config.tags if config.tags else ["finance", "stock"]
    datasets = config.datasets if config.datasets else ["train"]
    languages = config.languages if config.languages else ["ko"]
    license = config.license or "apache-2.0"

    # YAML Header 생성
    yaml_lines = ["---"]
    if config.pretty_name:
        yaml_lines.append(f"pretty_name: {config.pretty_name}")
    if config.description:
        yaml_lines.append(f"description: {config.description}")
    yaml_lines.append(f"license: {license}")
    yaml_lines.append("tags:")
    yaml_lines.extend([f"  - {tag}" for tag in tags])
    yaml_lines.append("datasets:")
    yaml_lines.extend([f"  - {dataset}" for dataset in datasets])
    yaml_lines.append("language:")
    yaml_lines.extend([f"  - {lang}" for lang in languages])
    yaml_lines.append("---")

    # Body sections 생성
    body_lines = []

    # 제목
    body_lines.append(f"# 📈 {config.pretty_name or 'Dataset'}\n")

    # 설명
    if config.description:
        body_lines.append(f"**{config.description}**\n")

    # 본문 메시지
    body_lines.append(msg.strip())

    # 데이터셋 정보
    body_lines.append("\n## 📌 데이터셋 정보")
    body_lines.append(f"- 라이선스: {license}")
    body_lines.append(f"- 사용 언어: {', '.join(languages)}")
    body_lines.append(f"- 관련 데이터셋: {', '.join(datasets)}")

    # 사용 예시 코드
    body_lines.append("\n## 💡 사용 예시")
    dataset_id = datasets[0]
    body_lines.append("```python")
    body_lines.append("from datasets import load_dataset")
    body_lines.append(f"dataset = load_dataset('{dataset_id}')")
    body_lines.append("print(dataset['train'][0])  # 하나의 샘플 출력")
    body_lines.append("```")

    # 마지막 업데이트 날짜
    body_lines.append("\n## 📅 마지막 업데이트")
    body_lines.append(f"- {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} 기준으로 최신입니다.")

    return "\n".join(yaml_lines) + "\n\n" + "\n".join(body_lines)


# Example usage
if __name__ == "__main__":
    try:
        config = ReadmeConfig(
            tags=["finance", "stock"],
            datasets=["krx-daily"],
            languages=["ko"],
            license="MIT",
            pretty_name="Daily KRX Index Price",
            description="KRX의 일일 종가 데이터셋입니다."
        )

        readme_text = create_readme(
            msg="이 데이터셋은 한국 주식 시장의 일일 종가 데이터를 포함합니다.",
            config=config
        )

        print(readme_text)

    except ValueError as e:
        print(f"[ERROR] README 생성 실패: {e}")
