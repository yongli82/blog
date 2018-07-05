---
title: 使用ElasticSearch搭建文章搜索引擎
date: 2018-07-05 12:00
tags: 基础技术
categories: 基础技术
---

# 安装

环境 Ubuntu 16.04 

安装文档:https://www.elastic.co/guide/en/elasticsearch/reference/current/deb.html

```
apt-get install openjdk-8-jdk

wget -qO - https://artifacts.elastic.co/GPG-KEY-elasticsearch | apt-key add -
apt-get install apt-transport-https

echo "deb https://artifacts.elastic.co/packages/6.x/apt stable main" |  tee -a /etc/apt/sources.list.d/elastic-6.x.list

apt-get update &&  apt-get install elasticsearch
```

修改配置文件 `/etc/elasticsearch/elasticsearch.yml`

```
# ---------------------------------- Cluster -----------------------------------
#
# Use a descriptive name for your cluster:
#
cluster.name: elastic
#
# ---------------------------------- Network -----------------------------------
#
# Set the bind address to a specific IP (IPv4 or IPv6):
#
network.host: 0.0.0.0
#
# Set a custom port for HTTP:
#
http.port: 9200
#
```

# 启动

Running Elasticsearch with `systemdedit`

To configure Elasticsearch to start automatically when the system boots up, run the following commands:

```
systemctl daemon-reload
systemctl enable elasticsearch.service
```

Elasticsearch can be started and stopped as follows:

```
systemctl start elasticsearch.service
systemctl stop elasticsearch.service
systemctl restart elasticsearch.service
```

访问: `http://ip:9200/`

```
lsof -i:9200
```

日志：
```
journalctl --unit elasticsearch

journalctl --unit elasticsearch --since  "2018-07-01 00:00:00"
```

# 安装中文分词器


