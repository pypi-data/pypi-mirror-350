# !/usr/bin/env python
# -*- coding: UTF-8 -*-
#
# @Project ：data-service-sdk-python
# @Author ：qm
# @Date ：2025/5/9 9:59
# @Description:

import unittest
from pygard.config.gardmeta_config import GardMetaConfig
from pygard.service.gardmeta_client import GardMetaClient


class TestGardMetaClient(unittest.TestCase):
    """
    Test case for GardMetaClient.
    """

    def test_create_client(self):
        """
        Set up the test case with a default configuration.
        """
        # Create GardMetaConfig object
        config = GardMetaConfig()
        # Create GardMetaClient object
        gard_meta_client = GardMetaClient(config=config)
        # List all records
        result = gard_meta_client.list_all()
        print("Length of result:", len(result))
        print(result)

    def test_query_by_id(self):
        """
        Test querying by ID.
        """
        config = GardMetaConfig()
        gard_meta_client = GardMetaClient(config=config)
        # Query by ID
        result = gard_meta_client.query_by_id(did=1)
        print(type(result))
        print(result)

    def test_search_by_tags(self):
        """
        Test searching by tags.
        """
        config = GardMetaConfig()
        gard_meta_client = GardMetaClient(config=config)
        # Search by tags
        result = gard_meta_client.search_by_tags(tags=['tag1', 'tag2'])
        print(result)

    def test_search_by_keywords(self):
        """
        Test searching by keywords.
        """
        config = GardMetaConfig()
        gard_meta_client = GardMetaClient(config=config)
        # Search by keywords
        result = gard_meta_client.search_by_keywords(keywords='地表 热流')
        print(result)


if __name__ == '__main__':
    pass
