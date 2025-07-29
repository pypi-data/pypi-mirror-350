from .._proto.base.base_pb2 import AdFloatType, ExpressionType

from ..types.adfloat import _to_ad_proto, _from_ad_proto


def _named_variables_to_proto(
    named_variables: dict[str, float | str],
) -> dict[str, AdFloatType]:
    return {
        k: (
            _to_ad_proto(v)
            if isinstance(v, float)
            else AdFloatType(expression=ExpressionType(expression=v))
        )
        for k, v in named_variables.items()
    }


def _named_variables_from_proto(
    named_variables: dict[str, AdFloatType],
) -> dict[str, float | str]:
    return {
        k: v.variable.expression if v.HasField("variable") else _from_ad_proto(v)
        for k, v in named_variables.items()
    }
