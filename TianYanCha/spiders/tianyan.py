# -*- coding: utf-8 -*-
import scrapy
from functools import reduce

from TianYanCha.items import TianyanchaItem


class TianyanSpider(scrapy.Spider):
    name = 'tianyan'
    allowed_domains = ['tianyancha.com']
    start_urls = ['https://www.tianyancha.com/company/2316149614']
    # cookies值是变动的，最好的办法是用selenium模拟登入，然后获取cookie值保存，然后动态登入，这里不做演示，此外反爬的为验证码，根据A图片
    # 文字，在B图中点击，暂时未找到解决方式，可以采用第三方，获取坐标地址提交
    cookies = {
        'TYCID': 'a6072510d8f611e7905d6bf50389c472',
        'undefined': 'a6072510d8f611e7905d6bf50389c472',
        'ssuid': '6932371139',
        'RTYCID': '5296df7047fd4c149d4aa7707bb42660',
        'aliyungf_tc': 'AQAAAMdE3SPfBgUAU0BlmcwaWz5W3baP',
        'csrfToken': 'QP4paXQmL6Yerdm99UJQaTqq',
        'tyc-user-info': '%7B%22token%22%3A%22eyJhbGciOiJIUzUxMiJ9.eyJzdWIiOiIxNTY3OTc5MDEzMCIsImlhdCI6MTUxMjYyNDk5NiwiZXhwIjoxNTI4MTc2OTk2fQ.K-SHmx1y7eS17JhAzLlsD-mCVLtbcURimS29XVebzcnprxsok6y25Z7YKHQbvUUfoFQi3wCmKxsZEzhCszAPBw%22%2C%22integrity%22%3A%220%25%22%2C%22state%22%3A%220%22%2C%22vipManager%22%3A%220%22%2C%22vnum%22%3A%220%22%2C%22onum%22%3A%220%22%2C%22mobile%22%3A%2215679790130%22%7D',
        'auth_token': 'eyJhbGciOiJIUzUxMiJ9.eyJzdWIiOiIxNTY3OTc5MDEzMCIsImlhdCI6MTUxMjYyNDk5NiwiZXhwIjoxNTI4MTc2OTk2fQ.K-SHmx1y7eS17JhAzLlsD-mCVLtbcURimS29XVebzcnprxsok6y25Z7YKHQbvUUfoFQi3wCmKxsZEzhCszAPBw',
        'jsid': 'SEM-BAIDU-PZPC-000000',
        '_csrf': 'h/hb3qHWiPewwOMtS+vC8g==',
        'OA': 'N+Az86zNnI5Im9xyOXXC4hM9/rmqk3SLmffKN4Ju4xJwwvuVOGl5mu+3ROhJi/MO',
        '_csrf_bk':'186f98d507939af6c8b3bb232ea88455',
        'Hm_lvt_e92c8d65d92d534b0fc290df538b4758': '1512624957',
        'Hm_lpvt_e92c8d65d92d534b0fc290df538b4758': '1512625018'
    }

    # 这里为字体库的映射关系,可以在css样式中找到
    di = {'(':'(',')':')','人':'人','民':'民','币':'币','万':'万','元':'元','':'','6': '1', '7': '0', '2': '6', '1': '.', '9': '2', '8': '4', '5': '3', '4': '7', '0': '9', '3': '5', '-': '-'}

    # 可以重写Spider类的start_requests方法，附带Cookie值，发送get请求
    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url, cookies=self.cookies)

    def parse(self, response):
        html = response.text
        item = TianyanchaItem()
        # try:
        #     # 企业名字
        item['name'] = response.xpath('//*[@id="company_web_top"]/div[2]/div[2]/div[1]/span[1]/text()').extract_first()
        #     # 企业电话
        item['phone'] = response.xpath('//div[@class="f14 sec-c2 mt10"]/div[1]/span[2]/text()').extract_first()
        #     # 企业邮箱
        item['mail'] = response.xpath('//div[@class="f14 sec-c2 mt10"]/div[2]/span[2]/text()').extract_first()
        #     # 企业网页地址
        item['net_addr'] = response.xpath(
            '//*[@id="company_web_top"]/div[2]/div[2]/div[1]/div[3]/div[1]/a/text()').extract_first()
        #     # 企业地址
        item['addr'] = response.xpath(
            '//*[@id="company_web_top"]/div[2]/div[2]/div[1]/div[3]/div[2]/span[2]/text()').extract_first()
        #     # 企业描述
        item['desc'] = response.xpath(
            '//*[@id="company_web_top"]/div[2]/div[2]/div[2]/span[1]/text()').extract_first()
        #     # 法人
        item['faren'] = response.xpath(
            '//div[@class="company_header_width ie9Style"]/div[1]/span[1]/text()').extract_first()
        #     # 拥有的公司
        item['owner_company'] = ''.join(response.xpath(
            '//div[@class="human-bottom sec-c4 pt10"]/div[@class="pb10 f12 lh"]//text()').extract())
        #     # 注册资本,注意价格的渲染-----以下的价格和日期部分都用了eot格式，注意转换
        print(item)
        num = response.xpath(
            '//*[@id="_container_baseInfo"]/div/div[2]/table//tr/td[2]/div[1]/div[2]//text()').extract_first()
        print(num)
        item['register_money'] = reduce(lambda x, y: x + self.di[y], list(num), '')
        #     # 注册时间,注意这里的时间是经过渲染的
        num = response.xpath(
            '//*[@id="_container_baseInfo"]/div/div[2]/table//tr/td[2]/div[2]/div[2]//text()').extract_first()
        item['register_time'] = reduce(lambda x, y: x + self.di[y], list(num), '')
        #     # 公司状态
        item['company_state'] = response.xpath(
            '//*[@id="_container_baseInfo"]/div/div[2]/table//tr/td[2]/div/div[2]/div[1]/text()').extract_first()
        #     # 工商注册代码
        item['registration_num'] = response.xpath(
            '//div[@class="base0910"]/table//tr[1]/td[2]/text()').extract_first()
        #     # 组织机构代码
        item['organization_num'] = response.xpath(
            '//*[@class="base0910"]/table//tr[1]/td[4]/text()').extract_first()
        #     # 统一信用代码
        item['credit_num'] = response.xpath(
            '//*[@class="base0910"]/table//tr[2]/td[2]/text()').extract_first()
        #     # 公司类型
        item['company_type'] = response.xpath(
            '//*[@class="base0910"]/table//tr[2]/td[4]/text()').extract_first()
        #     # 纳税人识别号
        item['taxpayer_num'] = response.xpath(
            '//*[@class="base0910"]/table//tr[3]/td[2]/text()').extract_first()
        #     # 行业
        item['ndustry'] = response.xpath(
            '//*[@class="base0910"]/table//tr[3]/td[4]/text()').extract_first()
        #     # 营业期限
        item['bussiness_time'] = response.xpath(
            '//*[@class="base0910"]/table//tr[4]/td[2]//text()').extract_first()
        #     # 核准时间
        num = response.xpath(
            '//*[@class="base0910"]/table//tr[4]/td[4]//text()').extract_first()
        item['check_time'] = reduce(lambda x, y: x + self.di[y], list(num),'')
        #     # 登记机关
        item['register_office'] = response.xpath(
            '//*[@class="base0910"]/table//tr[5]/td[2]/text()').extract_first()
        #     # 英文名字
        item['company_eng'] = response.xpath(
            '//*[@class="base0910"]/table//tr[5]/td[4]/text()').extract_first()
        #     # 注册地址
        item['register_addr'] = response.xpath(
            '//*[@class="base0910"]/table//tr[6]/td[2]/text()').extract_first()
        #     # 经营范围
        item['manage_orange'] = response.xpath(
            '//*[@class="base0910"]/table//tr[7]/td[2]//span[1]/text()').extract_first()
        print(item)
        # yield item
        # except  as f:
        #     print(f,'------')