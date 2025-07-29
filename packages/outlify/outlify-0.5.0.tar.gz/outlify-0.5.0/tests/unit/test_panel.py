from typing import Union, Optional, Any, Sequence

import pytest

from outlify.panel import PanelBase, Panel, ParamsPanel
from outlify.style import Align, BorderStyle, AnsiCodes


class ReleasedPanelBase(PanelBase):
    def __init__(
            self, content: str = 'test', *, width: Optional[int] = None,
            title: str = '', title_align: Union[str, Align] = 'center',
            title_style: Optional[Sequence[Union[AnsiCodes, str]]] = None,
            subtitle: str = '', subtitle_align: Union[str, Align] = 'center',
            subtitle_style: Optional[Sequence[Union[AnsiCodes, str]]] = None,
            border: Union[str | BorderStyle] = '╭╮╰╯─│',
            border_style: Optional[Sequence[Union[AnsiCodes, str]]] = None,
    ):
        super().__init__(
            content, width=width,
            title=title, title_align=title_align, title_style=title_style,
            subtitle=subtitle, subtitle_align=subtitle_align, subtitle_style=subtitle_style,
            border=border, border_style=border_style
        )

    def get_content(self, content: str, *, width: int, char: str, border_style: str) -> str:
        return ''


@pytest.mark.unit
@pytest.mark.parametrize(
    'width,result',
    [
        (10, 6),     # small size
        (80, 76),    # default size
        (160, 156),  # big size
        (4, None),
        (0, None),
    ]
)
def test_get_inner_width(width: int, result: int):
    base = ReleasedPanelBase()
    if result is not None:
        assert base._get_inner_width(width) == result
        return

    with pytest.raises(ValueError):
        base._get_inner_width(width)


@pytest.mark.unit
@pytest.mark.parametrize(
    'style,result',
    [
        ('╭╮╰╯─│', BorderStyle('╭', '╮', '╰', '╯', '─', '│')),
        ('╭╮╰╯─', BorderStyle('╭', '╮', '╰', '╯', '─', '')),
        ('123456', BorderStyle('1', '2', '3', '4', '5', '6')),
        ('12345', BorderStyle('1', '2', '3', '4', '5', '')),
        (123, None),
        ('╭╮', None),
        ('╭╮╰╯─│{', None),
        (BorderStyle('╭', '╮', '╰', '╯', '─', '│'), BorderStyle('╭', '╮', '╰', '╯', '─', '│')),
        (BorderStyle('1', '2', '3', '4', '5', '6'), BorderStyle('1', '2', '3', '4', '5', '6')),
    ]
)
def test_parse_border_style(style: Union[str, BorderStyle], result: BorderStyle):
    base = ReleasedPanelBase()
    if result is not None:
        assert base._parse_border(style) == result
        return

    with pytest.raises(ValueError):
        base._parse_border(style)


@pytest.mark.unit
@pytest.mark.parametrize(
    'title,align,char,result',
    [
        ('TITLE', Align.left, '-', '- TITLE --'),
        ('TITLE', Align.center, '-', '- TITLE --'),
        ('TITLE', Align.right, '-', '-- TITLE -'),
    ]
)
def test_fill_header(title: str, align: Align, char: str, result: str):
    assert ReleasedPanelBase()._fill_header(
        title, align=align, width=10, char=char, title_style='', title_style_reset='', border_style=''
    ) == result


@pytest.mark.unit
@pytest.mark.parametrize(
    'title,align,left,char,right,result',
    [
        ('TITLE', Align.left, '╭', '-', '╮', '╭- TITLE --╮'),
        ('TITLE', Align.center, '╭', '-', '╮', '╭- TITLE --╮'),
        ('TITLE', Align.right, '╭', '-', '╮', '╭-- TITLE -╮'),
        ('fake', Align.center, '╭', '-', '╮', '╭-- fake --╮'),
        ('fake', Align.center, '+', ' ', '+', '+   fake   +'),
    ]
)
def test_get_header(title: str, align: Align, left: str, char: str, right: str, result: str):
    base = ReleasedPanelBase()
    assert base.get_header(
        title, align=align, title_style='', title_style_reset='', width=12,
        left=left, char=char, right=right, border_style=''
    ) == result


@pytest.mark.unit
@pytest.mark.parametrize(
    'line,width,char,indent,result',
    [
        ('test', 6, '|', '', '| test   |'),
        ('test', 6, '|', ' ', '|  test  |'),
        ('test', 6, '|', '-', '| -test  |'),
        ('test', 6, '1', '-', '1 -test  1'),
        ('test', 10, '|', ' ', '|  test      |'),
    ]
)
def test_fill(line: str, width: int, char: str, indent: str, result: str):
    assert ReleasedPanelBase().fill(
        line, width=width, char=char, indent=indent, border_style=''
    ) == result


