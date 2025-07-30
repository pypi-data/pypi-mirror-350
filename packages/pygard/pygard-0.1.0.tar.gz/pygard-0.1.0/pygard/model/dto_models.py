# !/usr/bin/env python
# -*- coding: UTF-8 -*-
#
# @Project ：data-service-sdk-python
# @Author ：qm
# @Date ：2025/5/13 18:14
# @Description:

from pygard.model.enum_models import EnumFormat


class DataInstanceMetaRequest:
    did: int
    format: EnumFormat

    def __init__(self, did: int, _format: EnumFormat):
        self.did = did
        self.format = _format
