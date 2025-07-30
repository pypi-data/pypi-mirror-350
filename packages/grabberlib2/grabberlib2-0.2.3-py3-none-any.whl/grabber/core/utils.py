import asyncio
import multiprocessing
import pathlib
import shutil
from collections.abc import AsyncGenerator, Iterable
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import dataclass
from functools import partial
from itertools import islice
from time import sleep
from typing import Any, cast
from urllib import parse

import requests
from boltons.setutils import IndexedSet
from bs4 import BeautifulSoup, Tag
from casefy.casefy import snakecase
from lxml import etree
from PIL import Image
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.service import Service
from telegraph import Telegraph, exceptions
from tenacity import retry, wait_chain, wait_fixed
from tqdm import tqdm
from webdriver_manager.chrome import ChromeDriverManager

from grabber.core.bot.core import send_message
from grabber.core.settings import (
    AUTHOR_NAME,
    AUTHOR_URL,
    MAX_IMAGES_PER_POST,
    SHORT_NAME,
    get_media_root,
)

DEFAULT_THREADS_NUMBER = multiprocessing.cpu_count()
PAGINATION_QUERY = "div.jeg_navigation.jeg_pagination"
PAGINATION_PAGES_COUNT_QUERY = f"{PAGINATION_QUERY} span.page_info"
PAGINATION_BASE_URL_QUERY = "div.jeg_navigation.jeg_pagination a.page_number"
POSTS_QUERY_XPATH = (
    "/html/body/div[2]/div[5]/div/div[1]/div/div/div[2]/div/div/div[2]/div/div[1]/div/div/div/article/div/div/a"
)