@pytest.mark.unit
@pytest.mark.parametrize(
    'text,title,title_align,subtitle,subtitle_align,result',
    [
        (
            'test', '', 'center', '', 'center',
            '╭──────────────────╮\n'
            '│ test             │\n'
            '╰──────────────────╯'
        ),
        (
            'test looooong text', '', 'center', '', 'center',
            '╭──────────────────╮\n'
            '│ test looooong    │\n'
            '│ text             │\n'
            '╰──────────────────╯'
        ),
        (
            'test looooonooooooooog', '', 'center', '', 'center',
            '╭──────────────────╮\n'
            '│ test looooonoooo │\n'
            '│ ooooog           │\n'
            '╰──────────────────╯'
        ),

        (
            'test', 'title1', 'left', 'title2', 'left',
            '╭─ title1 ─────────╮\n'
            '│ test             │\n'
            '╰─ title2 ─────────╯'
        ),
        (
            'test', 'title1', 'center', 'title2', 'center',
            '╭───── title1 ─────╮\n'
            '│ test             │\n'
            '╰───── title2 ─────╯'
        ),

        (
            'test', 'title1', 'right', 'title2', 'right',
            '╭───────── title1 ─╮\n'
            '│ test             │\n'
            '╰───────── title2 ─╯'
        ),
        (
            'test', 'title1', 'left', 'title2', 'center',
            '╭─ title1 ─────────╮\n'
            '│ test             │\n'
            '╰───── title2 ─────╯'
        ),
        (
            'test', 'title1', 'left', 'title2', 'right',
            '╭─ title1 ─────────╮\n'
            '│ test             │\n'
            '╰───────── title2 ─╯'
        ),

        (
            'test', 'title1', 'center', 'title2', 'left',
            '╭───── title1 ─────╮\n'
            '│ test             │\n'
            '╰─ title2 ─────────╯'
        ),
        (
            'test', 'title1', 'center', 'title2', 'right',
            '╭───── title1 ─────╮\n'
            '│ test             │\n'
            '╰───────── title2 ─╯'
        ),

        (
            'test', 'title1', 'right', 'title2', 'left',
            '╭───────── title1 ─╮\n'
            '│ test             │\n'
            '╰─ title2 ─────────╯'
        ),
        (
            'test', 'title1', 'right', 'title2', 'center',
            '╭───────── title1 ─╮\n'
            '│ test             │\n'
            '╰───── title2 ─────╯'
        ),
    ]
)
def test_panel(text: str, title: str, title_align: str, subtitle: str, subtitle_align: str, result: str):
    panel = Panel(
        text, width=20, title=title, subtitle=subtitle,
        title_align=title_align, title_style='',
        subtitle_align=subtitle_align, subtitle_style='',
        border_style=''
    )
    assert str(panel) == result


@pytest.mark.unit
@pytest.mark.parametrize(
    'params,title,title_align,subtitle,subtitle_align,result',
    [
        (
            {'x': 10, 'y': 20}, '', 'center', '', 'center',
            '╭──────────────────╮\n'
            '│ x = 10           │\n'
            '│ y = 20           │\n'
            '╰──────────────────╯'
        ),
        (
            {'x': 10000000000000}, '', 'center', '', 'center',
            '╭──────────────────╮\n'
            '│ x = 100000000000 │\n'
            '│     00           │\n'
            '╰──────────────────╯'
        ),

        (
            {'x': 10}, 'title1', 'left', 'title2', 'left',
            '╭─ title1 ─────────╮\n'
            '│ x = 10           │\n'
            '╰─ title2 ─────────╯'
        ),
        (
            {'x': 10}, 'title1', 'center', 'title2', 'center',
            '╭───── title1 ─────╮\n'
            '│ x = 10           │\n'
            '╰───── title2 ─────╯'
        ),
        (
            {'x': 10}, 'title1', 'right', 'title2', 'right',
            '╭───────── title1 ─╮\n'
            '│ x = 10           │\n'
            '╰───────── title2 ─╯'
        ),

        (
            {'x': 10}, 'title1', 'left', 'title2', 'center',
            '╭─ title1 ─────────╮\n'
            '│ x = 10           │\n'
            '╰───── title2 ─────╯'
        ),
        (
            {'x': 10}, 'title1', 'left', 'title2', 'right',
            '╭─ title1 ─────────╮\n'
            '│ x = 10           │\n'
            '╰───────── title2 ─╯'
        ),

        (
            {'x': 10}, 'title1', 'center', 'title2', 'left',
            '╭───── title1 ─────╮\n'
            '│ x = 10           │\n'
            '╰─ title2 ─────────╯'
        ),
        (
            {'x': 10}, 'title1', 'center', 'title2', 'right',
            '╭───── title1 ─────╮\n'
            '│ x = 10           │\n'
            '╰───────── title2 ─╯'
        ),

        (
            {'x': 10}, 'title1', 'right', 'title2', 'left',
            '╭───────── title1 ─╮\n'
            '│ x = 10           │\n'
            '╰─ title2 ─────────╯'
        ),
        (
            {'x': 10}, 'title1', 'right', 'title2', 'center',
            '╭───────── title1 ─╮\n'
            '│ x = 10           │\n'
            '╰───── title2 ─────╯'
        ),
    ]
)
def test_params_panel(
        params: dict[Any, Any], title: str, title_align: str, subtitle: str, subtitle_align: str,
        result: str
):
    panel = ParamsPanel(
        params, width=20, title=title, subtitle=subtitle,
        title_align=title_align, title_style='',
        subtitle_align=subtitle_align, subtitle_style='',
        border_style='', params_style=''
    )
    assert str(panel) == result
