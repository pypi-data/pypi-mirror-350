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
import json
import pathlib
from datetime import timedelta, datetime
from typing import Union, Iterable, Callable

import redis
import requests
from addict import Dict
from diskcache import Cache
from guolei_py3_requests import requests_request, RequestsResponseCallable
from requests import Response
from retrying import retry


class RequestsResponseCallable(RequestsResponseCallable):

    @staticmethod
    def status_code_200_text_is_str_null(response: Response = None):
        return RequestsResponseCallable.status_code_200_text(response=response).strip() == "null"

    @staticmethod
    def status_code_200_json_addict_status_100(response: Response = None):
        json_addict = RequestsResponseCallable.status_code_200_json_addict(response=response)
        return json_addict.status == 100 or json_addict.status == "100"

    @staticmethod
    def status_code_200_json_addict_status_100_data(response: Response = None):
        if RequestsResponseCallable.status_code_200_json_addict_status_100(response=response):
            return RequestsResponseCallable.status_code_200_json_addict(response=response).data
        return Dict({})

    @staticmethod
    def status_code_200_json_addict_status_100_data_result_list(response: Response = None):
        if RequestsResponseCallable.status_code_200_json_addict_status_100(response=response):
            return RequestsResponseCallable.status_code_200_json_addict(response=response).data.resultList
        return Dict({})