query_mapping = {
    "xiuren.biz": ("div.content-inner img", "src"),
    "nudebird.biz": ("div.thecontent a", "href"),
    "hotgirl.biz": ("div.thecontent a", "href"),
    "nudecosplay.biz": ("div.content-inner a img", "src"),
    "www.v2ph.com": (
        "div.photos-list.text-center img",
        "src",
    ),  # Needs to handle pagination
    "cgcosplay.org": ("div.gallery-icon.portrait img", "src"),
    "mitaku.net": ("div.msacwl-img-wrap img", "src"),
    "www.xasiat.com": ("div.images a", "href"),
    "telegra.ph": ("img", "src"),
    "www.4khd.com": (
        "div.is-layout-constrained.entry-content.wp-block-post-content img",
        "src",
    ),
    "yellow": (
        "div.elementor-widget-container a[href^='https://terabox.com']",
        "href",
    ),
    "everia.club": ("div.divone div.mainleft img", "data-original"),
    "www.everiaclub.com": ("div.divone div.mainleft img", "src"),
    "bestgirlsexy.com": ("div.elementor-widget-container p img", "src"),
    "asigirl.com": ("a.asigirl-item", "href"),
    "cosplaytele.com": ("img.attachment-full.size-full", "src"),
    "hotgirl.asia": ("div.galeria_img img", "src"),
    "4kup.net": ("div#gallery div.caption a.cp", "href"),
    "buondua.com": ("div.article-fulltext p img", "src"),
    "www.erome.com": (
        "div.col-sm-12.page-content div div.media-group div.img div.img-blur img",
        "data-src",
    ),
    "erome.com": (
        "div.col-sm-12.page-content div div.media-group div.img div.img-blur img",
        "data-src",
    ),
    "es.erome.com": (
        "div.col-sm-12.page-content div div.media-group div.img div.img-blur img",
        "data-src",
    ),
    "notion": (
        "div.notion-page-content > div > div > div > div > div > div.notion-cursor-default > div > div > div > img",
        "src",
    ),
    "new.pixibb.com": (
        "div.blog-post-wrap > article.post-details > div.entry-content img",
        "src",
    ),
    "sexy.pixibb.com": (
        "div.blog-post-wrap > article.post-details > div.entry-content img",
        "src",
    ),
    "spacemiss.com": ("div.tdb-block-inner.td-fix-index > img", "src"),
    "www.hentaiclub.net": (
        "div.content div.post.row img.post-item-img.lazy",
        "data-original",
    ),
    "ugirls.pics": ("div#main div.my-2 img", "src"),
    "xlust.org": (
        "div.entry-wrapper div.entry-content.u-clearfix div.rl-gallery-container a",
        "href",
    ),
    "bikiniz.net": ("div.image_div img", "src"),
    "hotgirlchina.com": ("div.entry-inner p img", "src"),
    "cup2d.com": (
        "div.gridshow-posts-wrapper > article div.entry-content.gridshow-clearfix a",
        "href",
    ),
    "en.taotu.org": ("div#content div#MainContent_piclist.piclist a", "href"),
    "pt.jrants.com": ("div.bialty-container p img", "src"),
    "jrants.com": ("div.entry-content p img", "src"),
    "en.jrants.com": ("div.entry-content p img", "src"),
    "misskon.com": ("article div.entry p img", "data-src"),
    "www.nncos.com": ("div.entry-content div.entry.themeform p img", "data-src"),
    "www.lovecos.net": ("div.img p a img", "src"),
    "e-hentai.org": ("div#i3 img", "src"),
    "fuligirl.top": ("div.my-1 img", "src"),
    "youwu.lol": ("div.my-2 img", "src"),
    "cosxuxi.club": ("div.contentme a img", "src"),
    "www.hotgirl2024.com": (
        "div.article__content ul.article__image-list li.article__image-item a img",
        "data-src",
    ),
    "www.tokyobombers.com": (
        "div.gallery figure.gallery-item div.gallery-icon.portrait a img",
        "src",
    ),
    "tokyocafe.org": ("div.gallery figure.gallery-item div.gallery-icon.portrait a img", "src"),
    "forum.lewdweb.net": (
        "section.message-attachments ul.attachmentList li.file.file--linked a.file-preview",
        "href",
    ),
    "nudecosplaygirls.com": ("div#content article div.entry-inner div img", "src"),
    "vazounudes.com": ("div#content article div.entry-inner div img", "data-src"),
    "sheeshfans.com": ("div.block-album div.album-holder div.images a", "href"),
    "nsfw247.to": ("source", "src"),
    "asianviralhub.com": ("div.fp-player video", "src"),
    "www.sweetlicious.net": ("div.article__entry.entry-content div.wp-video video source", "src"),
    "happy.5ge.net": ("article p section img.image.lazyload", "data-src"),
    "sexygirl.cc": ("div.row.justify-content-center.m-1 div.row.mt-2 img", "src"),
    "xiunice.com": ("div.tdb-block-inner.td-fix-index figure img", "src"),
    "imgcup.com": ("div.post-entry div.inner-post-entry.entry-content figure img", "data-src"),
    "nudogram.com": ("div.content div.block-video div.video-holder div.player div.player-holder a img", "src"),
    "dvir.ru": ("div.content div.block-video div.video-holder div.player div.player-holder a img", "src"),
    "fapello.com": ("div a div.max-w-full img", "src"),
    "fapeza.com": ("div.image-row div.flex-1 a img", "src"),
    "kemono.su": ("div.post__files div.post__thumbnail figure a", "href"),
    "fapachi.com": ("div.container div.row div.col-6.col-md-4.my-2.model-media-prew a img", "data-src"),
    "nudostar.tv": ("div.box div.list-videos div#list_videos_common_videos_list_items div.item a div.img img", "src"),
    "thefappening.plus": ("div.gallery figure.gallery__item a img.gallery_thumb", "src"),
    "fapomania.com": ("div.leftocontar div.previzakosblo div.previzako a div.previzakoimag img", "src"),
    "fapello.pics": ("div.site-content div.content-area main.site-main article a[rel='screenshot']", "href"),
    "fapello.to": ("", ""),
}


@dataclass(kw_only=True)
class PaginationXPath:
    pagination_query: str
    pages_count_query: str
    pagination_base_url_query: str
    posts_query_xpath: str

    def __post_init__(self) -> None:
        self.pages_count_query = f"{self.pagination_query} {self.pages_count_query}"


query_pagination_mapping = {
    "xiuren.biz": PaginationXPath(
        pagination_query="div.jeg_navigation.jeg_pagination",
        pages_count_query="span.page_info",
        pagination_base_url_query="div.jeg_navigation.jeg_pagination a.page_number",
        posts_query_xpath=(
            "/html/body/div[2]/div[5]/div/div[1]/div/div/div[2]/div/div/div[2]/div/div[1]/div/div/div/article/div/div/a"
        ),
    ),
    "yellow": PaginationXPath(
        pagination_query="div.jeg_navigation.jeg_pagination",
        pages_count_query="span.page_info",
        pagination_base_url_query="div.jeg_navigation.jeg_pagination a.page_number",
        posts_query_xpath=(
            "/html/body/div[3]/div[4]/div/div[1]/div/div/div[2]/div/div/div[2]/div/div[1]/div/div/div/article/div/div/a"
        ),
    ),
    "nudecosplay.biz": PaginationXPath(
        pagination_query="div.jeg_navigation.jeg_pagination",
        pages_count_query="span.page_info",
        pagination_base_url_query="div.jeg_navigation.jeg_pagination a.page_number",
        posts_query_xpath="/html/body/div[2]/div[5]/div/div[1]/div/div/div[2]/div/div/div[2]/div/div/div/div/div/article/div/a",
    ),
    "buondua.com": PaginationXPath(
        pagination_query="div.pagination-list",
        pages_count_query="span a.pagination-link",
        pagination_base_url_query="div.pagination-list span a.pagination-link.is-current",
        posts_query_xpath="/html/body/div[2]/div/div[2]/nav[1]/div/span/a",
    ),
    "www.v2ph.com": PaginationXPath(
        pagination_query="div.py-2",
        pages_count_query="a.page-link",
        pagination_base_url_query="div.py-2 ul li.active a",
        posts_query_xpath="/html/body/div/div[2]/div/img",
    ),
}


