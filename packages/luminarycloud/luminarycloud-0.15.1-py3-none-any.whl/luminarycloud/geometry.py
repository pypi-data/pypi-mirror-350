# Copyright 2023-2024 Luminary Cloud, Inc. All Rights Reserved.
from __future__ import annotations

from datetime import datetime
import random
from uuid import uuid4
import time
from typing import Sequence

from typing_extensions import TYPE_CHECKING

import luminarycloud as lc

from ._client import get_default_client
from ._helpers._timestamp_to_datetime import timestamp_to_datetime
from ._proto.api.v0.luminarycloud.geometry import geometry_pb2 as geometrypb
from ._proto.geometry import geometry_pb2 as gpb
from .enum import GeometryStatus
from .params.geometry import Surface, Volume
from .tag import Tag
from ._wrapper import ProtoWrapper, ProtoWrapperBase
from .params.geometry import (
    Shape,
    shapes,
)
from .types import Vector3, GeometryFeatureID, ProjectID
from .volume_selection import VolumeSelection

if TYPE_CHECKING:
    from .project import Project


@ProtoWrapper(geometrypb.Geometry)
class Geometry(ProtoWrapperBase):
    """Represents a Geometry object."""

    id: str
    "Geometry ID."
    name: str
    "Geometry name."
    status: GeometryStatus
    "The status of the geometry."

    _proto: geometrypb.Geometry

    @property
    def create_time(self) -> datetime:
        """
        The time the geometry was created.
        """
        return timestamp_to_datetime(self._proto.create_time)

    @property
    def update_time(self) -> datetime:
        """
        The time the geometry was last updated.
        """
        return timestamp_to_datetime(self._proto.update_time)

    def project(self) -> "Project":
        """
        Get the project this geometry belongs to.
        """
        return lc.get_project(ProjectID(self._proto.project_id))

    def copy(self, name: str = "") -> "Geometry":
        """
        Copy the geometry.

        Returns
        -------
        Geometry
            A new copy of this geometry.
        """
        req = geometrypb.CopyGeometryRequest(
            geometry_id=self.id,
            request_id=str(uuid4()),
            name=name,
        )
        res: geometrypb.CopyGeometryResponse = get_default_client().CopyGeometry(req)
        return Geometry(res.geometry)

    def select_volumes(self, volumes: Sequence[Volume | int]) -> VolumeSelection:
        """
        Select the given volumes in the geometry for modification.

        Parameters
        ----------
        volumes : list[Volume | int]
            The volumes or volume IDs to select. Empty selection is allowed.
        """
        if not isinstance(volumes, list):
            raise TypeError("volumes must be a list")
        return VolumeSelection(self, volumes)

    def add_farfield(self, shape: Shape, propagate_tool_tags: bool = True) -> None:
        """
        Create a farfield feature in the geometry.
        This operation automatically subtracts the geometry from the farfield.

        Parameters
        ----------
        shape : Cube | Cylinder | HalfSphere | Sphere | Torus | Cone
            The shape of the farfield.
        propagate_tool_tags : bool
            If true, tags associated with the volumes to be subtracted will be propagated to their
            surfaces before performing the farfield subtraction.

        Examples
        --------
        Add a spherical farfield:

        >>> sphere = shapes.Sphere(center=Vector3(x=0.0, y=0.0, z=0.0), radius=2.0)
        >>> geometry.add_farfield(sphere)
        """
        create_proto = gpb.Create()
        if isinstance(shape, shapes.Sphere):
            create_proto.sphere.CopyFrom(shape._to_proto())  # type: ignore
        elif isinstance(shape, shapes.Cube):
            create_proto.box.CopyFrom(shape._to_proto())  # type: ignore
        elif isinstance(shape, shapes.Cylinder):
            create_proto.cylinder.CopyFrom(shape._to_proto())  # type: ignore
        elif isinstance(shape, shapes.Torus):
            create_proto.torus.CopyFrom(shape._to_proto())  # type: ignore
        elif isinstance(shape, shapes.Cone):
            create_proto.cone.CopyFrom(shape._to_proto())  # type: ignore
        elif isinstance(shape, shapes.HalfSphere):
            create_proto.half_sphere.CopyFrom(shape._to_proto())  # type: ignore
        else:
            raise TypeError(f"Unsupported shape for farfield: {type(shape)}")
        self._modify(
            modification=gpb.Modification(
                mod_type=gpb.Modification.MODIFICATION_TYPE_CREATE_FEATURE,
                feature=gpb.Feature(
                    id=str(uuid4()),
                    feature_name="Farfield",
                    farfield=gpb.Farfield(
                        create=create_proto,
                        propagate_tool_tags=propagate_tool_tags,
                    ),
                ),
            )
        )

    def undo(self) -> None:
        """
        Undo the last modification to the geometry.

        Examples
        --------
        >>> # Initialize create a farfield
        >>> geometry.add_farfield(
        ...     lc.params.geometry.shapes.Sphere(radius=2.0, center=Vector3(0.0, 0.0, 0.0))
        ... )
        >>> # Undo the last modification
        >>> geometry.undo()
        >>> # Re-create a bigger farfield with a different center
        >>> geometry.add_farfield(
        ...     lc.params.geometry.shapes.Sphere(radius=3.0, center=Vector3(1.0, 1.0, 1.0))
        ... )
        """
        self._modify(
            modification=gpb.Modification(
                mod_type=gpb.Modification.MODIFICATION_TYPE_UNDO,
            )
        )

    def redo(self) -> None:
        """
        Redo the last modification to the geometry.
        """
        self._modify(
            modification=gpb.Modification(
                mod_type=gpb.Modification.MODIFICATION_TYPE_REDO,
            )
        )

    def rename_feature(self, feature_id: GeometryFeatureID, new_name: str) -> None:
        """
        Rename a feature in the geometry.

        Parameters
        ----------
        feature_id : str
            The ID of the feature to rename.
        new_name : str
            The new name for the feature.
        """
        self._modify(
            modification=gpb.Modification(
                mod_type=gpb.Modification.MODIFICATION_TYPE_RENAME_FEATURE,
                feature=gpb.Feature(
                    id=feature_id,
                    feature_name=new_name,
                ),
            )
        )

    def delete_feature(self, feature_id: GeometryFeatureID) -> None:
        """
        Delete a feature from the geometry.

        Parameters
        ----------
        feature_id : str
            The ID of the feature to delete.
        """
        self._modify(
            modification=gpb.Modification(
                mod_type=gpb.Modification.MODIFICATION_TYPE_DELETE_FEATURE,
                feature=gpb.Feature(
                    id=feature_id,
                ),
            )
        )

    def delete_tags(self, names: list[str]) -> None:
        """
        Delete tags from the geometry.

        Parameters
        ----------
        tag_names : list[str]
            The names of the tags to delete.
        """
        self._modify(
            modification=gpb.Modification(
                mod_type=gpb.Modification.MODIFICATION_TYPE_DELETE_TAGS,
                delete_tags=gpb.DeleteTags(
                    names=names,
                ),
            )
        )

    def check(self) -> tuple[bool, list[str]]:
        """
        Check the geometry for any issues that may prevent meshing.

        Returns
        -------
        ok : boolean
            If true, the geometry is ready for meshing.

            If false, the geometry contains errors. Inspect issues and resolve
            any errors.
        issues : list[str]
            A list of issues with the geometry.

            When ok=True, issues may be empty or non-empty but contain only
            warning or informational messages. When ok=False, issues will
            contain at least one error message and possibly additional warning
            or informational messages.
        """
        req = geometrypb.GetGeometryRequest(geometry_id=self.id)
        res_geo: geometrypb.GetGeometryResponse = get_default_client().GetGeometry(req)
        geometry_version_id = res_geo.geometry.last_version_id

        get_default_client().StartCheckGeometry(
            geometrypb.CheckGeometryRequest(
                geometry_id=self.id,
                geometry_version_id=geometry_version_id,
            )
        )

        while True:
            res: geometrypb.GetCheckGeometryResponse = get_default_client().GetCheckGeometry(
                geometrypb.CheckGeometryRequest(
                    geometry_id=self.id,
                    geometry_version_id=geometry_version_id,
                )
            )
            if res.finished:
                self.refresh()
                return res.ok, list(res.issues)
            jitter = random.uniform(0.5, 1.5)
            time.sleep(2 + jitter)

    def create_tag(self, name: str, entities: Sequence[Volume | Surface]) -> None:
        """
        Create a tag in the geometry.

        Parameters
        ----------
        name : str
            The name of the tag to create.
        entities : list of Volumes or Surfaces
            The Volumes and Surfaces to tag.
        """
        volume_ids = []
        surface_ids = []
        for entity in entities:
            if isinstance(entity, Volume):
                volume_ids.append(int(entity.id))
            elif isinstance(entity, Surface):
                surface_ids.append(int(entity._native_id))
            else:
                raise TypeError("entities must be of type Volume or Surface")

        req = geometrypb.ModifyGeometryRequest(
            geometry_id=self.id,
            modification=gpb.Modification(
                mod_type=gpb.Modification.MODIFICATION_TYPE_CREATE_TAG,
                create_or_update_tag=gpb.CreateOrUpdateTag(
                    name=name,
                    bodies=volume_ids,
                    faces=surface_ids,
                ),
            ),
        )
        get_default_client().ModifyGeometry(req)

    def rename_tag(self, old_name: str, new_name: str) -> None:
        """
        Rename a tag in the geometry.

        Parameters
        ----------
        old_name : str
            The name of the tag to rename.
        new_name : str
            The new name for the tag.
        """
        self._modify(
            modification=gpb.Modification(
                mod_type=gpb.Modification.MODIFICATION_TYPE_RENAME_TAG,
                rename_tag=gpb.RenameTag(
                    old_name=old_name,
                    new_name=new_name,
                ),
            ),
        )

    def untag_entities(self, name: str, entities: Sequence[Volume | Surface]) -> None:
        """
        Untag entities from a tag in the geometry.

        Parameters
        ----------
        name : str
            The name of the tag.
        entities : list of Volumes or Surfaces
            The Volumes and Surfaces to untag. If empty, all entities with the
            tag will be untagged.
        """
        volume_ids = []
        surface_ids = []
        for entity in entities:
            if isinstance(entity, Volume):
                volume_ids.append(int(entity.id))
            elif isinstance(entity, Surface):
                surface_ids.append(int(entity._native_id))
            else:
                raise TypeError("entities must be of type Volume or Surface")

        self._modify(
            modification=gpb.Modification(
                mod_type=gpb.Modification.MODIFICATION_TYPE_DELETE_TAG,
                delete_tag=gpb.DeleteTag(
                    name=name,
                    bodies=volume_ids,
                    faces=surface_ids,
                ),
            ),
        )

    def update_tag(self, name: str, entities: Sequence[Volume | Surface]) -> None:
        """
        Adds entities to a tag in the geometry.

        Parameters
        ----------
        name : str
            The name of the tag to update.
        entities : list of Volumes or Surfaces
        """
        volume_ids = []
        surface_ids = []
        for entity in entities:
            if isinstance(entity, Volume):
                volume_ids.append(int(entity.id))
            elif isinstance(entity, Surface):
                surface_ids.append(int(entity._native_id))
            else:
                raise TypeError("entities must be of type Volume or Surface")

        self._modify(
            modification=gpb.Modification(
                mod_type=gpb.Modification.MODIFICATION_TYPE_UPDATE_TAG,
                create_or_update_tag=gpb.CreateOrUpdateTag(
                    name=name,
                    bodies=volume_ids,
                    faces=surface_ids,
                ),
            ),
        )

    def list_tags(self) -> list[Tag]:
        """
        Get the tags currently associated with the geometry.

        Returns
        -------
        list[Tag]
        """
        req = geometrypb.ListTagsRequest(
            geometry_id=self.id,
        )
        res: geometrypb.ListTagsResponse = get_default_client().ListTags(req)
        return [Tag(t) for t in res.tags]

    def list_entities(self) -> tuple[list[Surface], list[Volume]]:
        """
        List all the entities in the geometry.

        Returns
        -------
        surfaces : list[Surface]
            A list of all the surfaces in the geometry.
        volumes : list[Volume]
            A list of all the volumes in the geometry.
        """

        res: geometrypb.ListGeometryEntitiesResponse = get_default_client().ListGeometryEntities(
            geometrypb.ListGeometryEntitiesRequest(geometry_id=self.id)
        )
        surfaces = [
            Surface(
                geometry_id=self.id,
                id=f.id,
                _native_id=f.native_id,
                bbox_min=Vector3(f.bbox_min.x, f.bbox_min.y, f.bbox_min.z),
                bbox_max=Vector3(f.bbox_max.x, f.bbox_max.y, f.bbox_max.z),
            )
            for f in res.faces
        ]
        volumes = [
            Volume(
                geometry_id=self.id,
                id=str(b.id),
                _lcn_id=str(b.lcn_id),
                bbox_min=Vector3(b.bbox_min.x, b.bbox_min.y, b.bbox_min.z),
                bbox_max=Vector3(b.bbox_max.x, b.bbox_max.y, b.bbox_max.z),
            )
            for b in res.bodies
        ]
        return surfaces, volumes

    def _modify(self, modification: gpb.Modification) -> None:
        """
        Apply a modification to the geometry.

        Parameters
        ----------
        modification : Modification
            The modification to apply to the geometry. If the modification type is
            `MODIFICATION_TYPE_CREATE_FEATURE`, and the feature is a `farfield`, the
            geometry will be automatically subtracted from the farfield.
        """
        req = geometrypb.ModifyGeometryRequest(
            geometry_id=self.id,
            modification=modification,
            request_id=str(uuid4()),
        )
        get_default_client().ModifyGeometry(req)

    def _list_features(
        self,
    ) -> list[gpb.Feature]:
        """
        List the current features in the geometry.

        Returns
        -------
        features : list[Feature]
            A list of the current features in the geometry.
        """
        req = geometrypb.ListGeometryFeaturesRequest(
            geometry_id=self.id,
        )
        res: geometrypb.ListGeometryFeaturesResponse = get_default_client().ListGeometryFeatures(
            req
        )
        return list(res.features)

    def _list_feature_issues(
        self,
    ) -> list[gpb.FeatureIssues]:
        """
        List any issues with features in the geometry.

        Returns
        -------
        feature_issues : list[FeatureIssues]
            A list of any issues with features in the geometry. Issues may be
            informational, warnings or errors.
        """
        req = geometrypb.ListGeometryFeatureIssuesRequest(
            geometry_id=self.id,
        )
        res: geometrypb.ListGeometryFeatureIssuesResponse = (
            get_default_client().ListGeometryFeatureIssues(req)
        )
        return list(res.features_issues)

    def refresh(self) -> None:
        """
        Refresh the geometry status.
        """
        req = geometrypb.GetGeometryRequest(geometry_id=self.id)
        res: geometrypb.GetGeometryResponse = get_default_client().GetGeometry(req)
        self._proto = res.geometry


def get_geometry(id: str) -> Geometry:
    """
    Get a specific geometry with the given ID.

    Parameters
    ----------
    id : str
        Geometry ID.

    Returns
    -------
    Geometry
        The requested Geometry.
    """

    req = geometrypb.GetGeometryRequest(geometry_id=id)
    res: geometrypb.GetGeometryResponse = get_default_client().GetGeometry(req)
    return Geometry(res.geometry)
