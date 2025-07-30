"""
This module provides utility classes for the management of OmniTracker
EcoVadis NHRR (Nachhaltigkeits Risiko Rating) processing for Department UMH
"""
from __future__ import annotations
from typing import Any, TypeAlias

import pandas as pd
import numpy as np

from ka_uts_aod.aod import AoD
from ka_uts_dic.dic import Dic
from ka_uts_dic.doa import DoA
from ka_uts_dic.doaod import DoAoD
from ka_uts_dfr.pddf import PdDf
from ka_uts_log.log import Log

from ka_uts_eco.cfg.utils import CfgUtils as Cfg

TyPdDf: TypeAlias = pd.DataFrame

TyArr = list[Any]
TyAoStr = list[str]
TyBool = bool
TyDic = dict[Any, Any]
TyAoA = list[TyArr]
TyAoD = list[TyDic]
TyDoAoA = dict[Any, TyAoA]
TyDoAoD = dict[Any, TyAoD]
TyAoD_DoAoD = TyAoD | TyDoAoD
TyTup = tuple[Any]
TyTask = Any
TyDoPdDf = dict[Any, TyPdDf]
TyPdDf_DoPdDf = TyPdDf | TyDoPdDf
TyToAoDDoAoD = tuple[TyAoD, TyDoAoD]

TnDic = None | TyDic
TnAoD = None | TyAoD
TnDoAoA = None | TyDoAoA
TnDoAoD = None | TyDoAoD
TnPdDf = None | TyPdDf
TnStr = None | str


class Evup:
    """
    EcoVadis Upload class
    """
    @staticmethod
    def sh_aod_evup_adm(doaod: TyDoAoD, operation: str) -> TyAoD:
        """
        Show array of dictionaries for admin function for evup
        """
        match operation:
            case 'CU', 'CUD':
                aod: TyAoD = DoAoD.union_by_keys(doaod, ['new', 'ch_y'])
            case 'C', 'CD':
                aod: TyAoD = DoAoD.union_by_keys(doaod, ['new'])
            case 'U', 'UD':
                aod: TyAoD = DoAoD.union_by_keys(doaod, ['ch_y'])
            case _:
                aod: TyAoD = DoAoD.union(doaod)
        return aod


class Evex:
    """
    EcoVadis Export class
    """
    @staticmethod
    def sh_d_evex(df_evex: TnPdDf) -> TyDic:
        if df_evex is None:
            return {}
        _df_evex = df_evex.replace(to_replace=np.nan, value=None, inplace=False)
        _aod = _df_evex.to_dict(orient='records')
        if len(_aod) == 1:
            d_evex: TyDic = _aod[0]
            return d_evex
        msg = "Evex Dataframe: {F} contains multiple records: {R}"
        Log.error(msg.format(F=df_evex, R=_aod))
        return {}

    @staticmethod
    def sh_d_evup_del_from_dic(d_evex: TnDic) -> TyDic:
        d_evup: TyDic = {}
        if d_evex is None:
            return d_evup
        Dic.set_tgt_with_src_by_d_tgt2src(d_evup, d_evex, Cfg.d_del_evup2evex)
        return d_evup

    @classmethod
    def sh_d_evup_del_from_df(cls, df_evex_row: TyPdDf) -> TyDic:
        return cls.sh_d_evup_del_from_dic(cls.sh_d_evex(df_evex_row))

    @staticmethod
    def map(aod_evex: TnAoD) -> TyAoD:
        aod_evex_new: TyAoD = []
        if not aod_evex:
            return aod_evex_new
        for dic in aod_evex:
            dic_new = {}
            for key, value in dic.items():
                dic_new[key] = Cfg.d_ecv_iq2umh_iq.get(value, value)
            aod_evex_new.append(dic_new)
        return aod_evex_new