headers_mapping = {
    "nudebird.biz": {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36",
    },
    "nudecosplay.biz": {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36",
    },
    "www.v2ph.com": {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36",
    },
    "cgcosplay.org": {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36",
    },
    "mitaku.net": {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36",
    },
    "www.xasiat.com": {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36",
    },
    "www.4khd.com": {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36",
    },
    "buondua.com": {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36",
    },
    "bunkr": {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36"
    },
    "bestgirlsexy.com": {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36",
    },
    "new.pixibb.com": {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36",
    },
    "sexy.pixibb.com": {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36",
    },
    "spacemiss.com": {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36",
    },
    "www.hentaiclub.net": {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36",
    },
    "ugirls.pics": {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36",
    },
    "xlust.org": {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36",
    },
    "common": {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36",
    },
    "bikiniz.net": {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36",
    },
    "hotgirlchina.com": {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36",
    },
    "cup2d.com": {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36",
    },
    "en.taotu.org": {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36",
    },
    "misskon.com": {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36",
    },
    "www.nncos.com": {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36",
    },
    "www.lovecos.net": {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36",
    },
    "e-hentai.org": {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36",
    },
    "fuligirl.top": {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36",
    },
    "cosxuxi.club": {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36",
    },
    "forum.lewdweb.net": {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36",
    },
    "happy.5ge.net": {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36",
    },
    "www.xpics.me": {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36",
    },
    "xpics.me": {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36",
    },
    "fapomania.com": {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36",
    },
    "fapello.to": {
        "Accept": "*/*",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36",
    },
    "hotleaks.tv": {
        "Accept": "*/*",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36",
        "X-Requested-With": "XMLHttpRequest",
    },
}


CHUNK_MAPPING = {
    99: 45,
    100: 50,
    150: 60,
    200: 70,
    250: 80,
    300: 90,
}


async def get_webdriver() -> webdriver.Chrome:
    options = webdriver.ChromeOptions()
    options.add_argument("start-maximized")
    options.add_argument("--headless")
    options.add_argument("--remote-debugging-port=9222")
    options.add_argument(
        "user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36"
    )
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option("useAutomationExtension", False)
    # executable_path = "/Users/mazulo/Dev/packages/chromedriver/chromedriver"
    # executable_path = "/home/mazulo/packages/chrome/chromedriver-linux64/chromedriver"
    executable_path = ChromeDriverManager().install()
    chrome_executable: Service = ChromeService(executable_path=executable_path)
    driver = webdriver.Chrome(options=options, service=chrome_executable)
    # driver = webdriver.Chrome(ChromeDriverManager().install())

    # stealth(
    #     driver,
    #     languages=["en-US", "en"],
    #     vendor="Google Inc.",
    #     platform="Win32",
    #     webgl_vendor="Intel Inc.",
    #     renderer="Intel Iris OpenGL Engine",
    #     fix_hairline=True,
    # )

    return driver


@retry(
    wait=wait_chain(
        *[wait_fixed(3) for _ in range(5)]
        + [wait_fixed(7) for _ in range(4)]
        + [wait_fixed(9) for _ in range(3)]
        + [wait_fixed(15)],
    ),
    reraise=True,
)
async def get_image_stream(
    url,
    headers: dict[str, Any] | None = None,
) -> requests.Response:
    """Wait 3s for 5 attempts
    7s for the next 4 attempts
    9s for the next 3 attempts
    then 15 for all attempts thereafter
    """
    if headers is not None:
        r = requests.get(url, headers=headers, stream=True)
    else:
        r = requests.get(url, stream=True)

    if r.status_code >= 300:
        raise Exception(f"Not able to retrieve {url}: {r.status_code}\n")

    return r


