# Copyright 2025 Luminary Cloud, Inc. All Rights Reserved.
from __future__ import annotations

from datetime import datetime
from typing import List

from .._client import get_default_client
from .._helpers._timestamp_to_datetime import timestamp_to_datetime
from .._proto.api.v0.luminarycloud.physics_ai import physics_ai_pb2 as physaipb
from .._wrapper import ProtoWrapper, ProtoWrapperBase
from .._helpers.warnings import experimental
from ..types.ids import PhysicsAiModelID


@experimental
@ProtoWrapper(physaipb.PhysicsAiModel)
class PhysicsAiModel(ProtoWrapperBase):
    """Represents a Physics AI model."""

    id: PhysicsAiModelID
    name: str
    version: str

    _proto: physaipb.PhysicsAiModel

    @property
    def create_time(self) -> datetime:
        return timestamp_to_datetime(self._proto.create_time)

    @property
    def update_time(self) -> datetime:
        return timestamp_to_datetime(self._proto.update_time)


@experimental
def list_pretrained_models() -> List[PhysicsAiModel]:
    """
    List available pretrained Physics AI models.
    """
    req = physaipb.ListPretrainedModelsRequest()
    res = get_default_client().ListPretrainedModels(req)
    return [PhysicsAiModel(model) for model in res.models]
