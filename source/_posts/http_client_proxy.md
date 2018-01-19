---
title: SpringMVC后端代理获取图片文件，解决跨域问题
date: 2018-01-19
tags: SpringMVC
categories: 代码片段
---

要解决的问题:
-----------

前端用Canvas合成图片，但是如果素材图片是外域，会报跨域问题。
在不能修改图片服务器的`Access-Control-Allow-Origin`情况下，采用通过后端代理访问的方式来解决该问题。

代码片段

```
    <groupId>org.apache.httpcomponents</groupId>
    <artifactId>httpclient</artifactId>
    <version>4.5.4</version>
```

```java

import lombok.extern.slf4j.Slf4j;
import org.apache.commons.io.IOUtils;
import org.apache.http.HttpEntity;
import org.apache.http.HttpResponse;
import org.apache.http.client.methods.HttpGet;
import org.apache.http.impl.client.CloseableHttpClient;
import org.apache.http.impl.client.HttpClientBuilder;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.*;

import javax.servlet.ServletOutputStream;
import javax.servlet.http.HttpServletResponse;
import java.io.IOException;
import java.io.InputStream;
import java.net.URLDecoder;
import java.util.Map;
```


```java
@RequestMapping(value = "/proxy", method = {RequestMethod.GET, RequestMethod.POST})
    public void fileProxy(@RequestParam("target") String target, HttpServletResponse httpResponse) {
        CloseableHttpClient client = null;
        InputStream inputStream = null;
        try {
            target = URLDecoder.decode(target, "UTF-8");
            client = HttpClientBuilder.create().build();
            HttpGet request = new HttpGet(target);
            HttpResponse response = client.execute(request);
            HttpEntity entity = response.getEntity();
            if (null != entity) {
                httpResponse.setContentType(entity.getContentType().getValue());
                httpResponse.addHeader("Access-Control-Allow-Origin","*");
                inputStream = entity.getContent();
                ServletOutputStream outputStream = httpResponse.getOutputStream();
                IOUtils.copy(inputStream, outputStream);
            }
        } catch (IOException e) {
            log.error("Failed to proxy url:" + target, e);
        } finally {
            IOUtils.closeQuietly(inputStream);
            IOUtils.closeQuietly(client);
        }
    }

```