[IK中文分词器](https://github.com/medcl/elasticsearch-analysis-ik)

[Elasticsearch 默认分词器和中分分词器之间的比较及使用方法](https://zhuanlan.zhihu.com/p/29183128)
 
 [ElasticSearch 6.x 学习笔记：4.IK分词器插件](https://blog.csdn.net/chengyuqiang/article/details/78991570)
 
 
 IK分词器地址 ： https://github.com/medcl/elasticsearch-analysis-ik/releases
 
 ```
 cd /usr/share/elasticsearch
 
 ./bin/elasticsearch-plugin install https://github.com/medcl/elasticsearch-analysis-ik/releases/download/v6.3.0/elasticsearch-analysis-ik-6.3.0.zip
 ```
 
####  ik_max_word 和 ik_smart 什么区别?
 
> ik_max_word: 会将文本做最细粒度的拆分，比如会将“中华人民共和国国歌”拆分为“中华人民共和国,中华人民,中华,华人,人民共和国,人民,人,民,共和国,共和,和,国国,国歌”，会穷尽各种可能的组合；

> ik_smart: 会做最粗粒度的拆分，比如会将“中华人民共和国国歌”拆分为“中华人民共和国,国歌”。


# Head插件（Chrome插件）

https://chrome.google.com/webstore/detail/elasticsearch-head/ffmkiejjmecolpfloofpjologoblkegm

![image](https://note.youdao.com/yws/public/resource/89fd8107d2eb24f39dcb46930ab604ab/xmlnote/093D56EBF8A043579EC35967DB663D12/3564)

# 创建文章索引

### 文章结构

```
{
    "id": 10000,
    "url": "http://www......",
    "site": "site name",
    "title": "a notice title",
    "content": "a notice content .............. very large",
    "publishTime": "2018-06-01 00:00:00"
}
```

输入关键字，搜索title和content两个字段，按PublishTime倒序排列。

字段用中文分词。

操作步骤参考 
[IK中文分词器](https://github.com/medcl/elasticsearch-analysis-ik)

### 创建索引

索引名称`article`

```
curl -XPUT http://localhost:9200/article
```
输出

```
{"acknowledged":true,"shards_acknowledged":true,"index":"article"}
```

### 创建映射

映射名称 `policy`

```
curl -XPOST http://localhost:9200/article/policy/_mapping -H 'Content-Type:application/json' -d'
{
    "properties": {
        "content": {
            "type": "text",
            "analyzer": "ik_max_word",
            "search_analyzer": "ik_max_word"
        },
        "title": {
            "type": "text",
            "analyzer": "ik_max_word",
            "search_analyzer": "ik_max_word",
            "fields": {
                "raw": {
                    "type": "keyword",
                    "ignore_above": 256
                }
            }
        },
        "id":{
            "type": "long"
        },
        "url":{
            "type": "keyword"
        },
        "site":{
            "type": "text",
            "analyzer": "ik_max_word",
            "search_analyzer": "ik_max_word",
            "fields": {
                "raw": {
                    "type": "keyword",
                    "ignore_above": 256
                }
            }
        },
        "publishTime":{
            "type": "date",
            "format": "yyyy-MM-dd HH:mm:ss"
        }
    }
}'
```

输出:

```
{"acknowledged":true}
```

### 查看索引信息

`curl http://localhost:9200/_mapping?pretty=true`

输出:

```
{
  "article" : {
    "mappings" : {
      "policy" : {
        "properties" : {
          "content" : {
            "type" : "text",
            "analyzer" : "ik_max_word"
          },
          "id" : {
            "type" : "long"
          },
          "publishTime" : {
            "type" : "date",
            "format" : "yyyy-MM-dd HH:mm:ss"
          },
          "site" : {
            "type" : "text",
            "fields" : {
              "raw" : {
                "type" : "keyword",
                "ignore_above" : 256
              }
            },
            "analyzer" : "ik_max_word"
          },
          "title" : {
            "type" : "text",
            "fields" : {
              "raw" : {
                "type" : "keyword",
                "ignore_above" : 256
              }
            },
            "analyzer" : "ik_max_word"
          },
          "url" : {
            "type" : "keyword"
          }
        }
      }
    }
  }
}
```

### 增加数据

```
curl -XPUT http://localhost:9200/article/policy/1 -H 'Content-Type:application/json' -d'
{
    "id": 100,
    "url": "http://www.mofcom.gov.cn/article/b/c/201806/20180602755321.shtml",
    "site": "商务部",
    "title": "商务部公告2018年第47号 关于艾德凡斯树脂和化学品责任有限公司继承霍尼韦尔树脂和化学品责任有限公司在锦纶6切片反倾销措施和己内酰胺反倾销措施中所适用税率的公告",
    "content": "【发布单位】中华人民共和国商务部【发布文号】公告2018年第47号【发布日期】2018-6-8【实施日期】2018-6-9\n\n　　2010年4月21日，中华人民共和国商务部（以下简称商务部）发布2010年第15号公告，决定对原产于美国、欧盟、俄罗斯和台湾地区的进口锦纶6切片征收反倾销税。2016年4月21日，商务部发布2016年第4号公告，决定维持该反倾销措施，为期5年。其中，美国的霍尼韦尔树脂和化学品责任有限公司在该反倾销案中适用的反倾销税率为36.2%，其他美国公司适用的反倾销税率为96.5%。\n　　2011年10月18日，商务部发布2011年第68号公告，决定对原产于欧盟和美国的进口己内酰胺征收反倾销税。2017年10月21日，商务部发布2017年第53号公告，决定维持该反倾销措施，为期5年。其中，美国的霍尼韦尔树脂和化学品责任有限公司在该反倾销案中适用的反倾销税率为3.6%，其他美国公司适用的反倾销税率为24.2%。\n　　2017年12月27日，美国的艾德凡斯树脂和化学品责任有限公司向商务部提交申请，称为了上市，霍尼韦尔树脂和化学品责任有限公司的名称已经变更为艾德凡斯树脂和化学品责任有限公司，请求由变更后的公司继承原公司在锦纶6　切片反倾销措施、己内酰胺反倾销措施中所适用的反倾销税率，并提交了股东决议、更名前后的公司章程、注册文件、管理人员情况、生产能力、原材料供应商和销售客户信息，中华人民共和国驻美国大使馆的认证文件等相关证明材料。\n　　商务部就上述申请事宜分别通知了中国大陆锦纶6切片产业和己内酰胺产业。在规定时间内，相关产业未提出异议。\n　　经审查，商务部认为，现有证据材料表明，霍尼韦尔树脂和化学品责任有限公司名称变更符合其相关法律规定，公司名称变更前后关于锦纶6切片、己内酰胺的经营管理、生产能力、供应商关系和客户基础等均未发生变化。\n　　据此，商务部决定：\n　　一、由艾德凡斯树脂和化学品责任有限公司（AdvanSix Resins & Chemicals LLC）继承霍尼韦尔树脂和化学品责任有限公司（Honeywell Resins & Chemicals LLC）在锦纶6切片反倾销措施中所适用的36.2%的反倾销税率及其他权利义务。以霍尼韦尔树脂和化学品责任有限公司（HoneywellResins &amp; Chemicals LLC）名称向中国大陆出口的锦纶6切片产品，适用锦纶6切片反倾销措施中其他美国公司96.5%的反倾销税率。\n　　二、由艾德凡斯树脂和化学品责任有限公司（AdvanSix Resins & Chemicals LLC）继承霍尼韦尔树脂和化学品责任有限公司（Honeywell Resins & Chemicals LLC）在己内酰胺反倾销措施中所适用的3.6%的反倾销税率及其他权利义务。以霍尼韦尔树脂和化学品责任有限公司（HoneywellResins & Chemicals LLC）名称向中国大陆出口的己内酰胺产品，适用己内酰胺反倾销措施中其他美国公司24.2%的反倾销税率。\n　　本公告自2018年6月9日起执行。\n商 务 部2018年6月8日\n \n",
    "publishTime": "2018-06-08 09:22:41"
}'
```


输出:

```
{"_index":"article","_type":"policy","_id":"1","_version":1,"result":"created","_shards":{"total":2,"successful":1,"failed":0},"_seq_no":0,"_primary_term":1}
```

### 查看数据记录

```
curl -XGET http://localhost:9200/article/policy/1
```

### 查询

```
curl -XPOST http://localhost:9200/article/policy/_search  -H 'Content-Type:application/json' -d'
{
    "query" : { "match" : { "content" : "反倾销"}},
    "highlight" : {
        "pre_tags" : ["<tag1>", "<tag2>"],
        "post_tags" : ["</tag1>", "</tag2>"],
        "fields" : {
            "content" : {}
        }
    }
}
'
```

输出:

```
{
   "took":10,
   "timed_out":false,
   "_shards":{
      "total":5,
      "successful":5,
      "skipped":0,
      "failed":0
   },
   "hits":{
      "total":1,
      "max_score":1.1982318,
      "hits":[
         {
            "_index":"article",
            "_type":"policy",
            "_id":"1",
            "_score":1.1982318,
            "_source":{
               "id":100,
               "url":"http://www.mofcom.gov.cn/article/b/c/201806/20180602755321.shtml",
               "site":"商务部",
               "title":"商务部公告2018年第47号 关于艾德凡斯树脂和化学品责任有限公司继承霍尼韦尔树脂和化学品责任有限公司在锦纶6切片反倾销措施和己内酰胺反倾销措施中所适用税率的公告",
               "content":"【发布单位】中华人民共和国商务部【发布文号】公告2018年第47号【发布日期】2018-6-8【实施日期】2018-6-9\n\n　　2010年4月21日，中华人民共和国商务部（以下简称商务部）发布2010年第15号公告，决定对原产于美国、欧盟、俄罗斯和台湾地区的进口锦纶6切片征收反倾销税。2016年4月21日，商务部发布2016年第4号公告，决定维持该反倾销措施，为期5年。其中，美国的霍尼韦尔树脂和化学品责任有限公司在该反倾销案中适用的反倾销税率为36.2%，其他美国公司适用的反倾销税率为96.5%。\n　　2011年10月18日，商务部发布2011年第68号公告，决定对原产于欧盟和美国的进口己内酰胺征收反倾销税。2017年10月21日，商务部发布2017年第53号公告，决定维持该反倾销措施，为期5年。其中，美国的霍尼韦尔树脂和化学品责任有限公司在该反倾销案中适用的反倾销税率为3.6%，其他美国公司适用的反倾销税率为24.2%。\n　　2017年12月27日，美国的艾德凡斯树脂和化学品责任有限公司向商务部提交申请，称为了上市，霍尼韦尔树脂和化学品责任有限公司的名称已经变更为艾德凡斯树脂和化学品责任有限公司，请求由变更后的公司继承原公司在锦纶6　切片反倾销措施、己内酰胺反倾销措施中所适用的反倾销税率，并提交了股东决议、更名前后的公司章程、注册文件、管理人员情况、生产能力、原材料供应商和销售客户信息，中华人民共和国驻美国大使馆的认证文件等相关证明材料。\n　　商务部就上述申请事宜分别通知了中国大陆锦纶6切片产业和己内酰胺产业。在规定时间内，相关产业未提出异议。\n　　经审查，商务部认为，现有证据材料表明，霍尼韦尔树脂和化学品责任有限公司名称变更符合其相关法律规定，公司名称变更前后关于锦纶6切片、己内酰胺的经营管理、生产能力、供应商关系和客户基础等均未发生变化。\n　　据此，商务部决定：\n　　一、由艾德凡斯树脂和化学品责任有限公司（AdvanSix Resins & Chemicals LLC）继承霍尼韦尔树脂和化学品责任有限公司（Honeywell Resins & Chemicals LLC）在锦纶6切片反倾销措施中所适用的36.2%的反倾销税率及其他权利义务。以霍尼韦尔树脂和化学品责任有限公司（HoneywellResins &amp; Chemicals LLC）名称向中国大陆出口的锦纶6切片产品，适用锦纶6切片反倾销措施中其他美国公司96.5%的反倾销税率。\n　　二、由艾德凡斯树脂和化学品责任有限公司（AdvanSix Resins & Chemicals LLC）继承霍尼韦尔树脂和化学品责任有限公司（Honeywell Resins & Chemicals LLC）在己内酰胺反倾销措施中所适用的3.6%的反倾销税率及其他权利义务。以霍尼韦尔树脂和化学品责任有限公司（HoneywellResins & Chemicals LLC）名称向中国大陆出口的己内酰胺产品，适用己内酰胺反倾销措施中其他美国公司24.2%的反倾销税率。\n　　本公告自2018年6月9日起执行。\n商 务 部2018年6月8日\n \n",
               "publishTime":"2018-06-08 09:22:41"
            },
            "highlight":{
               "content":[
                  "其中，美国的霍尼韦尔树脂和化学品责任有限公司在该<tag1>反倾销</tag1>案中适用的<tag1>反倾销</tag1>税率为36.2%，其他美国公司适用的<tag1>反倾销</tag1>税率为96.5%。\n　　",
                  "2011年10月18日，商务部发布2011年第68号公告，决定对原产于欧盟和美国的进口己内酰胺征收<tag1>反倾销</tag1>税。2017年10月21日，商务部发布2017年第53号公告，决定维持该<tag1>反倾销</tag1>措施，为期5年。",
                  "其中，美国的霍尼韦尔树脂和化学品责任有限公司在该<tag1>反倾销</tag1>案中适用的<tag1>反倾销</tag1>税率为3.6%，其他美国公司适用的<tag1>反倾销</tag1>税率为24.2%。\n　　",
                  "36.2%的<tag1>反倾销</tag1>税率及其他权利义务。",
                  "3.6%的<tag1>反倾销</tag1>税率及其他权利义务。"
               ]
            }
         }
      ]
   }
}

```


## 在Java程序中使用ElasticSearch

SpringBoot应用中可以使用Spring-data-ElasticSearch来进行操作

https://docs.spring.io/spring-data/elasticsearch/docs/current/reference/html/

https://github.com/spring-projects/spring-data-elasticsearch


### 配置

如下配置为JHipster中的默认配置

#### 依赖
`build.gradle`

```
    compile "org.springframework.boot:spring-boot-starter-data-elasticsearch"
    // needed to get around elasticsearch stacktrace about jna not found
    // https://github.com/elastic/elasticsearch/issues/13245
    compile "net.java.dev.jna:jna"
```

#### Java Configuration

```
package com.policy.collection.config;

import com.fasterxml.jackson.databind.DeserializationFeature;
import com.fasterxml.jackson.databind.ObjectMapper;
import org.elasticsearch.client.Client;
import org.springframework.boot.autoconfigure.condition.ConditionalOnProperty;
import org.springframework.boot.autoconfigure.data.elasticsearch.ElasticsearchProperties;
import org.springframework.boot.context.properties.EnableConfigurationProperties;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.data.elasticsearch.core.ElasticsearchTemplate;
import org.springframework.data.elasticsearch.core.EntityMapper;
import org.springframework.http.converter.json.Jackson2ObjectMapperBuilder;

import java.io.IOException;

@Configuration
@EnableConfigurationProperties(ElasticsearchProperties.class)
@ConditionalOnProperty("spring.data.elasticsearch.cluster-nodes")
public class ElasticsearchConfiguration {

    @Bean
    public ElasticsearchTemplate elasticsearchTemplate(Client client, Jackson2ObjectMapperBuilder jackson2ObjectMapperBuilder) {
        return new ElasticsearchTemplate(client, new CustomEntityMapper(jackson2ObjectMapperBuilder.createXmlMapper(false).build()));
    }

    public class CustomEntityMapper implements EntityMapper {

        private ObjectMapper objectMapper;

        public CustomEntityMapper(ObjectMapper objectMapper) {
            this.objectMapper = objectMapper;
            objectMapper.configure(DeserializationFeature.FAIL_ON_UNKNOWN_PROPERTIES, false);
            objectMapper.configure(DeserializationFeature.ACCEPT_SINGLE_VALUE_AS_ARRAY, true);
        }

        @Override
        public String mapToString(Object object) throws IOException {
            return objectMapper.writeValueAsString(object);
        }

        @Override
        public <T> T mapToObject(String source, Class<T> clazz) throws IOException {
            return objectMapper.readValue(source, clazz);
        }
    }
}
```

appplication.yml

```
spring:
    data:
        elasticsearch:
            cluster-name: elastic
            cluster-nodes: localhost:9300
```

#### 创建ElasticsearchRepository接口

```
package com.policy.collection.dto;

import lombok.Data;
import org.springframework.data.elasticsearch.annotations.Document;

import java.time.ZonedDateTime;

@Data
@Document(indexName = "article", type = "policy")
public class PolicyArticle {
    private Long id;
    private String url;
    private String site;
    private String title;
    private String content;
    private ZonedDateTime publishTime;
}
```

```
package com.policy.collection.repository.search;

import com.policy.collection.dto.PolicyArticle;
import org.springframework.data.elasticsearch.repository.ElasticsearchRepository;

/**
 * Spring Data Elasticsearch repository for the PolicyArticle entity.
 */
public interface PolicyArticleSearchRepository extends ElasticsearchRepository<PolicyArticle, Long> {
}

```

其中`ElasticsearchRepository`具有如下搜索方法，并且它继承了CRUD功能。
```
@NoRepositoryBean
public interface ElasticsearchRepository<T, ID extends Serializable> extends ElasticsearchCrudRepository<T, ID> {

    <S extends T> S index(S entity);

    Iterable<T> search(QueryBuilder query);

    Page<T> search(QueryBuilder query, Pageable pageable);

    Page<T> search(SearchQuery searchQuery);

    Page<T> searchSimilar(T entity, String[] fields, Pageable pageable);

    void refresh();

    Class<T> getEntityClass();
}

```

### 增加和更新数据

```
package com.policy.collection.repository.search;

import com.google.common.collect.Lists;
import com.policy.collection.TestBase;
import com.policy.collection.domain.ContentPage;
import com.policy.collection.dto.PolicyArticle;
import com.policy.collection.repository.ContentPageRepository;
import com.policy.collection.repository.PageSourceRepository;
import com.policy.collection.utils.DateUtil;
import org.apache.commons.collections4.CollectionUtils;
import org.apache.commons.lang3.StringUtils;
import org.elasticsearch.index.query.QueryBuilder;
import org.junit.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.PageRequest;
import org.springframework.data.domain.Sort;
import org.elasticsearch.index.query.*;

import java.util.List;

public class PolicyArticleSearchRepositoryTest extends TestBase {

    @Autowired
    private PolicyArticleSearchRepository searchRepository;

    @Autowired
    private ContentPageRepository contentPageRepository;

    @Autowired
    private PageSourceRepository pageSourceRepository;


    @Test
    public void addData() {
        int pageNo = 0;
        int pageSize = 100;
        while (true) {
            Page<ContentPage> page = contentPageRepository.findAll(PageRequest.of(pageNo, pageSize, Sort.Direction.ASC, "id"));
            List<ContentPage> list = page.getContent();
            if (CollectionUtils.isEmpty(list)) {
                break;
            }

            pageNo++;

            List<PolicyArticle> policyArticles = Lists.newArrayList();
            for (ContentPage contentPage : list) {
                PolicyArticle article = new PolicyArticle();
                article.setId(contentPage.getId());
                article.setUrl(contentPage.getUrl());
                article.setTitle(contentPage.getTitle());
                article.setContent(contentPage.getTextContent());
                String publishTime = DateUtil.format(contentPage.getPublishTime());
                if(StringUtils.isNotBlank(publishTime)) {
                    article.setPublishTime(publishTime);
                }
                Long sourceId = contentPage.getSourceId();
                pageSourceRepository.findById(sourceId).ifPresent(source -> article.setSite(source.getSite()));
                policyArticles.add(article);
            }

            searchRepository.saveAll(policyArticles);
            logger.info("Save articles to es with size={}", policyArticles.size());
        }
    }
}

```


### 搜索

```
    @Test
    public void search(){
        QueryBuilder builder = new QueryStringQueryBuilder("content:反倾销");
        Page<PolicyArticle> page = searchRepository.search(builder, PageRequest.of(0, 10));
        logger.info("page={}", page);
        for (PolicyArticle article : page) {
            logger.info("article={}", article);
        }
    }
```



