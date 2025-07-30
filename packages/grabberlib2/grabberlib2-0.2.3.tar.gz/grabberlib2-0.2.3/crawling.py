import asyncio

from crawlee import Glob
from crawlee.beautifulsoup_crawler import BeautifulSoupCrawler, BeautifulSoupCrawlingContext
from crawlee.playwright_crawler import PlaywrightCrawler, PlaywrightCrawlingContext



async def nudecosplay() -> None:
    crawler = BeautifulSoupCrawler(
        # Limit the crawl to max requests. Remove or increase it for crawling all links.
        max_requests_per_crawl=2000,
    )

    # Define the default request handler, which will be called for every request.
    @crawler.router.default_handler
    async def request_handler(context: BeautifulSoupCrawlingContext) -> None:
        source = context.request.url
        context.log.info(f'Processing {source} ...')
        data = {
            'title': context.soup.find('title').get_text(strip=True),
            'url': context.request.url,
        }
        dataset = await crawler.get_dataset(name="nudecosplay_biz_run_1.biz")
        dataset_data = await dataset.get_data()

        if (
            data not in dataset_data.items
            and source != "https://nudecosplay.biz/category/ero-cosplay/"
            and source != "https://nudecosplay.biz/"
            and "https://nudecosplay.biz/page/" not in source
        ):
            await context.push_data(data, dataset_name="nudecosplay_biz_run_1.biz")

        # Enqueue all the documentation links found on the page, except for the examples.
        await context.enqueue_links(
            # include=[
            #     Glob('https://nudecosplay.biz/category/ero-cosplay/'),
            #     Glob('https://nudecosplay.biz/category/nude/'),
            # ],
            exclude=[
                Glob('https://nudecosplay.biz/tag/**'),
                Glob('https://nudecosplay.biz/category/**'),
                # Glob('https://nudecosplay.biz/page/**'),
                Glob('https://nudecosplay.biz/popular-this-month/**'),
                Glob('https://nudecosplay.biz/popular-this-week/**'),
                Glob('https://nudecosplay.biz/most-popular/**'),
                Glob('https://nudecosplay.biz/cdn-cgi/**'),
                Glob('https://nudecosplay.biz/author/**'),
                Glob('https://nudecosplay.biz/wp-content/**'),
            ],
        )

    # Run the crawler with the initial list of requests.
    # _ = await crawler.run(['https://nudecosplay.biz/category/ero-cosplay/'])
    _ = await crawler.run(['https://nudecosplay.biz/'])
    await crawler.export_data_json(
        dataset_name="nudecosplay_biz_run_1.biz",
        path='nudecosplay_biz_run_1.json',
        ensure_ascii=False,
        indent=4,
    )


async def everia() -> None:
    crawler = PlaywrightCrawler(
        # Limit the crawl to max requests. Remove or increase it for crawling all links.
        max_requests_per_crawl=200,
        # Headless mode, set to False to see the browser in action.
        headless=True,
        # Browser types supported by Playwright.
        browser_type='chromium',
    )

    # Define the default request handler, which will be called for every request.
    @crawler.router.default_handler
    async def request_handler(context: PlaywrightCrawlingContext) -> None:
        source = context.request.url
        context.log.info(f'Processing {source} ...')
        page_title = await context.page.title()

        if page_title:
            page_title = page_title.strip().split("- EVERIA")[0]
        else:
            context.log.warning('No page title found.')
            page_title = ''

        data = {
            'title': page_title,
            'url': source,
        }
        dataset = await crawler.get_dataset(name="everia_cosplay_run_1")
        dataset_data = await dataset.get_data()

        if (
            data not in dataset_data.items
            # and "cos" in source
            and source != "https://everia.club/"
            and "https://everia.club/category/" not in source
            and "https://everia.club/tag/" not in source
        ):
            await context.push_data(data, dataset_name="everia_cosplay_run_1")

        # next_pages = await context.page.query_selector_all("a.page-numbers")

        await context.enqueue_links(
            exclude=[
                Glob('https://everia.club/category/[!djawa]/**'),
                Glob('https://everia.club/tag/**'),
            ],
        )

        # if next_pages:
        #     await context.enqueue_links(
        #         exclude=[
        #             # Glob('https://everia.club/category/[!cosplay]/**'),
        #             Glob('https://everia.club/tag/**'),
        #         ],
        #         selector="a.page-numbers",
        #     )
        # else:
        #     await context.enqueue_links(
        #         exclude=[
        #             # Glob('https://everia.club/category/[!cosplay]/**'),
        #             Glob('https://everia.club/tag/**'),
        #         ],
        #     )

    # Run the crawler with the initial list of requests.
    # _ = await crawler.run(['https://everia.club/tag/djawa/'])
    _ = await crawler.run(['https://everia.club/category/cosplay/'])
    await crawler.export_data_json(
        dataset_name="everia_cosplay_run_1",
        path='everia_cosplay_run_1.json',
        ensure_ascii=False,
        indent=4,
    )
    await crawler.export_data_json(dataset_name="everia_cosplay_run_1", path='everia_cosplay_run_1.json')


if __name__ == '__main__':
    # asyncio.run(nudecosplay())
    asyncio.run(everia())