@retry(
    wait=wait_chain(
        *[wait_fixed(3) for _ in range(5)]
        + [wait_fixed(7) for _ in range(4)]
        + [wait_fixed(9) for _ in range(3)]
        + [wait_fixed(15)],
    ),
    reraise=True,
)
async def get_tags(
    url: str,
    query: str,
    headers: dict[str, Any] | None = None,
    uses_js: bool | None = False,
    should_retry: bool | None = True,
    bypass_cloudflare: bool | None = False,
) -> tuple[list[Tag], BeautifulSoup]:
    """Wait 3s for 5 attempts
    7s for the next 4 attempts
    9s for the next 3 attempts
    then 15 for all attempts thereafter
    """
    if uses_js or bypass_cloudflare:
        driver = await get_webdriver()
        driver.get(url)
        await asyncio.sleep(5)
        soup = BeautifulSoup(driver.page_source, features="lxml")
        tags = soup.select(query)
        if not tags and should_retry:
            driver.refresh()
            await asyncio.sleep(5)
            soup = BeautifulSoup(driver.page_source, features="lxml")
            tags = soup.select(query)
            if not tags:
                print("Page not rendered properly. Retrying one more time...")
                return await get_tags(
                    url=url,
                    query=query,
                    headers=headers,
                    uses_js=uses_js,
                    should_retry=False,
                )
    else:
        soup = await get_soup(target_url=url, headers=headers)
        tags = soup.select(query)

    return tags, soup


async def get_soup(
    target_url: str,
    headers: dict[str, str] | None = None,
    use_web_driver: bool | None = False,
) -> BeautifulSoup:
    if use_web_driver:
        driver = await get_webdriver()
        driver.get(target_url)
        page_source = driver.page_source
    else:
        response = requests.get(target_url, headers=headers)
        page_source = response.content

    return BeautifulSoup(page_source, features="lxml")


def wrapper(coro):
    return asyncio.run(coro)


async def downloader(
    titles: list[str],
    title_folder_mapping: dict[str, tuple[IndexedSet, pathlib.Path]],
    headers: dict[str, str] | None = None,
) -> None:
    with ThreadPoolExecutor(max_workers=DEFAULT_THREADS_NUMBER) as executor:
        # Dictionary to hold Future objects
        futures_to_title = {}
        future_counter = 0
        coroutines = []
        for title in titles:
            images_set, folder_dest = title_folder_mapping[title]
            partial_download = partial(
                download_images,
                images_set=images_set,
                new_folder=folder_dest,
                headers=headers,
                title=title,
            )
            coroutines.append(partial_download())
            future_counter += 1

        # Handling futures as they complete
        for future in tqdm(
            executor.map(wrapper, coroutines),
            total=future_counter,
            desc=f"Retrieving {future_counter} tasks of downloading images",
        ):
            print(future)  # Get the result from the future object


async def download_images(
    images_set,
    new_folder: pathlib.Path,
    title: str,
    headers: dict[str, str] | None = None,
) -> str:
    """Download an image from a given URL and save it to the specified filename.

    Parameters
    ----------
    - image_url: The URL of the image to be downloaded.
    - filename: The filename to save the image to.

    """
    result = {}
    tqdm_iterable = tqdm(
        images_set,
        total=len(images_set),
        desc=f"Downloading images for {title} in {new_folder}",
    )
    should_convert_images = False

    for img_name, img_filename, image_url in tqdm_iterable:
        filename = new_folder / f"{img_filename}"
        should_convert_images = filename.suffix == ".webp"
        resp = await get_image_stream(image_url, headers=headers)

        with open(filename.as_posix(), "wb") as img_file:
            resp.raw.decode_content = True
            shutil.copyfileobj(resp.raw, img_file)
        tqdm_iterable.set_description(f"Saved image {filename}")

    if should_convert_images:
        await convert_from_webp_to_jpg(new_folder)

    result[title] = new_folder

    return "Done"


async def download_from_bunkr(
    links: list[str],
    headers: dict[str, str] | None = None,
) -> None:
    if headers is None:
        headers = headers_mapping["bunkr"]

    query = "div.grid-images div.grid-images_box div a.grid-images_box-link"

    for link in links:
        sources = set()
        soup = BeautifulSoup(requests.get(link, headers=headers).content)
        a_tags = soup.select(query)
        for a_tag in a_tags:
            sources.add(a_tag.attrs["href"])

        for source in sources:
            second_soup = BeautifulSoup(requests.get(source, headers=headers).content)
            video_source = second_soup.find("source")
            video_url = video_source.attrs["src"]
            filename = video_url.rsplit("/", 2)[-1]
            video_resp = requests.get(video_url, headers=headers, stream=True)
            with open(get_media_root() / filename, "wb") as file:
                for chunk in video_resp.iter_content(chunk_size=1024):
                    if chunk:
                        file.write(chunk)
                        file.flush()


