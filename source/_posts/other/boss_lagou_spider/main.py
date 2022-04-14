"""
爬取boss 拉钩上的代码
"""
from requests.api import head
from utils import *
from bs4 import BeautifulSoup
import json
import time
import traceback

class Spider(object):
    platform = None
    headers = {}
    company_dict = {}
    
    def spider(self):
        pass

    def parse(self):
        pass

    def get_proxy(self):
        proxy = get_proxy()
        return proxy
    

class LagouSpider(Spider):
    platform = '拉钩'
    headers = {
        'Accept': '*/*',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'User-Agent':'Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit/604.1.38 (KHTML, like Gecko) Version/11.0 Mobile/15A372 Safari/604.1',
        'Referer':'https://m.lagou.com',
        'content-type': 'application/json',
        'Origin': 'https://m.lagou.com',
        'x-l-req-header': '{"ACCESSTYPE":"PRIVATE","INNERREQUEST":true,"deviceType":1}',
        'Cookie': 'user_trace_token=20210725234649-e032ce7c-8ed4-49aa-9eef-539df13b930d; _ga=GA1.2.774895120.1627228010; LGUID=20210725234649-9a7839de-1f96-4f10-a047-c726fa46db1c; privacyPolicyPopup=false; index_location_city=%E4%B8%8A%E6%B5%B7; gate_login_token=2ec0ee79ffb7ea81ce3d9e30eaabfe7d2cf8950c8bb635ee; LG_LOGIN_USER_ID=f158036a20f5648e64264251d802969dad270e751bf392ab; LG_HAS_LOGIN=1; Hm_lvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1627228010,1627546439; _gat=1; LGSID=20210729161359-1836ee75-e9a5-49f1-9f74-4cf21792b7d4; PRE_UTM=m_cf_cpc_sogou_pc; PRE_HOST=www.sogou.com; PRE_SITE=https%3A%2F%2Fwww.sogou.com%2Fbill%5Fcpc%3Fv%3D1%26p%3DWJ80%24xb%24YnJcpvyy32VcBGwSgoqpwYLuPkn20lBbd7eW8LBeMVPXxiHRfD2b4xcgF6e3Ra0MDMq2Oo8XFlQfqQZ4CmEttsB49h2XUuBWWuJxBreeVMGjeohv6oJA3TTdDsJhsB89d5evsWFDg5LteaZUojrNk7F1q5LjB5TACGvAilhd0Jat4Vq0Hd3vT50A%4023AiVFbT506H506kuyk4fkTsAxBCtk728fETxbjxD66Btqbu%24U6QBr4IekBuPuOe%247zub%24zly6aJexPjW3zZrPnrAjmnY0OlAy7RvtZr0c%40fdCjeOuGb9Ypx0%24Bxy7YTTitTfmhkIVxAoLa7UAw1UA30c7eyc0F128jhG8vT2kvJVcuepkwoInVp5LO2aPYj7ohUcyURGCv0wCv0Bw78BwGRBa2FlClZGFYeGFvh20yh2eUAILa3bC9A2VlAoWa%24FxbjxIuyxi0PSlE15UpekzuwVcOk7K4eBvQa7vSzuAqBJqAXvrVhDqvUIez3GS%24oln9UIetaGgVuyYkG8uculm86197yvfQC2FA2jVnle1yGRwlLieSR4y1l9HkA1k%3D%26q%3DWJe0lllllylx%26query%3D%25E6%258B%2589%25E5%258B%25BE%25E7%25BD%2591; PRE_LAND=https%3A%2F%2Fwww.lagou.com%2Flanding-page%2Fpc%2Fsearch.html%3Futm%5Fsource%3Dm%5Fcf%5Fcpc%5Fsogou%5Fpc%26m%5Fkw%3Dsogou%5Fcpc%5Fbj%5F96db97%5Fd2162e%5F%25E6%258B%2589%25E5%258B%25BE%25E7%25BD%2591; _putrc=AE8D7DC1EE78677A; login=true; unick=%E4%BB%BB%E5%8D%AB%E5%BC%BA; __SAFETY_CLOSE_TIME__8115873=1; _gid=GA1.2.462935116.1627546462; WEBTJ-ID=20210729161433-17af15453bb4b3-0ff078a6fd95d4-35637203-1296000-17af15453bc202; _ga=GA1.3.774895120.1627228010; JSESSIONID=ABAAABAABGJABAJ023C5AD9912845BB5BE9EB0A79F1536E; sensorsdata2015session=%7B%7D; __lg_stoken__=9b2254e3464eb9b98fc9168f32de8aea2a02a4050da98df9f146617dbdbfd9ec53135cdd8510d4b644a5031dc5a28eafdc0202020547ea2bbcaa0aefddaeb86f40927d7f8078; X_HTTP_TOKEN=1e14b0835f2cc7b31256457261fba94eeb41bcef8f; Hm_lpvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1627546521; sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%228115873%22%2C%22%24device_id%22%3A%2217ade5907ac133-0504fabdc5d127-34637600-1296000-17ade5907adaa9%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E7%9B%B4%E6%8E%A5%E6%B5%81%E9%87%8F%22%2C%22%24latest_referrer%22%3A%22%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC_%E7%9B%B4%E6%8E%A5%E6%89%93%E5%BC%80%22%2C%22%24os%22%3A%22MacOS%22%2C%22%24browser%22%3A%22Chrome%22%2C%22%24browser_version%22%3A%2292.0.4515.107%22%2C%22lagou_company_id%22%3A%22%22%7D%2C%22first_id%22%3A%2217ade5907ac133-0504fabdc5d127-34637600-1296000-17ade5907adaa9%22%7D; LGRID=20210729161531-835d6409-8f91-4cc3-9859-c09e4d85c904'
    }
    companys_dict = {
        '米哈游': '9f8c95b92321a8e11nJz2Nu7',
        '紫龙游戏': '72beee498839340a0Hd-2Nu_',
        'B站': 'ae1ff0467cbd29ea1nZ-3ts~',
        '游族': '1ac487daf336ea020XB62dW_Eg~~',
        '盛趣游戏': '3b7486730f9f0b091H1z3Nm8Eg~~',
        '巨人网络': 'b8fd49d9d59961761nN839i4',
        '叠纸游戏': '220eafdd671bf26d0nB_2N6_Eg~~',
        '完美世界': '139ba6a6fa587b411nd629w~',
        '三七互娱': '961f8d30b1d5546b1X1-2965Fg~~',
        '莉莉丝': '056e2261259a7e151nxy2N2-',
        '网易游戏': '1f9c13f93a2492291XRz39S1',
        '腾讯': '2e64a887a110ea9f1nRz'
    }

    def parse(self, html, company):
        html = html.strip()
        soup = BeautifulSoup(html, 'lxml')
        data = []
        for li in soup.select('li'):
            href = li.select_one('a.a-link')['href']
            salary = li.select_one('h4>span.price').get_text().strip()
            position = list(li.select_one('h4').children)[-1].strip()
            city = list(li.select_one('div').children)[0].strip()
            work_year = list(li.select_one('div').children)[2].strip()
            item = {
                'href': href,
                'salary': salary,
                'position': position,
                'city': city,
                'work_year': work_year,
                'company': company
            }
            data.append(item)
        return data
    
    def spider(self):
        for company, company_id in self.companys_dict.items():
            try:
                with open(f'./boss/{company}.jsonl', 'w') as wp:
                    print(company, '开始---')
                    page_no = 1
                    res = self.spider(company_id, page_no)
                    if res == False:
                        print('启动爬虫被封!')
                    else:
                        data = []
                        has_next, items = res
                        items = self.parse(items, company)
                        for item in items:
                            wp.write(json.dumps(item, ensure_ascii=False) + '\n')
                        while has_next:
                            page_no += 1
                            res = self.spider(company_id, page_no)
                            if res != False:
                                if res[1] == '被封':
                                    time.sleep(random.randint(5, 20))
                                    continue
                                has_next, items = res
                                items = self.parse(items, company)
                                for item in items:
                                    wp.write(json.dumps(item, ensure_ascii=False) + '\n')
                                data += items
                            else:
                                has_next = False
                            time.sleep(random.randint(5, 20))
                    print(company, '结束---')
                time.sleep(random.randint(50, 100))
            except:
                traceback.print_exc()
                continue

