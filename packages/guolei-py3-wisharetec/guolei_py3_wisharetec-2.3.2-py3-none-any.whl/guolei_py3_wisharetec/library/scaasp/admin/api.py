#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
"""
=================================================
作者:[郭磊]
手机:[5210720528]
email:[174000902@qq.com]
github:[https://github.com/guolei19850528/guolei_py3_wisharetec]
=================================================
"""
import hashlib
from datetime import timedelta
from typing import Union, Callable

import diskcache
import redis
import requests
from addict import Dict
from guolei_py3_requests.library import ResponseCallback, Request
from jsonschema.validators import Draft202012Validator, validate
from requests import Response


class ResponseCallback(ResponseCallback):
    """
    Response Callable Class
    """

    @staticmethod
    def text_start_with_null(response: Response = None, status_code: int = 200):
        text = ResponseCallback.text(response=response, status_code=status_code)
        return isinstance(text, str) and text.lower().startswith("null")

    @staticmethod
    def json_status_100_data(response: Response = None, status_code: int = 200):
        json_addict = ResponseCallback.json_addict(response=response, status_code=status_code)
        if Draft202012Validator({
            "type": "object",
            "properties": {
                "status": {
                    "oneOf": [
                        {"type": "integer", "const": 100},
                        {"type": "string", "const": "100"},
                    ]
                }
            },
            "required": ["status", "data"],
        }).is_valid(json_addict):
            return json_addict.data
        return None

    def json_status_100_data_resultlist(response: Response = None, status_code: int = 200):
        json_addict = ResponseCallback.json_addict(response=response, status_code=status_code)
        if Draft202012Validator({
            "type": "object",
            "properties": {
                "status": {
                    "oneOf": [
                        {"type": "integer", "const": 100},
                        {"type": "string", "const": "100"},
                    ]
                },
                "data": {
                    "type": "object",
                    "properties": {
                        "resultList": {
                            "type": "array",
                            "minItems": 1,
                        },
                        "required": ["resultList"]
                    }
                }
            },
            "required": ["status", "data"],
        }).is_valid(json_addict):
            return json_addict.data.resultList
        return None


class UrlSetting(object):
    """
    Url Settings
    """
    LOGIN: str = "/manage/login"
    QUERY_LOGIN_STATE: str = "/old/serverUserAction!checkSession.action"
    QUERY_COMMUNITY_BY_PAGINATOR: str = "/manage/communityInfo/getAdminCommunityList"
    QUERY_COMMUNITY_DETAIL: str = "/manage/communityInfo/getCommunityInfo"
    QUERY_ROOM_BY_PAGINATOR: str = "/manage/communityRoom/listCommunityRoom"
    QUERY_ROOM_DETAIL: str = "/manage/communityRoom/getFullRoomInfo"
    QUERY_ROOM_EXPORT: str = "/manage/communityRoom/exportDelayCommunityRoomList"
    QUERY_REGISTER_USER_BY_PAGINATOR: str = "/manage/user/register/list"
    QUERY_REGISTER_USER_DETAIL: str = "/manage/user/register/detail"
    QUERY_REGISTER_USER_EXPORT: str = "/manage/user/register/list/export"
    QUERY_REGISTER_OWNER_BY_PAGINATOR: str = "/manage/user/information/register/list"
    QUERY_REGISTER_OWNER_DETAIL: str = "/manage/user/information/register/detail"
    QUERY_REGISTER_OWNER_EXPORT: str = "/manage/user/information/register/list/export"
    QUERY_UNREGISTER_OWNER_BY_PAGINATOR: str = "/manage/user/information/unregister/list"
    QUERY_UNREGISTER_OWNER_DETAIL: str = "/manage/user/information/unregister/detail"
    QUERY_UNREGISTER_OWNER_EXPORT: str = "/manage/user/information/unregister/list/export"
    QUERY_SHOP_GOODS_CATEGORY_BY_PAGINATOR: str = "/manage/productCategory/getProductCategoryList"
    QUERY_SHOP_GOODS_BY_PAGINATOR: str = "/manage/shopGoods/getAdminShopGoods"
    QUERY_SHOP_GOODS_DETAIL: str = "/manage/shopGoods/getShopGoodsDetail"
    SAVE_SHOP_GOODS: str = "/manage/shopGoods/saveSysShopGoods"
    UPDATE_SHOP_GOODS: str = "/manage/shopGoods/updateShopGoods"
    QUERY_SHOP_GOODS_PUSH_TO_STORE: str = "/manage/shopGoods/getGoodsStoreEdits"
    SAVE_SHOP_GOODS_PUSH_TO_STORE: str = "/manage/shopGoods/saveGoodsStoreEdits"
    QUERY_STORE_PRODUCT_BY_PAGINATOR: str = "/manage/storeProduct/getAdminStoreProductList"
    QUERY_STORE_PRODUCT_DETAIL: str = "/manage/storeProduct/getStoreProductInfo"
    UPDATE_STORE_PRODUCT: str = "/manage/storeProduct/updateStoreProductInfo"
    UPDATE_STORE_PRODUCT_STATUS: str = "/manage/storeProduct/updateProductStatus"
    QUERY_BUSINESS_ORDER_BY_PAGINATOR: str = "/manage/businessOrderShu/list"
    QUERY_BUSINESS_ORDER_DETAIL: str = "/manage/businessOrderShu/view"
    QUERY_BUSINESS_ORDER_EXPORT_1: str = "/manage/businessOrder/exportToExcelByOrder"
    QUERY_BUSINESS_ORDER_EXPORT_2: str = "/manage/businessOrder/exportToExcelByProduct"
    QUERY_BUSINESS_ORDER_EXPORT_3: str = "/manage/businessOrder/exportToExcelByOrderAndProduct"
    QUERY_WORK_ORDER_BY_PAGINATOR: str = "/old/orderAction!viewList.action"
    QUERY_WORK_ORDER_DETAIL: str = "/old/orderAction!view.action"
    QUERY_WORK_ORDER_EXPORT: str = "/manage/order/work/export"
    QUERY_PARKING_AUTH_BY_PAGINATOR: str = "/manage/carParkApplication/carParkCard/list"
    QUERY_PARKING_AUTH_DETAIL: str = "/manage/carParkApplication/carParkCard"
    UPDATE_PARKING_AUTH: str = "/manage/carParkApplication/carParkCard"
    QUERY_PARKING_AUTH_AUDIT_BY_PAGINATOR: str = "/manage/carParkApplication/carParkCard/parkingCardManagerByAudit"
    QUERY_PARKING_AUTH_AUDIT_CHECK_BY_PAGINATOR: str = "/manage/carParkApplication/getParkingCheckList"
    UPDATE_PARKING_AUTH_AUDIT_STATUS: str = "/manage/carParkApplication/completeTask"
    QUERY_EXPORT_BY_PAGINATOR: str = "/manage/export/log"
    UPLOAD: str = "/upload"
    QUERY_SURVEY_LIST_WITH_PAGINATOR = "/manage/questionnaire/list/managent"
    QUERY_SURVEY_PARTICIPATION_LIST_WITH_PAGINATOR = "/manage/questionnaire/joinuser/list"