async def telegraph_uploader(
    unique_img_urls: IndexedSet,
    page_title: str,
    posts_sent_counter: int = 0,
    telegraph_client: Telegraph | None = None,
    tqdm_iterable: tqdm | None = None,
    entity: str | None = "",
    send_to_telegram: bool | None = True,
) -> tuple[bool, list[str]]:
    was_successful = False

    if telegraph_client is None:
        telegraph_client = await get_new_telegraph_client()

    posts: list[str] = []
    html_post = await create_html_template(unique_img_urls, entity=entity)
    post_url = await create_page(
        title=page_title,
        html_content=html_post,
        telegraph_client=telegraph_client,
    )
    channels_sent: list[str] = [""]

    if not post_url:
        print(f"Failed to create post for {page_title}")
        was_successful, channels_sent = False, [""]
        return was_successful, channels_sent

    telegraph_post = f"{page_title} - {post_url}"
    posts.append(telegraph_post)

    if posts_sent_counter == 10:
        await asyncio.sleep(10)

    if send_to_telegram:
        try:
            was_successful, channels_sent = await send_message(
                post_text=telegraph_post,
                retry=True,
                posts_counter=posts_sent_counter,
                tqdm_iterable=tqdm_iterable,
                image_urls=set(unique_img_urls),
                entity=entity,
            )
        except Exception:
            await asyncio.sleep(20)
            was_successful, channels_sent = await send_message(
                post_text=telegraph_post,
                retry=True,
                posts_counter=posts_sent_counter,
                tqdm_iterable=tqdm_iterable,
                image_urls=set(unique_img_urls),
                entity=entity,
            )
    else:
        albums_dir = pathlib.Path.home() / ".albums_data"
        albums_dir.mkdir(parents=True, exist_ok=True)
        albums_file = albums_dir / "pages.txt"

        with albums_file.open("w") as f:
            _ = f.write("\n".join(posts))

        albums_links = albums_file.read_text().split("\n")
        await print_albums_message(albums_links)

    return was_successful, channels_sent


def sort_file(file: pathlib.Path) -> str:
    filename = file.name.split(".")[0]
    filename = filename.zfill(2)
    return filename


async def convert_from_webp_to_jpg(folder: pathlib.Path) -> None:
    files = list(folder.iterdir())
    tqdm_iterable = tqdm(
        files,
        total=len(files),
        desc="Converting images from WebP to JPEG",
        leave=False,
    )

    for file in tqdm_iterable:
        if file.suffix == ".webp":
            image = Image.open(file).convert("RGB")
            new_file = file.with_suffix(".jpg")
            image.save(new_file, "JPEG")
            file.unlink()


async def get_new_telegraph_client() -> Telegraph:
    telegraph_factory = Telegraph()
    resp = telegraph_factory.create_account(
        short_name=SHORT_NAME,
        author_name=AUTHOR_NAME,
        author_url=AUTHOR_URL,
        replace_token=True,
    )
    access_token = resp["access_token"]
    telegraph_client = Telegraph(access_token=access_token)
    return telegraph_client


async def upload_file(
    file: pathlib.Path,
    telegraph_client: Telegraph,
    try_again: bool | None = True,
) -> str | None:
    source = None
    try:
        uploaded = telegraph_client.upload_file(file)
    except (
        Exception,
        exceptions.TelegraphException,
        exceptions.RetryAfterError,
    ) as exc:
        error_message = str(exc)
        if "try again" in error_message.lower() or "retry" in error_message.lower():
            sleep(5)
            if try_again:
                telegraph_client = await get_new_telegraph_client()
                return await upload_file(file=file, telegraph_client=telegraph_client, try_again=False)
        uploaded = None

    if uploaded:
        source = uploaded[0]["src"]

    return source


