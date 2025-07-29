# Copyright 2023-2024 Luminary Cloud, Inc. All Rights Reserved.
from enum import IntEnum
from .._proto.quantity import quantity_pb2 as quantitypb
from .._proto.quantity import quantity_options_pb2 as quantityoptspb


class QuantityType(IntEnum):
    """
    Represents a quantity type.

    Attributes
    ----------
    ABS_MASS_FLOW
    AREA
    DENSITY
    DISK_ROTATION_RATE
    DISK_THRUST
    DISK_TORQUE
    DOWNFORCE
    DOWNFORCE_COEFFICIENT
    DRAG
    DRAG_COEFFICIENT
    ENERGY_FLUX
    FRICTION_FORCE
    FRICTION_FORCE_COEFFICIENT
    INNER_ITERATION_COUNT
    LIFT
    LIFT_COEFFICIENT
    MACH
    MASS_FLOW
    PITCHING_MOMENT
    PITCHING_MOMENT_COEFFICIENT
    PRESSURE
    PRESSURE_DRAG
    PRESSURE_DRAG_COEFFICIENT
    PRESSURE_FORCE
    PRESSURE_FORCE_COEFFICIENT
    RESIDUAL_DENSITY
    RESIDUAL_X_MOMENTUM
    RESIDUAL_Y_MOMENTUM
    RESIDUAL_Z_MOMENTUM
    RESIDUAL_ENERGY
    RESIDUAL_SA_VARIABLE
    RESIDUAL_TKE
    RESIDUAL_OMEGA
    RESIDUAL_GAMMA
    RESIDUAL_RE_THETA
    RESIDUAL_N_TILDE
    ROLLING_MOMENT
    ROLLING_MOMENT_COEFFICIENT
    SIDEFORCE
    SIDEFORCE_COEFFICIENT
    TEMPERATURE
    TOTAL_FORCE
    TOTAL_FORCE_COEFFICIENT
    TOTAL_MOMENT
    TOTAL_MOMENT_COEFFICIENT
    TOTAL_PRESSURE
    TOTAL_TEMPERATURE
    VELOCITY
    VELOCITY_MAGNITUDE
    VISCOUS_DRAG
    VISCOUS_DRAG_COEFFICIENT
    Y_PLUS
    YAWING_MOMENT
    YAWING_MOMENT_COEFFICIENT
    """

    UNSPECIFIED = quantitypb.INVALID_QUANTITY_TYPE

    # Force quantity types
    DISK_THRUST = quantitypb.DISK_THRUST
    DISK_TORQUE = quantitypb.DISK_TORQUE
    DOWNFORCE = quantitypb.DOWNFORCE
    DOWNFORCE_COEFFICIENT = quantitypb.DOWNFORCE_COEFFICIENT
    DRAG = quantitypb.DRAG
    DRAG_COEFFICIENT = quantitypb.DRAG_COEFFICIENT
    FRICTION_FORCE = quantitypb.FRICTION_FORCE
    FRICTION_FORCE_COEFFICIENT = quantitypb.FRICTION_FORCE_COEFFICIENT
    LIFT = quantitypb.LIFT
    LIFT_COEFFICIENT = quantitypb.LIFT_COEFFICIENT
    PITCHING_MOMENT = quantitypb.PITCHING_MOMENT
    PITCHING_MOMENT_COEFFICIENT = quantitypb.PITCHING_MOMENT_COEFFICIENT
    PRESSURE_FORCE = quantitypb.PRESSURE_FORCE
    PRESSURE_FORCE_COEFFICIENT = quantitypb.PRESSURE_FORCE_COEFFICIENT
    ROLLING_MOMENT = quantitypb.ROLLING_MOMENT
    ROLLING_MOMENT_COEFFICIENT = quantitypb.ROLLING_MOMENT_COEFFICIENT
    SIDEFORCE = quantitypb.SIDEFORCE
    SIDEFORCE_COEFFICIENT = quantitypb.SIDEFORCE_COEFFICIENT
    TOTAL_FORCE = quantitypb.TOTAL_FORCE
    TOTAL_FORCE_COEFFICIENT = quantitypb.TOTAL_FORCE_COEFFICIENT
    TOTAL_MOMENT = quantitypb.TOTAL_MOMENT
    TOTAL_MOMENT_COEFFICIENT = quantitypb.TOTAL_MOMENT_COEFFICIENT
    YAWING_MOMENT = quantitypb.YAWING_MOMENT
    YAWING_MOMENT_COEFFICIENT = quantitypb.YAWING_MOMENT_COEFFICIENT
    PRESSURE_DRAG = quantitypb.PRESSURE_DRAG
    PRESSURE_DRAG_COEFFICIENT = quantitypb.PRESSURE_DRAG_COEFFICIENT
    VISCOUS_DRAG = quantitypb.VISCOUS_DRAG
    VISCOUS_DRAG_COEFFICIENT = quantitypb.VISCOUS_DRAG_COEFFICIENT

    # Average quantity types
    DENSITY = quantitypb.DENSITY
    ENERGY_FLUX = quantitypb.ENERGY_FLUX
    MACH = quantitypb.MACH
    PRESSURE = quantitypb.PRESSURE
    TEMPERATURE = quantitypb.TEMPERATURE
    TOTAL_PRESSURE = quantitypb.TOTAL_PRESSURE
    TOTAL_TEMPERATURE = quantitypb.TOTAL_TEMPERATURE
    VELOCITY = quantitypb.VELOCITY
    VELOCITY_MAGNITUDE = quantitypb.VELOCITY_MAGNITUDE
    Y_PLUS = quantitypb.Y_PLUS

    # Residual quantity types
    RESIDUAL_DENSITY = quantitypb.RESIDUAL_DENSITY
    RESIDUAL_X_MOMENTUM = quantitypb.RESIDUAL_X_MOMENTUM
    RESIDUAL_Y_MOMENTUM = quantitypb.RESIDUAL_Y_MOMENTUM
    RESIDUAL_Z_MOMENTUM = quantitypb.RESIDUAL_Z_MOMENTUM
    RESIDUAL_ENERGY = quantitypb.RESIDUAL_ENERGY
    RESIDUAL_SA_VARIABLE = quantitypb.RESIDUAL_SA_VARIABLE
    RESIDUAL_TKE = quantitypb.RESIDUAL_TKE
    RESIDUAL_OMEGA = quantitypb.RESIDUAL_OMEGA
    RESIDUAL_GAMMA = quantitypb.RESIDUAL_GAMMA
    RESIDUAL_RE_THETA = quantitypb.RESIDUAL_RE_THETA
    RESIDUAL_N_TILDE = quantitypb.RESIDUAL_N_TILDE

    # Other quantity types
    ABS_MASS_FLOW = quantitypb.ABS_MASS_FLOW
    AREA = quantitypb.AREA
    DISK_ROTATION_RATE = quantitypb.DISK_ROTATION_RATE
    INNER_ITERATION_COUNT = quantitypb.INNER_ITERATION_COUNT
    MASS_FLOW = quantitypb.MASS_FLOW

    @classmethod
    def _is_average(cls, quantity: "QuantityType") -> bool:
        return quantity._has_tag(quantityoptspb.TAG_ANALYZER_AVERAGE)

    @classmethod
    def _is_force(cls, quantity: "QuantityType") -> bool:
        return quantity._has_tag(quantityoptspb.TAG_ANALYZER_FORCES)

    def _has_tag(self, tag: int | str) -> bool:
        """
        Check if the QuantityType has a given QuantityTag.

        Parameters
        ----------
        tag : int | str
            The tag to check. Can be the string representation, e.g. "TAG_MOMENT", or the enum
            value, e.g. luminarycloud._proto.quantity.quantity_options_pb2.TAG_MOMENT.

        Returns
        -------
        bool
            True if the QuantityType has the tag, False otherwise.
        """
        if isinstance(tag, str):
            if tag not in quantityoptspb.QuantityTag.keys():
                raise ValueError(f"Invalid tag: {tag}")
            tag = quantityoptspb.QuantityTag.Value(tag)
        if tag not in quantityoptspb.QuantityTag.values():
            raise ValueError(f"Invalid tag: {tag}")
        quantity_metadata = _get_quantity_metadata(self)
        return tag in quantity_metadata.tags.vals


def _get_quantity_metadata(quantity_type: QuantityType) -> quantityoptspb.Quantity:
    return (
        quantitypb.QuantityType.DESCRIPTOR.values_by_number[quantity_type]
        .GetOptions()
        .Extensions[quantitypb.quantity]
    )