class AdminApi(object):
    """
    慧享(绿城)科技 智慧社区全域服务平台 Admin API Class
    """

    def __init__(
            self,
            base_url: str = "",
            uid: str = "",
            pwd: str = "",
            diskcache: Cache = None,
            strict_redis: redis.StrictRedis = None
    ):
        """
        慧享(绿城)科技 智慧社区全域服务平台 Class 构造函数
        :param base_url: base url
        :param uid: 用户名
        :param pwd: 密码
        :param diskcache: diskcache.core.Cache
        :param strict_redis: redis.StrictRedis
        """
        self._base_url = base_url
        self._uid = uid
        self._pwd = pwd
        self._token_data = Dict({})
        self._diskcache = diskcache
        self._strict_redis = strict_redis

    @property
    def base_url(self):
        """
        base url
        :return:
        """
        return self._base_url[:-1] if self._base_url.endswith("/") else self._base_url

    @base_url.setter
    def base_url(self, value: str = "") -> str:
        """
        base url
        :param value:
        :return:
        """
        self._base_url = value

    @property
    def uid(self) -> str:
        """
        用户名
        :return:
        """
        return self._uid

    @uid.setter
    def uid(self, value: str = ""):
        """
        用户名
        :param value:
        :return:
        """
        self._uid = value

    @property
    def pwd(self) -> str:
        """
        密码
        :return:
        """
        return self._pwd

    @pwd.setter
    def pwd(self, value: str = ""):
        """
        密码
        :param value:
        :return:
        """
        self._pwd = value

    @property
    def token_data(self) -> dict:
        """
        token data
        :return:
        """
        return self._token_data

    @property
    def diskcache(self) -> Cache:
        """
        diskcache.core.Cache Class Object
        :return:
        """
        return self._diskcache

    @diskcache.setter
    def diskcache(self, value: Cache = None):
        """
        diskcache.core.Cache Class Object
        :param value:
        :return:
        """
        return self._diskcache

    @property
    def strict_redis(self) -> redis.StrictRedis:
        """
        redis.StrictRedis Class Object
        :return:
        """
        return self._strict_redis

    @strict_redis.setter
    def strict_redis(self, value: redis.StrictRedis = None):
        """
        redis.StrictRedis Class Object
        :param value:
        :return:
        """
        self._strict_redis = value

    def check_login(
            self,
            requests_response_callable: Callable = RequestsResponseCallable.status_code_200_text_is_str_null,
            requests_request_args: Iterable = (),
            requests_request_kwargs: dict = {}
    ) -> bool:
        """
        检测登录
        :param requests_response_callable: RequestsResponseCallable.status_code_200_text_is_str_null
        :param requests_request_args: requests_request(requests_response_callable,requests_request_args,requests_request_kwargs)
        :param requests_request_kwargs: requests_request(requests_response_callable,requests_request_args,requests_request_kwargs)
        :return:
        """
        if not isinstance(self.token_data, dict):
            return False
        if not len(self.token_data.keys()):
            return False
        if not isinstance(Dict(self.token_data).token, str):
            return False
        if not len(Dict(self.token_data).token):
            return False
        requests_request_kwargs = Dict(requests_request_kwargs)
        requests_request_kwargs = Dict({
            "url": f"{self.base_url}/old/serverUserAction!checkSession.action",
            "method": "GET",
            "headers": {
                "Token": Dict(self.token_data).token,
                "Companycode": Dict(self.token_data).companyCode,
            },
            **requests_request_kwargs,
        })
        return requests_request(
            requests_response_callable=requests_response_callable,
            requests_request_args=requests_request_args,
            requests_request_kwargs=requests_request_kwargs
        )

    def login(
            self,
            requests_response_callable: Callable = RequestsResponseCallable.status_code_200_json_addict_status_100_data,
            requests_request_args: Iterable = (),
            requests_request_kwargs: dict = {}
    ) -> bool:
        """
        登录
        :param requests_response_callable: RequestsResponseCallable.status_code_200_json_addict_status_100_data
        :param requests_request_args: requests_request(requests_response_callable,requests_request_args,requests_request_kwargs)
        :param requests_request_kwargs: requests_request(requests_response_callable,requests_request_args,requests_request_kwargs)
        :return:
        """
        requests_request_kwargs = Dict(requests_request_kwargs)
        requests_request_kwargs = Dict({
            "url": f"{self.base_url}/manage/login",
            "method": "POST",
            "data": {
                "username": self.uid,
                "password": hashlib.md5(self.pwd.encode("utf-8")).hexdigest(),
                "mode": "PASSWORD",
            },
            **requests_request_kwargs,
        })
        self._token_data = requests_request(
            requests_response_callable=requests_response_callable,
            requests_request_args=requests_request_args,
            requests_request_kwargs=requests_request_kwargs
        )
        if not len(self.token_data.keys()):
            return False
        return True

    def login_with_strict_redis(self, strict_redis: redis.StrictRedis = None):
        """
        使用redis.StrictRedis登录
        :param strict_redis: redis.StrictRedis if None usage self.strict_redis
        :return:
        """
        # 缓存key
        cache_key = "_".join([
            f"guolei_py3_wisharetec",
            f"scaasp",
            f"AdminApi",
            f"redis",
            f"token_data",
            f"{hashlib.md5(self.base_url.encode('utf-8')).hexdigest()}",
            f"{self.uid}",
        ])
        if strict_redis is None or not isinstance(strict_redis, redis.StrictRedis):
            strict_redis = self.strict_redis
        if isinstance(strict_redis, redis.StrictRedis):
            self._token_data = Dict(json.loads(strict_redis.get(cache_key)))
        if not self.check_login():
            if self.login():
                if isinstance(strict_redis, redis.StrictRedis):
                    strict_redis.setex(name=cache_key, value=json.dumps(self.token_data), time=timedelta(days=90))
        return self

    def login_with_diskcache(self, diskcache: Cache = None):
        """
        使用diskcache登录
        :param cache: diskcache.core.Cache if None usage self.diskcache
        :return:
        """
        # 缓存key
        cache_key = "_".join([
            f"guolei_py3_wisharetec",
            f"scaasp",
            f"AdminApi",
            f"diskcache",
            f"token_data",
            f"{hashlib.md5(self.base_url.encode('utf-8')).hexdigest()}",
            f"{self.uid}",
        ])
        if diskcache is None or not isinstance(diskcache, Cache):
            diskcache = self.diskcache
        if isinstance(diskcache, Cache):
            self._token_data = diskcache.get(key=cache_key, default={})
        if not self.check_login():
            if self.login():
                if isinstance(diskcache, Cache):
                    diskcache.set(key=cache_key, value=self.token_data, expire=timedelta(days=90).total_seconds())
        return self

    def login_with_cache(self, cache_type: str = "diskcache", cache: Union[Cache, redis.StrictRedis] = None):
        """
        使用缓存登录
        :param cache_type: diskcache=login_with_diskcache(cache) strict_redis=login_with_strict_redis(cache)
        :param cache: diskcache.core.Cache if None usage self.diskcache or redis.StrictRedis if None usage self.strict_redis
        :return:
        """
        if isinstance(cache_type, str) and cache_type.lower() in [
            "disk_cache".lower(),
            "diskcache".lower(),
            "disk".lower(),
        ]:
            return self.login_with_diskcache(diskcache=cache)
        if isinstance(cache_type, str) and cache_type.lower() in [
            "strict_redis".lower(),
            "strictredis".lower(),
            "redis".lower(),
        ]:
            return self.login_with_strict_redis(strict_redis=cache)
        self.login()
        return self

    def query_communities(
            self,
            requests_request_kwargs_params: dict = {},
            requests_response_callable: Callable = RequestsResponseCallable.status_code_200_json_addict_status_100_data,
            requests_request_args: Iterable = (),
            requests_request_kwargs: dict = {},
    ):
        """
        分页查询项目列表
        :param requests_request_kwargs_params:
        :param requests_response_callable: requests_response_with_code_200_json_addict_status_100_data
        :param requests_request_args: requests_request(requests_response_callable,requests_request_args,requests_request_kwargs)
        :param requests_request_kwargs: requests_request(requests_response_callable,requests_request_args,requests_request_kwargs)
        :return:
        """
        requests_request_kwargs_params = Dict(requests_request_kwargs_params)
        requests_request_kwargs = Dict(requests_request_kwargs)
        requests_request_kwargs = Dict(
            {
                "url": f"{self.base_url}/manage/communityInfo/getAdminCommunityList",
                "method": "GET",
                "headers": {
                    "Token": Dict(self.token_data).token if isinstance(Dict(self.token_data).token, str) else "",
                    "Companycode": Dict(self.token_data).companyCode if isinstance(Dict(self.token_data).companyCode,
                                                                                   str) else "",
                    **requests_request_kwargs.headers,
                },
                "params": {
                    "pageSize": 20,
                    **requests_request_kwargs_params,
                    **requests_request_kwargs.params,
                },
                **requests_request_kwargs,
            }
        )
        return requests_request(
            requests_response_callable=requests_response_callable,
            requests_request_args=requests_request_args,
            requests_request_kwargs=requests_request_kwargs
        )

    def query_shops(
            self,
            requests_request_kwargs_params: dict = {},
            requests_response_callable: Callable = RequestsResponseCallable.status_code_200_json_addict_status_100_data,
            requests_request_args: Iterable = (),
            requests_request_kwargs: dict = {},
    ):
        """
        分页查询商家信息
        :param requests_request_kwargs_params:
        :param requests_response_callable: RequestsResponseCallable.status_code_200_json_addict_status_100_data
        :param requests_request_args: requests_request(requests_response_callable,requests_request_args,requests_request_kwargs)
        :param requests_request_kwargs: requests_request(requests_response_callable,requests_request_args,requests_request_kwargs)
        :return:
        """
        requests_request_kwargs_params = Dict(requests_request_kwargs_params)
        requests_request_kwargs = Dict(requests_request_kwargs)
        requests_request_kwargs = Dict(
            {
                "url": f"{self.base_url}/manage/shop/page",
                "method": "GET",
                "headers": {
                    "Token": Dict(self.token_data).token if isinstance(Dict(self.token_data).token, str) else "",
                    "Companycode": Dict(self.token_data).companyCode if isinstance(Dict(self.token_data).companyCode,
                                                                                   str) else "",
                    **requests_request_kwargs.headers,
                },
                "params": {
                    "pageSize": 20,
                    **requests_request_kwargs_params,
                    **requests_request_kwargs.params,
                },
                **requests_request_kwargs,
            }
        )
        return requests_request(
            requests_response_callable=requests_response_callable,
            requests_request_args=requests_request_args,
            requests_request_kwargs=requests_request_kwargs
        )

    def query_shop(
            self,
            id: str = None,
            requests_response_callable: Callable = RequestsResponseCallable.status_code_200_json_addict_status_100_data,
            requests_request_args: Iterable = (),
            requests_request_kwargs: dict = {},
    ):
        """
        查询商家详情
        :param id: 商家id
        :param requests_response_callable: RequestsResponseCallable.status_code_200_json_addict_status_100_data
        :param requests_request_args: requests_request(requests_response_callable,requests_request_args,requests_request_kwargs)
        :param requests_request_kwargs: requests_request(requests_response_callable,requests_request_args,requests_request_kwargs)
        :return:
        """
        requests_request_kwargs = Dict(requests_request_kwargs)
        requests_request_kwargs = Dict(
            {
                "url": f"{self.base_url}/manage/shop/getShopInfo",
                "method": "GET",
                "headers": {
                    "Token": Dict(self.token_data).token if isinstance(Dict(self.token_data).token, str) else "",
                    "Companycode": Dict(self.token_data).companyCode if isinstance(Dict(self.token_data).companyCode,
                                                                                   str) else "",
                    **requests_request_kwargs.headers,
                },
                "params": {
                    "shopId": id,
                    **requests_request_kwargs.params,
                },
                **requests_request_kwargs,
            }
        )
        return requests_request(
            requests_response_callable=requests_response_callable,
            requests_request_args=requests_request_args,
            requests_request_kwargs=requests_request_kwargs
        )

    def query_stores(
            self,
            requests_request_kwargs_params: dict = {},
            requests_response_callable: Callable = RequestsResponseCallable.status_code_200_json_addict_status_100_data,
            requests_request_args: Iterable = (),
            requests_request_kwargs: dict = {},
    ):
        """
        分页查询门店列表
        :param requests_request_kwargs_params:
        :param requests_response_callable: RequestsResponseCallable.status_code_200_json_addict_status_100_data
        :param requests_request_args: requests_request(requests_response_callable,requests_request_args,requests_request_kwargs)
        :param requests_request_kwargs: requests_request(requests_response_callable,requests_request_args,requests_request_kwargs)
        :return:
        """
        requests_request_kwargs_params = Dict(requests_request_kwargs_params)
        requests_request_kwargs = Dict(requests_request_kwargs)
        requests_request_kwargs = Dict(
            {
                "url": f"{self.base_url}/manage/store/page",
                "method": "GET",
                "headers": {
                    "Token": Dict(self.token_data).token if isinstance(Dict(self.token_data).token, str) else "",
                    "Companycode": Dict(self.token_data).companyCode if isinstance(Dict(self.token_data).companyCode,
                                                                                   str) else "",
                    **requests_request_kwargs.headers,
                },
                "params": {
                    "pageSize": 20,
                    **requests_request_kwargs_params,
                    **requests_request_kwargs.params,
                },
                **requests_request_kwargs,
            }
        )
        return requests_request(
            requests_response_callable=requests_response_callable,
            requests_request_args=requests_request_args,
            requests_request_kwargs=requests_request_kwargs
        )

    def query_store(
            self,
            id: str = None,
            requests_response_callable: Callable = RequestsResponseCallable.status_code_200_json_addict_status_100_data,
            requests_request_args: Iterable = (),
            requests_request_kwargs: dict = {},
    ):
        """
        查询门店详情
        :param id: 门店id
        :param requests_response_callable: RequestsResponseCallable.status_code_200_json_addict_status_100_data
        :param requests_request_args: requests_request(requests_response_callable,requests_request_args,requests_request_kwargs)
        :param requests_request_kwargs: requests_request(requests_response_callable,requests_request_args,requests_request_kwargs)
        :return:
        """
        requests_request_kwargs = Dict(requests_request_kwargs)
        requests_request_kwargs = Dict(
            {
                "url": f"{self.base_url}/manage/store/getStoreDetail",
                "method": "GET",
                "headers": {
                    "Token": Dict(self.token_data).token if isinstance(Dict(self.token_data).token, str) else "",
                    "Companycode": Dict(self.token_data).companyCode if isinstance(Dict(self.token_data).companyCode,
                                                                                   str) else "",
                    **requests_request_kwargs.headers,
                },
                "params": {
                    "storeId": id,
                    **requests_request_kwargs.params,
                },
                **requests_request_kwargs,
            }
        )
        return requests_request(
            requests_response_callable=requests_response_callable,
            requests_request_args=requests_request_args,
            requests_request_kwargs=requests_request_kwargs
        )

    def query_shop_products(
            self,
            requests_request_kwargs_params: dict = {},
            requests_response_callable: Callable = RequestsResponseCallable.status_code_200_json_addict_status_100_data,
            requests_request_args: Iterable = (),
            requests_request_kwargs: dict = {},
    ):
        """
        分页查询商家产品列表
        :param requests_request_kwargs_params:
        :param requests_response_callable:
        :param requests_request_args: requests_request(requests_response_callable,requests_request_args,requests_request_kwargs)
        :param requests_request_kwargs: requests_request(requests_response_callable,requests_request_args,requests_request_kwargs)
        :return:
        """
        requests_request_kwargs_params = Dict(requests_request_kwargs_params)
        requests_request_kwargs = Dict(requests_request_kwargs)
        requests_request_kwargs = Dict(
            {
                "url": f"{self.base_url}/manage/shopGoods/getAdminShopGoods",
                "method": "GET",
                "headers": {
                    "Token": Dict(self.token_data).token if isinstance(Dict(self.token_data).token, str) else "",
                    "Companycode": Dict(self.token_data).companyCode if isinstance(Dict(self.token_data).companyCode,
                                                                                   str) else "",
                    **requests_request_kwargs.headers,
                },
                "params": {
                    "pageSize": 20,
                    **requests_request_kwargs_params,
                    **requests_request_kwargs.params,
                },
                **requests_request_kwargs,
            }
        )
        return requests_request(
            requests_response_callable=requests_response_callable,
            requests_request_args=requests_request_args,
            requests_request_kwargs=requests_request_kwargs
        )

    def query_shop_product(
            self,
            id: str = None,
            requests_response_callable: Callable = RequestsResponseCallable.status_code_200_json_addict_status_100_data,
            requests_request_args: Iterable = (),
            requests_request_kwargs: dict = {},
    ):
        """
        查询商家产品详情
        :param id: 商家产品id
        :param requests_response_callable: RequestsResponseCallable.status_code_200_json_addict_status_100_data
        :param requests_request_args: requests_request(requests_response_callable,requests_request_args,requests_request_kwargs)
        :param requests_request_kwargs: requests_request(requests_response_callable,requests_request_args,requests_request_kwargs)
        :return:
        """
        requests_request_kwargs = Dict(requests_request_kwargs)
        requests_request_kwargs = Dict(
            {
                "url": f"{self.base_url}/manage/shopGoods/getShopGoodsDetail",
                "method": "GET",
                "headers": {
                    "Token": Dict(self.token_data).token if isinstance(Dict(self.token_data).token, str) else "",
                    "Companycode": Dict(self.token_data).companyCode if isinstance(Dict(self.token_data).companyCode,
                                                                                   str) else "",
                    **requests_request_kwargs.headers,
                },
                "params": {
                    "id": id,
                    **requests_request_kwargs.params,
                },
                **requests_request_kwargs,
            }
        )
        return requests_request(
            requests_response_callable=requests_response_callable,
            requests_request_args=requests_request_args,
            requests_request_kwargs=requests_request_kwargs
        )

    def query_shop_product_store_edits(
            self,
            id: str = None,
            requests_response_callable: Callable = RequestsResponseCallable.status_code_200_json_addict_status_100_data,
            requests_request_args: Iterable = (),
            requests_request_kwargs: dict = {},
    ):
        """
        查询商家产品推送到门店信息
        :param id: 商家产品id
        :param requests_response_callable: RequestsResponseCallable.status_code_200_json_addict_status_100_data
        :param requests_request_args: requests_request(requests_response_callable,requests_request_args,requests_request_kwargs)
        :param requests_request_kwargs: requests_request(requests_response_callable,requests_request_args,requests_request_kwargs)
        :return:
        """
        requests_request_kwargs = Dict(requests_request_kwargs)
        requests_request_kwargs = Dict(
            {
                "url": f"{self.base_url}/manage/shopGoods/getGoodsStoreEdits",
                "method": "GET",
                "headers": {
                    "Token": Dict(self.token_data).token if isinstance(Dict(self.token_data).token, str) else "",
                    "Companycode": Dict(self.token_data).companyCode if isinstance(Dict(self.token_data).companyCode,
                                                                                   str) else "",
                    **requests_request_kwargs.headers,
                },
                "params": {
                    "id": id,
                    **requests_request_kwargs.params,
                },
                **requests_request_kwargs,
            }
        )
        return requests_request(
            requests_response_callable=requests_response_callable,
            requests_request_args=requests_request_args,
            requests_request_kwargs=requests_request_kwargs
        )

    def save_shop_product_store_edits(
            self,
            requests_request_kwargs_json: dict = {},
            requests_response_callable: Callable = RequestsResponseCallable.status_code_200_json_addict_status_100,
            requests_request_args: Iterable = (),
            requests_request_kwargs: dict = {}
    ) -> bool:
        """
        保存商家产品信息推送到门店
        :param requests_request_kwargs_json:
        :param requests_response_callable: RequestsResponseCallable.status_code_200_json_addict_status_100_data
        :param requests_request_args: requests_request(requests_response_callable,requests_request_args,requests_request_kwargs)
        :param requests_request_kwargs: requests_request(requests_response_callable,requests_request_args,requests_request_kwargs)
        :return:
        """
        requests_request_kwargs_json = Dict(requests_request_kwargs_json)
        requests_request_kwargs = Dict(requests_request_kwargs)
        requests_request_kwargs = Dict(
            {
                "url": f"{self.base_url}/manage/shopGoods/saveGoodsStoreEdits",
                "method": "POST",
                "headers": {
                    "Token": Dict(self.token_data).token if isinstance(Dict(self.token_data).token, str) else "",
                    "Companycode": Dict(self.token_data).companyCode if isinstance(Dict(self.token_data).companyCode,
                                                                                   str) else "",
                    **requests_request_kwargs.headers,
                },
                "json": {
                    **requests_request_kwargs_json,
                    **requests_request_kwargs.json,
                },
                **requests_request_kwargs,
            }
        )
        return requests_request(
            requests_response_callable=requests_response_callable,
            requests_request_args=requests_request_args,
            requests_request_kwargs=requests_request_kwargs
        )

    def save_shop_product(
            self,
            requests_request_kwargs_json: dict = {},
            requests_response_callable: Callable = RequestsResponseCallable.status_code_200_json_addict_status_100,
            requests_request_args: Iterable = (),
            requests_request_kwargs: dict = {}
    ) -> bool:
        """
        保存商家产品信息
        :param requests_request_kwargs_json:
        :param requests_response_callable: RequestsResponseCallable.status_code_200_json_addict_status_100_data
        :param requests_request_args: requests_request(requests_response_callable,requests_request_args,requests_request_kwargs)
        :param requests_request_kwargs: requests_request(requests_response_callable,requests_request_args,requests_request_kwargs)
        :return:
        """
        requests_request_kwargs_json = Dict(requests_request_kwargs_json)
        requests_request_kwargs = Dict(requests_request_kwargs)
        requests_request_kwargs = Dict(
            {
                "url": f"{self.base_url}/manage/shopGoods/saveSysShopGoods",
                "method": "POST",
                "headers": {
                    "Token": Dict(self.token_data).token if isinstance(Dict(self.token_data).token, str) else "",
                    "Companycode": Dict(self.token_data).companyCode if isinstance(Dict(self.token_data).companyCode,
                                                                                   str) else "",
                    **requests_request_kwargs.headers,
                },
                "json": {
                    **requests_request_kwargs_json,
                    **requests_request_kwargs.json,
                },
                **requests_request_kwargs,
            }
        )
        if isinstance(requests_request_kwargs_json.id, str) and len(requests_request_kwargs_json.id):
            requests_request_kwargs.method = "PUT"
            requests_request_kwargs.url = f"{self.base_url}/manage/shopGoods/updateShopGoods"
        return requests_request(
            requests_response_callable=requests_response_callable,
            requests_request_args=requests_request_args,
            requests_request_kwargs=requests_request_kwargs
        )

    def query_store_goodses(
            self,
            requests_request_kwargs_params: dict = {},
            requests_response_callable: Callable = RequestsResponseCallable.status_code_200_json_addict_status_100_data,
            requests_request_args: Iterable = (),
            requests_request_kwargs: dict = {}
    ):
        """
        分页查询门店商品列表
        :param requests_request_kwargs_params:
        :param requests_response_callable: RequestsResponseCallable.status_code_200_json_addict_status_100_data
        :param requests_request_args: requests_request(requests_response_callable,requests_request_args,requests_request_kwargs)
        :param requests_request_kwargs: requests_request(requests_response_callable,requests_request_args,requests_request_kwargs)
        :return:
        """
        requests_request_kwargs_params = Dict(requests_request_kwargs_params)
        requests_request_kwargs = Dict(requests_request_kwargs)
        requests_request_kwargs = Dict(
            {
                "url": f"{self.base_url}/manage/storeProduct/getAdminStoreProductList",
                "method": "GET",
                "headers": {
                    "Token": Dict(self.token_data).token if isinstance(Dict(self.token_data).token, str) else "",
                    "Companycode": Dict(self.token_data).companyCode if isinstance(Dict(self.token_data).companyCode,
                                                                                   str) else "",
                    **requests_request_kwargs.headers,
                },
                "params": {
                    "pageSize": 20,
                    **requests_request_kwargs_params,
                    **requests_request_kwargs.params,
                },
                **requests_request_kwargs,
            }
        )
        return requests_request(
            requests_response_callable=requests_response_callable,
            requests_request_args=requests_request_args,
            requests_request_kwargs=requests_request_kwargs
        )

    def query_store_goods(
            self,
            id: str = None,
            requests_response_callable: Callable = RequestsResponseCallable.status_code_200_json_addict_status_100_data,
            requests_request_args: Iterable = (),
            requests_request_kwargs: dict = {},
    ):
        """
        查询门店商品详情
        :param id: 门店商品id
        :param requests_response_callable: RequestsResponseCallable.status_code_200_json_addict_status_100_data
        :param requests_request_args: requests_request(requests_response_callable,requests_request_args,requests_request_kwargs)
        :param requests_request_kwargs: requests_request(requests_response_callable,requests_request_args,requests_request_kwargs)
        :return:
        """
        requests_request_kwargs = Dict(requests_request_kwargs)
        requests_request_kwargs = Dict(
            {
                "url": f"{self.base_url}/manage/storeProduct/getStoreProductInfo",
                "method": "GET",
                "headers": {
                    "Token": Dict(self.token_data).token if isinstance(Dict(self.token_data).token, str) else "",
                    "Companycode": Dict(self.token_data).companyCode if isinstance(Dict(self.token_data).companyCode,
                                                                                   str) else "",
                    **requests_request_kwargs.headers,
                },
                "params": {
                    "id": id,
                    **requests_request_kwargs.params,
                },
                **requests_request_kwargs,
            }
        )
        return requests_request(
            requests_response_callable=requests_response_callable,
            requests_request_args=requests_request_args,
            requests_request_kwargs=requests_request_kwargs
        )

    def update_store_goods(
            self,
            requests_request_kwargs_json: dict = {},
            requests_response_callable: Callable = RequestsResponseCallable.status_code_200_json_addict_status_100_data,
            requests_request_args: Iterable = (),
            requests_request_kwargs: dict = {},
    ) -> bool:
        """
        更新门店商品信息
        :param requests_request_kwargs_json:
        :param requests_response_callable: RequestsResponseCallable.status_code_200_json_addict_status_100_data
        :param requests_request_args: requests_request(requests_response_callable,requests_request_args,requests_request_kwargs)
        :param requests_request_kwargs: requests_request(requests_response_callable,requests_request_args,requests_request_kwargs)
        :return:
        """
        requests_request_kwargs_json = Dict(requests_request_kwargs_json)
        requests_request_kwargs = Dict(requests_request_kwargs)
        requests_request_kwargs = Dict(
            {
                "url": f"{self.base_url}/manage/storeProduct/updateStoreProductInfo",
                "method": "POST",
                "headers": {
                    "Token": Dict(self.token_data).token if isinstance(Dict(self.token_data).token, str) else "",
                    "Companycode": Dict(self.token_data).companyCode if isinstance(Dict(self.token_data).companyCode,
                                                                                   str) else "",
                    **requests_request_kwargs.headers,
                },
                "json": {
                    **requests_request_kwargs_json,
                    **requests_request_kwargs.json,
                },
                **requests_request_kwargs,
            }
        )
        return requests_request(
            requests_response_callable=requests_response_callable,
            requests_request_args=requests_request_args,
            requests_request_kwargs=requests_request_kwargs
        )

    def update_shop_product_status(
            self,
            requests_request_kwargs_data: dict = {},
            requests_response_callable: Callable = RequestsResponseCallable.status_code_200_json_addict_status_100_data,
            requests_request_args: Iterable = (),
            requests_request_kwargs: dict = {},
    ) -> bool:
        """
        更新门店商品上下架状态
        :param requests_request_kwargs_data:
        :param requests_response_callable: RequestsResponseCallable.status_code_200_json_addict_status_100_data
        :param requests_request_args: requests_request(requests_response_callable,requests_request_args,requests_request_kwargs)
        :param requests_request_kwargs: requests_request(requests_response_callable,requests_request_args,requests_request_kwargs)
        :return:
        """
        requests_request_kwargs_data = Dict(requests_request_kwargs_data)
        requests_request_kwargs = Dict(requests_request_kwargs)
        requests_request_kwargs = Dict(
            {
                "url": f"{self.base_url}/manage/storeProduct/updateStoreProductInfo",
                "method": "PUT",
                "headers": {
                    "Token": Dict(self.token_data).token if isinstance(Dict(self.token_data).token, str) else "",
                    "Companycode": Dict(self.token_data).companyCode if isinstance(Dict(self.token_data).companyCode,
                                                                                   str) else "",
                    **requests_request_kwargs.headers,
                },
                "data": {
                    **requests_request_kwargs_data,
                    **requests_request_kwargs.data,
                },
                **requests_request_kwargs,
            }
        )
        return requests_request(
            requests_response_callable=requests_response_callable,
            requests_request_args=requests_request_args,
            requests_request_kwargs=requests_request_kwargs
        )

    def update_store_goods_status(
            self,
            requests_request_kwargs_data: dict = {},
            requests_response_callable: Callable = RequestsResponseCallable.status_code_200_json_addict_status_100_data,
            requests_request_args: Iterable = (),
            requests_request_kwargs: dict = {},
    ) -> bool:
        """
        更新门店商品上下架状态
        :param requests_request_kwargs_data:
        :param requests_response_callable: RequestsResponseCallable.status_code_200_json_addict_status_100_data
        :param requests_request_args: requests_request(requests_response_callable,requests_request_args,requests_request_kwargs)
        :param requests_request_kwargs: requests_request(requests_response_callable,requests_request_args,requests_request_kwargs)
        :return:
        """
        requests_request_kwargs_data = Dict(requests_request_kwargs_data)
        requests_request_kwargs = Dict(requests_request_kwargs)
        requests_request_kwargs = Dict(
            {
                "url": f"{self.base_url}/manage/storeProduct/updateProductStatus",
                "method": "PUT",
                "headers": {
                    "Token": Dict(self.token_data).token if isinstance(Dict(self.token_data).token, str) else "",
                    "Companycode": Dict(self.token_data).companyCode if isinstance(Dict(self.token_data).companyCode,
                                                                                   str) else "",
                    **requests_request_kwargs.headers,
                },
                "data": {
                    **requests_request_kwargs_data,
                    **requests_request_kwargs.data,
                },
                **requests_request_kwargs,
            }
        )
        return requests_request(
            requests_response_callable=requests_response_callable,
            requests_request_args=requests_request_args,
            requests_request_kwargs=requests_request_kwargs
        )

    def query_parking_auth_audits(
            self,
            requests_request_kwargs_params: dict = {},
            requests_response_callable: Callable = RequestsResponseCallable.status_code_200_json_addict_status_100_data,
            requests_request_args: Iterable = (),
            requests_request_kwargs: dict = {},
    ):
        """
        分页查询停车授权审核列表
        :param requests_request_kwargs_params:
        :param requests_response_callable: RequestsResponseCallable.status_code_200_json_addict_status_100_data
        :param requests_request_args: requests_request(requests_response_callable,requests_request_args,requests_request_kwargs)
        :param requests_request_kwargs: requests_request(requests_response_callable,requests_request_args,requests_request_kwargs)
        :return:
        """
        requests_request_kwargs_params = Dict(requests_request_kwargs_params)
        requests_request_kwargs = Dict(requests_request_kwargs)
        requests_request_kwargs = Dict(
            {
                "url": f"{self.base_url}/manage/carParkApplication/carParkCard/parkingCardManagerByAudit",
                "method": "GET",
                "headers": {
                    "Token": Dict(self.token_data).token if isinstance(Dict(self.token_data).token, str) else "",
                    "Companycode": Dict(self.token_data).companyCode if isinstance(Dict(self.token_data).companyCode,
                                                                                   str) else "",
                    **requests_request_kwargs.headers,
                },
                "params": {
                    "pageSize": 20,
                    **requests_request_kwargs_params,
                    **requests_request_kwargs.params,
                },
                **requests_request_kwargs,
            }
        )
        return requests_request(
            requests_response_callable=requests_response_callable,
            requests_request_args=requests_request_args,
            requests_request_kwargs=requests_request_kwargs
        )

    def query_parking_auth_audit_checks(
            self,
            requests_request_kwargs_params: dict = {},
            requests_response_callable: Callable = RequestsResponseCallable.status_code_200_json_addict_status_100_data,
            requests_request_args: Iterable = (),
            requests_request_kwargs: dict = {},
    ):
        """
        查询停车授权审核进程列表
        :param requests_request_kwargs_params:
        :param requests_response_callable: RequestsResponseCallable.status_code_200_json_addict_status_100_data
        :param requests_request_args: requests_request(requests_response_callable,requests_request_args,requests_request_kwargs)
        :param requests_request_kwargs: requests_request(requests_response_callable,requests_request_args,requests_request_kwargs)
        :return:
        """
        requests_request_kwargs_params = Dict(requests_request_kwargs_params)
        requests_request_kwargs = Dict(requests_request_kwargs)
        requests_request_kwargs = Dict(
            {
                "url": f"{self.base_url}/manage/carParkApplication/getParkingCheckList",
                "method": "GET",
                "headers": {
                    "Token": Dict(self.token_data).token if isinstance(Dict(self.token_data).token, str) else "",
                    "Companycode": Dict(self.token_data).companyCode if isinstance(Dict(self.token_data).companyCode,
                                                                                   str) else "",
                    **requests_request_kwargs.headers,
                },
                "params": {
                    **requests_request_kwargs_params,
                    **requests_request_kwargs.params,
                },
                **requests_request_kwargs,
            }
        )
        return requests_request(
            requests_response_callable=requests_response_callable,
            requests_request_args=requests_request_args,
            requests_request_kwargs=requests_request_kwargs
        )

    def query_parking_auths(
            self,
            requests_request_kwargs_params: dict = {},
            requests_response_callable: Callable = RequestsResponseCallable.status_code_200_json_addict_status_100_data,
            requests_request_args: Iterable = (),
            requests_request_kwargs: dict = {},
    ):
        """
        分页查询停车授权列表
        :param requests_request_kwargs_params:
        :param requests_response_callable: RequestsResponseCallable.status_code_200_json_addict_status_100_data
        :param requests_request_args: requests_request(requests_response_callable,requests_request_args,requests_request_kwargs)
        :param requests_request_kwargs: requests_request(requests_response_callable,requests_request_args,requests_request_kwargs)
        :return:
        """
        requests_request_kwargs_params = Dict(requests_request_kwargs_params)
        requests_request_kwargs = Dict(requests_request_kwargs)
        requests_request_kwargs = Dict(
            {
                "url": f"{self.base_url}/manage/carParkApplication/carParkCard/list",
                "method": "GET",
                "headers": {
                    "Token": Dict(self.token_data).token if isinstance(Dict(self.token_data).token, str) else "",
                    "Companycode": Dict(self.token_data).companyCode if isinstance(Dict(self.token_data).companyCode,
                                                                                   str) else "",
                    **requests_request_kwargs.headers,
                },
                "params": {
                    "pageSize": 20,
                    **requests_request_kwargs_params,
                    **requests_request_kwargs.params,
                },
                **requests_request_kwargs,
            }
        )
        return requests_request(
            requests_response_callable=requests_response_callable,
            requests_request_args=requests_request_args,
            requests_request_kwargs=requests_request_kwargs
        )

    def query_parking_auth(
            self,
            id: Union[int, str] = 0,
            requests_response_callable: Callable = RequestsResponseCallable.status_code_200_json_addict_status_100_data,
            requests_request_args: Iterable = (),
            requests_request_kwargs: dict = {},
    ):
        """
        查询停车授权详情
        :param id: 停车授权id
        :param requests_response_callable: RequestsResponseCallable.status_code_200_json_addict_status_100_data
        :param requests_request_args: requests_request(requests_response_callable,requests_request_args,requests_request_kwargs)
        :param requests_request_kwargs: requests_request(requests_response_callable,requests_request_args,requests_request_kwargs)
        :return:
        """
        requests_request_kwargs = Dict(requests_request_kwargs)
        requests_request_kwargs = Dict(
            {
                "url": f"{self.base_url}/manage/carParkApplication/carParkCard",
                "method": "GET",
                "headers": {
                    "Token": Dict(self.token_data).token if isinstance(Dict(self.token_data).token, str) else "",
                    "Companycode": Dict(self.token_data).companyCode if isinstance(Dict(self.token_data).companyCode,
                                                                                   str) else "",
                    **requests_request_kwargs.headers,
                },
                "params": {
                    "id": id,
                    **requests_request_kwargs.params,
                },
                **requests_request_kwargs,
            }
        )
        return requests_request(
            requests_response_callable=requests_response_callable,
            requests_request_args=requests_request_args,
            requests_request_kwargs=requests_request_kwargs
        )

    def query_house(
            self,
            id: Union[int, str] = 0,
            requests_response_callable: Callable = RequestsResponseCallable.status_code_200_json_addict_status_100_data,
            requests_request_args: Iterable = (),
            requests_request_kwargs: dict = {},
    ):
        """
        查询房屋详情
        :param id: 房屋id
        :param requests_response_callable: RequestsResponseCallable.status_code_200_json_addict_status_100_data
        :param requests_request_args: requests_request(requests_response_callable,requests_request_args,requests_request_kwargs)
        :param requests_request_kwargs: requests_request(requests_response_callable,requests_request_args,requests_request_kwargs)
        :return:
        """
        requests_request_kwargs = Dict(requests_request_kwargs)
        requests_request_kwargs = Dict(
            {
                "url": f"{self.base_url}/manage/communityRoom/getFullRoomInfo",
                "method": "GET",
                "headers": {
                    "Token": Dict(self.token_data).token if isinstance(Dict(self.token_data).token, str) else "",
                    "Companycode": Dict(self.token_data).companyCode if isinstance(Dict(self.token_data).companyCode,
                                                                                   str) else "",
                    **requests_request_kwargs.headers,
                },
                "params": {
                    "id": id,
                    **requests_request_kwargs.params,
                },
                **requests_request_kwargs,
            }
        )
        return requests_request(
            requests_response_callable=requests_response_callable,
            requests_request_args=requests_request_args,
            requests_request_kwargs=requests_request_kwargs
        )

    def query_business_orders(
            self,
            requests_request_kwargs_params: dict = {},
            requests_response_callable: Callable = RequestsResponseCallable.status_code_200_json_addict_status_100_data,
            requests_request_args: Iterable = (),
            requests_request_kwargs: dict = {},
    ):
        """
        分页查询商业订单列表
        :param requests_request_kwargs_params:
        :param requests_response_callable: RequestsResponseCallable.status_code_200_json_addict_status_100_data
        :param requests_request_args: requests_request(requests_response_callable,requests_request_args,requests_request_kwargs)
        :param requests_request_kwargs: requests_request(requests_response_callable,requests_request_args,requests_request_kwargs)
        :return:
        """
        requests_request_kwargs_params = Dict(requests_request_kwargs_params)
        requests_request_kwargs = Dict(requests_request_kwargs)
        requests_request_kwargs = Dict(
            {
                "url": f"{self.base_url}/manage/businessOrderShu/list",
                "method": "GET",
                "headers": {
                    "Token": Dict(self.token_data).token if isinstance(Dict(self.token_data).token, str) else "",
                    "Companycode": Dict(self.token_data).companyCode if isinstance(Dict(self.token_data).companyCode,
                                                                                   str) else "",
                    **requests_request_kwargs.headers,
                },
                "params": {
                    "pageSize": 20,
                    **requests_request_kwargs_params,
                    **requests_request_kwargs.params,
                },
                **requests_request_kwargs,
            }
        )
        return requests_request(
            requests_response_callable=requests_response_callable,
            requests_request_args=requests_request_args,
            requests_request_kwargs=requests_request_kwargs
        )

    def upload_file(
            self,
            requests_request_kwargs_params: dict = {},
            requests_request_kwargs_data: dict = {},
            requests_request_kwargs_files=None,
            requests_response_callable: Callable = RequestsResponseCallable.status_code_200_json_addict_status_100_data,
            requests_request_args: Iterable = (),
            requests_request_kwargs: dict = {}
    ):
        """
        上传文件
        :param requests_request_kwargs_params:
        :param requests_request_kwargs_data:
        :param requests_request_kwargs_files:
        :param requests_response_callable: RequestsResponseCallable.status_code_200_json_addict_status_100_data
        :param requests_request_args: requests_request(requests_response_callable,requests_request_args,requests_request_kwargs)
        :param requests_request_kwargs: requests_request(requests_response_callable,requests_request_args,requests_request_kwargs)
        :return:
        """
        requests_request_kwargs_params = Dict(requests_request_kwargs_params)
        requests_request_kwargs_data = Dict(requests_request_kwargs_data)
        requests_request_kwargs = Dict(requests_request_kwargs)
        requests_request_kwargs = Dict(
            {
                "url": f"{self.base_url}/upload",
                "method": "POST",
                "headers": {
                    "Token": Dict(self.token_data).token if isinstance(Dict(self.token_data).token, str) else "",
                    "Companycode": Dict(self.token_data).companyCode if isinstance(Dict(self.token_data).companyCode,
                                                                                   str) else "",
                    **requests_request_kwargs.headers,
                },
                "params": {
                    **requests_request_kwargs_params,
                    **requests_request_kwargs.params,
                },
                "data": {
                    **requests_request_kwargs_data,
                    **requests_request_kwargs.data,
                },
                "files": requests_request_kwargs_files,
                **requests_request_kwargs,
            }
        )
        return requests_request(
            requests_response_callable=requests_response_callable,
            requests_request_args=requests_request_args,
            requests_request_kwargs=requests_request_kwargs
        )

    def query_registered_owners(
            self,
            requests_request_kwargs_params: dict = {},
            requests_response_callable: Callable = RequestsResponseCallable.status_code_200_json_addict_status_100_data,
            requests_request_args: Iterable = (),
            requests_request_kwargs: dict = {},
    ):
        """
        分页查询注册业主列表
        :param requests_request_kwargs_params:
        :param requests_response_callable: RequestsResponseCallable.status_code_200_json_addict_status_100_data
        :param requests_request_args: requests_request(requests_response_callable,requests_request_args,requests_request_kwargs)
        :param requests_request_kwargs: requests_request(requests_response_callable,requests_request_args,requests_request_kwargs)
        :return:
        """
        requests_request_kwargs_params = Dict(requests_request_kwargs_params)
        requests_request_kwargs = Dict(requests_request_kwargs)
        requests_request_kwargs = Dict(
            {
                "url": f"{self.base_url}/manage/user/information/register/list",
                "method": "GET",
                "headers": {
                    "Token": Dict(self.token_data).token if isinstance(Dict(self.token_data).token, str) else "",
                    "Companycode": Dict(self.token_data).companyCode if isinstance(Dict(self.token_data).companyCode,
                                                                                   str) else "",
                    **requests_request_kwargs.headers,
                },
                "params": {
                    "pageSize": 20,
                    **requests_request_kwargs_params,
                    **requests_request_kwargs.params,
                },
                **requests_request_kwargs,
            }
        )
        return requests_request(
            requests_response_callable=requests_response_callable,
            requests_request_args=requests_request_args,
            requests_request_kwargs=requests_request_kwargs
        )

    def query_unregistered_owners(
            self,
            requests_request_kwargs_params: dict = {},
            requests_response_callable: Callable = RequestsResponseCallable.status_code_200_json_addict_status_100_data,
            requests_request_args: Iterable = (),
            requests_request_kwargs: dict = {},
    ):
        """
        分页查询未注册业主列表
        :param requests_request_kwargs_params:
        :param requests_response_callable: RequestsResponseCallable.status_code_200_json_addict_status_100_data
        :param requests_request_args: requests_request(requests_response_callable,requests_request_args,requests_request_kwargs)
        :param requests_request_kwargs: requests_request(requests_response_callable,requests_request_args,requests_request_kwargs)
        :return:
        """
        requests_request_kwargs_params = Dict(requests_request_kwargs_params)
        requests_request_kwargs = Dict(requests_request_kwargs)
        requests_request_kwargs = Dict(
            {
                "url": f"{self.base_url}/manage/user/information/unregister/list",
                "method": "GET",
                "headers": {
                    "Token": Dict(self.token_data).token if isinstance(Dict(self.token_data).token, str) else "",
                    "Companycode": Dict(self.token_data).companyCode if isinstance(Dict(self.token_data).companyCode,
                                                                                   str) else "",
                    **requests_request_kwargs.headers,
                },
                "params": {
                    "pageSize": 20,
                    **requests_request_kwargs_params,
                    **requests_request_kwargs.params,
                },
                **requests_request_kwargs,
            }
        )
        return requests_request(
            requests_response_callable=requests_response_callable,
            requests_request_args=requests_request_args,
            requests_request_kwargs=requests_request_kwargs
        )

    def query_service_orders(
            self,
            requests_request_kwargs_params: dict = {},
            requests_response_callable: Callable = RequestsResponseCallable.status_code_200_json_addict_status_100_data,
            requests_request_args: Iterable = (),
            requests_request_kwargs: dict = {},
    ):
        """
        分页查询服务工单列表
        :param requests_request_kwargs_params:
        :param requests_response_callable: RequestsResponseCallable.status_code_200_json_addict_status_100_data
        :param requests_request_args: requests_request(requests_response_callable,requests_request_args,requests_request_kwargs)
        :param requests_request_kwargs: requests_request(requests_response_callable,requests_request_args,requests_request_kwargs)
        :return:
        """
        requests_request_kwargs_params = Dict(requests_request_kwargs_params)
        requests_request_kwargs = Dict(requests_request_kwargs)
        requests_request_kwargs = Dict(
            {
                "url": f"{self.base_url}/old/orderAction!viewList.action",
                "method": "GET",
                "headers": {
                    "Token": Dict(self.token_data).token if isinstance(Dict(self.token_data).token, str) else "",
                    "Companycode": Dict(self.token_data).companyCode if isinstance(Dict(self.token_data).companyCode,
                                                                                   str) else "",
                    **requests_request_kwargs.headers,
                },
                "params": {
                    "pageSize": 20,
                    **requests_request_kwargs_params,
                    **requests_request_kwargs.params,
                },
                **requests_request_kwargs,
            }
        )
        return requests_request(
            requests_response_callable=requests_response_callable,
            requests_request_args=requests_request_args,
            requests_request_kwargs=requests_request_kwargs
        )

    def query_exports(
            self,
            requests_request_kwargs_params: dict = {},
            requests_response_callable: Callable = RequestsResponseCallable.status_code_200_json_addict_status_100_data,
            requests_request_args: Iterable = (),
            requests_request_kwargs: dict = {},
    ):
        """
        分页查询数据导出列表
        :param requests_request_kwargs_params:
        :param requests_response_callable: RequestsResponseCallable.status_code_200_json_addict_status_100_data
        :param requests_request_args: requests_request(requests_response_callable,requests_request_args,requests_request_kwargs)
        :param requests_request_kwargs: requests_request(requests_response_callable,requests_request_args,requests_request_kwargs)
        :return:
        """
        requests_request_kwargs_params = Dict(requests_request_kwargs_params)
        requests_request_kwargs = Dict(requests_request_kwargs)
        requests_request_kwargs = Dict(
            {
                "url": f"{self.base_url}/manage/export/log",
                "method": "GET",
                "headers": {
                    "Token": Dict(self.token_data).token if isinstance(Dict(self.token_data).token, str) else "",
                    "Companycode": Dict(self.token_data).companyCode if isinstance(Dict(self.token_data).companyCode,
                                                                                   str) else "",
                    **requests_request_kwargs.headers,
                },
                "params": {
                    "pageSize": 20,
                    "userType": 102,
                    "myExport": 1,
                    **requests_request_kwargs_params,
                    **requests_request_kwargs.params,
                },
                **requests_request_kwargs,
            }
        )
        return requests_request(
            requests_response_callable=requests_response_callable,
            requests_request_args=requests_request_args,
            requests_request_kwargs=requests_request_kwargs
        )

    def business_orders_export(
            self,
            export_type: int = 1,
            requests_request_kwargs_params: dict = {},
            requests_response_callable: Callable = RequestsResponseCallable.status_code_200_json_addict_status_100_data,
            requests_request_args: Iterable = (),
            requests_request_kwargs: dict = {},
            retry_args: Iterable = (),
            retry_kwargs: dict = {},
    ):
        """
        商业订单数据导出
        :param export_type:
        :param requests_request_kwargs_params:
        :param requests_response_callable: RequestsResponseCallable.status_code_200_json_addict_status_100_data
        :param requests_request_args: requests_request(requests_response_callable,requests_request_args,requests_request_kwargs)
        :param requests_request_kwargs: requests_request(requests_response_callable,requests_request_args,requests_request_kwargs)
        :param retry_args:
        :param retry_kwargs:
        :return:
        """
        requests_request_kwargs_params = Dict(requests_request_kwargs_params)
        requests_request_kwargs = Dict(requests_request_kwargs)
        requests_request_kwargs = Dict(
            {
                "method": "GET",
                "headers": {
                    "Token": Dict(self.token_data).token if isinstance(Dict(self.token_data).token, str) else "",
                    "Companycode": Dict(self.token_data).companyCode if isinstance(Dict(self.token_data).companyCode,
                                                                                   str) else "",
                    **requests_request_kwargs.headers,
                },
                "params": {
                    **requests_request_kwargs_params,
                    **requests_request_kwargs.params,
                },
                **requests_request_kwargs
            }
        )
        if export_type == 1:
            requests_request_kwargs.url = f"{self.base_url}/manage/businessOrder/exportToExcelByOrder"
        if export_type == 2:
            requests_request_kwargs.url = f"{self.base_url}/manage/businessOrder/exportToExcelByProduct"
        if export_type == 3:
            requests_request_kwargs.url = f"{self.base_url}/manage/businessOrder/exportToExcelByOrderAndProduct"
        retry_kwargs = Dict(
            {
                "stop_max_attempt_number": timedelta(minutes=6).seconds,
                "wait_fixed": timedelta(seconds=10).seconds * 1000,
                **retry_kwargs,
            }
        )

        @retry(*retry_args, **retry_kwargs)
        def _retry_func(
                requests_response_callable: Callable = RequestsResponseCallable.status_code_200_json_addict_status_100_data,
                requests_request_args: Iterable = (),
                requests_request_kwargs: dict = {},
        ):
            print(
                f"{datetime.now()} exec business_orders_export({requests_response_callable},{requests_request_args},{requests_request_kwargs})")
            result = requests_request(
                requests_response_callable=requests_response_callable,
                requests_request_args=requests_request_args,
                requests_request_kwargs=requests_request_kwargs
            )
            if not isinstance(result, int):
                raise Exception(
                    f"{datetime.now()} exec business_orders_export({requests_response_callable},{requests_request_args},{requests_request_kwargs}) error")
            return result

        return _retry_func(
            requests_response_callable=requests_response_callable,
            requests_request_args=requests_request_args,
            requests_request_kwargs=requests_request_kwargs
        )

    def houses_export(
            self,
            requests_request_kwargs_params: dict = {},
            requests_response_callable: Callable = RequestsResponseCallable.status_code_200_json_addict_status_100_data,
            requests_request_args: Iterable = (),
            requests_request_kwargs: dict = {},
            retry_args: Iterable = (),
            retry_kwargs: dict = {},
    ):
        """
        有效房号数据导出
        :param requests_request_kwargs_params:
        :param requests_response_callable: RequestsResponseCallable.status_code_200_json_addict_status_100_data
        :param requests_request_args: requests_request(requests_response_callable,requests_request_args,requests_request_kwargs)
        :param requests_request_kwargs: requests_request(requests_response_callable,requests_request_args,requests_request_kwargs)
        :param retry_args:
        :param retry_kwargs:
        :return:
        """
        requests_request_kwargs_params = Dict(requests_request_kwargs_params)
        requests_request_kwargs = Dict(requests_request_kwargs)
        requests_request_kwargs = Dict(
            {
                "url": f"{self.base_url}/manage/communityRoom/exportDelayCommunityRoomList",
                "method": "GET",
                "headers": {
                    "Token": Dict(self.token_data).token if isinstance(Dict(self.token_data).token, str) else "",
                    "Companycode": Dict(self.token_data).companyCode if isinstance(Dict(self.token_data).companyCode,
                                                                                   str) else "",
                    **requests_request_kwargs.headers,
                },
                "params": {
                    **requests_request_kwargs_params,
                    **requests_request_kwargs.params,
                },
                **requests_request_kwargs
            }
        )
        retry_kwargs = Dict(
            {
                "stop_max_attempt_number": timedelta(minutes=6).seconds,
                "wait_fixed": timedelta(seconds=10).seconds * 1000,
                **retry_kwargs,
            }
        )

        @retry(*retry_args, **retry_kwargs)
        def _retry_func(
                requests_response_callable: Callable = RequestsResponseCallable.status_code_200_json_addict_status_100_data,
                requests_request_args: Iterable = (),
                requests_request_kwargs: dict = {},
        ):
            print(
                f"{datetime.now()} exec houses_export({requests_response_callable},{requests_request_args},{requests_request_kwargs})")
            result = requests_request(
                requests_response_callable=requests_response_callable,
                requests_request_args=requests_request_args,
                requests_request_kwargs=requests_request_kwargs
            )
            if not isinstance(result, int):
                raise Exception(
                    f"{datetime.now()} exec houses_export({requests_response_callable},{requests_request_args},{requests_request_kwargs}) error")
            return result

        return _retry_func(
            requests_response_callable=requests_response_callable,
            requests_request_args=requests_request_args,
            requests_request_kwargs=requests_request_kwargs
        )

    def registered_owners_export(
            self,
            requests_request_kwargs_params: dict = {},
            requests_response_callable: Callable = RequestsResponseCallable.status_code_200_json_addict_status_100_data,
            requests_request_args: Iterable = (),
            requests_request_kwargs: dict = {},
            retry_args: Iterable = (),
            retry_kwargs: dict = {},
    ):
        """
        注册业主数据导出
        :param requests_request_kwargs_params:
        :param requests_response_callable: RequestsResponseCallable.status_code_200_json_addict_status_100_data
        :param requests_request_args: requests_request(requests_response_callable,requests_request_args,requests_request_kwargs)
        :param requests_request_kwargs: requests_request(requests_response_callable,requests_request_args,requests_request_kwargs)
        :param retry_args:
        :param retry_kwargs:
        :return:
        """
        requests_request_kwargs_params = Dict(requests_request_kwargs_params)
        requests_request_kwargs = Dict(requests_request_kwargs)
        requests_request_kwargs = Dict(
            {
                "url": f"{self.base_url}/manage/user/information/register/list/export",
                "method": "GET",
                "headers": {
                    "Token": Dict(self.token_data).token if isinstance(Dict(self.token_data).token, str) else "",
                    "Companycode": Dict(self.token_data).companyCode if isinstance(Dict(self.token_data).companyCode,
                                                                                   str) else "",
                    **requests_request_kwargs.headers,
                },
                "params": {
                    **requests_request_kwargs_params,
                    **requests_request_kwargs.params,
                },
                **requests_request_kwargs
            }
        )
        retry_kwargs = Dict(
            {
                "stop_max_attempt_number": timedelta(minutes=6).seconds,
                "wait_fixed": timedelta(seconds=10).seconds * 1000,
                **retry_kwargs,
            }
        )

        @retry(*retry_args, **retry_kwargs)
        def _retry_func(
                requests_response_callable: Callable = RequestsResponseCallable.status_code_200_json_addict_status_100_data,
                requests_request_args: Iterable = (),
                requests_request_kwargs: dict = {},
        ):
            print(
                f"{datetime.now()} exec registered_owners_export({requests_response_callable},{requests_request_args},{requests_request_kwargs})")
            result = requests_request(
                requests_response_callable=requests_response_callable,
                requests_request_args=requests_request_args,
                requests_request_kwargs=requests_request_kwargs
            )
            if not isinstance(result, int):
                raise Exception(
                    f"{datetime.now()} exec registered_owners_export({requests_response_callable},{requests_request_args},{requests_request_kwargs}) error")
            return result

        return _retry_func(
            requests_response_callable=requests_response_callable,
            requests_request_args=requests_request_args,
            requests_request_kwargs=requests_request_kwargs
        )

    def unregistered_owners_export(
            self,
            requests_request_kwargs_params: dict = {},
            requests_response_callable: Callable = RequestsResponseCallable.status_code_200_json_addict_status_100_data,
            requests_request_args: Iterable = (),
            requests_request_kwargs: dict = {},
            retry_args: Iterable = (),
            retry_kwargs: dict = {},
    ):
        """
        未注册业主信息数据导出
        :param requests_request_kwargs_params:
        :param requests_response_callable: RequestsResponseCallable.status_code_200_json_addict_status_100_data
        :param requests_request_args: requests_request(requests_response_callable,requests_request_args,requests_request_kwargs)
        :param requests_request_kwargs: requests_request(requests_response_callable,requests_request_args,requests_request_kwargs)
        :param retry_args:
        :param retry_kwargs:
        :return:
        """
        requests_request_kwargs_params = Dict(requests_request_kwargs_params)
        requests_request_kwargs = Dict(requests_request_kwargs)
        requests_request_kwargs = Dict(
            {
                "url": f"{self.base_url}/manage/user/information/unregister/list/export",
                "method": "GET",
                "headers": {
                    "Token": Dict(self.token_data).token if isinstance(Dict(self.token_data).token, str) else "",
                    "Companycode": Dict(self.token_data).companyCode if isinstance(Dict(self.token_data).companyCode,
                                                                                   str) else "",
                    **requests_request_kwargs.headers,
                },
                "params": {
                    **requests_request_kwargs_params,
                    **requests_request_kwargs.params,
                },
                **requests_request_kwargs
            }
        )
        retry_kwargs = Dict(
            {
                "stop_max_attempt_number": timedelta(minutes=6).seconds,
                "wait_fixed": timedelta(seconds=10).seconds * 1000,
                **retry_kwargs,
            }
        )

        @retry(*retry_args, **retry_kwargs)
        def _retry_func(
                requests_response_callable: Callable = RequestsResponseCallable.status_code_200_json_addict_status_100_data,
                requests_request_args: Iterable = (),
                requests_request_kwargs: dict = {},
        ):
            print(
                f"{datetime.now()} exec unregistered_owners_export({requests_response_callable},{requests_request_args},{requests_request_kwargs})")
            result = requests_request(
                requests_response_callable=requests_response_callable,
                requests_request_args=requests_request_args,
                requests_request_kwargs=requests_request_kwargs
            )
            if not isinstance(result, int):
                raise Exception(
                    f"{datetime.now()} exec unregistered_owners_export({requests_response_callable},{requests_request_args},{requests_request_kwargs}) error")
            return result

        return _retry_func(
            requests_response_callable=requests_response_callable,
            requests_request_args=requests_request_args,
            requests_request_kwargs=requests_request_kwargs
        )

    def service_orders_export(
            self,
            requests_request_kwargs_params: dict = {},
            requests_response_callable: Callable = RequestsResponseCallable.status_code_200_json_addict_status_100_data,
            requests_request_args: Iterable = (),
            requests_request_kwargs: dict = {},
            retry_args: Iterable = (),
            retry_kwargs: dict = {},
    ):
        """
        服务工单数据导出
        :param requests_request_kwargs_params:
        :param requests_response_callable: RequestsResponseCallable.status_code_200_json_addict_status_100_data
        :param requests_request_args: requests_request(requests_response_callable,requests_request_args,requests_request_kwargs)
        :param requests_request_kwargs: requests_request(requests_response_callable,requests_request_args,requests_request_kwargs)
        :param retry_args:
        :param retry_kwargs:
        :return:
        """
        requests_request_kwargs_params = Dict(requests_request_kwargs_params)
        requests_request_kwargs = Dict(requests_request_kwargs)
        requests_request_kwargs = Dict(
            {
                "url": f"{self.base_url}/manage/order/work/export",
                "method": "GET",
                "headers": {
                    "Token": Dict(self.token_data).token if isinstance(Dict(self.token_data).token, str) else "",
                    "Companycode": Dict(self.token_data).companyCode if isinstance(Dict(self.token_data).companyCode,
                                                                                   str) else "",
                    **requests_request_kwargs.headers,
                },
                "params": {
                    **requests_request_kwargs_params,
                    **requests_request_kwargs.params,
                },
                **requests_request_kwargs
            }
        )
        retry_kwargs = Dict(
            {
                "stop_max_attempt_number": timedelta(minutes=6).seconds,
                "wait_fixed": timedelta(seconds=10).seconds * 1000,
                **retry_kwargs,
            }
        )

        @retry(*retry_args, **retry_kwargs)
        def _retry_func(
                requests_response_callable: Callable = RequestsResponseCallable.status_code_200_json_addict_status_100_data,
                requests_request_args: Iterable = (),
                requests_request_kwargs: dict = {},
        ):
            print(
                f"{datetime.now()} exec service_orders_export({requests_response_callable},{requests_request_args},{requests_request_kwargs})")
            result = requests_request(
                requests_response_callable=requests_response_callable,
                requests_request_args=requests_request_args,
                requests_request_kwargs=requests_request_kwargs
            )
            if not isinstance(result, int):
                raise Exception(
                    f"{datetime.now()} exec service_orders_export({requests_response_callable},{requests_request_args},{requests_request_kwargs}) error")
            return result

        return _retry_func(
            requests_response_callable=requests_response_callable,
            requests_request_args=requests_request_args,
            requests_request_kwargs=requests_request_kwargs
        )

    def shop_products_export(
            self,
            requests_request_kwargs_params: dict = {},
            requests_response_callable: Callable = RequestsResponseCallable.status_code_200_json_addict_status_100_data,
            requests_request_args: Iterable = (),
            requests_request_kwargs: dict = {},
            retry_args: Iterable = (),
            retry_kwargs: dict = {},
    ):
        """
        商家产品数据导出
        :param requests_request_kwargs_params:
        :param requests_response_callable: RequestsResponseCallable.status_code_200_json_addict_status_100_data
        :param requests_request_args: requests_request(requests_response_callable,requests_request_args,requests_request_kwargs)
        :param requests_request_kwargs: requests_request(requests_response_callable,requests_request_args,requests_request_kwargs)
        :param retry_args:
        :param retry_kwargs:
        :return:
        """
        requests_request_kwargs_params = Dict(requests_request_kwargs_params)
        requests_request_kwargs = Dict(requests_request_kwargs)
        requests_request_kwargs = Dict(
            {
                "url": f"{self.base_url}/manage/goods/exportShopGoods",
                "method": "GET",
                "headers": {
                    "Token": Dict(self.token_data).token if isinstance(Dict(self.token_data).token, str) else "",
                    "Companycode": Dict(self.token_data).companyCode if isinstance(Dict(self.token_data).companyCode,
                                                                                   str) else "",
                    **requests_request_kwargs.headers,
                },
                "params": {
                    **requests_request_kwargs_params,
                    **requests_request_kwargs.params,
                },
                **requests_request_kwargs
            }
        )
        retry_kwargs = Dict(
            {
                "stop_max_attempt_number": timedelta(minutes=6).seconds,
                "wait_fixed": timedelta(seconds=10).seconds * 1000,
                **retry_kwargs,
            }
        )

        @retry(*retry_args, **retry_kwargs)
        def _retry_func(
                requests_response_callable: Callable = RequestsResponseCallable.status_code_200_json_addict_status_100_data,
                requests_request_args: Iterable = (),
                requests_request_kwargs: dict = {},
        ):
            print(
                f"{datetime.now()} exec shop_products_export({requests_response_callable},{requests_request_args},{requests_request_kwargs})")
            result = requests_request(
                requests_response_callable=requests_response_callable,
                requests_request_args=requests_request_args,
                requests_request_kwargs=requests_request_kwargs
            )
            if not isinstance(result, int):
                raise Exception(
                    f"{datetime.now()} exec shop_products_export({requests_response_callable}{requests_request_args},{requests_request_kwargs}) error")
            return result

        return _retry_func(
            requests_response_callable=requests_response_callable,
            requests_request_args=requests_request_args,
            requests_request_kwargs=requests_request_kwargs
        )

    def store_goodses_export(
            self,
            requests_request_kwargs_params: dict = {},
            requests_response_callable: Callable = RequestsResponseCallable.status_code_200_json_addict_status_100_data,
            requests_request_args: Iterable = (),
            requests_request_kwargs: dict = {},
            retry_args: Iterable = (),
            retry_kwargs: dict = {},
    ):
        """
        门店商品数据导出
        :param requests_request_kwargs_params:
        :param requests_response_callable: RequestsResponseCallable.status_code_200_json_addict_status_100_data
        :param requests_request_args: requests_request(requests_response_callable,requests_request_args,requests_request_kwargs)
        :param requests_request_kwargs: requests_request(requests_response_callable,requests_request_args,requests_request_kwargs)
        :param retry_args:
        :param retry_kwargs:
        :return:
        """
        requests_request_kwargs_params = Dict(requests_request_kwargs_params)
        requests_request_kwargs = Dict(requests_request_kwargs)
        requests_request_kwargs = Dict(
            {
                "url": f"{self.base_url}/manage/storeProduct/exportStoreProductList",
                "method": "GET",
                "headers": {
                    "Token": Dict(self.token_data).token if isinstance(Dict(self.token_data).token, str) else "",
                    "Companycode": Dict(self.token_data).companyCode if isinstance(Dict(self.token_data).companyCode,
                                                                                   str) else "",
                    **requests_request_kwargs.headers,
                },
                "params": {
                    **requests_request_kwargs_params,
                    **requests_request_kwargs.params,
                },
                **requests_request_kwargs
            }
        )
        retry_kwargs = Dict(
            {
                "stop_max_attempt_number": timedelta(minutes=6).seconds,
                "wait_fixed": timedelta(seconds=10).seconds * 1000,
                **retry_kwargs,
            }
        )

        @retry(*retry_args, **retry_kwargs)
        def _retry_func(
                requests_response_callable: Callable = RequestsResponseCallable.status_code_200_json_addict_status_100_data,
                requests_request_args: Iterable = (),
                requests_request_kwargs: dict = {},
        ):
            print(
                f"{datetime.now()} exec store_goodses_export({requests_response_callable},{requests_request_args},{requests_request_kwargs})")
            result = requests_request(
                requests_response_callable=requests_response_callable,
                requests_request_args=requests_request_args,
                requests_request_kwargs=requests_request_kwargs
            )
            if not isinstance(result, int):
                raise Exception(
                    f"{datetime.now()} exec store_goodses_export({requests_response_callable},{requests_request_args},{requests_request_kwargs}) error")
            return result

        return _retry_func(
            requests_response_callable=requests_response_callable,
            requests_request_args=requests_request_args,
            requests_request_kwargs=requests_request_kwargs
        )

    def download_export(
            self,
            export_id: int = 0,
            export_fp: str = "",
            requests_response_callable: Callable = RequestsResponseCallable.status_code_200_json_addict_status_100_data_result_list,
            requests_request_args: Iterable = (),
            requests_request_kwargs: dict = {},
            retry_args: Iterable = (),
            retry_kwargs: dict = {},
    ):
        """
        下载数据导出文件
        :param export_id:
        :param export_fp:
        :param requests_response_callable: RequestsResponseCallable.status_code_200_json_addict_status_100_data_result_list
        :param requests_request_args: requests_request(requests_response_callable,requests_request_args,requests_request_kwargs)
        :param requests_request_kwargs: requests_request(requests_response_callable,requests_request_args,requests_request_kwargs)
        :param retry_args:
        :param retry_kwargs:
        :return:
        """
        requests_request_kwargs = Dict(requests_request_kwargs)
        retry_kwargs = Dict(
            {
                "stop_max_attempt_number": timedelta(minutes=60).seconds,
                "wait_fixed": timedelta(seconds=10).seconds * 1000,
                **retry_kwargs,
            }
        )

        @retry(*retry_args, **retry_kwargs)
        def _retry_func(
                export_fp=export_fp,
                requests_response_callable: Callable = RequestsResponseCallable.status_code_200_json_addict_status_100_data_result_list,
                requests_request_args: Iterable = (),
                requests_request_kwargs: dict = {}
        ):
            # print(
            #     f"{datetime.now()} exec download_export({export_id},{export_fp},{requests_response_callable},{requests_request_args},{requests_request_kwargs})")
            exports = self.login_with_cache().query_exports(
                requests_response_callable=requests_response_callable,
                requests_request_args=requests_request_args,
                requests_request_kwargs=requests_request_kwargs
            )
            export = Dict({})
            if isinstance(exports, list):
                for i in exports:
                    if isinstance(i.id, int) and i.id == export_id:
                        print(datetime.now(), i)
                        if isinstance(i.status, int) and i.status == 2:
                            export = i
                            break
                    continue
                if isinstance(export.filePath, str) and len(export.filePath):
                    if "".join(pathlib.Path(export.filePath).suffixes).lower() not in "".join(
                            pathlib.Path(export_fp).suffixes).lower():
                        export_fp = f"{export_fp}{''.join(pathlib.Path(export.filePath).suffixes)}"
                    response = requests.get(export.filePath)
                    with open(export_fp, "wb") as f:
                        f.write(response.content)
                    return export_fp
            raise Exception(
                f"{datetime.now()} retry exec download_export({export_id},{export_fp},{requests_response_callable},{requests_request_args},{requests_request_kwargs}) {export}")

        return _retry_func(
            export_fp=export_fp,
            requests_response_callable=requests_response_callable,
            requests_request_args=requests_request_args,
            requests_request_kwargs=requests_request_kwargs
        )

    def query_devices(
            self,
            requests_request_kwargs_params: dict = {},
            requests_response_callable: Callable = RequestsResponseCallable.status_code_200_json_addict_status_100_data,
            requests_request_args: Iterable = (),
            requests_request_kwargs: dict = {},
    ):
        """
        分页查询设备列表
        :param requests_request_kwargs_params: requests.request.params
        :param requests_response_callable: requests_response_with_code_200_json_addict_status_100_data
        :param requests_request_args: requests_request(requests_response_callable,requests_request_args,requests_request_kwargs)
        :param requests_request_kwargs: requests_request(requests_response_callable,requests_request_args,requests_request_kwargs)
        :return:
        """
        requests_request_kwargs_params = Dict(requests_request_kwargs_params)
        requests_request_kwargs = Dict(requests_request_kwargs)
        requests_request_kwargs = Dict(
            {
                "url": f"{self.base_url}/manage/device/DeviceList",
                "method": "GET",
                "headers": {
                    "Token": Dict(self.token_data).token if isinstance(Dict(self.token_data).token, str) else "",
                    "Companycode": Dict(self.token_data).companyCode if isinstance(Dict(self.token_data).companyCode,
                                                                                   str) else "",
                    **requests_request_kwargs.headers,
                },
                "params": {
                    "pageSize": 20,
                    **requests_request_kwargs_params,
                    **requests_request_kwargs.params,
                },
                **requests_request_kwargs,
            }
        )
        return requests_request(
            requests_response_callable=requests_response_callable,
            requests_request_args=requests_request_args,
            requests_request_kwargs=requests_request_kwargs
        )

    def query_device_patrol(
            self,
            id: str = "",
            requests_response_callable: Callable = RequestsResponseCallable.status_code_200_json_addict_status_100_data,
            requests_request_args: Iterable = (),
            requests_request_kwargs: dict = {},
    ):
        """
        查询设备巡检信息
        :param id: 设备id
        :param requests_response_callable: RequestsResponseCallable.status_code_200_json_addict_status_100_data
        :param requests_request_args: requests_request(requests_response_callable,requests_request_args,requests_request_kwargs)
        :param requests_request_kwargs: requests_request(requests_response_callable,requests_request_args,requests_request_kwargs)
        :return:
        """
        requests_request_kwargs = Dict(requests_request_kwargs)
        requests_request_kwargs = Dict(
            {
                "url": f"{self.base_url}/manage/devicePatrol/detail",
                "method": "GET",
                "headers": {
                    "Token": Dict(self.token_data).token if isinstance(Dict(self.token_data).token, str) else "",
                    "Companycode": Dict(self.token_data).companyCode if isinstance(Dict(self.token_data).companyCode,
                                                                                   str) else "",
                    **requests_request_kwargs.headers,
                },
                "params": {
                    "id": id,
                    **requests_request_kwargs.params,
                },
                **requests_request_kwargs,
            }
        )
        return requests_request(
            requests_response_callable=requests_response_callable,
            requests_request_args=requests_request_args,
            requests_request_kwargs=requests_request_kwargs
        )

    def query_enterprise_users(
            self,
            requests_request_kwargs_params: dict = {},
            requests_response_callable: Callable = RequestsResponseCallable.status_code_200_json_addict_status_100_data,
            requests_request_args: Iterable = (),
            requests_request_kwargs: dict = {},
    ):
        """
        分页查询企业用户列表
        :param requests_request_kwargs_params: requests.request.params
        :param requests_response_callable: RequestsResponseCallable.status_code_200_json_addict_status_100_data
        :param requests_request_args: requests_request(requests_response_callable,requests_request_args,requests_request_kwargs)
        :param requests_request_kwargs: requests_request(requests_response_callable,requests_request_args,requests_request_kwargs)
        :return:
        """
        requests_request_kwargs_params = Dict(requests_request_kwargs_params)
        requests_request_kwargs = Dict(requests_request_kwargs)
        requests_request_kwargs = Dict(
            {
                "url": f"{self.base_url}/manage/newEnterpriseUserInfo/selectEnterpriseUserInfoList",
                "method": "GET",
                "headers": {
                    "Token": Dict(self.token_data).token if isinstance(Dict(self.token_data).token, str) else "",
                    "Companycode": Dict(self.token_data).companyCode if isinstance(Dict(self.token_data).companyCode,
                                                                                   str) else "",
                    **requests_request_kwargs.headers,
                },
                "params": {
                    "pageSize": 20,
                    **requests_request_kwargs_params,
                    **requests_request_kwargs.params,
                },
                **requests_request_kwargs,
            }
        )
        return requests_request(
            requests_response_callable=requests_response_callable,
            requests_request_args=requests_request_args,
            requests_request_kwargs=requests_request_kwargs
        )

    def update_device_patrol_info(
            self,
            requests_request_kwargs_json: dict = {},
            requests_response_callable: Callable = RequestsResponseCallable.status_code_200_json_addict_status_100_data,
            requests_request_args: Iterable = (),
            requests_request_kwargs: dict = {},
    ):
        """
        更新设备巡检信息
        :param requests_request_kwargs_json:
        :param requests_response_callable: RequestsResponseCallable.status_code_200_json_addict_status_100_data
        :param requests_request_args: requests_request(requests_response_callable,requests_request_args,requests_request_kwargs)
        :param requests_request_kwargs: requests_request(requests_response_callable,requests_request_args,requests_request_kwargs)
        :return:
        """
        requests_request_kwargs_json = Dict(requests_request_kwargs_json)
        requests_request_kwargs = Dict(requests_request_kwargs)
        requests_request_kwargs = Dict(
            {
                "url": f"{self.base_url}/manage/devicePatrol/patrol/save",
                "method": "POST",
                "headers": {
                    "Token": Dict(self.token_data).token if isinstance(Dict(self.token_data).token, str) else "",
                    "Companycode": Dict(self.token_data).companyCode if isinstance(Dict(self.token_data).companyCode,
                                                                                   str) else "",
                    **requests_request_kwargs.headers,
                },
                "json": {
                    **requests_request_kwargs_json,
                    **requests_request_kwargs.json,
                },
                **requests_request_kwargs,
            }
        )
        return requests_request(
            requests_response_callable=requests_response_callable,
            requests_request_args=requests_request_args,
            requests_request_kwargs=requests_request_kwargs
        )

    def update_parking_auth_audit_status(
            self,
            requests_request_kwargs_json: dict = {},
            requests_response_callable: Callable = RequestsResponseCallable.status_code_200_json_addict_status_100_data,
            requests_request_args: Iterable = (),
            requests_request_kwargs: dict = {},
    ) -> bool:
        """
        更新停车授权审核状态
        :param requests_request_kwargs_json:
        :param requests_response_callable: RequestsResponseCallable.status_code_200_json_addict_status_100_data
        :param requests_request_args: requests_request(requests_response_callable,requests_request_args,requests_request_kwargs)
        :param requests_request_kwargs: requests_request(requests_response_callable,requests_request_args,requests_request_kwargs)
        :return:
        """
        requests_request_kwargs_json = Dict(requests_request_kwargs_json)
        requests_request_kwargs = Dict(requests_request_kwargs)
        requests_request_kwargs = Dict(
            {
                "url": f"{self.base_url}/manage/carParkApplication/completeTask",
                "method": "POST",
                "headers": {
                    "Token": Dict(self.token_data).token if isinstance(Dict(self.token_data).token, str) else "",
                    "Companycode": Dict(self.token_data).companyCode if isinstance(Dict(self.token_data).companyCode,
                                                                                   str) else "",
                    **requests_request_kwargs.headers,
                },
                "json": {
                    **requests_request_kwargs_json,
                    **requests_request_kwargs.json,
                },
                **requests_request_kwargs,
            }
        )
        return requests_request(
            requests_response_callable=requests_response_callable,
            requests_request_args=requests_request_args,
            requests_request_kwargs=requests_request_kwargs
        )

    def update_parking_auth(
            self,
            requests_request_kwargs_json: dict = {},
            requests_response_callable: Callable = RequestsResponseCallable.status_code_200_json_addict_status_100_data,
            requests_request_args: Iterable = (),
            requests_request_kwargs: dict = {},
    ):
        """
        更新停车授权
        :param requests_request_kwargs_json:
        :param requests_response_callable: RequestsResponseCallable.status_code_200_json_addict_status_100_data
        :param requests_request_args: requests_request(requests_response_callable,requests_request_args,requests_request_kwargs)
        :param requests_request_kwargs: requests_request(requests_response_callable,requests_request_args,requests_request_kwargs)
        :return:
        """
        requests_request_kwargs_json = Dict(requests_request_kwargs_json)
        requests_request_kwargs = Dict(requests_request_kwargs)
        requests_request_kwargs = Dict(
            {
                "url": f"{self.base_url}/manage/carParkApplication/carParkCard",
                "method": "PUT",
                "headers": {
                    "Token": Dict(self.token_data).token if isinstance(Dict(self.token_data).token, str) else "",
                    "Companycode": Dict(self.token_data).companyCode if isinstance(Dict(self.token_data).companyCode,
                                                                                   str) else "",
                    **requests_request_kwargs.headers,
                },
                "json": {
                    **requests_request_kwargs_json,
                    **requests_request_kwargs.json,
                },
                **requests_request_kwargs,
            }
        )
        return requests_request(
            requests_response_callable=requests_response_callable,
            requests_request_args=requests_request_args,
            requests_request_kwargs=requests_request_kwargs
        )

    def query_shop_product_categories(
            self,
            shop_id: str = "",
            requests_response_callable: Callable = RequestsResponseCallable.status_code_200_json_addict_status_100_data,
            requests_request_args: Iterable = (),
            requests_request_kwargs: dict = {},
    ):
        """
        查询商家自定义分类
        :param shop_id:
        :param requests_response_callable: RequestsResponseCallable.status_code_200_json_addict_status_100_data
        :param requests_request_args: requests_request(requests_response_callable,requests_request_args,requests_request_kwargs)
        :param requests_request_kwargs: requests_request(requests_response_callable,requests_request_args,requests_request_kwargs)
        :return:
        """
        requests_request_kwargs = Dict(requests_request_kwargs)
        requests_request_kwargs = Dict(
            {
                "url": f"{self.base_url}/manage/productCategory/getProductCategoryList",
                "method": "GET",
                "headers": {
                    "Token": Dict(self.token_data).token if isinstance(Dict(self.token_data).token, str) else "",
                    "Companycode": Dict(self.token_data).companyCode if isinstance(Dict(self.token_data).companyCode,
                                                                                   str) else "",
                    **requests_request_kwargs.headers,
                },
                "params": {
                    "busId": shop_id,
                    **requests_request_kwargs.params,
                },
                **requests_request_kwargs,
            }
        )
        return requests_request(
            requests_response_callable=requests_response_callable,
            requests_request_args=requests_request_args,
            requests_request_kwargs=requests_request_kwargs
        )


    def query_surveys(
            self,
            requests_request_kwargs_params: dict = {},
            requests_response_callable: Callable = RequestsResponseCallable.status_code_200_json_addict_status_100_data,
            requests_request_args: Iterable = (),
            requests_request_kwargs: dict = {},
    ):
        """
        分页查询调查问卷列表
        :param requests_request_kwargs_params: requests.request.params
        :param requests_response_callable: RequestsResponseCallable.status_code_200_json_addict_status_100_data
        :param requests_request_args: requests_request(requests_response_callable,requests_request_args,requests_request_kwargs)
        :param requests_request_kwargs: requests_request(requests_response_callable,requests_request_args,requests_request_kwargs)
        :return:
        """
        requests_request_kwargs_params = Dict(requests_request_kwargs_params)
        requests_request_kwargs = Dict(requests_request_kwargs)
        requests_request_kwargs = Dict(
            {
                "url": f"{self.base_url}/manage/questionnaire/list/managent",
                "method": "GET",
                "headers": {
                    "Token": Dict(self.token_data).token if isinstance(Dict(self.token_data).token, str) else "",
                    "Companycode": Dict(self.token_data).companyCode if isinstance(Dict(self.token_data).companyCode,
                                                                                   str) else "",
                    **requests_request_kwargs.headers,
                },
                "params": {
                    "pageSize": 20,
                    **requests_request_kwargs_params,
                    **requests_request_kwargs.params,
                },
                **requests_request_kwargs,
            }
        )
        return requests_request(
            requests_response_callable=requests_response_callable,
            requests_request_args=requests_request_args,
            requests_request_kwargs=requests_request_kwargs
        )

    def query_survey_participations(
            self,
            requests_request_kwargs_params: dict = {},
            requests_response_callable: Callable = RequestsResponseCallable.status_code_200_json_addict_status_100_data,
            requests_request_args: Iterable = (),
            requests_request_kwargs: dict = {},
    ):
        """
        分页查询调查问卷参与人列表
        :param requests_request_kwargs_params: requests.request.params
        :param requests_response_callable: RequestsResponseCallable.status_code_200_json_addict_status_100_data
        :param requests_request_args: requests_request(requests_response_callable,requests_request_args,requests_request_kwargs)
        :param requests_request_kwargs: requests_request(requests_response_callable,requests_request_args,requests_request_kwargs)
        :return:
        """
        requests_request_kwargs_params = Dict(requests_request_kwargs_params)
        requests_request_kwargs = Dict(requests_request_kwargs)
        requests_request_kwargs = Dict(
            {
                "url": f"{self.base_url}/manage/questionnaire/joinuser/list",
                "method": "GET",
                "headers": {
                    "Token": Dict(self.token_data).token if isinstance(Dict(self.token_data).token, str) else "",
                    "Companycode": Dict(self.token_data).companyCode if isinstance(Dict(self.token_data).companyCode,
                                                                                   str) else "",
                    **requests_request_kwargs.headers,
                },
                "params": {
                    "pageSize": 20,
                    **requests_request_kwargs_params,
                    **requests_request_kwargs.params,
                },
                **requests_request_kwargs,
            }
        )
        return requests_request(
            requests_response_callable=requests_response_callable,
            requests_request_args=requests_request_args,
            requests_request_kwargs=requests_request_kwargs
        )