class EvinVerify:
    """
    OmniTracker EcoVadis class
    """

    @staticmethod
    def verify_duns(d_otex: TyDic, doaod_vfy: TyDoAoD) -> TyBool:
        _sw: TyBool = True
        _duns = Dic.get(d_otex, Cfg.otex_key_duns)
        if not _duns:
            _sw = False
            DoA.append_unique_by_key(doaod_vfy, 'duns_is_empty', d_otex)
        return _sw

    @staticmethod
    def verify_objectid(d_otex: TyDic, doaod_vfy: TyDoAoD) -> TyBool:
        _sw: TyBool = True
        _objectid = Dic.get(d_otex, Cfg.otex_key_objectid)
        if not _objectid:
            _sw = False
            DoA.append_unique_by_key(doaod_vfy, 'objectid_is_empty', d_otex)
        return _sw

    @staticmethod
    def verify_countrycode(d_otex: TyDic, doaod_vfy: TyDoAoD) -> TyBool:
        _sw: TyBool = True
        _coco: TnStr = Dic.get(d_otex, Cfg.otex_key_coco)
        if not _coco:
            _sw = False
            DoA.append_unique_by_key(doaod_vfy, 'coco_is_empty', d_otex)
        else:
            import pycountry
            try:
                country = pycountry.countries.get(alpha_2=_coco.upper())
            except KeyError:
                DoA.append_unique_by_key(doaod_vfy, 'coco_is_invalid', d_otex)
                _sw = False
        return _sw

    @staticmethod
    def verify_town_in_country(d_otex: TyDic, doaod_vfy: TyDoAoD) -> TyBool:
        _sw: TyBool = True
        _town: TnStr = Dic.get(d_otex, Cfg.otex_key_town)
        if not _town:
            _sw = False
            DoA.append_unique_by_key(doaod_vfy, 'town_is_empty', d_otex)
        else:
            _coco = Dic.get(d_otex, Cfg.otex_key_coco)
            if not _coco:
                return _sw
            from geopy.geocoders import Nominatim
            from geopy.exc import GeocoderTimedOut
            geolocator = Nominatim(user_agent="geo_verifier")
            try:
                location = geolocator.geocode(_town)
                if location is None:
                    DoA.append_unique_by_key(doaod_vfy, 'town_is_invalid', d_otex)
                else:
                    if _coco.lower() not in location.address.lower():
                        DoA.append_unique_by_key(
                                doaod_vfy, 'town_is_invalid', d_otex)
                        _sw = False
            except GeocoderTimedOut:
                DoA.append_unique_by_key(doaod_vfy, 'town_is_invalid', d_otex)
                _sw = False
        return _sw

    @staticmethod
    def verify_postalcode_in_country(d_otex: TyDic, doaod_vfy: TyDoAoD) -> TyBool:
        _sw: TyBool = True
        _poco: TnStr = Dic.get(d_otex, Cfg.otex_key_poco)
        if not _poco:
            _sw = False
            DoA.append_unique_by_key(doaod_vfy, 'poco_is_empty', d_otex)
        else:
            _coco = Dic.get(d_otex, Cfg.otex_key_coco)
            from postal_codes_tools.postal_codes import verify_postal_code_format
            if not verify_postal_code_format(postal_code=_poco, country_iso2=_coco):
                _sw = False
                DoA.append_unique_by_key(doaod_vfy, 'poco_is_invalid', d_otex)
        return _sw

    @classmethod
    def verify_d_otex(
            cls, d_otex: TyDic, doaod_vfy: TyDoAoD, kwargs: TyDic
    ) -> TyBool:
        _sw: TyBool = True
        # Verify DUNS-Number
        _sw_vfy_duns = kwargs.get('sw_vfy_duns', True)
        if _sw_vfy_duns:
            _sw = _sw and cls.verify_duns(d_otex, doaod_vfy)

        # Verify ObjectID
        _sw_vfy_objectid = kwargs.get('sw_vfy_objectid', True)
        if _sw_vfy_objectid:
            _sw_objectid = cls.verify_objectid(d_otex, doaod_vfy)
            _sw = _sw and _sw_objectid

        _sw_ignore = _sw

        # Verify Country Code
        _sw_vfy_coco = kwargs.get('sw_vfy_coco', True)
        if _sw_vfy_coco:
            _sw = _sw and cls.verify_countrycode(d_otex, doaod_vfy)

        # Verify Town in Country
        _sw_vfy_town = kwargs.get('sw_vfy_town', False)
        if _sw_vfy_town:
            _sw = _sw and cls.verify_town_in_country(d_otex, doaod_vfy)

        # Verify Postal Code
        _sw_vfy_poco = kwargs.get('sw_vfy_poco', True)
        if _sw_vfy_poco:
            _sw = _sw and cls.verify_postalcode_in_country(d_otex, doaod_vfy)

        _sw_vfy_ignore = kwargs.get('sw_vfy_ignore', True)
        if _sw_vfy_ignore:
            _sw_vfy_ignore_duns = kwargs.get('sw_vfy_ignore_duns', True)
            if _sw_vfy_ignore_duns:
                return _sw_objectid
            else:
                return _sw_ignore

        return _sw

    @classmethod
    def verify_aod_otex(
            cls, aod_otex, doaod_vfy, kwargs: TyDic
    ) -> TyAoD:
        _aod_otex: TyAoD = []
        for _d_otex in aod_otex:
            _sw: bool = cls.verify_d_otex(_d_otex, doaod_vfy, kwargs)
            if _sw:
                _aod_otex.append(_d_otex)
        return _aod_otex


