# encoding: utf-8
"""
读取excel导入到neo4j中
"""
from tqdm import tqdm
import pandas as pd
import os
from py2neo import Graph, Node, Relationship

input_base_dir = r"E:\\work\\neo4j学术文献挖掘"
path = os.path.join(input_base_dir, 'data.xlsx')

# 读取数据
df = pd.read_excel(path)

# 定义节点
papers = []
degrees = []
authors = []
schools = {}
keywords = {}
teachers = {}
# 定义边
paper_author = []
author_school = []
author_degree = [] # TODO 暂时去掉，要不然节点太多
paper_keyword = []
author_teacher = []
# 遍历数据
for index, row in df.iterrows():
    paper_name = row['标题'],
    paper = {
        'name': paper_name,
        'englist_title': row['外文题名'],
        'year': row['学位年度'],
        'abstract': row['摘要'],
        'english_abstract': row['外文摘要'],
        'link': row['链接']
    }

    author_name = row['作者'].strip()
    author = {
        'name': author_name,
        'degree': row['学位名称']
    }

    school_name = row['学位授予单位']
    school = {
        'name': school_name
    }

    keyword_names = str(row['关键词']).strip().split('；')

    teacher_names = str(row['导师姓名']).strip().split('，')
    
    # 添加节点
    papers.append(paper)
    authors.append(author)
    if schools.get(school_name, -1) == -1:
        schools[school_name] = school
    for keyword_name in keyword_names:
        keyword = {
            'name': keyword_name
        }
        if keywords.get(keyword_name, -1) == -1:
            keywords[keyword_name] = keyword
    for teacher_name in teacher_names:
        teacher = {
            'name': teacher_name
        }
        if teachers.get(teacher_name, -1) == -1:
            teachers[teacher_name] = teacher
    # 添加边
    paper_author.append({
        'src': paper_name,
        'dst': author_name
    })
    author_school.append({
        'src': author_name,
        'dst': school_name
    })
    for keyword_name in keyword_names:
        paper_keyword.append({
            'src': paper_name,
            'dst': keyword_name
        })
    for teacher_name in teacher_names:
        author_teacher.append({
            'src': author_name,
            'dst': teacher_name
        })

# 连接neo4j数据库，输入地址、用户名、密码
graph = Graph("http://localhost:7474", username="neo4j", password='123456')
graph.delete_all() #清除neo4j中原有的结点等所有信息

# 插入节点
print('插入papers')
papers_map = {

}