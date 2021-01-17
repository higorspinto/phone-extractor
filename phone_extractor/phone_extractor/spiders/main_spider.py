import scrapy
import re
import json

from urllib.parse import urljoin, urlparse

class MainSpider(scrapy.Spider):
    
    name = "main"

    def __init__(self, url_lst=None):
        self.url_lst = url_lst

    def start_requests(self):                
        for url in self.url_lst:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        website = response.url

        # parse page title
        title = response.xpath('//title/text()').get()
        html_text = response.text

        # parse logo
        logo_url = self.parse_logo(response)

        #parse phone numbers - using different regex for different formats
        phone_regex = re.compile(r"(^\d{3}[-\.\s]\d{3}[-\.\s]\d{4}" + 
                r"|\(\d{3}\)\s*\d{3}[-\.\s]??\d{4}" + 
                r"|^\d{3}[-\.\s]\d{4}[-\.\s]\d{4,5}" + 
                r"|^\d{3}[-\.\s]\d{4,7}" + 
                r"|\d{2}[-\.\s]\d{5}[-\.\s]\d{4}" +
                r"|\(\d{2}\)\d{5}[-\.\s]\d{4}" +
                r"|\+\d{1,3}[-\.\s]\(\d{3}\)[-\.\s]\d{3}[-\.\s]\d{2,3}[-\.\s]\d{2,3}" +
                r"|\+\d{2,3}[-\.\s]\(?\d{2,3}\)?[-\.\s]\d{4,5}[-\.\s]\d{4}" + 
                r"|\+\d{1,2}[-\.\s]\(?\d{2,3}\)[-\.\s]\d{3}[-\.\s]\d{4}" +
                r"|^\d{1}[-\.\s]\d{4}[-\.\s]\d{4}" + 
                r"|\+\d{1,2}[-\.\s]\d{1}[-\.\s]\d{4}[-\.\s]\d{4}" +
                r"|\d{4}[ ]\d{6}|^\d{4}[-\.\s]\d{3}[-\.\s]\d{3}" +
                r"|\(\d{2,3}\)[-\.\s]\d{4,5}[-\.\s]\d{4,5}" +
                r"|^\+\d{2,3}[-\.\s]\d{2,3}[-\.\s]\d{2,3}[-\.\s]\d{2,5}" +
                r"|\(\d{3}\)[-\.\s][-\.\s\/]?[-\.\s]\d{3}[-\.\s]\d{5}" +
                r"|\d{2,3}[-\.\s]\d{4}[-\.\s]\d{4}" +
                r"|\d{4}[-\.\s]\d{3}[-\.\s]\d{3}" +
                r"|\+\d{1,3}[-\.\s]\d{3}[-\.\s]\d{3}[-\.\s]\d{4}" +
                r"|\+\d{2,3}[-\.\s]\(\d{2,3}\)[-\.\s]\d{3,4}[-\.\s]\d{3,4}" +
                r"|\d{2,3}[-\.\s][\/][-\.\s]\d{3,4}[-\.\s]\d{5})")
        phone_list = re.findall(phone_regex, html_text)

        # light cleaning the phones
        phone_list_cleaned = []
        for phone in phone_list:
            phone_list_cleaned.append(self.phone_light_cleaning(phone))

        # remove duplicates
        phone_contact_list = []
        for phone in phone_list_cleaned:
            if phone not in phone_contact_list:
                phone_contact_list.append(phone)

        contact = {}
        contact['website'] = website
        contact['phones'] = phone_contact_list
        contact['logo_url'] = logo_url

        yield contact

    def parse_logo(self, response):
        '''
        it looks for every link (<a> tag) that contains an image (<img>tag)
        check if the links or class names contain any pattern equals to 'logo'
        (case insensitive) then returns all the matches
        '''

        logos = []

        ### find logo by image url
        for tag_a in response.xpath('//a'):
            for tag_img in tag_a.xpath('.//img'):
                img_url = tag_img.xpath('@src').extract()
                if len(img_url) > 0: 
                    img_url_str = str(img_url[0])
                    lower_case = img_url_str.lower()
                    ind = lower_case.find('logo')
                    if ind > 0:
                        base_url = response.url
                        relative_url = img_url_str
                        logo_url = urljoin(base_url, relative_url)
                        logos.append(logo_url)

        ### find logo by class name
        for img in response.css('img'):
            img_classes = img.xpath('@class')
            img_src = img.xpath('@src').get()

            for img_class in img_classes.getall():
                lower_case = img_class.lower()
                ind = lower_case.find('logo')
                if ind > 0:
                    base_url = response.url
                    relative_url = img_src
                    logo_url = urljoin(base_url, relative_url)
                    logos.append(logo_url)

        # remove duplicated logos
        unique_logos = []
        for logo in logos:
            if logo not in unique_logos:
                unique_logos.append(logo)

        return unique_logos

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
