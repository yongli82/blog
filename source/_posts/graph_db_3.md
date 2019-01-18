---
title: 3、Neo4j的Java API
date: 2019-01-01 00:00
tags: graph_db
categories: 基础技术
---

# Neo4j的Java和Python API


## Java API

### 使用流程

	1、引进依赖库
	2、配置Neo4j链接
	3、加载数据: 节点、边和属性
	4、查询数据
	5、更新数据
	6、复杂查询


### 1、引入依赖库

有多种方式在Java项目中访问Neo4j数据库

#### 1.1 Neo4j Java Driver

使用Neo4j的Java驱动，用原生方式访问独立的Neo4j服务器


```
<dependency>
    <groupId>org.neo4j.driver</groupId>
    <artifactId>neo4j-java-driver</artifactId>
    <version>1.4.4</version>
</dependency>
```

#### 1.2 Embedded Neo4j

使用嵌入式Jar，在程序JVM中运行Neo4j，内容保存本地文件中。

```
<dependency>
    <groupId>org.neo4j</groupId>
    <artifactId>neo4j</artifactId>
    <version>3.4.6</version>
</dependency>
```

#### 1.3 Spring Data Neo4j

兼容Spring Data接口 
https://neo4j.com/developer/spring-data-neo4j/

#### 其它方式

参考 https://neo4j.com/developer/java/

- Object-Graph-Mapping with Neo4j-OGM
- Using Neo4j’s Embedded Java API
- User Defined Procedures and Functions
- Extending Neo4j Server with a REST Server Extension
- Using Neo4j Server with JDBC
- Neo4j Community Drivers
- JCypher
- Groovy & Grails: Neo4j Grails Plugin
- Clojure: Neocons
- Scala: AnormCypher
- JPA: Hibernate OGM


### 2、配置Neo4j链接

从Neo4j的管理界面上获取`bolt://`链接

#### 2.1 使用Neo4j Java Driver


```
Driver driver = GraphDatabase.driver(
            "bolt://server:7687", AuthTokens.basic("neo4j", "password"));
```


https://neo4j.com/docs/driver-manual/1.7/sessions-transactions/



### 参考文档：