class Evin:
    """
    EcoVadis input data (from Systems like OmniTracker) class
    """

    @staticmethod
    def sh_d_evup_adm(d_otex: TyDic) -> TyDic:
        d_evup: TyDic = {}
        Dic.set_tgt_with_src(d_evup, Cfg.d_evup2const)
        Dic.set_tgt_with_src_by_d_tgt2src(d_evup, d_otex, Cfg.d_evup2otex)
        return d_evup

    @classmethod
    def sh_aod_evup_adm(cls, aod_otex) -> TyAoD:
        _aod_evup: TyAoD = []
        for _d_otex in aod_otex:
            AoD.append_unique(_aod_evup, Evin.sh_d_evup_adm(_d_otex))
        return _aod_evup

    @classmethod
    def sh_doaod_adm_new(cls, aod_otex) -> TyDoAoD:
        _doaod_evup: TyDoAoD = {}
        for _d_otex in aod_otex:
            _d_evup = cls.sh_d_evup_adm(_d_otex)
            DoA.append_unique_by_key(_doaod_evup, 'new', _d_evup)
        return _doaod_evup


class EvinEvex:
    """
    Check EcoVadis input data (from Systems like OmniTracker) against
    EcoVadis export data
    """
    msg_evex = ("No entries found in Evex dataframe for "
                "Evex key: '{K1}' and Evin value: {V1} and "
                "Evex key: '{K2}' and Evin value: {V2}")
    msg_otex = "Evin Key: '{K}' not found in Evin Dictionary {D}"

    @classmethod
    def query_with_key(
            cls, d_otex: TyDic, df_evex: TyPdDf, otex_key: Any, otex_value_cc: Any
    ) -> TnPdDf:
        otex_value = Dic.get(d_otex, otex_key)
        if otex_value:
            evex_key = Cfg.d_otex2evex_keys[otex_key]
            condition = (df_evex[evex_key] == otex_value) & (df_evex[Cfg.evex_key_cc] == otex_value_cc)
            df: TnPdDf = df_evex.loc[condition]
            Log.info(cls.msg_evex.format(
                K1=evex_key, V1=otex_value, K2=Cfg.evex_key_cc, V2=otex_value_cc))
            return df
        else:
            Log.debug(cls.msg_otex.format(K=otex_key, D=d_otex))
            return None

    @classmethod
    def query_with_keys(cls, d_otex: TyDic, df_evex: TyPdDf) -> TnPdDf:
        otex_value_cc = d_otex.get(Cfg.otex_key_cc)
        if not otex_value_cc:
            Log.error(cls.msg_otex.format(K=Cfg.otex_key_cc, D=d_otex))
            return None
        for otex_key in Cfg.a_otex_key:
            df = cls.query_with_key(d_otex, df_evex, otex_key, otex_value_cc)
            if df is not None:
                return df
        return None

    @classmethod
    def query(cls, d_otex: TyDic, df_evex: TyPdDf) -> TyDic:
        _df: TnPdDf = PdDf.query_with_key(
            df_evex, d_otex,
            dic_key=Cfg.otex_key_objectid, d_key2key=Cfg.d_otex2evex_keys)
        if _df is not None:
            return Evex.sh_d_evex(_df)

        _df = PdDf.query_with_key(
            df_evex, d_otex,
            dic_key=Cfg.otex_key_duns, d_key2key=Cfg.d_otex2evex_keys)
        if _df is not None:
            return Evex.sh_d_evex(_df)

        _df = cls.query_with_keys(d_otex, df_evex)
        return Evex.sh_d_evex(_df)

    @classmethod
    def join_adm(
            cls, aod_otex: TnAoD, df_evex: TnPdDf, doaod_vfy: TyDoAoD, sw_ch_n: TyBool
    ) -> TyDoAoD:
        if not aod_otex:
            return {}
        if df_evex is None:
            return Evin.sh_doaod_adm_new(aod_otex)

        _doaod_evup: TyDoAoD = {}
        for _d_otex in aod_otex:
            _df: TnPdDf = PdDf.query_with_key(
                    df_evex, _d_otex,
                    dic_key=Cfg.otex_key_objectid, d_key2key=Cfg.d_otex2evex_keys)
            if _df is None:
                DoA.append_unique_by_key(doaod_vfy, 'adm_otev_new', _d_otex)
                _d_evup = Evin.sh_d_evup_adm(_d_otex)
                DoA.append_unique_by_key(_doaod_evup, 'new', _d_evup)
            else:
                DoA.append_unique_by_key(doaod_vfy, 'adm_otev_old', _d_otex)
                _d_evex = Evex.sh_d_evex(_df)
                _change_status, _d_evup = cls.sh_d_evup_adm(_d_otex, _d_evex, sw_ch_n)
                DoA.append_unique_by_key(_doaod_evup, _change_status, _d_evup)

        return _doaod_evup

    @classmethod
    def join_del(
            cls, aod_otex: TnAoD, df_evex: TnPdDf, doaod_vfy: TyDoAoD
    ) -> TyAoD:
        _aod_evup: TyAoD = []
        if not aod_otex:
            return _aod_evup

        for _d_otex in aod_otex:
            _df_evex_row: TnPdDf = PdDf.query_with_key(
                    df_evex, _d_otex,
                    dic_key=Cfg.otex_key_objectid, d_key2key=Cfg.d_otex2evex_keys)
            if _df_evex_row is None:
                DoA.append_unique_by_key(doaod_vfy, 'del_otev_n', _d_otex)
            else:
                DoA.append_unique_by_key(doaod_vfy, 'del_otev_y', _d_otex)
                _d_evup = Evex.sh_d_evup_del_from_df(Evex.sh_d_evex(_df_evex_row))
                AoD.append_unique(_aod_evup, _d_evup)
        return _aod_evup

    @staticmethod
    def sh_d_evup_adm(
            d_otex: TyDic, d_evex: TyDic, sw_ch_n: TyBool) -> tuple[str, TyDic]:
        d_evup: TyDic = {}
        Dic.set_tgt_with_src(d_evup, Cfg.d_evup2const)
        Dic.set_tgt_with_src_by_d_tgt2src(d_evup, d_evex, Cfg.d_evup2evex)
        Dic.set_tgt_with_src_by_d_tgt2src(d_evup, d_otex, Cfg.d_evup2otex)
        change_status = 'ch_n'
        if sw_ch_n:
            return change_status, d_evup
        for key_otex, key_evex in Cfg.d_otex2evex.items():
            if d_otex[key_otex] != d_evex[key_evex]:
                key_evup = Cfg.d_otex2evup[key_otex]
                d_evup[key_evup] = d_otex[key_otex]
                change_status = 'ch_y'
        return change_status, d_evup


class EvexEvin:
    """
    Check EcoVadis Export Data against
    EcoVadis input data (from Systems like OmniTracker)
    """
    @classmethod
    def join_del(
            cls, aod_evex: TnAoD, df_otex: TnPdDf, doaod_vfy: TyDoAoD
    ) -> TyAoD:
        _aod_evup: TyAoD = []
        if not aod_evex or df_otex is None:
            return _aod_evup
        for _d_evex in aod_evex:
            _df_otex_row: TnPdDf = PdDf.query_with_key(
                    df_otex, _d_evex,
                    dic_key=Cfg.otex_key_objectid, d_key2key=Cfg.d_evex2otex_keys)
            if _df_otex_row is None:
                DoA.append_unique_by_key(doaod_vfy, 'del_evot_n', _d_evex)
                AoD.append_unique(_aod_evup, Evex.sh_d_evup_del_from_dic(_d_evex))
            else:
                DoA.append_unique_by_key(doaod_vfy, 'del_evot_y', _d_evex)
        return _aod_evup
