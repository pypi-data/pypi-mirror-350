from dataclasses import dataclass
from typing import List

import bs4
from bs4 import BeautifulSoup


class ParseSearchError(Exception):
    def __init__(self, error_message: str, error_string: str, *args: object) -> None:
        super().__init__(error_message, *args)
        self.error_string = error_string
        self.error_message = error_message


@dataclass
class FileMeta:
    name: str
    size_text: str


@dataclass
class ParsedItem:
    magnet: str
    release_date: str  # yyyy-mm-dd
    size_text: str
    file_list: List[FileMeta]


def btfa(el: bs4.Tag, *args, **kwargs) -> List[bs4.Tag]:
    """bs4_typed_find_all"""
    return el.find_all(*args, **kwargs)


# https://cilisousuo.com/magnet/ilrS
def parse_item(html: str) -> ParsedItem:
    soup = BeautifulSoup(html, "lxml")

    meta: bs4.Tag = btfa(soup, "dl", class_="meta")[0]
    dt_s = btfa(meta, "dt")
    dd_s = btfa(meta, "dd")
    if dt_s[0].getText() != "种子特征码 :":
        msg = "Except '种子特征码 :'"
        raise ValueError(msg)
    magnet = dd_s[0].getText()
    if dt_s[1].getText() != "发布日期 :":
        msg = "Except '发布日期 :'"
        raise ValueError(msg)
    release_date = dd_s[1].getText()
    if dt_s[2].getText() != "文件大小 :":
        msg = "Except '文件大小 :'"
        raise ValueError(msg)

    size_text = dd_s[2].getText()

    file_trs = btfa(btfa(btfa(soup, "table", class_="files")[0], "tbody")[0], "tr")

    return ParsedItem(
        magnet=magnet,
        release_date=release_date,
        size_text=size_text,
        file_list=[
            FileMeta(name=btfa(f, "td")[0].getText(), size_text=btfa(f, class_="td-size")[0].getText())
            for f in file_trs
        ],
    )
