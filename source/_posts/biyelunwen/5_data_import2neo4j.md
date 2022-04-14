---
title: 导入数据到neo4j
date: 2022-02-21 11:40:43
tags:
 - 毕业设计
categories:
 - 毕业设计
---

> 删除所有的节点:`match (n) detach delete n`

# demo1

> 湖北能源副总经理金彪辞职 2020年薪酬为99.41万

| 事件元素 | 元素值 | 
| - | - |
公告公司 | 湖北能源 | 
离职高管名称 | 金彪 | 
高管职务 | 副总经理 | 

创建4个实体，分别为：

- 事件提及句
```
create (s: event_sentence {id: 1, content: '湖北能源副总经理金彪辞职 2020年薪酬为99.41万', url: 'http://stock.jrj.com.cn/2021/12/22213234049020.shtml'})
```
- 事件类型

```
create (et: event_type {id: 1, name: "高管离职"})
```

- 公司
```
create (c: company {id: 1, name: '湖北能源'} )
```
- 高管
```
create (m: manager {id: 1, name: '金彪'})
```
- 职务
```
create (p: post {id: 1, name: '副总经理'})
```


创建对应的关系

- (事件提及句)-[has_an_event]->(事件类型)
```
match (s: event_sentence), (et: event_type)
where s.id = 1 and et.id=1
create (s)-[r:has_an_event]->(et)
return r
```

- (事件提及句)-[公告公司]->(公司)
```
match(s: event_sentence), (c: company)
where s.id=1 and c.id=1
create (s)-[r:公告公司]->(c)
return r
```

- (事件提及句)-[离职高管]->(高管)
```
match(s: event_sentence), (m: manager)
where s.id = 1 and m.id = 1
create (s)-[r:离职高管]->(m)
return r
```

- (高管)-[职务]->(职务)

```
match(m: manager), (p: post)
where m.id = 1 and p.id = 1
create (m)-[r:职务]->(p)
return r
```



# demo2
> 长源电力(000966.SZ)：湖北能源减持1674.16万股 持股比例减至5%

| 事件元素 | 元素值 | 
| - | - |
| 公告公司 | 长源电力 | 
| 减持方_公司 | 湖北能源 | 
| 减持股本数 | 1674.16万 | 

创建节点，分别为：

- 事件提及句

```
create (s: sentence {id: 2, content: '长源电力(000966.SZ)：湖北能源减持1674.16万股 持股比例减至5%', url: 'http://stock.jrj.com.cn/2021/12/22213234049020.shtml'})
```

- 事件类型

```
create (et: event_type {id: 2, name: '股东减持'})
```

- 公告公司
```
create (c: company {id: 2, name: '长源电力'})
```

- 减持方_公司
```
create (c: company {id: 2, name: '湖北能源'})
```

- 股本数

```
create (sm: stock_num {id: 2, value: '股本数'})
```

创建关系，分别为：

- (事件提及句)-[has_an_evnt]->(事件类型)
```
match (s: event_sentence), (et: event_type)
where s.id = 2 and et.id = 3
create (s)-[r:has_an_event]->(et)
return r
```

- (事件提及句)-[减持方]->(公司)
```
match (s: event_sentence), (c: company)
where s.id = 2 and c.id = 1
create (s)-[r:减持方]->(c)
return r
```

- (事件提及句)-[被减持方]->(公司)
```
match (s:event_sentence), (c: company)
where s.id = 2 and c.id = 2
create (s)-[r:被减持方]->(c)
return r
```

- (事件提及句)-[股本数]->(股本数)

```
match (s: event_sentence), (sm: stock_num)
where s.id = 2 and sm.id =2
create (s)-[r:减持股本数]->(sm)
return r
```

- (事件提及句)-[顺承]->(事件提及句)

```
match (s1: event_sentence), (s2: event_sentence)
where s1.id = 1 and s2.id = 2
create (s2)-[r:顺承 {p: 1}]->(s1)
```


# 创建节点以及节点之间的对应关系

# Cypher语句

## 创建节点

- 事件提及句

```cypher
create(s1:event_sentence {id: 1, content: '湖北能源副总经理金彪辞职 2020年薪酬为99.41万', url: 'http://stock.jrj.com.cn/2021/12/22213234049020.shtml'})

create(s2:event_sentence {id: 2, content: '长源电力(000966.SZ)：湖北能源减持1674.16万股 持股比例减至5%', url: 'http://stock.jrj.com.cn/2021/09/01200233369282.shtml'
})

match (s1:event_sentence), (s2:event_sentence)
where s1.id = 2 and s2.id=1
create (s1)-[r:seq]->(s2)
return r

match(s1:event_sentence), (et2:event_type)
where s1.id = 2 and et2.id = 2
create (s1)-[r:has_an_event]->(et2)
return r

match (s1:event_sentence), (c1:company)
where s1.id=2 and c1.id=2
create (s1)-[r:has_an_company]->(c1)

match(s1:event_sentence), (c2:company)
where s1.id=2 and c2.id=1
create(s1)-[r:减持方]->(c2)
```

- 事件类型

```cypher
create(et1:event_type {id: 1, content: '高管离职'})
create(et2:event_type {id: 2, content: '股东减持'})
```

- 公司

```cypher
create(c1:company {id: 1, name: '湖北能源'})
create(c1:company {id: 2, name: '长源电力'})
```

- 高管

```
create(m1:manager {id: 1, name: '金彪'})
```

- 职位

```
create(p1:post {id: 1, name: '总经理'})
```


## 创建关系

```
create (sentence_id_1:event_sentence) - [r1:has_an_company]-> (company_id_1:company)
```

```
MATCH (s1:event_sentence),(c1:company)
WHERE s1.id = 1 AND c1.id = 1
CREATE (s1)-[r:has_an_company] -> (c1)
RETURN r
```

```
MATCH (s1:event_sentence), (et1:event_type)
WHERE s1.id=1 and et1.id = 1
CREATE (s1)-[r:has_an_event] -> (et1)
return r
```

```
MATCH (et1: event_type), (m1:manager)
WHERE et1.id=1 and m1.id = 1
CREATE (et1)-[r:has_an_attribute]->(m1)
return r
```

```
MATCH (s1: event_sentence), (m1:manager)
where s1.id = 1 and m1.id = 1
create (s1)-[r:has_an_attribute]->(m1)
return r
```

- 高管-职位
```
match (m1:manager), (p1:post)
where m1.id=1 and p1.id=1
create (m1)-[r:has_an_post]->(p1)
return r
```