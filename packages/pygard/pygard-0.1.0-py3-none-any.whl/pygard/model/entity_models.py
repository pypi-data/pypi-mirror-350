# !/usr/bin/env python
# -*- coding: UTF-8 -*-
#
# @Project ：data-service-sdk-python
# @Author ：qm
# @Date ：2025/5/9 10:14
# @Description:


from datetime import datetime
from typing import Optional
from pydantic import BaseModel
from pygard.model.enum_models import (EnumFormat, EnumGtsType, EnumDataType, EnumGeometryType, EnumDataStatus,
                                      EnumTemporalType,
                                      EnumSourceType, EnumAccessLevel, EnumSpatialRepresentation)


class BBox2D(BaseModel):
    min_x: float
    min_y: float
    max_x: float
    max_y: float


class Buffer(BaseModel):
    info: str


class Other(BaseModel):
    info: str


class RevisionHistory(BaseModel):
    time: datetime
    editor: str
    message: str
    version: str


class VerticalRange(BaseModel):
    z_min: float
    z_max: float


class GardMeta(BaseModel):
    """
    GardMeta class for representing metadata of geo data.
    """
    did: int
    name: str
    description: str
    dataType: Optional[EnumDataType]
    format: EnumFormat
    isSpatial: bool
    isTemporal: bool
    storagePath: str
    size: int
    version: str
    createTime: datetime
    updateTime: datetime
    dataStatus: Optional[EnumDataStatus]
    accessLevel: Optional[EnumAccessLevel]
    thumbnail: Optional[str]
    tags: Optional[list[str]]
    other: Optional[str]
    buffer: Optional[str]
    coordinateSystem: Optional[str]
    spatialRepresentation: Optional[EnumSpatialRepresentation]
    geometryType: Optional[EnumGeometryType]
    bbox: Optional[BBox2D]
    verticalRange: Optional[VerticalRange]
    spatialResolution: Optional[float]
    isPaleo: Optional[bool]
    isCirca: Optional[bool]
    temporalType: Optional[EnumTemporalType]
    gtsType: Optional[EnumGtsType]
    startTime: Optional[datetime]
    endTime: Optional[datetime]
    geologicStart: Optional[str]
    geologicEnd: Optional[str]
    isotopeStart: Optional[str]
    isotopeEnd: Optional[str]
    temporalResolution: Optional[str]
    sourceType: Optional[EnumSourceType]
    provider: str
    collectionType: str
    collectionDate: Optional[datetime]
    reference: Optional[str]
    license: Optional[str]
    reliabilityScore: Optional[float]
    revisionHistory: Optional[list[RevisionHistory]]
    hasMultipleVersion: bool
    recordsNum: Optional[int]
    attributesNum: Optional[int]


class CsvColumnInfo(BaseModel):
    name: str
    type: str
    unit: str
    precision: int
    description: str


class CsvDataInstance(BaseModel):
    csvId: int
    gardMetaDid: int
    name: str
    description: str
    csvColumnInfo: list[CsvColumnInfo]
    instanceTableName: str
