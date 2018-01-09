---
title: JHipster学习笔记2
tags: JHipster, SpringMVC
date: 2016/08/22
categories: 框架学习
---

## 修改默认首页welcomePage

Jhipster的首页`index.html`是默认的入口页面，并且使用`yo jhipster:entity`等命令添加模型时，会自动修改`index.html`页面。
当我们想要使用定制的首页时，就不能使用`index.html`，需要在将`/`路由到另外一个页面，比如`home.html`。

在SpringMVC中，使用Java Config的方式，将路径路由到一个静态页面，有如下方式。

### 1 添加一个`WebMvcConfigurerAdapter`,在`addViewControllers`方法中进行`forward`映射。

```java
import org.springframework.context.annotation.Configuration;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.servlet.config.annotation.ViewControllerRegistry;
import org.springframework.web.servlet.config.annotation.WebMvcConfigurerAdapter;

@Configuration
public class ForwardConfiguration extends WebMvcConfigurerAdapter {

    @Override
    public void addViewControllers(ViewControllerRegistry registry) {
        //这个配置不生效,因为WebAutoConfiguration的配置会覆盖它
        //需要在IndexController中使用
        // @RequestMapping(value = "/")
        // public String index(ModelMap model) {
        //     return "forward:/avon.html";
        // }
        // 来覆盖自动配置
        registry.addViewController("/").setViewName("forward:/avon.html");

        //如下配置生效
        registry.addViewController("/avon").setViewName("forward:/avon.html");
    }

}

```

### 2 添加一个`Controller`, 进行映射

```java
import org.springframework.stereotype.Controller;
import org.springframework.ui.ModelMap;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.servlet.ModelAndView;

@Controller
public class IndexController {

    @RequestMapping(value = "/")
    public String index(ModelMap model) {
        return "forward:/avon.html";
    }

    @RequestMapping(value = "/admin")
    public String admin(ModelMap model) {
        return "forward:/index.html";
    }

    @RequestMapping(value = "/home")
    public String home(ModelMap model) {
        return "home";
    }
}
```

## HTML文件

在JHipster中，可以使用一个静态html页面作为前端框架，通过AngularJS加载内容。
比如一个文件`test.html`放在`webapp`目录下，可以直接用`/test.html`路径来访问。
也可以按上面的方法添加一个映射，通过`/test`来访问。

如果要使用`Thymeleaf`模板，动态返回html框架页面，需要配置`Thymeleaf`模板位置，一般是放在`resources/templates`目录下。

```java
import org.apache.commons.lang.CharEncoding;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.context.annotation.Description;
import org.thymeleaf.templateresolver.ClassLoaderTemplateResolver;

@Configuration
public class ThymeleafConfiguration {

    @SuppressWarnings("unused")
    private final Logger log = LoggerFactory.getLogger(ThymeleafConfiguration.class);

    @Bean
    @Description("Thymeleaf template resolver serving HTML 5 emails")
    public ClassLoaderTemplateResolver emailTemplateResolver() {
        ClassLoaderTemplateResolver emailTemplateResolver = new ClassLoaderTemplateResolver();
        emailTemplateResolver.setPrefix("mails/");
        emailTemplateResolver.setSuffix(".html");
        emailTemplateResolver.setTemplateMode("HTML5");
        emailTemplateResolver.setCharacterEncoding(CharEncoding.UTF_8);
        emailTemplateResolver.setOrder(1);
        return emailTemplateResolver;
    }

    @Bean
    @Description("Thymeleaf template resolver serving HTML 5 pages")
    public ClassLoaderTemplateResolver webTemplateResolver() {
        ClassLoaderTemplateResolver webTemplateResolver = new ClassLoaderTemplateResolver();
        webTemplateResolver.setPrefix("/templates/");
        webTemplateResolver.setSuffix(".html");
        webTemplateResolver.setTemplateMode("HTML5");
        webTemplateResolver.setCharacterEncoding(CharEncoding.UTF_8);
        webTemplateResolver.setOrder(1);
        return webTemplateResolver;
    }
}
```
