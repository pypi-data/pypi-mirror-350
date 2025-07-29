from abc import ABC, abstractmethod
from typing import Sequence, Any, Optional

from outlify.style import AnsiCodes
from outlify._utils import resolve_width, parse_styles, get_reset_by_style


__all__ = ['TitledList']


class ListBase(ABC):

    def __init__(
            self, content: Sequence[Any], *, width: Optional[int],
            title: str, title_separator: str, title_style: Optional[Sequence[AnsiCodes]],
    ):
        self.width = resolve_width(width)
        title_style = parse_styles(title_style)
        title_reset = get_reset_by_style(title_style)
        self.title = self._get_title(title, count=len(content), style=title_style, reset=title_reset)
        self.title_separator = title_separator

        content = self._prepare_content(content)
        self.content = self.get_content(content, width=self.width)

    @abstractmethod
    def get_content(self, content: list[Any], *, width: int) -> str:
        pass

    @staticmethod
    def _get_title(title: str, *, count: int, style: str, reset: str) -> str:
        return f'{style}{title} ({count}){reset}'

    @staticmethod
    def _prepare_content(content: Sequence[Any]) -> list[str]:
        return [str(elem) for elem in content]

    def __str__(self) -> str:
        if len(self.content) == 0:
            return self.title
        return self.title_separator.join((self.title, self.content))

    def __repr__(self) -> str:
        return self.__str__()


class TitledList(ListBase):

    def __init__(
            self, content: Sequence[Any], *, title: str = 'Content', title_style: Optional[Sequence[AnsiCodes]] = None,
            separator: str = '  ',
    ):
        """ A simple list for displaying elements with customizable title.

        Can be used to list installed packages, processed files, etc.

        :param content: element enumeration
        :param title: title displayed before elements
        :param title_style: enumeration of styles. Any class inherited from AnsiCodes, including Colors and Styles
        :param separator: separator between title and elements
        """
        self.separator = separator
        super().__init__(content, width=None, title=title, title_separator=': ', title_style=title_style)

    def get_content(self, content: list[str], *, width: int) -> str:
        return self.separator.join(content)


if __name__ == '__main__':
    print(
        'Outlify helps you create list output in a beautiful format\n',
        'The first one is the simplest: a titled list', sep='\n'
    )
    print(TitledList(['ruff@1.0.0', 'pytest@1.2.3', 'mkdocs@3.2.1', 'mike@0.0.1'], title='Packages'))
