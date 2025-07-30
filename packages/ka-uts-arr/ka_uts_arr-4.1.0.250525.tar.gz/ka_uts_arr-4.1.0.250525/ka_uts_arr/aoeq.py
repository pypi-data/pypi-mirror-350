# coding=utf-8
from typing import Any
from collections.abc import Callable

# from ka_uts_obj.pokv import PoKV
from ka_uts_dic.doeq import DoEq

TyArr = list[Any]
TyCall = Callable[..., Any]
TyDic = dict[Any, Any]

TnDic = None | TyDic


class AoEq:
    """ Dictionary of Equates
    """
    @staticmethod
    def _sh_d_eq(a_equ: TyArr) -> TyDic:
        d_eq = {}
        for s_eq in a_equ[1:]:
            a_eq = s_eq.split('=')
            if len(a_eq) == 1:
                d_eq['cmd'] = a_eq[0]
            else:
                d_eq[a_eq[0]] = a_eq[1]
                d_eq[a_eq[0]] = a_eq[1]
        return d_eq

    @classmethod
    def sh_d_eq(cls, a_equ: TyArr, **kwargs) -> TyDic:
        """ show equates dictionary
        """
        d_parms: TnDic = kwargs.get('d_parms')
        _sh_prof = kwargs.get('sh_prof')
        d_eq: TyDic = cls._sh_d_eq(a_equ)
        d_eq_new: TyDic = DoEq.verify(d_eq, d_parms)
        DoEq._set_sh_prof(d_eq_new, _sh_prof)
        return d_eq_new
