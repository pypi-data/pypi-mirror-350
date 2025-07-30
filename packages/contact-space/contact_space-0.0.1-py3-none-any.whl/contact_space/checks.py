
from datetime import datetime
import inspect
import requests as reqs
from contact_space.exceptions import InvalidDateRangeException, NotEqualSizeException

class Checks():

    def __init__(self):
        return
    
    @staticmethod
    def _auth_check(header : dict, base_url : str, timeout : int) -> None:
        """"""
        if base_url.endswith("/") and not base_url.endswith("//"):
            url = base_url + "GetUsers"
        elif base_url.endswith("//"):
            fixed_url = base_url.rstrip("/")
            url = fixed_url + "GetUsers"
        else:
            url = base_url + "/GetUsers"
        response = reqs.post(url, headers=header, timeout=timeout)
        response.raise_for_status()
        return
    
    @staticmethod
    def _date_format_check(date_val : str) -> str:
        """"""
        if not isinstance(date_val, str):
            datetime.strftime(date_val, date_format="%Y-%m-%d %H:%M:%S")
        try:
            datetime.strptime(date_val, "%Y-%m-%d %H:%M:%S")
        except ValueError:
            try:
                datetime.strptime(date_val, "%Y-%m-%d")
            except:
                raise
    
    @staticmethod
    def _date_order_check(date1 : str, date2 : str) -> None:
        try:
            dt1 = datetime.strptime(date1, "%Y-%m-%d %H:%M:%S")
            dt2 = datetime.strptime(date2, "%Y-%m-%d %H:%M:%S")
        except ValueError:
            try:           
                dt1 = datetime.strptime(date1, "%Y-%m-%d")
                dt2 = datetime.strptime(date2, "%Y-%m-%d")
            except:
                raise

        if dt2 < dt1:
            raise InvalidDateRangeException(date1, date2)

    @staticmethod
    def _type_check(func, params : dict) -> None:
        type_map = inspect.signature(func)
        for name, param in type_map.parameters.items():
            if name not in params:
                raise ValueError(f"Parameter '{name}' is missing from provided parameters")
            expected_type = param.annotation
            if expected_type is inspect._empty:
                # No annotation given, skip check
                continue
            value = params[name]
            if not isinstance(value, expected_type):
                raise TypeError(f"{name} must be {expected_type.__name__}, got {type(value).__name__}")    
                
    @staticmethod
    def _equal_check(list1 : list, list2 : list) -> None:
        if not len(list1) == len(list2):
            raise NotEqualSizeException()



