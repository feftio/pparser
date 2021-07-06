import typing as t
import asyncio
from pyppeteer.browser import Browser
from pyppeteer.launcher import launch
from pparser.utils import merge_options, run_async


def DEFAULT_BROWSER_SETTINGS(**options) -> t.Dict[str, t.Any]:
    return {
        'headless': True,
        'ignoreHTTPSErrors': False,
        'args': [
            '--window-size={},{}'.format(options.get('width', 1920),
                                         options.get('height', 1080))
        ],
        'width': options.get('width', 1920),
        'height': options.get('height', 1080)
    }


class PBrowser:
    def __init__(self, **options):
        self.options: t.Dict[t.Any, t.Any] = merge_options(
            DEFAULT_BROWSER_SETTINGS(**options),
            options)
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

    def get_content(self, url: str, waitable_selector: t.Optional[str] = None, timeout: int = 15000, sleep: float = 0.2):
        async def wrapper():
            page = await self.browser.newPage()
            await page.setViewport({
                'width': self.options['width'],
                'height': self.options['height'],
            })
            await page.goto(url, options={'timeout': timeout})
            if waitable_selector is not None:
                await page.waitForSelector(waitable_selector, options={'timeout': timeout})
            await asyncio.sleep(sleep)
            # await page.screenshot({'path': 'screenshot.png'})
            return await page.content()
        return run_async(wrapper())


if __name__ == '__main__':
    pbrowser = PBrowser()
    pbrowser.get_content('https://www.google.com')
