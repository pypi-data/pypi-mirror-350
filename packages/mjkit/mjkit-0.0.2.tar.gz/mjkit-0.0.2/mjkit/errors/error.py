# -*- coding: utf-8 -*-

class NoDataReceivedError(ValueError):
    """
    조회된 데이터가 없을때 발생하는 오류
    """
    def __init__(self, msg="No data received"):
        super().__init__(msg)