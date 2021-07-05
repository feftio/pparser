from pparser.utils import merge_settings
import typing as t
import asyncio
from pyppeteer.browser import Browser
from pyppeteer.launcher import launch
from pparser.utils import merge_settings, run_async


DEFAULT_BROWSER_SETTINGS = {
    'headless': True,
    'ignoreHTTPSErrors': False,
    'args': [

    ]
    # SIZE_TEMPLATE
}


def SIZE_TEMPLATE(width: int, height: int) -> t.Dict[t.Any, t.Any]:
    return {
        'args': [
            f'--window-size={width},{height}'
        ],
        'width': width,
        'height': height
    }


def prepare_settings(settings: t.Dict[t.Any, t.Any], width: int, height: int):
    return merge_settings(DEFAULT_BROWSER_SETTINGS, SIZE_TEMPLATE(width, height))


class PBrowser:
    def __init__(self, **settings):
        self.settings: t.Dict[t.Any, t.Any] = merge_settings(
            prepare_settings(DEFAULT_BROWSER_SETTINGS, settings.get('width', 1920), settings.get('height', 1080)), settings)
        self.browser: Browser = run_async(launch(options=self.settings))

    async def get_content(self, url: str, waitable_selector: t.Optional[str] = None, timeout: int = 4000, sleep: float = 0.2):
        page = await self.browser.newPage()
        await page.setViewport({
            'width': self.settings['width'],
            'height': self.settings['height'],
        })
        await page.goto(url, options={'timeout': timeout})
        if waitable_selector is not None:
            await page.waitForSelector(waitable_selector)
        await asyncio.sleep(sleep)
        await page.screenshot({'path': 'screenshot.png'})
        return await page.content()


if __name__ == '__main__':
    pbrowser = PBrowser(headless=False)
    print(pbrowser.settings)
