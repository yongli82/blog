---
title: ElasticSearch实践(一)
date: 2018-04-24 12:00
tags: 基础技术
categories: 基础技术
---

# ElasticSearch实践(一)

官方文档：[Elasticsearch: 权威指南]( https://www.elastic.co/guide/cn/elasticsearch/guide/current/index.html)

> Elasticsearch 是一个分布式、可扩展、实时的搜索与数据分析引擎。 它能从项目一开始就赋予你的数据以搜索、分析和探索的能力。

用途:
1、查询
2、搜索
3、聚类统计

基本概念:
集群、节点、分片
索引、类型
文档、字段、映射
doc\_values、field\_data

客户端

<技术架构图>

常用操作:
1、创建索引、设置映射
2、基础数据增删改查
3、复杂查询
4、大批量处理
5、聚类统计


---


## Python API调用框架

使用前先安装模块 `pip install elasticsearch`

API文档: https://elasticsearch-py.readthedocs.io/en/master/

```
from elasticsearch import Elasticsearch, Urllib3HttpConnection
from pprint import pprint

def client(env='test'):
    """
    不同环境使用不同的配置
    """
    hosts = [
        {"host": "10.20.124.xx1"},
        {"host": "10.20.124.xx2"},
        {"host": "10.20.124.xx3"}
    ]
    http_auth = ('appkey', 'appToken')

    if env == 'prod':
        hosts = [
            {"host": "10.69.213.xx1"},
            {"host": "10.69.213.xx2"},
            {"host": "10.69.213.xx3"}
        ]
        http_auth = ('appkey', 'appToken')

    es = Elasticsearch(
        hosts=hosts,
        http_auth=http_auth,
        connection_class=Urllib3HttpConnection,
        port=8080,
        sniff_on_start=True,
        sniff_on_connection_fail=True,
        sniffer_timeout=6000,
        timeout=6000
    )
    return es

if __name__ == "__main__":
    """
    调用基本模式，首先获取es客户端，然后构造操作body，调用es的API时指定index和doc_type
    """
    es = client(env='test')
    body = {
      "query": {
        "bool": {
          "must": [
            {
              "match_all": {}
            }
          ],
          "must_not": [],
          "should": [],
          "filter": []
        }
      },
      "from": 0,
      "size": 10,
      "sort": []
    }
    result = es.search(index="test_index", doc_type="test_type", body=body)
    pprint(result)
```

### 创建索引、设置映射

```
from eager_client import client

INDEX = "hiring_people"

true = "true"
false = "false"

# 配置映射
mappings = {
    "mappings": {
        "staff": {
            "_all": {
                "enabled": false
            },
            "properties": {
                "title": {
                    "type": "text",
                    "index": true,
                    "analyzer": "mtseg_dict_smart"
                },
                "name": {
                    "type": "text",
                    "index": true,
                    "analyzer": "ik_smart"
                },
                "gender": {
                    "type": "keyword",
                    "index": true,
                    "doc_values": true
                }
            }
        }
    },
    "settings": {
        "index": {
            "number_of_shards": "5",
            "number_of_replicas": "1"
        }
    }
}

es = client()
if not es.indices.exists(index=INDEX):
    print("=== create index =====")
    es.indices.create(index=INDEX, body=mappings)

```

#### 常用映射类型样例

对"type": "text"类型的，最好指定对应的analyzer。

```
"id": {
  "type": "long"
},
"name": {
  "type": "keyword"
},
"gender": {
  "type": "keyword"
},
"desc": {
  "type": "text",
  "fields": {
    "keyword": {
      "type": "keyword",
      "ignore_above": 256
    }
  }
},
"has_attachment": {
  "type": "boolean"
},
"highestDegree": {
  "type": "keyword"
},
"score": {
  "type": "float"
},
"birth_day": {
  "type": "date",
  "format": "yyyy-MM-dd"
},
"storageTime": {
  "type": "date",
  "format": "yyyy-MM-dd HH:mm:ss"
}

```

### 基本增删改查

接上文创建的索引，使用index函数进行增加和更新数据，用delete函数删除数据，用search函数查询数据。
http://elasticsearch-py.readthedocs.io/en/master/api.html

#### 增加数据
```
print("=== add data =====")
for i in range(0, 100):
    if i < 50:
        title = "工程师"
    else:
        title = "产品经理"

    name = "%s%03d" % (title, i)
    if i % 2 == 0:
        gender = "男"
    else:
        gender = "女"
    staff = {
        "title": title,
        "name": name,
        "gender": gender
    }

    es.index(index=INDEX, doc_type="staff", body=staff)
```

#### 查询数据

```
print("=== search ===")
result = es.search(index=INDEX, doc_type="staff", body={
    "query": {
        "term": {
            "gender": "女"
        }
    }
})

pprint(result)

```

#### 修改数据

修改数据和添加数据一样也使用index函数，但要指定id参数(document Id)

#### 删除数据

使用delete函数通过id删除文档，或者用delete_by_query函数通过查询条件删除文档


### 复杂搜索

ElasticSearch的主要用途是进行各种条件的搜索。

#### 基本搜索处理框架:

```
body = {
    # 查询条件
    # 过滤条件
    # 聚合参数
    # 分页参数
    # 排序参数
}
result = es.search(index="your_index", doc_type="you_type", body=body)
# pprint(result)
hits = result["hits"]["hits"]
for hit in hits:
    # 处理hit

```

#### 组合条件

通常使用bool来组合查询条件。

比较复杂，之后再贴几个示例，主要参考官方文档吧。

https://www.elastic.co/guide/cn/elasticsearch/guide/current/search-in-depth.html


#### 抽样数据

使用`script`, 按对象中的Id取模进行数据抽样
参考 [Script Query](https://www.elastic.co/guide/en/elasticsearch/reference/6.2/query-dsl-script-query.html)

```
{
  "query": {
    "bool": {
      "must": [
        {
          "script": {
            "script": {
              "source": "doc['id'].value % 1000 == 0"
            }
          }
        }
      ],
      "must_not": [],
      "should": [],
      "filter": []
    }
  },
  "from": 0,
  "size": 1000,
  "sort": []
}
```

#### 对嵌套对象字段进行聚合

参考: https://www.elastic.co/guide/cn/elasticsearch/guide/current/nested-aggregation.html

```
{
  "aggs": {
    "workExpList": {
      "nested": {
        "path": "workExpList"
      },
      "aggs": {
        "position": {
          "terms": {
            "field": "workExpList.position.keyword", //使用keyword原始值
            "size":10000 //聚合结果的数量
          }
        }
      }
    }
  },
  "from": 0,
  "size": 0,
  "sort": []
}
```

结果:

```
{
  "took": 228,
  "timed_out": false,
  "_shards": {
    "total": 5,
    "successful": 5,
    "skipped": 0,
    "failed": 0
  },
  "hits": {
    "total": ****5679,
    "max_score": 0,
    "hits": []
  },
  "aggregations": {
    "workExpList": {
      "doc_count": ***6109,
      "position": {
        "doc_count_error_upper_bound": 7416,
        "sum_other_doc_count": ***9921,
        "buckets": [
          {
            "key": "",
            "doc_count": ***012
          },
          {
            "key": "销售代表",
            "doc_count": 110544
          },
          {
            "key": "软件工程师",
            "doc_count": 50842
          },
          {
            "key": "销售经理",
            "doc_count": 45795
          },
          .......
          {
            "key": "会计",
            "doc_count": 23434
          },
          {
            "key": "产品经理",
            "doc_count": 22868
          },
          {
            "key": "行政专员/助理",
            "doc_count": 18841
          },
          {
            "key": "项目经理",
            "doc_count": 17664
          }
        ]
      }
    }
  }
}
```

### 大数据量搜索处理

ES分页查询默认限制最多查询10000条
数据量太大的查询涉及到深度排序问题，性能较差。
大数据量通常使用scan来做迭代查询处理

```
import traceback
from elasticsearch.helpers import scan
from eager_client import client

def scan_search():
    try:
        """
        使用游标，避免10000条记录限制
        :return:
        """
        body = {
            "query": {
                "range": {
                    "storageTime": {
                        "gte": start_timestamp,
                        "lte": end_timestamp
                    }
                }
            },
            "sort": [{"_doc": {"order": "asc"}}],  # 用_doc表明唯一标志，用"_id"不行
        }
        test_es = client('test')
        results = scan(test_es, query=body, scroll='10m', index="your_index", doc_type="your_type")
        count = 0
        total = 0
        for hit in results:
            try:
                total += 1
                content = hit["_source"]
                # 处理content
                # 无需处理的跳过
                count += 1
                if count % 10 == 0:
                    print(".", end="")
            except Exception as e:
                print(e)
                print(traceback.format_exc())

        print("\n[%s - %s] handled=%s, total=%s" % (start_time, end_time, count, total))
    except:
        print("\n[%s - %s] failed:" % (start_time, end_time))
        print(traceback.format_exc())
```