async def create_page(
    title: str,
    html_content: str,
    telegraph_client: Telegraph,
    try_again: bool | None = True,
) -> str | None:
    source = None
    try:
        page = telegraph_client.create_page(
            title=title,
            html_content=html_content,
            author_name=AUTHOR_NAME,
            author_url=AUTHOR_URL,
        )
        source = page["url"]
    except (
        Exception,
        exceptions.TelegraphException,
        exceptions.RetryAfterError,
    ) as exc:
        error_message = str(exc)
        if "try again" in error_message.lower() or "retry" in error_message.lower():
            sleep(5)
            if try_again:
                telegraph_client = await get_new_telegraph_client()
                return await create_page(
                    title=title,
                    html_content=html_content,
                    telegraph_client=telegraph_client,
                    try_again=False,
                )

    return source


async def create_html_template(image_tags: IndexedSet, entity: str | None = "") -> str:
    if entity == "e-hentai.org":
        img_html_template = """<figure contenteditable="false"><img style="height:722px;width:1280px" src="{file_path}" data-original="{file_path}"><figcaption dir="auto" class="editable_text" data-placeholder="{title}"></figcaption></figure>"""
    else:
        img_html_template = """<figure contenteditable="false"><img src="{file_path}" data-original="{file_path}"><figcaption dir="auto" class="editable_text" data-placeholder="{title}"></figcaption></figure>"""

    video_html_template = (
        '<video src="{video_path}" preload="metadata" controls="controls" poster="{video_poster}" muted></video>'
    )

    template_tags: list[str] = []
    for title, poster, media_src in image_tags:
        if "mp4" in media_src:
            template_tags.append(video_html_template.format(title=title, video_path=media_src, video_poster=poster))
        else:
            template_tags.append(img_html_template.format(file_path=media_src, title=title))

    html_post = "\n".join(template_tags)
    return html_post


async def upload_to_telegraph(
    folder: pathlib.Path,
    telegraph_client: Telegraph,
    page_title: str | None = "",
    send_to_telegram: bool | None = False,
) -> str:
    files = sorted(list(folder.iterdir()), key=sort_file)
    title = page_title or folder.name
    title = title.strip().rstrip()

    contents = []
    files_urls = []
    html_template = """<figure contenteditable="false"><img src="{file_path}"><figcaption dir="auto" class="editable_text" data-placeholder="{title}"></figcaption></figure>"""

    uploaded_files_url_path = pathlib.Path(f"{snakecase(title)}.txt")
    if uploaded_files_url_path.exists() and uploaded_files_url_path.stat().st_size > 0:
        contents = uploaded_files_url_path.read_text().split("\n")
    else:
        iterable_files = tqdm(
            files,
            total=len(files),
            desc=f"Uploading files for {folder.name}",
            leave=False,
        )
        image_title = f"{title}"
        for file in iterable_files:
            file_url = await upload_file(file, telegraph_client=telegraph_client)
            if not file_url:
                continue
            files_urls.append(file_url)
            contents.append(html_template.format(file_path=file_url, title=image_title))

    if contents:
        content = "\n".join(contents)
        try:
            page_url = create_page(
                title=title,
                html_content=content,
                telegraph_client=telegraph_client,
            )
        except exceptions.TelegraphException as exc:
            return f"Error: {exc} - {title} - {folder}"

        post = f"{title} - {page_url}"

        if send_to_telegram:
            await send_message(post, image_urls=files_urls)

        pages_file = get_media_root() / "assets/pages.txt"

        if not pages_file.exists():
            pages_file.touch(exist_ok=True)

        with open(pages_file, "a") as f:
            f.write(f"{post}\n")

        return post

    return "No content, please try again later"


async def upload_folders_to_telegraph(
    folder_name: pathlib.Path | None,
    telegraph_client: Telegraph,
    limit: int | None = 0,
    send_to_channel: bool | None = False,
) -> None:
    folders = []

    if folder_name:
        root = get_media_root() / folder_name
        folders += [f for f in list(root.iterdir()) if f.is_dir()]
    else:
        root_folders = [folder for folder in get_media_root().iterdir() if folder.is_dir()]
        for folder in root_folders:
            if folder.is_dir():
                nested_folders = [f for f in folder.iterdir() if f.is_dir()]
                if nested_folders:
                    folders += nested_folders
                else:
                    folders = root_folders

    futures_to_folder = {}
    selected_folders = folders[:limit] if limit else folders
    with ThreadPoolExecutor(max_workers=DEFAULT_THREADS_NUMBER) as executor:
        future_counter = 0
        for folder in selected_folders:
            partial_upload = partial(
                upload_to_telegraph,
                folder,
                send_to_telegram=send_to_channel,
                telegraph_client=telegraph_client,
            )
            future = executor.submit(partial_upload)
            futures_to_folder[future] = folder
            future_counter += 1

        page_urls: list[tuple[str, str]] = []
        for future in tqdm(
            as_completed(futures_to_folder),
            total=future_counter,
            desc=f"Uploading {future_counter} albums to Telegraph...",
        ):
            result = future.result()
            page_urls.append(result)

        content = "\n".join([f"{page_url}" for page_url in page_urls])
        print(content)


