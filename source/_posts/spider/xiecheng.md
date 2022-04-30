---
title: 携程酒店_景点爬虫与评论
date: 2022-04-26 15:20:49
tags:
 - 爬虫
categories:
 - 爬虫
---

# 酒店爬虫

## 酒店列表

> 现在网上的[代码](https://blog.csdn.net/m0_51271122/article/details/112512441)基本都过时，所以参考的代码为本[链接](https://github.com/songweiwei/pachong/blob/master/main.py)

API为:`https://m.ctrip.com/restapi/soa2/21881/getRecommendHotels`

```python
def crawl_hotels(city_name='上海', city_id=2, page_size=5):
    all_dataset = []
    for page_index in range(1, page_size + 1):
        url = "https://m.ctrip.com/restapi/soa2/21881/getRecommendHotels"
        print(url, page_index, 'start')
        params = {
            "cityId": city_id,
            "platform": "online",
            "pageID": "102001",
            "pageNo": page_index,
            "head": {
                "Version": "",
                "userRegion": "CN",
                "Locale": "zh-CN",
                "LocaleController": "zh-CN",
                "TimeZone": "8",
                "Currency": "CNY",
                "PageId": "102001"
            }
        }
        try:
            response = requests.post(url, headers=headers, data=json.dumps(params))
        except: 
            print(url, '请求失败')
            continue

        if response.status_code != 200:
            print('响应码: ', response.status_code)
            continue 
        try:
            data = response.json()
        except:
            print('不是JSON响应')
            continue 
        try:
            hotel_list = data["Response"]["hotels"]
        except:
            print('没有酒店信息')
            continue
        dataset = []
        for hotel in hotel_list:
            name = hotel['hotelName']
            star = hotel['star']
            price = hotel['price']
            _url = hotel['url']
            inner_id = hotel['url'].split('/')[2].strip('.html')
            dataset.append(
                [name, star, price, _url, inner_id]
            )
        df = pd.DataFrame(data=dataset, columns=['name', 'star', 'price', 'url', 'inner_id', ])
        df['city'] = city_name
        all_dataset.append(df)
    df = pd.concat(all_dataset)
    df = df.drop_duplicates()
    df.to_sql('app_hotel', conn, index=False, if_exists='append')
    for _, row in df.iterrows():
        hotel_id = row['inner_id']
        crawl_comments(hotel_id, 30)
```

> 需要注意的是该代码能够爬取到每一个城市的酒店的数量是有限的，因为是`酒店推荐`。


## 酒店评论

参考本篇[文章](https://zhuanlan.zhihu.com/p/270648077)

```python
def crawl_comments(hotel_id, page_size=10):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Trident/7.0; rv:11.0) like Gecko',"Content-Type": "application/json"}
    for page_index in range(1, page_size + 1):
        time.sleep(0.5)
        print('评论-', page_index, 'start')
        params = {
            "hotelId": hotel_id, 
            "pageIndex": page_index, 
            "tagId": 0, 
            "pageSize": 10, 
            "groupTypeBitMap": 2,
            "needStatisticInfo": 0, 
            "order": 0, 
            "basicRoomName": "", 
            "travelType": -1,
            "head": {"cid": "09031174312350135405", "ctok": "", "cver": "1.0", "lang": "01", "sid": "8888","syscode": "09", "auth": "93C8AE20D20009DC90E6E10BB588DE61E67EBBC236DE15433FDDADFD95636F28", "extension": []}
        }
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Trident/7.0; rv:11.0) like Gecko', "Content-Type": "application/json"}
        url = 'http://m.ctrip.com/restapi/soa2/16765/gethotelcomment?_fxpcqlniredt=09031144211504567945'
        try:
            response = requests.post(url, headers=headers, data=json.dumps(params))
        except:
            print('请求失败!')
            continue

        if response.status_code != 200:
            print('响应码: ', response.status_code)
            continue
        try:
            data = response.json()
        except:
            print('无JSON数据')
            continue
        result = data.get('othersCommentList', False)
        if result is False:
            print('无数据')
            continue
        dataset = []
        items = result
        for row in items:
            try:
                inner_id = row['id']
                content = row['content'].strip()
                label = predict(content)
                dataset.append(
                    [inner_id, content, label]
                )
            except:
                traceback.print_exc()
                continue
        if len(dataset) == 0:
            continue
        df = pd.DataFrame(data=dataset, columns=['inner_id', 'content', 'label'])
        df['hotel_id'] = hotel_id
        df.to_sql('app_hotelcomment', conn, if_exists='append', index=False)
        print('评论-', page_index, 'end')
```

# 景点爬虫

TODO 


## 景点列表

## 景点评论