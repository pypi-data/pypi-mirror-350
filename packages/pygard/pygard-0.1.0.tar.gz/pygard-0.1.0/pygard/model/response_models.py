# !/usr/bin/env python
# -*- coding: UTF-8 -*-
#
# @Project ：data-service-sdk-python
# @Author ：qm
# @Date ：2025/5/9 10:07
# @Description:


from typing import Generic, TypeVar, Optional
from pydantic import BaseModel, Field

T = TypeVar('T')


class ResponseWrapper(BaseModel, Generic[T]):
    """
    ResponseWrapper class for wrapping API responses.
    """

    code: int = Field(..., description="Response code")
    message: str = Field(..., description="Response message")
    data: Optional[T] = Field(None, description="Response data")


class PageResult(BaseModel, Generic[T]):
    """
    PageResult class for paginated API responses.
    """
    records: Optional[T] = Field(None, description="List of items")
    total: int = Field(..., description="Total number of items")
    size: int = Field(..., description="Number of items per page")
    current: int = Field(..., description="Current page number")
    pages: int = Field(..., description="Total page number")


class PageResponseWrapper(BaseModel, Generic[T]):
    """
    PageResponseWrapper class for wrapping paginated API responses.
    """

    code: int = Field(..., description="Response code")
    message: str = Field(..., description="Response message")
    data: PageResult[T] = Field(None, description="Total number of items")