[1] 官网 [Using Neo4j from Java](https://neo4j.com/developer/java/)


[2] [A Guide to Neo4J with Java](https://www.baeldung.com/java-neo4j)  2018-08-25

### 示例

```
package com.demo.service.graph;

import com.demo.api.graph.Edge;
import com.demo.api.graph.GraphService;
import com.demo.api.graph.Triplet;
import com.demo.api.graph.Vertex;
import org.neo4j.driver.v1.*;
import org.neo4j.driver.v1.summary.ResultSummary;

import javax.annotation.PreDestroy;
import java.util.List;

import static org.neo4j.driver.v1.Values.parameters;

public class Neo4jGraphServiceImpl implements GraphService {

    Driver driver = GraphDatabase.driver(
            "bolt://server:7687", AuthTokens.basic("neo4j", "password"));

    /**
     * 添加节点
     * 如果已经存在，不添加新节点，计数器加一
     *
     * @param vertexType
     * @param vertexNameList
     */
    @Override
    public void addVertex(String vertexType, final List<String> vertexNameList) {
        try (Session session = driver.session()) {
            session.writeTransaction(tx -> {
                for (String vertexName : vertexNameList) {
                    String cypher = "MERGE (v:$vertexType {name: '$vertexName'}) " +
                            "on create SET v.count = 1 " +
                            "on match SET v.count = v.count + 1 " +
                            "return v";
                    cypher = cypher.replace("$vertexType", vertexType).replace("$vertexName", vertexName);
                    ResultSummary resultSummary = tx.run(cypher,
                            parameters("vertexName", vertexName)).consume();
                }
                return "success";
            });
        }
    }

    /**
     * 添加关系
     *
     * @param edgeName
     * @param vertexType
     * @param vertexNameList
     */
    @Override
    public void addEdges(String edgeName, String vertexType, List<String> vertexNameList) {
        try (Session session = driver.session()) {
            session.writeTransaction(tx -> {
                for (String vertexNameSource : vertexNameList) {
                    for (String vertexNameDest : vertexNameList) {
                        if (vertexNameSource.equals(vertexNameDest)) {
                            continue;
                        }

                        String cypher = "MATCH (source:$vertexType {name: '$vertexNameSource'})" +
                                "MATCH (dest:$vertexType {name: '$vertexNameDest'}) " +
                                " MERGE (source)-[edge:$edgeName]->(dest) " +
                                "on create SET edge.count = 1 " +
                                "on match SET edge.count = edge.count + 1 " +
                                "return edge.count";
                        cypher = cypher.replace("$vertexType", vertexType)
                                .replace("$edgeName", edgeName)
                                .replace("$vertexNameSource", vertexNameSource)
                                .replace("$vertexNameDest", vertexNameDest);
                        ResultSummary resultSummary = tx.run(cypher,
                                parameters("vertexNameSource", vertexNameSource,
                                        "vertexNameDest", vertexNameDest)).consume();

                    }
                }

                return "success";
            });
        }
    }

    /**
     * Suggest
     *
     * @param vertexType
     * @param prefix
     * @param pageSize
     * @param pageNo
     * @return
     */
    @Override
    public List<String> suggestVertexNames(String vertexType, String prefix, int pageSize, int pageNo) {
        try (Session session = driver.session()) {
            String cypher = "MATCH (a:$vertexType) " +
                    " WHERE a.name =~ '(?i)$prefix.*' " +
                    " WITH a, SIZE((a)-[]->()) as r_size " +
                    " ORDER BY SIZE(a.name) asc, r_size desc " +
                    " RETURN a, r_size " +
                    " SKIP $skipSize LIMIT $maxSize";
            int skipSize = pageNo * pageSize;
            cypher = cypher.replace("$vertexType", vertexType)
                    .replace("$prefix", prefix.replace(".", "\\.").replace("*", "\\*"))
                    .replace("$maxSize", String.valueOf(pageSize))
                    .replace("$skipSize", String.valueOf(skipSize));

            List<String> nodeNames = session.run(cypher).list(record -> {
                        String name = record.get("a").get("name", "prefix");
                        return name;
                    }
            );

            return nodeNames;
        }
    }

    /**
     * 查询关联节点
     *
     * @param vertexType
     * @param vertexName
     * @param maxSize
     * @return
     */
    @Override
    public List<Triplet> queryRelatives(String vertexType, String vertexName, int maxSize) {
        try (Session session = driver.session()) {
            String cypher = "MATCH (a:$vertexType {name: '$vertexName'})-[r]->(b:$vertexType)  " +
                    " RETURN a,r,b " +
                    " ORDER BY r.count desc,b.count desc " +
                    " LIMIT $maxSize ";
            cypher = cypher.replace("$vertexType", vertexType)
                    .replace("$vertexName", vertexName)
                    .replace("$maxSize", String.valueOf(maxSize));

            List<Triplet> triplets = session.run(cypher).list((record) -> {
                Value a = record.get("a");
                Vertex source = new Vertex(a.get("name", ""), a.get("count", 1L));
                Value b = record.get("b");
                Vertex dest = new Vertex(b.get("name", ""), b.get("count", 1L));
                Value r = record.get("r");
                Edge edge = new Edge(r.asRelationship().type(), r.get("count", 1L));
                Triplet triplet = new Triplet(source, edge, dest);
                return triplet;
            });
            return triplets;
        }
    }

    @PreDestroy
    public void preDestroy() {
        driver.close();
    }
}

```


## Python API 

参考 https://py2neo.org/v4/

```
pip install py2neo
```


```
#!/usr/bin/env python
# -*- coding:utf-8 -*-
# https://py2neo.org/v4/

from py2neo import Graph
from py2neo.ogm import GraphObject, Property, RelatedTo

graph = Graph("bolt://server:7687", user="neo4j", password="password")


class Skill(GraphObject):
    __primarylabel__ = "SKILL"
    __primarykey__ = "name"

    name = Property()
    count = Property()
    belongTo = RelatedTo("Category", "belongTo")


class Category(GraphObject):
    __primarylabel__ = "Category"
    __primarykey__ = "name"

    name = Property()


count = 0
with open("skill_keyword_count.txt") as f:
    for line in f:
        line = line.strip()
        if line:
            count += 1
            print(line)
            name, category_name, match_count = line.split("\t")
            skill = Skill()
            skill.name = name
            category = Category()
            category.name = category_name
            skill.belongTo.add(category, count=int(match_count))
            graph.merge(category)
            graph.merge(skill)
            if count % 1000 == 0:
                print(count)

```


# 专题文章

[图数据库 ](/graph_db_0)

[1、图数据库的基本概念](/graph_db_1)

[2、Neo4j的使用：安装， Cypher， 数据管理，导入导出， 前端Html，聚类](/graph_db_2)

[3、Neo4j的Java API](/graph_db_3)

[4、JanusGraph的使用: 安装，Gremlin，数据管理，导入导出，前端HTML](/graph_db_4)

[5、Gremlin的Java API](/graph_db_5)

[6、D3展示图](/graph_db_6)