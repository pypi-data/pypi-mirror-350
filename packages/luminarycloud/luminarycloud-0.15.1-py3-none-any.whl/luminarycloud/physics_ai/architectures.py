# Copyright 2025 Luminary Cloud, Inc. All Rights Reserved.
from __future__ import annotations

from typing import List

from .._client import get_default_client
from .._proto.api.v0.luminarycloud.physics_ai import physics_ai_pb2 as physaipb
from .._wrapper import ProtoWrapper, ProtoWrapperBase
from .._helpers.warnings import experimental
from ..types.ids import PhysicsAiArchitectureID


@experimental
@ProtoWrapper(physaipb.PhysicsAiArchitecture)
class PhysicsAiArchitecture(ProtoWrapperBase):
    """
    Represents a Physics AI architecture.

    warning:: This feature is experimental and may change or be removed without notice.
    """

    id: PhysicsAiArchitectureID
    name: str
    description: str
    version: str
    _proto: physaipb.PhysicsAiArchitecture


@experimental
def list_architectures() -> List[PhysicsAiArchitecture]:
    """
    List available Physics AI architectures for model training.

    warning:: This feature is experimental and may change or be removed without notice.
    """
    req = physaipb.ListArchitecturesRequest()
    res = get_default_client().ListArchitectures(req)
    return [PhysicsAiArchitecture(arch) for arch in res.architectures]
