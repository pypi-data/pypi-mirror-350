import json
import re
from typing import List, cast

import bs4
from bs4 import BeautifulSoup
from pydantic import BaseModel


def fa(soup: bs4.Tag, *args, **kwargs) -> List[bs4.Tag]:
    return cast(List[bs4.Tag], soup.find_all(*args, **kwargs))


def f(soup: bs4.Tag, *args, **kwargs) -> bs4.Tag:
    return cast(bs4.Tag, soup.find(*args, **kwargs))


class SearchResultItem(BaseModel):
    product_id: str = ""
    title: str = ""
    actress: List[str] = []
    release_date: str = ""  # YYYY-MM-DD maybe empty, 注意 这个日期 是meta里的 可能和 页面展示的有1天之差!?
    description: str = ""
    duration: str = ""
    url: str = ""
    cover_url: str = ""
    category: List[str] = []
    publisher: str = ""
    director: str = ""
    tags: List[str] = []
    seek_prefix: str = ""  # 时间轴预览图, 后面加上 _0.jpg一直到 _99.jpg 就是所有时间轴预览图


# https://missav.com/sone-315
# https://missav.com/dm24/sone-315
def parse_item(html: str) -> SearchResultItem:
    soup = BeautifulSoup(html, "lxml")

    r = SearchResultItem()

    r.url = f(soup, "meta", property="og:url").attrs["content"]
    r.product_id = r.url.split("/")[-1].upper()
    r.cover_url = f(soup, "meta", property="og:image").attrs["content"]
    r.release_date = f(soup, "meta", property="og:video:release_date").attrs["content"]
    r.description = f(soup, "meta", property="og:description").attrs["content"]
    r.duration = f(soup, "meta", property="og:video:duration").attrs["content"]
    r.title = f(soup, "meta", property="og:title").attrs["content"].replace(r.product_id, "").strip()
    r.actress = [meta.attrs["content"] for meta in fa(soup, "meta", property="og:video:actor")]

    info_div = f(soup, "div", class_="space-y-2")
    catespan = f(info_div, "span", string="類型:")
    r.category = [a.text for a in fa(cast(bs4.Tag, catespan.parent), "a")] if catespan else []
    catespan = f(info_div, "span", string="發行商:")
    r.publisher = f(cast(bs4.Tag, catespan.parent), "a").text
    catespan = f(info_div, "span", string="導演:")
    r.director = f(cast(bs4.Tag, catespan.parent), "a").text
    catespan = f(info_div, "span", string="標籤:")
    r.tags = [a.text for a in fa(cast(bs4.Tag, catespan.parent), "a")] if catespan else []

    res = re.search(r"urls: (.*seek\\/)_0.jpg", html)
    if res:
        json_str = res.group(1) + '"]'
        r.seek_prefix = json.loads(json_str)[0]

    return r
