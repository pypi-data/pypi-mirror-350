# coding=utf-8
from typing import TypeAlias

from datetime import date

from ka_uts_uts.utils.str import Str

TyDate: TypeAlias = date
TyAoS = list[str]
TyAoDate = list[TyDate]

TnAoDate = None | TyAoDate


class AoS:
    """ Manage Array of Strings
    """
    @staticmethod
    def nvl(aos: TyAoS) -> TyAoS:
        """ nvl function similar to SQL NVL function
        """
        if aos is None:
            return []
        return aos

    @staticmethod
    def sh_a_date(aos: TyAoS) -> TnAoDate:
        if aos is None:
            return None
        a_date: TyAoDate = []
        if aos == []:
            return a_date
        for item in aos:
            _date = Str.sh_date(item)
            if _date is None:
                return None
            a_date.append(_date)
        if a_date == []:
            return None
        else:
            return a_date

    @staticmethod
    def to_lower(aos: TyAoS) -> TyAoS:
        """ Lower all elements of the array of strings
        """
        return [element.lower() for element in aos]

    # class Unique:
    #     """ unique Array of Strings
    #     """
    #     @staticmethod
    #     def to(aos: TyAoS) -> TyAoS:
    #         """ Removes duplicate items from a list
    #         """
    #         aos_new = []
    #         for ee in aos:
    #             if ee not in aos_new:
    #                 aos_new.append(ee)
    #         return aos_new
    #
    #     @staticmethod
    #     def to_lower(aos: TyAoS) -> TyAoS:
    #         ''' Removes duplicate lower items from a list
    #         '''
    #         aos_new_lower = []
    #         for ee in aos:
    #             ee_lower = ee.lower()
    #             if ee_lower not in aos_new_lower:
    #                 aos_new_lower.append(ee_lower)
    #         return aos_new_lower
    #
    #     @staticmethod
    #     def to_lower_invariant(arr: TyAoS) -> TyAoS:
    #         """ Removes duplicate items (case invariant) from a list
    #         """
    #         arr_new = []
    #         arr_new_lower = []
    #         for ee in arr:
    #             ee_lower = ee.lower()
    #             if ee_lower not in arr_new_lower:
    #                 arr_new_lower.append(ee_lower)
    #                 arr_new.append(ee)
    #         return arr_new

    @staticmethod
    def to_unique(aos: TyAoS) -> TyAoS:
        """ Removes duplicate items from a list
        """
        aos_new = []
        for ee in aos:
            if ee not in aos_new:
                aos_new.append(ee)
        return aos_new

    @staticmethod
    def to_unique_lower(aos: TyAoS) -> TyAoS:
        ''' Removes duplicate lower items from a list
        '''
        aos_new_lower = []
        for _str in aos:
            _str_lower = _str.lower()
            if _str_lower not in aos_new_lower:
                aos_new_lower.append(_str_lower)
        return aos_new_lower

    @staticmethod
    def to_unique_lower_invariant(aos: TyAoS) -> TyAoS:
        """ Removes duplicate items (case invariant) from a list
        """
        aos_new = []
        aos_new_lower = []
        for _str in aos:
            _str_lower = _str.lower()
            if _str_lower not in aos_new_lower:
                aos_new_lower.append(_str_lower)
                aos_new.append(_str)
        return aos_new