class BossSpider(Spider):
    platform = 'BOSS'
    headers =  {
        'Accept': '*/*',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'User-Agent':'Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit/604.1.38 (KHTML, like Gecko) Version/11.0 Mobile/15A372 Safari/604.1',
        'Referer':'https://m.lagou.com/search.html',
        'Cookie': 'lastCity=101020100; __g=-; Hm_lvt_194df3105ad7148dcf2b98a91b5e727a=1627226436,1627541429,1627867752; ___gtid=1712692158; __fid=7a35d537a5523af7530e9a28b0280c71; acw_tc=0bcb2f0416278678234054043e653a5632060292916d5661201e5b96ae289f; __c=1627867752; __a=83011435.1627226436.1627541437.1627867752.19.3.5.19; Hm_lpvt_194df3105ad7148dcf2b98a91b5e727a=1627867824; __zp_stoken__=fd1ccPCBgMV9nM1dtCRdWJ3crF3YlHyBYQCF0cQkXD054Iw1HYXk8NVElbRF0TAMSR2NlXTp1UiIgCF89GRNqVUdtL1x9EGRnJ2xGUVk4fl1qRysYC08wXDFMEz9zbyp7fEB1YFt1W0hYOE0d',
        'Host': 'm.zhipin.com',
        'X-Requested-With': 'XMLHttpRequest',
        'Referer': 'https://m.zhipin.com/gongsir/2e64a887a110ea9f1nRz.html?ka=job-detail-company_custompage',
    } 
    companys_dict = {
        '米哈游': 7872,
        '紫龙': 150741,
        'B站': 30830,
        '游族': 14983,
        '盛趣游戏': 103343,
        '巨人网络': 1265,
        '叠纸游戏': 122560, 
        '完美世界': 10369,
        '腾讯': 451,
        '米哈游': 7872,
        '网易游戏': 22790,
        '三七互娱': 658,
        '莉莉丝': 1938,
    }

    def parse(self):
        pass
    
    def spider(self):
        for company, company_id in self.companys_dict.items():
            try:
                with open(f'./lagou/{company}.jsonl', 'w') as wp:
                    print(company, '开始---')
                    page_no = 1
                    res = self.spider(company_id, page_no)
                    if res == False:
                        print('启动爬虫被封!')
                    else:
                        data = []
                        has_next, items = res
                        data += items
                        for item in items:
                            wp.write(json.dumps(item, ensure_ascii=False) + '\n')
                        while has_next:
                            page_no += 1
                            res = self.spider(company_id, page_no)
                            if res != False:
                                if res[1] == '被封':
                                    time.sleep(random.randint(5, 20))
                                    continue
                                has_next, items = res
                                for item in items:
                                    wp.write(json.dumps(item, ensure_ascii=False) + '\n')
                                data += items
                            else:
                                has_next = False
                            time.sleep(random.randint(5, 20))
                    print(company, '结束---')
                time.sleep(random.randint(50, 100))
            except:
                traceback.print_exc()
                continue
    
if __name__ == '__main__':
    spider = BossSpider()
    spider.spider()