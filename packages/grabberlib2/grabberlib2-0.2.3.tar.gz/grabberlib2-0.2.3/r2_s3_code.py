# import asyncio
import os
# import time
import urllib.parse
from pathlib import Path

from boltons.setutils import IndexedSet
import boto3
from botocore.client import Config
# from selenium import webdriver
# from selenium.webdriver.chrome.service import Service as ChromeService
# from selenium.webdriver.chrome.options import Options
# from selenium.webdriver.common.service import Service
# from selenium.webdriver.common.by import By
from tenacity import retry, wait_chain, wait_fixed, stop_after_attempt
from tqdm import tqdm

from grabber.core.bot.core import send_message
from grabber.core.utils import create_page, create_html_template, get_new_telegraph_client, send_post_to_telegram


ACCOUNT_ID = os.environ.get('R2_ACCOUNT_ID')
ACCESS_KEY_ID = os.environ.get('R2_ACCESS_KEY_ID')
SECRET_ACCESS_KEY = os.environ.get('R2_SECRET_ACCESS_KEY')
BUCKET_NAME = os.environ.get('R2_BUCKET_NAME')
CHROME_DRIVER_PATH_MAC = os.environ.get('CHROME_DRIVER_PATH_MAC', "/Users/mazulo/Dev/packages/chromedriver/chromedriver")
CHILD_BUCKET = "images/albums/"
CLOUDFLARE_PUBLIC_URL = "https://pub-2ec00c15cd954e83ae63a4e12548784c.r2.dev/"

s3 = boto3.resource("s3",
    endpoint_url=f'https://{ACCOUNT_ID}.r2.cloudflarestorage.com',
    aws_access_key_id=ACCESS_KEY_ID,
    aws_secret_access_key=SECRET_ACCESS_KEY,
    config=Config(signature_version='s3v4')
)
# s3_client.list_objects(Bucket="assets")
s3_bucket = s3.Bucket(BUCKET_NAME)


# opts = Options()
# opts.add_argument("--headless=new")
# opts.add_argument("--no-sandbox")
# opts.add_argument("--disable-dev-shm-usage")
# opts.add_argument("--disable-client-side-phishing-detection")
# opts.add_argument("--no-first-run")
# opts.add_argument("--enable-automation")
# opts.add_argument("--disable-gpu")
# opts.add_argument("--silent")
# opts.add_argument("--disable-logging")
# opts.add_argument("--remote-debugging-port=9222")
# opts.add_argument("--disable-infobars")
# opts.add_argument('--window-size=1920,1080')
#
# file_download_path = Path("/Users/patrick.mazulo/Dev/configs/dot-files/.media/grabber/media/")
# profile = {
#     "plugins.plugins_list": [{"enabled": True, "name": "Download All Images"}],
#     "download.default_directory": file_download_path.as_posix(),
#     "download.extensions_to_open": "",
#     "download.prompt_for_download": False,
#     "plugins.plugins_disabled": ["Chrome PDF Viewer"],
# }
# opts.add_experimental_option("prefs", profile)
# opts.add_experimental_option("excludeSwitches", ["enable-automation"])
# opts.add_experimental_option("useAutomationExtension", False)
#
# executable_path = CHROME_DRIVER_PATH_MAC
# chrome_executable: Service = ChromeService(executable_path=executable_path)
# opts.binary_location = executable_path
#
# driver = webdriver.Chrome(service=chrome_executable, options=opts)
# driver.capabilities.update({"se:downloadsEnabled": True})
# driver.set_window_size(1920, 1080)
#
# urls = [
#     "https://sunset-guarantee-e1e.notion.site/104-29P4V-1020c88e963880dd8e5cead95059b116?pvs=4",
#     "https://sunset-guarantee-e1e.notion.site/37-100P-11a0c88e9638805a80e0fa16081dcfe6?pvs=4",
#     "https://sunset-guarantee-e1e.notion.site/38-50P-1170c88e963880558a3ce8fc6389a401?pvs=4",
#     "https://sunset-guarantee-e1e.notion.site/36-100P-1170c88e96388070ad64f3398e399e35?pvs=4",
#     "https://sunset-guarantee-e1e.notion.site/35-100P-1170c88e96388077ba0cdf5cf2135bdf?pvs=4",
# ]


@retry(
    wait=wait_chain(
        *[wait_fixed(1) for _ in range(5)]
        + [wait_fixed(1.5) for _ in range(4)]
        + [wait_fixed(2) for _ in range(3)]
        + [wait_fixed(2.5)],
    ),
    reraise=False,
    stop=stop_after_attempt(10)
)
def screenshot_element(driver, elem, file_path):
    driver.set_window_size(1920, 1080)
    result = elem.screenshot(file_path.as_posix())
    return result


# for url in urls:
#     print("created webdriver and will now request the page")
#     driver.get(url)
#     time.sleep(2)
#
#     downloaded_files = []
#     for idx, elem in enumerate(driver.find_elements(By.TAG_NAME, "img")):
#         index = f"{idx + 1}".zfill(2)
#         file_path = file_download_path / f"image-{index}.png"
#         print(f"Downloading {file_path}...")
#         result = screenshot_element(driver, elem, file_path)
#
#         if not result:
#             print(f"Failed to download {file_path}")
#         else:
#             print(f"Downloaded {file_path}")
#             downloaded_files.append(file_path)

    #
    # album_title = driver.title
    # album_key = f"{CHILD_BUCKET}{album_title}"

# cleaned_file_paths = []
#
# print(f"Uploading files to {album_key}...")
# for file_path in tqdm(downloaded_files, total=len(downloaded_files)):
#     filename = file_path.name
#     cleaned_filename = urllib.parse.quote(filename, safe="~()*!.'")
#     cleaned_file_paths.append((cleaned_filename, f"{album_key}/{cleaned_filename}"))
#     file_key = f"{album_key}/{filename}"
#     s3_bucket.upload_file(file_path.as_posix(), file_key)


async def run(path: str, page_title: str = "") -> None:
    image_urls = IndexedSet()

    root = Path(path)

    album_title = root.name
    album_key = f"{CHILD_BUCKET}{album_title}"
    cleaned_file_paths = []
    files = sorted(list(root.iterdir()))

    print(f"Uploading files to {album_key}...")
    for file_path in tqdm(files, total=len(files)):
        filename = file_path.name
        cleaned_filename = urllib.parse.quote(filename, safe="~()*!.'")
        cleaned_file_paths.append((cleaned_filename, f"{album_key}/{cleaned_filename}"))
        file_key = f"{album_key}/{filename}"
        s3_bucket.upload_file(file_path.as_posix(), file_key)

    print("Creating image URLs...")
    for fliename, cleaned_file_path in cleaned_file_paths:
        image_url = f"{CLOUDFLARE_PUBLIC_URL}{cleaned_file_path}"
        image_urls.add((filename, image_url))


    _ = await send_post_to_telegram(
        page_title=page_title or album_title,
        ordered_unique_img_urls=image_urls,
        telegraph_client=await get_new_telegraph_client(),
        posts_sent_counter=0,
        tqdm_sources_iterable=tqdm(image_urls),
        all_sources=[""],
        source_url="",
        entity="custom",
    )

    # print("Creating HTML template...")
    # html_content = await create_html_template(image_urls)
    # page_url = await create_page(
    #     title=album_title,
    #     html_content=html_content,
    #     telegraph_client=await get_new_telegraph_client(),
    # )
    # print(page_url)
    # post = f"{album_title} - {page_url}"
    # await send_message(post, channel="@fapello0000")
