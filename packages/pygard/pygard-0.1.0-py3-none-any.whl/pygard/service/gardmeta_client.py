# !/usr/bin/env python
# -*- coding: UTF-8 -*-
#
# @Project ：data-service-sdk-python
# @Author ：qm
# @Date ：2025/5/9 9:45
# @Description:


import json
import requests
from pygard.config.gardmeta_config import GardMetaConfig
from pygard.model.response_models import ResponseWrapper, PageResponseWrapper
from pygard.model.entity_models import GardMeta, CsvDataInstance
from pygard.model.dto_models import DataInstanceMetaRequest
from pygard.model.enum_models import EnumFormat


class GardMetaClient(object):
    """
    GardMetaClient class for interacting with the GardMeta service.
    """

    def __init__(self, config: GardMetaConfig = None):
        """
        Initialize the GardMetaClient with the given configuration.
        """
        self.config = config
        self.base_url = f"{self.config.protocol}://{self.config.host}:{self.config.port}"

    def list_all(self) -> list[GardMeta]:
        url = f"{self.base_url}/api/v1/data-service/gard/meta"
        response = requests.request("GET", url)
        response.raise_for_status()
        response_wrapper = ResponseWrapper[list[GardMeta]](**response.json())
        return response_wrapper.data

    def query_by_id(self, did: int) -> GardMeta:
        url = f"{self.base_url}/api/v1/data-service/gard/meta/{did}"
        response = requests.request("GET", url)
        response.raise_for_status()
        response_wrapper = ResponseWrapper[GardMeta](**response.json())
        return response_wrapper.data

    def search_by_tags(self, tags: list[str]) -> list[GardMeta]:
        url = f"{self.base_url}/api/v1/data-service/gard/meta/search"
        payload = json.dumps(tags)
        headers = {
            'Content-Type': 'application/json'
        }
        response = requests.request("POST", url, data=payload, headers=headers)
        response.raise_for_status()
        response_wrapper = ResponseWrapper[list[GardMeta]](**response.json())
        return response_wrapper.data

    def search_by_keywords(self, keywords: str) -> list[GardMeta]:
        url = f"{self.base_url}/api/v1/data-service/gard/meta/search?keywords={keywords}"
        response = requests.request("GET", url)
        response.raise_for_status()
        response_wrapper = ResponseWrapper[list[GardMeta]](**response.json())
        return response_wrapper.data

    def get_data_instance_meta(self, data_mark: DataInstanceMetaRequest) -> CsvDataInstance:
        url = f"{self.base_url}/api/v1/data-service/instance/meta"
        payload = json.dumps(data_mark, default=lambda o: o.__dict__)
        headers = {
            'Content-Type': 'application/json'
        }
        response = requests.request("POST", url, headers=headers, data=payload)
        response.raise_for_status()
        response_wrapper = ResponseWrapper[list[CsvDataInstance]](**response.json())
        return response_wrapper.data[0]

    def fetch_data_by_id(self, did: int, format: EnumFormat, format_meta: CsvDataInstance, sql: str = None):
        import pandas as pd
        url = f"{self.base_url}/api/v1/data-service/instance/data"
        payload = json.dumps(
            {
                "did": did,
                "format": format,
                "formatMeta": format_meta,
                **({"sql": sql} if sql is not None else {})
            },
            default=lambda o: o.__dict__)
        headers = {
            'Content-Type': 'application/json'
        }
        response = requests.request("POST", url, headers=headers, data=payload)
        response.raise_for_status()
        response_wrapper = PageResponseWrapper[list[dict]](**response.json())

        # records = json.loads(response.text)["data"]["records"]
        records = response_wrapper.data.records
        csv_columns = [col.name for col in format_meta.csvColumnInfo]
        data = [{k: row.get(k) for k in csv_columns} for row in records]
        return pd.DataFrame(data, columns=csv_columns)