class Api(Request):
    """
    智慧社区全域服务平台 Admin API Class
    """

    def __init__(
            self,
            base_url: str = "https://sq.wisharetec.com/",
            username: str = None,
            password: str = None,
            cache_instance: Union[diskcache.Cache, redis.Redis, redis.StrictRedis] = None
    ):
        """
        构造函数
        :param base_url: 基础url
        :param username: 用户名
        :param password: 密码
        :param cache_instance: 缓存实例
        """
        super().__init__()
        self._base_url = base_url
        self._username = username
        self._password = password
        self._cache_instance = cache_instance
        self._token_data = Dict()

    @property
    def base_url(self):
        """
        基础url
        :return:
        """
        return self._base_url[:-1] if self._base_url.endswith("/") else self._base_url

    @base_url.setter
    def base_url(self, base_url):
        """
        基础url
        :param base_url:
        :return:
        """
        self._base_url = base_url

    @property
    def username(self):
        """
        用户名
        :return:
        """
        return self._username

    @username.setter
    def username(self, username):
        """
        用户名
        :param username:
        :return:
        """
        self._username = username

    @property
    def password(self):
        """
        密码
        :return:
        """
        return self._password

    @password.setter
    def password(self, password):
        """
        密码
        :param password:
        :return:
        """
        self._password = password

    @property
    def cache_instance(self):
        """
        缓存实例
        :return:
        """
        return self._cache_instance

    @cache_instance.setter
    def cache_instance(self, cache_instance):
        """
        缓存实例
        :param cache_instance:
        :return:
        """
        self._cache_instance = cache_instance

    @property
    def token_data(self):
        """
        token 数据
        :return:
        """
        return Dict(self._token_data)

    @token_data.setter
    def token_data(self, token_data):
        """
        token 数据
        :param token_data:
        :return:
        """
        self._token_data = Dict(token_data)

    def get_token_data_by_cache(self, name: str = None):
        """
        get token data by cache

        if isinstance(self.cache_instance,(diskcache.Cache,redis.Redis,redis.StrictRedis)): usage cache

        :param name: cache key
        :return: token data
        """
        name = name or f"guolei_py3_wisharetec_token_data__{self.username}"
        if isinstance(self.cache_instance, diskcache.Cache):
            self.token_data = self.cache_instance.get(key=name)
        if isinstance(self.cache_instance, (redis.Redis, redis.StrictRedis)):
            self.token_data = self.cache_instance.hgetall(name=name)
        return Dict(self.token_data)

    def put_token_data_to_cache(
            self, name: str = None,
            expire: Union[float, int, timedelta] = None,
            token_data: dict = None
    ):
        """
        put token data into cache

        if isinstance(self.cache_instance,(diskcache.Cache,redis.Redis,redis.StrictRedis)): usage cache
        :param name: cache key
        :param expire: cache expire time
        :param token_data: token data
        :return:
        """
        token_data = Dict(self.token_data)
        if not Draft202012Validator({
            "type": "object",
            "properties": {
                "token": {"type": "string", "minLength": 1},
                "companyCode": {"type": "string", "minLength": 1},
            },
            "required": ["name", "expire", "token_data"]
        }).is_valid(token_data):
            return False
        name = name or f"guolei_py3_wisharetec_token_data__{self.username}"
        if isinstance(self.cache_instance, diskcache.Cache):
            return self.cache_instance.set(
                key=name,
                value=token_data,
                expire=expire or timedelta(days=30).total_seconds()
            )

        if isinstance(self.cache_instance, (redis.Redis, redis.StrictRedis)):
            self.cache_instance.hset(
                name=name,
                mapping=token_data
            )
            self.cache_instance.expire(
                name=name,
                time=expire or timedelta(days=30)
            )
            return True
        return False

    def get(self, on_response_callback: Callable = ResponseCallback.json_status_100_data, path: str = None, **kwargs):
        """
        execute Request.get()

        headers.setdefault("Token", self.token_data.get("token", ""))

        headers.setdefault("Companycode", self.token_data.get("companyCode", ""))

        :param on_response_callback: response callback
        :param path: if url is None: url=f"{self.base_url}{path}"
        :param kwargs: requests.get(**kwargs)
        :return: on_response_callback(response) or response
        """
        kwargs = Dict(kwargs)
        kwargs.setdefault("url", f"{self.base_url}{path}")
        kwargs.headers = Dict({
            **{
                "Token": self.token_data.get("token", ""),
                "Companycode": self.token_data.get("companyCode", "")
            }
        })
        return super().get(on_response_callback=on_response_callback, **kwargs.to_dict())

    def post(self, on_response_callback: Callable = ResponseCallback.json_status_100_data, path: str = None, **kwargs):
        """
        execute post by requests.post

        headers.setdefault("Token", self.token_data.get("token", ""))

        headers.setdefault("Companycode", self.token_data.get("companyCode", ""))

        :param on_response_callback: response callback
        :param path: if url is None: url=f"{self.base_url}{path}"
        :param kwargs: requests.get(**kwargs)
        :return: on_response_callback(response) or response
        """

        kwargs = Dict(kwargs)
        kwargs.setdefault("url", f"{self.base_url}{path}")
        kwargs.headers = Dict({
            **{
                "Token": self.token_data.get("token", ""),
                "Companycode": self.token_data.get("companyCode", "")
            }
        })
        return super().post(on_response_callback=on_response_callback, **kwargs.to_dict())

    def put(self, on_response_callback: Callable = ResponseCallback.json_status_100_data, path: str = None, **kwargs):
        """
        execute put by requests.put

        headers.setdefault("Token", self.token_data.get("token", ""))

        headers.setdefault("Companycode", self.token_data.get("companyCode", ""))

        :param on_response_callback: response callback
        :param path: if url is None: url=f"{self.base_url}{path}"
        :param kwargs: requests.get(**kwargs)
        :return: on_response_callback(response) or response
        """
        kwargs = Dict(kwargs)
        kwargs.setdefault("url", f"{self.base_url}{path}")
        kwargs.headers = Dict({
            **{
                "Token": self.token_data.get("token", ""),
                "Companycode": self.token_data.get("companyCode", "")
            }
        })
        return super().put(on_response_callback=on_response_callback, **kwargs.to_dict())

    def request(self, on_response_callback: Callable = ResponseCallback.json_status_100_data, path: str = None,
                **kwargs):
        """
        execute request by requests.request

        headers.setdefault("Token", self.token_data.get("token", ""))

        headers.setdefault("Companycode", self.token_data.get("companyCode", ""))

        :param on_response_callback: response callback
        :param path: if url is None: url=f"{self.base_url}{path}"
        :param kwargs: requests.get(**kwargs)
        :return: on_response_callback(response) or response
        """
        kwargs = Dict(kwargs)
        kwargs.setdefault("url", f"{self.base_url}{path}")
        kwargs.headers = Dict({
            **{
                "Token": self.token_data.get("token", ""),
                "Companycode": self.token_data.get("companyCode", "")
            }
        })
        return super().request(on_response_callback=on_response_callback, **kwargs.to_dict())

    def login(self):
        """
        execute login

        if isinstance(self.cache_instance,(diskcache.Cache,redis.Redis,redis.StrictRedis)): usage cache

        :return:
        """
        self.token_data = self.get_token_data_by_cache()
        result: bool = self.get(
            on_response_callback=ResponseCallback.text_start_with_null,
            path=f"{UrlSetting.QUERY_LOGIN_STATE}"
        )
        if result:
            return self
        result: dict = self.post(
            on_response_callback=ResponseCallback.json_status_100_data,
            path=f"{UrlSetting.LOGIN}",
            data={
                "username": self.username,
                "password": hashlib.md5(self.password.encode("utf-8")).hexdigest(),
                "mode": "PASSWORD",
            }
        )
        if Draft202012Validator({
            "type": "object",
            "properties": {
                "token": {"type": "string", "minLength": 1},
                "companyCode": {"type": "string", "minLength": 1},
            },
            "required": ["token", "companyCode"],
        }).is_valid(result):
            self.token_data = result
            self.put_token_data_to_cache()
        return self
