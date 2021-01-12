import scrapy
import re
import json

from urllib.parse import urljoin, urlparse

class MainSpider(scrapy.Spider):
    
    name = "main"

    def __init__(self, url_lst=None):
        self.url_lst = url_lst  # source file name

    def start_requests(self):                
        for url in self.url_lst:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        # parse page title
        title = response.xpath('//title/text()').get()
        html_text = response.text

        # parse logo
        logo_url = self.parse_logo(response)

        #parse phone numbers
        phone_regex = re.compile(r"(\+?\d?\d?[ ]?\(?\d{2,3}\)?[ .-]?\d{2,5}[ .-]?\d{2,5}[ .-]?\d{2,3})")
        phone_list = re.findall(phone_regex, html_text)

        # light cleaning the phones
        phone_list_cleaned = []
        for phone in phone_list:
            phone_list_cleaned.append(self.phone_light_cleaning(phone))

        contact = {}
        contact['title'] = title
        contact['phones'] = phone_list_cleaned
        contact['logo_url'] = logo_url

        yield contact

    def parse_logo(self, response):
        '''
        it looks for every link (<a> tag) that contains an image (<img>tag)
        check if those links contain any pattern equals to 'logo'
        then returns the first match
        '''

        logo_url = ""
        for tag_a in response.xpath('//a'):
            for tag_img in tag_a.xpath('.//img'):
                img_url = tag_img.xpath('@src').extract()
                if len(img_url) > 0: 
                    img_url_str = str(img_url[0])
                    ind = img_url_str.find('logo')
                    if ind > 0:
                        base_url = response.url
                        relative_url = img_url_str
                        logo_url = urljoin(base_url, relative_url)

        return logo_url

    def phone_light_cleaning(self, phone):
        '''
        replace any characters that are not digits, 
        a plus sign (+) or parentheses with whitespace
        '''
        filtered_str = ''
        allowed_chars = ['0','1','2','3','4','5','6','7','8','9','(',')','+']
        for char in phone:
            if char in allowed_chars:
                filtered_str += char
            else:
                filtered_str += ' '

        return filtered_str
