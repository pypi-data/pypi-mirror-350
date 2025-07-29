from typing import Union

import pytest

from outlify.style import Align
from outlify._utils import parse_title_align


@pytest.mark.unit
@pytest.mark.parametrize(
    'align,result',
    [
        ('left', Align.left),
        ('center', Align.center),
        ('right', Align.right),
        (Align.left, Align.left),
        (Align.center, Align.center),
        (Align.right, Align.right),
    ]
)
def test_resolve_title_align(align: Union[str, Align], result: Align):
    assert parse_title_align(align) == result
