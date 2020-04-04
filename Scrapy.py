#!/usr/bin/env python
# coding: utf-8

# # Extracting data from a website using xpath and scrapy and saving it in JSON format

# In[1]:


import scrapy
import logging


# In[2]:


from IPython.core.interactiveshell import InteractiveShell
InteractiveShell.ast_node_interactivity = "all"
# Show Python version
import platform
platform.python_version()


# In[3]:


try:
    import scrapy
except:
    get_ipython().system('pip install scrapy')
    import scrapy
from scrapy.crawler import CrawlerProcess


# In[4]:


import json


class JsonWriterPipeline(object):

    def open_spider(self, spider):
        self.file = open('Doctors1.jl', 'w')

    def close_spider(self, spider):
        self.file.close()

    def process_item(self, item, spider):
        line = json.dumps(dict(item)) + "\n"
        self.file.write(line)
        return item


# In[5]:



class QuotesSpider(scrapy.Spider):
    name = "quotes1"
    start_urls = [
        'http://www.burjeel.com/abu-dhabi/doctors/'
    ]
    custom_settings = {
        'LOG_LEVEL': logging.WARNING,
        'ITEM_PIPELINES': {'__main__.JsonWriterPipeline': 1}, # Used for pipeline 1
        'FEED_FORMAT':'json',                                 # Used for pipeline 2
        'FEED_URI': 'Doctors1.json'                        # Used for pipeline 2
    }
    
    def parse(self, response):
        doctors_name = response.xpath("/html/body/div[3]/div/div[4]/div/div/a[1]/h4/text()").extract()
        Position = response.xpath("/html/body/div[3]/div/div[4]/div/div/a[2]/h5/text()").extract()
        for (d,p) in zip(doctors_name, Position):
            scraped_info = {
                # key:value
                'Doctor': d,
                'Position': p}
            yield scraped_info


# In[6]:


process = CrawlerProcess({
    'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)'
})

process.crawl(QuotesSpider)
process.start()


# In[7]:


import pandas as pd
dfjson = pd.read_json('Doctors1.json')
dfjson

