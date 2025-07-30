# HTML画像化 [html2img]
# 【動作確認 / 使用例】

import sys
import ezpip
html2img = ezpip.load_develop("html2img", "../", develop_flag = True)

html = '<span style="color:gray;">Hello,</span><br>World!'
html2img(html, "result.png", viewport = (100, 100))