async def get_pages_from_pagination(
    url: str,
    target: str,
    headers: dict[str, str] | None = None,
) -> list[str]:
    pagination_params = query_pagination_mapping[target]
    source_urls = set()
    soup = await get_soup(url, headers=headers)
    dom = etree.HTML(str(soup))
    pagination_set = soup.select(pagination_params.pages_count_query)

    if not pagination_set:
        for a_tag in dom.xpath(pagination_params.posts_query_xpath):
            if a_tag is not None and a_tag.attrib["href"] not in source_urls:
                source_urls.add(a_tag.attrib["href"])
        return list(source_urls)

    pagination = pagination_set[0]
    pagination_text = pagination.text
    if "Page" in pagination_text:
        first, last = pagination_text.split("Page")[-1].strip().split("of")
    else:
        first = pagination.get_text(strip=True)
        last_page = pagination_set[-1]
        last = last_page.get_text(strip=True)

    first_page, last_page = int(first), int(last)

    first_link_pagination = soup.select(pagination_params.pagination_base_url_query)[0]
    href = first_link_pagination.attrs["href"]
    base_pagination_url = href.rsplit("/", 2)[0]

    for a_tag in dom.xpath(pagination_params.posts_query_xpath):
        source_urls.add(a_tag.attrib["href"])

    for index in range(first_page, last_page + 1):
        if index == 1:
            continue

        target_url = f"{base_pagination_url}/{index}/"

        soup = await get_soup(target_url)
        dom = etree.HTML(str(soup))
        source_urls.update([a_tag.attrib["href"] for a_tag in dom.xpath(pagination_params.posts_query_xpath)])

    return list(source_urls)


async def print_albums_message(albums_links: list[str]) -> None:
    albums_message = ""

    for album in albums_links:
        albums_message += f"\t- {album}\n"

    message = "All albums have been downloaded and saved to the specified folder.\n"
    message += "Albums saved are the following:\n"
    message += f"{albums_message}"
    print(message)


async def split_every(chunk_size: int, iterable: Iterable[Any]) -> AsyncGenerator[list[Any], None]:
    """
    Iterate in chunks.
    It's better when you have a big one that can
    overload the db/API/CPU.
    """
    i = iter(iterable)
    piece = list(islice(i, chunk_size))

    while piece:
        yield piece
        piece = list(islice(i, chunk_size))


async def get_entity(sources: list[str]) -> str:
    parsed_url = parse.urlparse(sources[0])
    return parsed_url.netloc


async def build_unique_img_urls(
    image_tags: list[Tag],
    src_attr: str,
    secondary_src_attr: str = "",
    entity: str | None = "",
) -> IndexedSet:
    unique_img_urls = IndexedSet()
    for idx, img_tag in enumerate(image_tags):
        img_src = (
            img_tag.attrs.get(src_attr, "")
            .strip()
            .rstrip()
            .replace("\r", "")
            .replace("\n", "")
            .replace("_300px", "")
            .replace("_320px", "")
            .replace("/300px/", "/full/")
            .replace("_400px", "")
            .replace("_280.jpg", ".jpg")
            .replace("_s.jpg", ".jpg")
        )

        if not img_src or "gif" in img_src:
            img_src = img_tag.attrs.get(secondary_src_attr, "").strip().rstrip().replace("\r", "").replace("\n", "")
        if "https:" not in img_src:
            if entity and entity == "fapachi.com":
                img_src = f"https://fapachi.com{img_src}"
            else:
                img_src = f"https:{img_src}"

        image_alt = img_tag.attrs.get("alt", "")
        image_name_prefix = f"{idx + 1}".zfill(3)

        if image_alt:
            img_name = image_alt.strip().rstrip().replace("\r", "").replace("\n", "")
        else:
            img_name: str = img_src.split("/")[-1].split("?")[0]
            img_name = img_name.strip().rstrip().replace("\r", "").replace("\n", "")

        if "html" in img_src:
            continue

        img_filename = img_src.split("/")[-1]
        unique_img_urls.add((image_name_prefix, f"{image_name_prefix}-{img_name}", f"{img_filename}", img_src))

    ordered_unique_img_urls = IndexedSet(sorted(unique_img_urls, key=lambda x: list(x).pop(0)))
    ordered_unique_img_urls = IndexedSet([a[1:] for a in ordered_unique_img_urls])

    return ordered_unique_img_urls


