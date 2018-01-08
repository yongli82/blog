---
title: 创建Maven Archetype项目原型
tags: Java
date: 2016/05/30
categories: Java
---
# 创建Maven Archetype项目原型

在工作中，每个公司都有自己一套技术栈，如果创建新的项目，希望会重用已有项目的技术框架，这时可以用Maven Archetype的原型功能，快速创建项目脚手架。


参考资料:

- [Introduction to Archetypes](https://maven.apache.org/guides/introduction/introduction-to-archetypes.html)
- [Guide to Creating Archetypes](https://maven.apache.org/guides/mini/guide-creating-archetypes.html)
- [Create a Maven Archetype from an existing project](https://www.luckyryan.com/2013/02/15/create-maven-archetype-from-existing-project/)


## 从现有项目创建原型

有一个SpringMVC的Web项目，我想以此为模板，创建一个Maven项目原型，在Web项目上，运行命令
`mvn archetype:create-from-project`

生成如下内容

![](/images/generated_sources.png)

生成的模板内容里有很多不需要的代码，需要手工进行清理。
![](/images/generated_sources_java.png)

还有配置文件中的一些值需要用变量来进行替换
![](/images/generated_sources_pom.png)

生成的archetype包含模板项目中所有的文档，避免冗余，可将多余文件删除，并对其项目结构做一些整理

可将文件夹改成_rootArtifactId_，这样生成项目结构时，这个目录名称就会变成新的项目名称

如果你也需要文件或者目录名字以artifactId生成，则需要用特殊变量__artifactId__(双下划线)作为占位符



## 部署

```
# 进入到生成的archetype目录
cd target\generated-sources\archetype

# 将archetype安装到本地
mvn install

# 执行下面操作更新本地的archetype-catalog.xml
mvn archetype:crawl
```


## 使用
使用该原型创建新项目，在项目目录下执行命令：

`mvn archetype:generate -DarchetypeCatalog=local`


```
> mvn archetype:generate -DarchetypeCatalog=local

Choose archetype:
1: local -> io.springside.examples:quickstart-archetype (SpringSide :: Archetype :: QuickStart)
2: local -> com.dianping.ba:ba-es-interview-web-archetype (ba-es-interview-web-archetype)
3: local -> com.dianping:ba-finance-spring-mvc-web (ba-finance-spring-mvc-web)
Choose a number or apply filter (format: [groupId:]artifactId, case sensitive contains): : 3
Define value for property 'groupId': : com.dianping
Define value for property 'artifactId': : ba-finance-settle-outer            
Define value for property 'version':  1.0-SNAPSHOT: :
Define value for property 'package':  com.dianping: : com.dianping.settle.web.outer
Confirm properties configuration:
groupId: com.dianping
artifactId: ba-finance-settle-outer
version: 1.0-SNAPSHOT
package: com.dianping.settle.web.outer
 Y: : Y

```
