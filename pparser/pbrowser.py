import typing as t
import asyncio
from pyppeteer.browser import Browser
from pyppeteer.launcher import launch
from pparser.utils import merge_dicts, run_async


def DEFAULT_BROWSER_OPTIONS(**options) -> t.Dict[str, t.Any]:
    DEFAULT_WIDTH = options.get('width', 1920)
    DEFAULT_HEIGHT = options.get('height', 1080)
    DEFAULT_DICT = {
        'headless': True,
        'ignoreHTTPSErrors': False,
        'args': [
            f'--window-size={DEFAULT_WIDTH},{DEFAULT_HEIGHT}'
        ],
        'width': DEFAULT_WIDTH,
        'height': DEFAULT_HEIGHT,
    }
    return merge_dicts(DEFAULT_DICT, options, expandable=True)


class PBrowser:
    def __init__(self, **options):
        self.options: t.Dict[t.Any, t.Any] = DEFAULT_BROWSER_OPTIONS(**options)
        self.browser: Browser = run_async(launch(options=self.options))

    def __call__(self, url: str) -> None:
        async def wrapper():
            page = await self.browser.newPage()
            await page.setViewport({
                'width': self.options['width'],
                'height': self.options['height'],
            })
            await page.goto(url)
            return page
        return run_async(wrapper())

    def get_content(self, url: str, **options):
        async def wrapper():
            page = await self.browser.newPage()
            await page.setViewport({
                'width': self.options['width'],
                'height': self.options['height'],
            })
            await page.goto(url, options={'timeout': options.get('timeout', 15000)})
            if options.get('waitable_selector', None) is not None:
                await page.waitForSelector(options['waitable_selector'], options={'timeout': options.get('timeout', 15000)})
            await asyncio.sleep(options.get('sleep', 0.2))
            # await page.screenshot({'path': 'screenshot.png'})
            return await page.content()
        return run_async(wrapper())
