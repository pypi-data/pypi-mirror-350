from enum import Enum
from typing import NamedTuple

from outlify._ansi import Colors, Back, Styles, AnsiCodes, AnsiColorsCodes, AnsiBackColorsCodes, AnsiStylesCodes  # noqa: F401


class Align(Enum):
    left = 'left'
    center = 'center'
    right = 'right'


class BorderStyle(NamedTuple):
    lt: str
    rt: str
    lb: str
    rb: str
    headers: str
    sides: str

if __name__ == '__main__':
    print(f'Outlify allow you {Styles.bold}styling{Styles.reset} your text')
    print(
        f'for example, you can {Colors.blue}color{Colors.reset} your text, '
        f'{Styles.underline}underline{Styles.reset} it.'
    )
