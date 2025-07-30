import asyncio
from grabber.core.utils import get_new_telegraph_client
from grabber.core.bot.core import send_message
from telegraph import TelegraphException, exceptions
from time import sleep


def upload_file(file, retry_count=5, telegraph=None):
    try:
        print(f"Trying to upload {file.name}")
        resp = telegraph.upload_file(file)
    except (TelegraphException, exceptions.RetryAfterError) as exc:
        print(f"Error trying to upload {file.name}: {exc}")
        if retry_count in [10, 15, 20, 25] or retry_count > 25:
            print("Creating new account for new token")
            account = telegraph.create_account(
                short_name=SHORT_NAME,
                author_name=AUTHOR_NAME,
                author_url=AUTHOR_URL,
                replace_token=True,
            )
            telegraph = Telegraph(access_token=account["access_token"])
        print(f"Sleeping {retry_count} before trying to upload again")
        sleep(retry_count)
        retry_count += 1
        resp = upload_file(file, retry_count=retry_count, telegraph=telegraph)
    if not resp:
        resp = upload_file(file, retry_count=retry_count, telegraph=telegraph)
    print(f"Uploaded {file.name}! URL: {resp[0]['src']}")
    file_resp = resp[0]
    return file_resp["src"]


def upload_files(files, retry_count=5, telegraph=None):
    urls = set()
    for file in files:
        urls.add(upload_file(file=file, retry_count=retry_count, telegraph=telegraph))
    return urls


def create_page(
    title: str,
    html_content: str,
    telegraph_client,
    try_again=True,
) -> str:
    try:
        page = telegraph_client.create_page(title=title, html_content=html_content)
    except (
        Exception,
        exceptions.TelegraphException,
        exceptions.RetryAfterError,
    ) as exc:
        error_message = str(exc)
        if "try again" in error_message.lower() or "retry" in error_message.lower():
            sleep(5)
            if try_again:
                telegraph_client = get_new_telegraph_client()
                return create_page(
                    title=title,
                    html_content=html_content,
                    telegraph_client=telegraph_client,
                    try_again=False,
                )
    return page["url"]


def create_new_page(title, urls, telegraph_client) -> str:
    html_template = """<figure contenteditable="false"><img src="{file_path}"><figcaption dir="auto" class="editable_text" data-placeholder="{title}"></figcaption></figure>"""
    contents = []

    for url in urls:
        contents.append(html_template.format(file_path=url, title=title))

    content = "\n".join(contents)
    page_url = create_page(
        title=title,
        html_content=content,
        telegraph_client=telegraph_client,
    )

    post = f"{title} - {page_url}"
    asyncio.run(send_message(post))

    return post



import pathlib
import shutil
from typing import Any
import asyncio
import multiprocessing
import pathlib
import shutil
from concurrent.futures import ThreadPoolExecutor
from functools import partial
from time import sleep
from typing import Any

import requests
from tenacity import retry, wait_chain, wait_fixed
from tqdm import tqdm
from boltons.setutils import IndexedSet

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

    for image_url in tqdm_iterable:
        img_filename = image_url.split("/")[-1]
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


images = set()
url = "https://leakxxx.com/api/v1/user/rintohsaka?page={page}&types[]=image&types[]=video&types[]=gallery&nsfw[]=0"

for page in tqdm(range(1, 30)):
    r = httpx.get(url.format(page=page))

    if r.status_code == 200:
        for post in r.json()["data"]["posts"]:
            image_url = post["data"]["url"]
            images.add(image_url)
    else:
        print(f"There was no response for page {page}")

print(len(images))
download_images(images, new_folder, title, headers=headers)
