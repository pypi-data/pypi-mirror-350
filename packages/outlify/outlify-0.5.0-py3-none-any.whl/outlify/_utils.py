from typing import Optional, Union, Any, Sequence
import shutil

from outlify.style import Align, Styles


def resolve_width(width: Optional[int]) -> int:
    if isinstance(width, int):
        return width
    if width is not None:
        raise ValueError(f'Invalid type for width: {width} is not int')

    try:
        return shutil.get_terminal_size().columns
    except (AttributeError, OSError):
        return 80  # Fallback width


def parse_title_align(align: Union[str, Align]) -> Align:
    return _parse_class(align, Align)


def _parse_class(element: Union[str, Any], cls: Any) -> Any:
    if isinstance(element, cls):
        return element
    return cls(element)


def parse_styles(codes: Optional[Sequence]) -> str:
    if codes is None:
        return ''
    return ''.join(codes)


def get_reset_by_style(style: str) -> str:
    """ Return the appropriate reset code for the given style

    If the style is empty, returns an empty reset.
    Otherwise, returns the standard reset
    """
    return Styles.reset if style != '' else ''