async def build_unique_video_urls(
    video_tags: list[Tag],
    src_attr: str,
    secondary_src_attr: str = "",
) -> IndexedSet:
    unique_video_urls = IndexedSet()
    for idx, video_tag in enumerate(video_tags):
        if ".mp4" not in video_tag.attrs.get(src_attr, ""):
            source_tag = cast(Tag, video_tag.find("source"))
            video_src = source_tag.attrs.get(src_attr, "").strip().rstrip().replace("\r", "").replace("\n", "")
        else:
            video_src = video_tag.attrs.get(src_attr, "").strip().rstrip().replace("\r", "").replace("\n", "")

        video_poster = video_tag.attrs.get("poster", "")
        video_name_prefix = f"{idx + 1}".zfill(3)
        video_name: str = video_src.split("/")[-1].split("?")[0]
        video_name = video_name.strip().rstrip().replace("\r", "").replace("\n", "")

        unique_video_urls.add((video_name_prefix, f"{video_name_prefix}-{video_name}", video_poster, video_src))

    ordered_unique_video_urls = IndexedSet(sorted(unique_video_urls, key=lambda x: list(x).pop(0)))
    ordered_unique_video_urls = IndexedSet([a[1:] for a in ordered_unique_video_urls])

    return ordered_unique_video_urls


async def run_downloader(
    final_dest: pathlib.Path | str,
    page_title: str,
    unique_img_urls: IndexedSet,
    titles: IndexedSet,
    title_folder_mapping: dict[str, tuple[IndexedSet, pathlib.Path]],
    headers: dict[str, str] | None = None,
) -> None:
    await downloader(
        titles=list(titles),
        title_folder_mapping=title_folder_mapping,
        headers=headers,
    )


async def send_post_to_telegram(
    page_title: str,
    ordered_unique_img_urls: IndexedSet,
    posts_sent_counter: int,
    telegraph_client: Telegraph | None,
    tqdm_sources_iterable: tqdm,
    all_sources: list[str] | None,
    source_url: str,
    ordered_unique_video_urls: IndexedSet | None = None,
    entity: str | None = "",
    send_to_telegram: bool | None = True,
) -> list[str] | None:
    if not all_sources:
        all_sources = []

    total_imgs = len(ordered_unique_img_urls)
    videos_chunk_size = 0
    was_successful = False
    channels_sent: list[str] = []

    match total_imgs:
        case total_imgs if total_imgs in list(range(100, 150)):
            chunk_size = 60
        case total_imgs if total_imgs in list(range(150, 200)):
            chunk_size = 70
        case total_imgs if total_imgs in list(range(200, 250)):
            chunk_size = 75
        case total_imgs if total_imgs in list(range(250, 300)):
            chunk_size = 80
        case _:
            chunk_size = 90

    if len(ordered_unique_img_urls) >= MAX_IMAGES_PER_POST:
        async for chunk in split_every(chunk_size, ordered_unique_img_urls):
            _, _ = await telegraph_uploader(
                unique_img_urls=IndexedSet(chunk),
                page_title=page_title,
                posts_sent_counter=posts_sent_counter,
                telegraph_client=telegraph_client,
                tqdm_iterable=tqdm_sources_iterable,
                entity=entity,
                send_to_telegram=send_to_telegram,
            )
            posts_sent_counter += 1
    else:
        _, _ = await telegraph_uploader(
            unique_img_urls=IndexedSet(ordered_unique_img_urls),
            page_title=page_title,
            posts_sent_counter=posts_sent_counter,
            telegraph_client=telegraph_client,
            tqdm_iterable=tqdm_sources_iterable,
            entity=entity,
            send_to_telegram=send_to_telegram,
        )

    if ordered_unique_video_urls is not None:
        videos_chunk_size = 3
        async for chunk in split_every(videos_chunk_size, ordered_unique_video_urls):
            _, _ = await telegraph_uploader(
                unique_img_urls=IndexedSet(chunk),
                page_title=page_title,
                posts_sent_counter=posts_sent_counter,
                telegraph_client=telegraph_client,
                tqdm_iterable=tqdm_sources_iterable,
                entity=entity,
                send_to_telegram=send_to_telegram,
            )
            posts_sent_counter += 1

    return all_sources


async def upload_to_r2_and_post_to_telegram(
    folder: pathlib.Path,
) -> None:
    pass
