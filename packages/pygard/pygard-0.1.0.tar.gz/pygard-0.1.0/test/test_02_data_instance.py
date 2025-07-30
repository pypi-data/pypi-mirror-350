# !/usr/bin/env python
# -*- coding: UTF-8 -*-
#
# @Project ：data-service-sdk-python
# @Author ：qm
# @Date ：2025/5/13 18:07
# @Description:

import unittest

from pygard.config.gardmeta_config import GardMetaConfig
from pygard.service.gardmeta_client import GardMetaClient
from pygard.model.dto_models import DataInstanceMetaRequest


class TestDataInstance(unittest.TestCase):
    def test_get_data_instance_by_id(self):
        # Step 1: Initialize the GardMetaClient
        config = GardMetaConfig()
        gard_meta_client = GardMetaClient(config=config)
        # Step 2: Query by ID
        result = gard_meta_client.query_by_id(did=1)
        print(result)
        # Step 3: Get data instance meta of certain ID
        data_instance_meta = gard_meta_client.get_data_instance_meta(data_mark=DataInstanceMetaRequest(
            did=result.did,
            _format=result.format
        ))
        print(data_instance_meta)
        # Step 4: Fetch data instance
        data = gard_meta_client.fetch_data_by_id(
            did=result.did,
            format=result.format,
            format_meta=data_instance_meta
        )
        print(data.head())

    def test_get_data_instance_by_sql(self):
        config = GardMetaConfig()
        gard_meta_client = GardMetaClient(config=config)
        result = gard_meta_client.query_by_id(did=1)
        # print(result)
        data_instance_meta = gard_meta_client.get_data_instance_meta(data_mark=DataInstanceMetaRequest(
            did=result.did,
            _format=result.format
        ))
        # print(data_instance_meta)

        # Step 4: Fetch data instance with SQL
        data = gard_meta_client.fetch_data_by_id(
            did=result.did,
            format=result.format,
            format_meta=data_instance_meta,
            sql="SELECT * FROM datahub.t_dde_01_geotherma_heat WHERE \"Lat\" > 80"
        )
        print(data.head())


if __name__ == "__main__":
    pass
