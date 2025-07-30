from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.service import Service
from selenium.webdriver.common.by import By


opts = Options()
opts.add_argument("--headless=new")
opts.add_argument("--no-sandbox")
opts.add_argument("--disable-dev-shm-usage")
opts.add_argument("--disable-client-side-phishing-detection")
opts.add_argument("--no-first-run")
opts.add_argument("--enable-automation")
opts.add_argument("--disable-gpu")
opts.add_argument("--silent")
opts.add_argument("--disable-logging")
opts.add_argument("--remote-debugging-port=9222")
opts.add_argument("--disable-infobars")
opts.add_argument("window-size=1080,1920")
# Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36
opts.add_argument("user-agent=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.140 Safari/537.36 Vivaldi/1.95.1077.55")

file_download_path = "/Users/patrick.mazulo/Dev/configs/dot-files/.media/grabber/files/"
profile = {
    "plugins.plugins_list": [{"enabled": True, "name": "Download All Images"}],
    "download.default_directory": file_download_path,
    "download.extensions_to_open": "",
    # "plugins.always_open_pdf_externally": True,
    "download.prompt_for_download": False,
    # "download.directory_upgrade": True,
    # "plugins.always_open_pdf_externally": True,
    "plugins.plugins_disabled": ["Chrome PDF Viewer"],
}
opts.add_experimental_option("prefs", profile)
opts.add_experimental_option("excludeSwitches", ["enable-automation"])
opts.add_experimental_option("useAutomationExtension", False)

# see: https://stackoverflow.com/questions/43470535/python-download-pdf-embedded-in-a-page/43471196#43471196
executable_path = "/Users/mazulo/Dev/packages/chromedriver/chromedriver"
chrome_executable: Service = ChromeService(executable_path=executable_path)
opts.binary_location = executable_path

try:
    driver = webdriver.Chrome(service=chrome_executable, options=opts)
    driver.capabilities.update({"se:downloadsEnabled": True})
except Exception as exc:
    if "(chrome not reachable)" in exc.msg:
        print("You forgot to start a google-chrome process")
        print(
            "Example: google-chrome --headless=new --disable-client-side-phishing-detection --no-first-run --enable-automation --no-sandbox --disable-dev-shm-usage --disable-gpu --silent --disable-logging --remote-debugging-port=9222 --window-size=1080,1920"
        )

# url = "https://sunset-guarantee-e1e.notion.site/58P-1140c88e9638808cba42c11b12d996e8?pvs=4"
# url = "https://www.nuyet.com/gallery/yuuhui-43271"
url = "https://www.nuyet.com/gallery/yuuhui-43427"
driver.get(url)

elem = driver.find_elements(By.TAG_NAME, "img")[7]
elem.screenshot("/home/mazulo/image.png")
