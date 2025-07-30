#! /usr/bin/env python3
#
# Copyright (C) 2025 Darron Broad
# All rights reserved.
#
# This file is part of cps_sget.
#
# cps_sget is free software: you can redistribute it and/or
# modify it under the terms of the GNU General Public License as published
# by the Free Software Foundation.
#
# cps_sget is distributed in the hope that it will be
# useful, but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General
# Public License for more details.
#
# You should have received a copy of the GNU General Public License along
# with cps_sget. If not, see http://www.gnu.org/licenses/
#
import argparse
import os
import tempfile

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

from bs4 import BeautifulSoup

from time import sleep

# akamaitechnologies hangs unless it recognises the User-Agent
USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:134.0) Gecko/20100101 Firefox/134."

def main():
    parser = argparse.ArgumentParser()

    parser.add_argument("-d", "--delay", type=int, help="Post GET delay in seconds (default:0)")
    parser.add_argument("-b", "--by", type=str, help="By type to wait for (default:ID)")
    parser.add_argument("-v", "--value", type=str, help="By value to wait for (default:None)")
    parser.add_argument("-n", "--nostrip", action="store_true", help="Do not strip JavaScript/CSS/Link")
    parser.add_argument("-s", "--scroll", action="store_true", help="Scroll page")
    parser.add_argument("url", type=str, help="url")
    parser.add_argument("file", type=str, help="file")

    args = parser.parse_args()

    tmpdir = tempfile.TemporaryDirectory(prefix="cps_sget.tmp.")
    os.environ["TMPDIR"] = tmpdir.name

    html = scrape(args.url, args.delay, args.by, args.value, args.nostrip, args.scroll)

    print(f"\nFILE = {args.file}")

    with open(args.file, "w", encoding="utf-8") as f:
        f.write(html)

    tmpdir.cleanup()

def scrape(url, delay, by, value, nostrip, scroll):
    print(f"\nURL = {url}")

    ##################################################################
    # Chrome driver options
    #
    options = Options()
    options.add_argument("--incognito")
    options.add_argument("--headless")
    options.add_argument(f"user-agent={USER_AGENT}")
    # Do not load images
    prefs = { "profile.managed_default_content_settings.images": 2 }
    options.add_experimental_option("prefs", prefs)

    ##################################################################
    # Get URL
    #
    driver = webdriver.Chrome(options=options)
    driver.implicitly_wait(60)
    driver.get(url)

    if by and not value:
        raise Exception("Value missing")

    if not by and value:
        by = "ID"

    if by:
        match by.upper():
            case "ID":
                driver.find_element(By.ID, value)
            case "NAME":
                driver.find_element(By.NAME, value)
            case "XPATH":
                driver.find_element(By.XPATH, value)
            case "CSS_SELECTOR":
                driver.find_element(By.CSS_SELECTOR, value)
            case "CLASS_NAME":
                driver.find_element(By.CLASS_NAME, value)
            case "TAG_NAME":
                driver.find_element(By.TAG_NAME, value)
            case "LINK_TEXT":
                driver.find_element(By.LINK_TEXT, value)
            case "PARTIAL_LINK_TEXT":
                driver.find_element(By.PARTIAL_LINK_TEXT, value)
            case _:
                raise Exception("By unknown")

    while scroll:
        old_height = driver.execute_script("return document.body.scrollHeight;")
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        new_height = driver.execute_script("return document.body.scrollHeight;")
        scroll = new_height != old_height

    if delay:
        sleep(int(delay)) # Post GET delay

    page_source = driver.execute_script("return document.documentElement.outerHTML;")

    driver.quit()

    ##################################################################
    # Extract HTML
    #
    soup = BeautifulSoup(page_source, "html.parser")

    ##################################################################
    # Tidy HTML
    #
    if nostrip == False:
        for noscript in soup("noscript"):
            noscript.decompose()

        for script in soup("script"):
            script.decompose()

        for style in soup("style"):
            style.decompose()

        for link in soup("link"):
            link.decompose()

        for link in soup("meta"):
            link.decompose()

    return soup.prettify()

if __name__=="__main__":
    main()

# vim: shiftwidth=4 tabstop=4 softtabstop=4 expandtab
