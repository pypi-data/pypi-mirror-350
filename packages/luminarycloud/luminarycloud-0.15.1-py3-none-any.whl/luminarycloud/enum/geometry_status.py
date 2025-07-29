# Copyright 2023-2024 Luminary Cloud, Inc. All Rights Reserved.
from enum import IntEnum
from .._proto.api.v0.luminarycloud.geometry import geometry_pb2


class GeometryStatus(IntEnum):
    """
    Represents the status of a geometry.

    Attributes
    ----------
    UNKNOWN
        Status is unknown.
    IMPORTING
        Geometry is still being processed.
    NEEDS_CHECK
        Geometry was created but has not yet been checked.
    FAILED_CHECK
        Geometry is not well-formed and cannot be used.
    READY
        Geometry is ready to use.
    """

    UNKNOWN = geometry_pb2.Geometry.UNKNOWN
    IMPORTING = geometry_pb2.Geometry.IMPORTING
    NEEDS_CHECK = geometry_pb2.Geometry.NEEDS_CHECK
    FAILED_CHECK = geometry_pb2.Geometry.FAILED_CHECK
    READY = geometry_pb2.Geometry.READY
