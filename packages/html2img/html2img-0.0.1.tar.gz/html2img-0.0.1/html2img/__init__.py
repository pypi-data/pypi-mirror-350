# HTML画像化 [html2img]

import sys
from playwright.sync_api import sync_playwright

# HTML画像化 [html2img]
def html2img(html, output_path = "output.png", viewport = (800, 600)):
	with sync_playwright() as p:
		browser = p.chromium.launch()
		page = browser.new_page(viewport = {'width': viewport[0], 'height': viewport[1]})
		page.set_content(html)
		page.screenshot(path = output_path)
		browser.close()

# モジュールと関数の同一視
sys.modules[__name__] = html2img
