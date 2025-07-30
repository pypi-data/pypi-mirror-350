import requests
from bs4 import BeautifulSoup

from grabber.core.utils import headers_mapping


url = "https://bestgirlsexy.com/tag/Zzizzi/page/2/"
query = (
    "div.site.grid-container.container.hfeed"
    " > div.site-content"
    " > div.elementor"
    " > section.elementor-section.elementor-top-section"
    " > div"
    " > div"
    " > div div.elementor-posts-container.elementor-posts.elementor-posts--skin-cards.elementor-grid"
    " > article a.elementor-post__thumbnail__link"
)

headers = headers_mapping['bestgirlsexy']
soup = BeautifulSoup(requests.get(url, headers=headers).content, features="lxml")
links = soup.select(query)

links = []

for link in soup.select(query):
    attrs = link.attrs
    href = attrs["href"]
    links.append(href)

links = list(set(links))
print(" ".join(links))
