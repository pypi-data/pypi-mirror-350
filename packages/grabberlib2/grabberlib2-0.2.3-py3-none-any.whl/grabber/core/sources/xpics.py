import asyncio
import multiprocessing
import pathlib
import shutil
from concurrent.futures import ThreadPoolExecutor
from functools import partial
from typing import Any, cast

import httpx
import requests
from boltons.setutils import IndexedSet
from bs4 import BeautifulSoup, Tag
from telegraph import Telegraph
from tenacity import retry, wait_chain, wait_fixed
from tqdm import tqdm
from unidecode import unidecode

from grabber.core.utils import headers_mapping, send_post_to_telegram

DEFAULT_THREADS_NUMBER = multiprocessing.cpu_count()


def wrapper(coro):
    return asyncio.run(coro)


headers = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36",
}


@retry(
    wait=wait_chain(
        *[wait_fixed(3) for _ in range(5)]
        + [wait_fixed(7) for _ in range(4)]
        + [wait_fixed(9) for _ in range(3)]
        + [wait_fixed(15)],
    ),
    reraise=True,
)
def get_image_stream(
    url,
    headers: dict[str, Any] = None,
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


def download_images(
    images_set,
    new_folder: pathlib.Path,
    title: str,
    headers: dict[str, str] = None,
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
    folder_files = list(new_folder.iterdir())

    for _, img_filename, image_url in tqdm_iterable:
        filename = new_folder / f"{img_filename}"
        if filename not in folder_files:
            resp = get_image_stream(image_url, headers=headers)

            with open(filename.as_posix(), "wb") as img_file:
                resp.raw.decode_content = True
                shutil.copyfileobj(resp.raw, img_file)
            tqdm_iterable.set_description(f"Saved image {filename}")

    result[title] = new_folder

    return "Done"


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


async def get_all_images_for_url(url: str, headers: dict[str, str]) -> IndexedSet:
    images = IndexedSet()
    model_name = url.split("@")[-1]
    base_url = (
        "https://www.xpics.me/api/v1/user/{model_name}?page={page}&types[]=image&types[]=video&types[]=gallery&nsfw[]=0"
    )

    counter = 1
    for page in tqdm(range(1, 100)):
        r = httpx.get(base_url.format(model_name=model_name, page=page), headers=headers)

        if r.status_code == 200:
            response_data: dict[Any, Any] = r.json()
            if len(response_data["data"]["posts"]) <= 1:
                for post in response_data["data"]["posts"]:
                    permalink: str = post["permalink"]
                    img_filename = permalink.split("/")[-1].strip().rstrip()
                    image_name_prefix = f"{counter}".zfill(3)
                    image_url: str = post["data"]["url"]
                    images.add(
                        (
                            image_name_prefix,
                            f"{image_name_prefix}-{img_filename}",
                            image_url,
                        )
                    )
                    counter += 1
                break
            for post in response_data["data"]["posts"]:
                permalink: str = post["permalink"]
                img_filename = permalink.split("/")[-1].strip().rstrip()
                image_name_prefix = f"{counter}".zfill(3)
                image_url: str = post["data"]["url"]
                images.add(
                    (
                        image_name_prefix,
                        f"{image_name_prefix}-{img_filename}",
                        f"{img_filename}",
                        image_url,
                    )
                )
                counter += 1
        else:
            print(f"There was no response for page {page}")

    print(len(images))
    return images


async def get_sources_for_xpics(
    sources: list[str],
    entity: str,
    telegraph_client: Telegraph | None = None,
    final_dest: str | pathlib.Path = "",
    save_to_telegraph: bool | None = False,
    **kwargs: Any,
) -> None:
    tqdm_sources_iterable = tqdm(
        sources,
        total=len(sources),
        desc="Retrieving URLs...",
    )
    headers = headers_mapping[entity]
    page_title = ""
    title_folder_mapping = {}
    posts_sent_counter = 0
    titles = IndexedSet()
    ordered_unique_img_urls = None
    all_sources: list[str] = []
    original_folder_path = final_dest

    for source_url in tqdm_sources_iterable:
        final_dest = pathlib.Path(str(original_folder_path)) if final_dest else ""

        response = httpx.get(
            source_url,
            headers=headers,
            follow_redirects=True,
        )
        soup = BeautifulSoup(response.content)

        page_title = cast(Tag, soup.find("title")).get_text(strip=True).strip().rstrip()
        page_title = page_title.split("- Fapello")[0].split("Nude")[0].replace("https:", "")
        page_title = unidecode(
            " ".join(
                f"#{part.strip().replace(' ', '').replace('.', '_').replace('-', '_')}"
                for part in page_title.split("/")
            )
        )
        titles.add(page_title)

        image_urls = await get_all_images_for_url(source_url, headers)
        ordered_unique_img_urls = IndexedSet(sorted(image_urls, key=lambda x: list(x).pop(0)))
        ordered_unique_img_urls = IndexedSet(a[1:] for a in ordered_unique_img_urls)

        tqdm_sources_iterable.set_description(f"Finished retrieving images for {page_title}")

        if final_dest:
            final_dest = pathlib.Path(final_dest) / unidecode(f"{page_title} - {entity}")
            if not final_dest.exists():
                final_dest.mkdir(parents=True, exist_ok=True)

            title_folder_mapping[page_title] = (ordered_unique_img_urls, final_dest)

        if save_to_telegraph:
            _ = await send_post_to_telegram(
                ordered_unique_img_urls=ordered_unique_img_urls,
                page_title=page_title,
                telegraph_client=telegraph_client,
                posts_sent_counter=posts_sent_counter,
                tqdm_sources_iterable=tqdm_sources_iterable,
                all_sources=all_sources,
                source_url=source_url,
                entity=entity,
            )
            page_title = ""

    if final_dest and ordered_unique_img_urls:
        await downloader(
            titles=list(titles),
            title_folder_mapping=title_folder_mapping,
            headers=headers,
        )
