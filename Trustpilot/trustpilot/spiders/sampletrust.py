import re
import json
import scrapy 
import datetime
from parsel import Selector
class trustpilot(scrapy.Spider):
    name='sampletrustcom'
    headers = {
            'authority': 'www.trustpilot.com',
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'accept-language': 'en-US,en;q=0.9',
            'cache-control': 'max-age=0',
            # 'cookie': 'TP.uuid=cc5115ed-f5cd-4a8f-b86c-a40476e6c5ea; ajs_anonymous_id=4bc89c09-acb7-4cd6-88e9-021e7493356a; _gcl_au=1.1.1326722567.1684235633; _ga=GA1.1.5349968.1684235633; _tt_enable_cookie=1; _ttp=uFdJvg87NMGTxcojg9IH_QPghkZ; OptanonAlertBoxClosed=2023-05-16T11:13:55.305Z; _hjSessionUser_391767=eyJpZCI6IjA4YmY0YTdiLThmNGYtNWMxNi05NjU5LTcyYjQ5ODEwMjBkMiIsImNyZWF0ZWQiOjE2ODQyMzU2MzIyMDMsImV4aXN0aW5nIjp0cnVlfQ==; g_state={"i_p":1684420211332,"i_l":1}; _hjDonePolls=842733%2C842734; amplitude_idundefinedtrustpilot.com=eyJvcHRPdXQiOmZhbHNlLCJzZXNzaW9uSWQiOm51bGwsImxhc3RFdmVudFRpbWUiOm51bGwsImV2ZW50SWQiOjAsImlkZW50aWZ5SWQiOjAsInNlcXVlbmNlTnVtYmVyIjowfQ==; _hjHasCachedUserAttributes=true; ln_or=eyIyNzAwNyI6ImQifQ%3D%3D; __gads=ID=8e18a6dafbeada11-2236b3d7d3e00017:T=1684239928:RT=1684755014:S=ALNI_MYLjS7NdFNvIeRrH-a4jG1btL4yVw; __gpi=UID=00000bf8569a8f1c:T=1684239928:RT=1684755014:S=ALNI_MZNO9q1BQ8BO5CivMA516T4nXsAGA; _hjSession_391767=eyJpZCI6IjFiYjg3OTc1LWNhNDUtNGIzMS05NjM3LTlmNmI5ODEwMmFkOCIsImNyZWF0ZWQiOjE2ODQ3NTc4MDQzMjIsImluU2FtcGxlIjpmYWxzZX0=; _hjAbsoluteSessionInProgress=0; _hjIncludedInSessionSample_391767=0; OptanonConsent=isGpcEnabled=0&datestamp=Mon+May+22+2023+18%3A27%3A21+GMT%2B0530+(India+Standard+Time)&version=6.28.0&isIABGlobal=false&hosts=&consentId=63880818-a19a-45bf-b393-73fdb59f1e32&interactionCount=1&landingPath=NotLandingPage&groups=C0001%3A1%2CC0002%3A1%2CC0003%3A1%2CC0004%3A1&geolocation=IN%3BTN&AwaitingReconsent=false; amplitude_id_67f7b7e6c8cb1b558b0c5bda2f747b07trustpilot.com=eyJkZXZpY2VJZCI6ImE4NTg5ZmM1LTBmZmYtNDQ3NS1hYWYxLWZjOTI0ODc3MDcxZlIiLCJ1c2VySWQiOm51bGwsIm9wdE91dCI6ZmFsc2UsInNlc3Npb25JZCI6MTY4NDc1NzgwNTU0NiwibGFzdEV2ZW50VGltZSI6MTY4NDc2MDI0MjEyNCwiZXZlbnRJZCI6NTUwLCJpZGVudGlmeUlkIjozNiwic2VxdWVuY2VOdW1iZXIiOjU4Nn0=; _ga_11HBWMC274=GS1.1.1684757792.20.1.1684760244.0.0.0; _ga_MD2Z7JEPWG=GS1.1.1684757792.21.1.1684760244.0.0.0',
            'sec-ch-ua': '"Google Chrome";v="113", "Chromium";v="113", "Not-A.Brand";v="24"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'document',
            'sec-fetch-mode': 'navigate',
            'sec-fetch-site': 'none',
            'sec-fetch-user': '?1',
            'upgrade-insecure-requests': '1',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36'
            }

    def start_requests(self):
        url='https://www.trustpilot.com/categories'
        yield scrapy.Request(url,callback=self.parse,headers=self.headers)              

    def address_string(self,data):
        cleaned_data=data.replace('-','')
        cleaned_data=data.replace('. . . ','')
        cleaned_data=data.replace('=- ','')
        cleaned_data=data.replace('=','')
        return cleaned_data.strip()
    
    def phone_string(self,data):
        cleaned_data=data.replace('.','')
        cleaned_data=data.replace('-','')
        cleaned_data=data.replace('=','')
        return cleaned_data
    
    def email_string(self,data):
        cleaned_data=data.replace('.','')
        cleaned_data=data.replace('-','')
        return cleaned_data

    def parse(self,response):
        for block in response.xpath('//li[contains(@class,"linkItem")]'):
            category_link=block.xpath('./a/@href').get('')
            yield scrapy.Request(response.urljoin(category_link),callback=self.parse_details,headers=self.headers)
    
    def parse_details(self,response):
        for product in response.xpath('//a[@name="business-unit-card"]/parent::div'):
            product_links=product.xpath('.//a/@href').get('')
            product_link=response.urljoin(product_links)
            yield scrapy.Request(product_link,callback=self.product_details,headers=self.headers, cb_kwargs={'product_link':product_link})

        next_page=response.xpath('//a[@aria-label="Next page"]/@href').get('')
        next_page_link=response.urljoin(next_page)
        if next_page:
            yield scrapy.Request(next_page_link,callback=self.parse_details)
    
    async def product_details(self,response, product_link):
        # if not response.xpath('//a[@name="pagination-button-last"]').getall():
        showmore_url=response.css('[name="show-all-reviews"]::attr("href")').get()
        
        nextpage_url=response.urljoin(response.css('[aria-label="Next page"]::attr(href)').get())
        if nextpage_url!=None:
            yield scrapy.Request(nextpage_url,callback=self.product_details)
        
        if showmore_url:
            last_page=response.url.split('?')[0]+"?languages=all"
            yield scrapy.Request(last_page,callback=self.product_details_new)
        
        else:
            # last_page=response.url+"?languages=all"
            yield scrapy.Request(product_link+"?languages=all",callback=self.product_details_new)
                
    async def product_details_new(self, response):
        item = {}
        data_find=response.xpath('//script[@type="application/json"]/text()').get('')
        data_json=json.loads(data_find) 
        find_json=data_json.get('props',{}).get('pageProps',{})
        item['url']=response.url
        item['product_url']=response.url
        item['name']=find_json.get('businessUnit','').get('displayName','')
        item['number_of_reviews']=find_json.get('businessUnit','').get('numberOfReviews','')
        item['trust_score']=find_json.get('businessUnit','').get('trustScore','')
        item['website_url']=find_json.get('businessUnit','').get('websiteUrl','')
        item['star']=find_json.get('businessUnit','').get('stars','')
        email=find_json.get('businessUnit','').get('contactInfo','').get('email','')
        email=self.email_string(email)
        if '@' in email:
            item['email']=email
        else:
            item['email']=''
        phone=find_json.get('businessUnit','').get('contactInfo','').get('phone','')
        item['phone']=self.phone_string(phone)
        if '@' in item['phone']:
            item['email'] = f"{item['email']} | {item['phone']}"
            item['phone'] = ""
        address=' '.join(response.xpath('//ul[contains(@class,"contactInfoAddressList")]/li/text()').getall())
        item['address']= self.address_string(address)
        categories_list = []
        for categorie in find_json.get('businessUnit','').get('categories',''):
            cate=categorie.get('name','')
            categories_list.append(cate)
        item['categories']='|'.join(categories_list)
        
        for review_texts in find_json.get('reviews',''):
            consumersReview=review_texts.get('consumersReviewCountOnSameDomain','')
            name=review_texts.get('consumer','').get('displayName','')
            item['reviewer_name']=name
            natives=review_texts.get('consumer','').get('countryCode','')
            item['reviewer_country']=natives
            if consumersReview>=2:
                id=review_texts.get('id','')
                review_hidden_link=f'https://www.trustpilot.com/api/businessunitprofile/service-reviews/{id}/stack' 
                review_hidden_reponse=await self.request_process(review_hidden_link,headers=self.headers)
                for review_object in review_hidden_reponse.json()['reviews']:
                    data=review_object.get('dates','').get('publishedDate','')
                    item['reviewer_published_date']=data
                    title_review=review_object.get('title','')
                    item['reviewer_title']=title_review
                    review=review_object.get('text','')
                    review = re.sub(r'\s+',' ',review)
                    item['reviewer_review']=review
                    revies_number=review_object.get('consumer','').get('numberOfReviews','')
                    item['reviewer_rating']=revies_number
                    item['timestamp' ]=datetime.datetime.now().strftime('%Y-%m-%dT%H:%M:%SZ')
                    yield item
            
            name=review_texts.get('consumer','').get('displayName','')
            item['reviewer_name']=name
            natives=review_texts.get('consumer','').get('countryCode','')
            item['reviewer_country']=natives
            data=review_texts.get('dates','').get('publishedDate','')
            item['reviewer_published_date']=data
            title_review=review_texts.get('title','')
            item['reviewer_title']=title_review
            review=review_texts.get('text','')
            review = re.sub(r'\s+',' ',review)
            item['reviewer_review']=review
            revies_number=review_texts.get('consumer','').get('numberOfReviews','')
            item['reviewer_rating']=revies_number
            item['timestamp' ]=datetime.datetime.now().strftime('%Y-%m-%dT%H:%M:%SZ')
            yield item
        nextpage_url=response.urljoin(response.css('[aria-label="Next page"]::attr(href)').get())
        if nextpage_url!=None:
            yield scrapy.Request(nextpage_url,callback=self.product_details_new)

    
    async def request_process(self, url,headers):
        if headers is None:
            request = scrapy.Request(url)
        else:
            request = scrapy.Request(url,headers=headers)
        response = await self.crawler.engine.download(request, self)
        return response