# Copyright 2023-2024 Luminary Cloud, Inc. All Rights Reserved.
import logging
from time import time, sleep

from .._proto.api.v0.luminarycloud.mesh.mesh_pb2 import Mesh, GetMeshRequest
from .._client import Client

logger = logging.getLogger(__name__)


def wait_for_mesh(
    client: Client,
    mesh: Mesh,
    *,
    interval_seconds: float = 2,
    timeout_seconds: float = float("inf"),
) -> Mesh.MeshStatus.ValueType:
    """
    Waits for a mesh to be done processing.

    Parameters
    ----------
    client: Client
        A LuminaryCloud Client (see client.py)
    mesh: Mesh
        The mesh to wait for.
    interval_seconds: float
        Number of seconds between polls. Default is 2 seconds.
    timeout_seconds: float
        Number of seconds before the operation times out. Default is infinity.

    Raises
    ------
    TimeoutError
    """
    deadline = time() + timeout_seconds
    while True:
        response = client.GetMesh(GetMeshRequest(id=mesh.id))
        status = response.mesh.status
        if status in [Mesh.MESH_STATUS_COMPLETED, Mesh.MESH_STATUS_FAILED]:
            return status
        sleep(max(0, min(interval_seconds, deadline - time())))
        if time() >= deadline:
            logger.error("`wait_for_mesh` timed out.")
            raise TimeoutError
