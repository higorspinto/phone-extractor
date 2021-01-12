import sys
import scrapy
import logging

from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings

import phone_extractor.phone_extractor.settings as custom_settings
from phone_extractor.phone_extractor.spiders.main_spider import MainSpider

if __name__ == "__main__":

  url_list = []
  for line in sys.stdin:
    line_stripped = line.strip()
    url_list.append(line_stripped)

  if sys.argv:
    dir_path = sys.argv[0]

  crawler_settings = Settings()
  crawler_settings.setmodule(custom_settings)

  process = CrawlerProcess(settings=crawler_settings)
  process.crawl(MainSpider, url_lst=url_list)
  process.start()