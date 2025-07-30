from typing import TYPE_CHECKING, TypeVar

from numpy.typing import ArrayLike

if TYPE_CHECKING:
    pass
T = TypeVar('T', bound=ArrayLike)


def get_fixed_quantizer(round_mode: str = 'TRN', overflow_mode: str = 'WRAP'):
    """Get a stateless fixed-point quantizer given the round and overflow mode.
    The quantizer is differentiable w.r.t. to the input and f, also i if using saturation overflow mode.

    Args:
        round_mode: round mode, one of
    """
    from ._fixed_point_ops import _get_fixed_quantizer

    return _get_fixed_quantizer(round_mode, overflow_mode)
