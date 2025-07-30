# !/usr/bin/env python
# -*- coding: UTF-8 -*-
#
# @Project ：data-service-sdk-python
# @Author ：qm
# @Date ：2025/5/9 9:47
# @Description:


class GardMetaConfig:
    """
    Configuration class for GardMetaClient.
    """

    host: str = "localhost"  # TODO: change to dev host
    port: int = 8083
    protocol: str = "http"

    def __init__(self, host: str = None, port: int = None, protocol: str = None):
        """
        Initialize the GardMetaConfig with optional host, port, and protocol.
        """
        if host:
            self.host = host
        if port:
            self.port = port
        if protocol:
            self.protocol = protocol
