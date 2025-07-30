# -*- coding: utf-8 -*-
import time
import os,sys

from pdb        import set_trace  as strace

from selenium import webdriver
from selenium.webdriver.common.keys import Keys

from common import util

def url_to_img(url, output):
    util.log(url, output)

    option = webdriver.ChromeOptions()
    option.add_argument('--headless')
    option.add_argument('--disable-gpu')
    option.add_argument("--window-size=1920,1080")
    option.add_argument("--hide-scrollbars")
    option.add_argument('--no-sandbox')
    option.add_argument('--lang=zh-CN')
    option.add_argument('--disable-web-security')
    option.add_argument('--disable-dev-shm-usage')
    option.add_argument('--blink-settings=imagesEnabled=true')

    driver = webdriver.Chrome(options=option)
    # driver.set_page_load_timeout(10)

    driver.get(url)
    util.log(output)

    scroll_width = driver.execute_script('return document.body.parentNode.scrollWidth')
    scroll_height = driver.execute_script('return document.body.parentNode.scrollHeight')

    driver.set_window_size(scroll_width, scroll_height)
    # strace()
    driver.save_screenshot(output)
    driver.quit()
    return True

def argv_parse():
    import argparse
    import datetime
    parser = argparse.ArgumentParser(
        prog=sys.argv[0],
        description="url转图片"
    )
    parser.add_argument(
        '--url',
        action='store',
        type=str,
        default='https://www.bing.com',
        help='网址必须带协议头，如：https://www.bing.com'
    )
    parser.add_argument(
        '-o', '--output',
        action='store',
        type=str,
        default='test.png',
        help='输出文件名，如： test.png'
    )

    return parser.parse_args()

def main():
    option = argv_parse()
    assert option.url.startswith("http") or option.url.startswith("file"),f"url必须带协议头：{option.url}"
    assert option.output.endswith(".png") ,f"输出只支持png格式"
    url_to_img(option.url, option.output)

if __name__ == '__main__':
    main()