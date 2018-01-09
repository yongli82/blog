---
title: JHipster学习笔记1
tags: JHipster, SpringMVC
date: 2016/08/21
categories: 框架学习
---

### JHipster 是一个 Yeoman generator, 用于创建基于 Spring Boot + AngularJS 的项目。
JHipster 目标是为开发者生成一个完整的现代 web 应用用作启动框架, 它结合了:
- 基于 Spring Boot 的高效稳健的 Java 服务端
- 高端大气，移动优先的 AngularJS ＋ Bootstrap 前端
- 强大的工作流，结合 Yeoman, Bower, Gulp 和 Maven 等来构建项目

### JHipster 快速开始
（假定你已经安装好了 Java, Git, Node.js, Bower, Yeoman 和 Gulp）
安装 JHipster `npm install -g generator-jhipster`
创建一个新的目录并切换到这个目录下 `mkdir myApp && cd myApp`
运行 JHipster 并根据屏幕提示进行操作 `yo jhipster`
用 JDL Studio 为你的数据建模，并下载生成的 `jhipster-jdl.jh `文件
通过这个命令导入数据模型 `yo jhipster:import-jdl jhipster-jdl.jh`

### 在中华局域网开发的一些加速Tips
##### 1.Gradle
（1）使用镜像
修改`gradle-wrapper.properties`中的`distributionUrl`路径

```
#Mon Sep 14 23:06:20 CST 2015
distributionBase=GRADLE_USER_HOME
distributionPath=wrapper/dists
zipStoreBase=GRADLE_USER_HOME
zipStorePath=wrapper/dists
distributionUrl=https\://services.gradle.org/distributions/gradle-2.3-all.zip
```

把`https\://services.gradle.org/distributions/gradle-2.3-all.zip` 替换成对应的镜像地址。

TODO: 镜像地址暂时未找到。


（2）在开发环境设置deamon模式，加快编译速度
方式1： 修改项目下的gradle.properties文件, 将`#org.gradle.daemon=true`取消注释。
这种方式不要应用在生产环境打包或CI环境，可能会造成构建不干净。

```
## below are some of the gradle performance improvement settings that can be used as required, these are not enabled by default

## The Gradle daemon aims to improve the startup and execution time of Gradle.
## When set to true the Gradle daemon is to run the build.
## TODO: disable daemon on CI, since builds should be clean and reliable on servers
## un comment the below line to enable the daemon

org.gradle.daemon=true
```
方式2： 在自己的用户目录下创建 ~/.gradle/gradle.properties, 设置`org.gradle.daemon=true`


##### 2.maven仓库

参考 [Gradle 修改 Maven 仓库地址](https://yrom.net/blog/2015/02/07/change-gradle-maven-repo-url/)

单个项目修改：修改项目根目录下的`build.gradle`，将`jcenter()`或者`mavenCentral()`替换掉即可：

```
allprojects {
    repositories {
        maven{ url 'http://maven.oschina.net/content/groups/public/'}
    }
}
```

全局修改: 将下面这段Copy到名为`init.gradle`文件中，并保存到 `USER_HOME/.gradle/`文件夹下即可。

```
allprojects{
    repositories {
        def REPOSITORY_URL = 'http://maven.oschina.net/content/groups/public'
        all { ArtifactRepository repo ->
            if(repo instanceof MavenArtifactRepository){
                def url = repo.url.toString()
                if (url.startsWith('https://repo1.maven.org/maven2') || url.startsWith('https://jcenter.bintray.com/')) {
                    project.logger.lifecycle "Repository ${repo.url} replaced by $REPOSITORY_URL."
                    remove repo
                }
            }
        }
        maven {
            url REPOSITORY_URL
        }
    }
}
```

init.gradle文件其实是Gradle的初始化脚本(Initialization Scripts)，也是运行时的全局配置。
更详细的介绍请参阅 http://gradle.org/docs/current/userguide/init_scripts.html


#####  3.npm
使用淘宝镜像, 设置alias
```
alias npm='npm --registry=https://registry.npm.taobao.org   --cache=~/.npm/.cache/cnpm   --disturl=https://npm.taobao.org/dist   --userconfig=~/.cnpmrc'
```
