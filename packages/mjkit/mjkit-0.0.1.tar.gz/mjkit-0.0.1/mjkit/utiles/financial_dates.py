from datetime import datetime, timedelta
import holidays

def is_holidays(date: str, lang="ko") -> bool:
    """
    지정한 날짜가 주말(토요일, 일요일) 또는 해당 국가의 공휴일인지 여부를 판단합니다.

    Args:
        date (str): 검사할 날짜 문자열. 형식은 'YYYYMMDD'입니다. 예: '20250301'
        lang (str): 공휴일 표시 언어. 기본값은 'ko'로 한국어를 사용합니다.
                    `holidays` 패키지에서 제공하는 다국어 지원을 활용합니다.

    Returns:
        bool: 해당 날짜가 주말 또는 공휴일이면 True, 아니면 False를 반환합니다.

    Notes:
        - 대체공휴일도 holidays.KR에 의해 자동으로 처리됩니다.
        - 날짜는 내부적으로 `datetime` 객체로 변환한 후 처리됩니다.
    """
    d = datetime.strptime(date, "%Y%m%d")

    is_not_weekday = d.weekday() in [5, 6]  # 5=토요일, 6=일요일
    kr_holidays = holidays.KR(years=d.year, language=lang)
    is_not_holidays = d in kr_holidays

    return is_not_weekday or is_not_holidays


def financial_dates(start: str, end: str, lang="ko") -> list[str]:
    """
    주어진 날짜 범위 내에서 주말 및 공휴일을 제외한 '금융 영업일' 리스트를 생성합니다.

    Args:
        start (str): 시작 날짜 문자열. 형식은 'YYYYMMDD'입니다. 예: '20250101'
        end (str): 끝 날짜 문자열. 형식은 'YYYYMMDD'입니다. 예: '20250312'
        lang (str): 공휴일 언어 설정. 기본값은 'ko'로 한국 공휴일을 기준으로 계산합니다.

    Example:
        >>> financial_dates("20250101", "20250312")
        ['20250102', '20250103', '20250104', ...]


    Returns:
        list[str]: 시작일과 종료일 사이의 모든 날짜 중 주말 및 공휴일을 제외한 날짜 리스트.
                   각 날짜는 'YYYYMMDD' 형식의 문자열로 반환됩니다.

    Notes:
        - 공휴일 정보는 `holidays` 패키지의 한국(KR) 기준으로 계산됩니다.
        - 각 날짜마다 `is_holidays` 함수를 호출하여 검사합니다.
        - 금융/증권 시장에서 유효한 영업일 계산에 유용하게 사용할 수 있습니다.
    """
    start_date = datetime.strptime(start, "%Y%m%d")
    end_date = datetime.strptime(end, "%Y%m%d")
    date_list = []

    current_date = start_date
    while current_date <= end_date:
        if not is_holidays(current_date.strftime("%Y%m%d"), lang=lang):
            date_list.append(current_date.strftime("%Y%m%d"))
        current_date += timedelta(days=1)

    return date_list


if __name__ == "__main__":
    print(financial_dates("20250101", "20250312"))
