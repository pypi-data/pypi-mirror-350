# !/usr/bin/env python
# -*- coding: UTF-8 -*-
#
# @Project ：data-service-sdk-python
# @Author ：qm
# @Date ：2025/5/13 18:03
# @Description:


from pydantic import BaseModel


class EnumDataType(BaseModel):
    id: int
    value: str


class EnumAccessLevel(BaseModel):
    id: int
    value: str


class EnumDataStatus(BaseModel):
    id: int
    value: str


class EnumFormat(BaseModel):
    id: int
    value: str


class EnumGeometryType(BaseModel):
    id: int
    value: str


class EnumGtsType(BaseModel):
    id: int
    value: str


class EnumSourceType(BaseModel):
    id: int
    value: str


class EnumSpatialRepresentation(BaseModel):
    id: int
    value: str


class EnumTemporalType(BaseModel):
    id: int
    value: str
