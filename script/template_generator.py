#!/usr/bin/env python
# -*- coding:utf-8 -*-

import re
from collections import OrderedDict

count = 0
category = ""

category_map = OrderedDict()
titles = []

with open("2019-01.txt") as f:
    lines = f.readlines()
    for line in lines:
        line = line.strip()
        if not line:
            continue
        if line.startswith("#"):
            if len(titles) > 0:
                category_map[category] = titles
            title, category = re.findall(r"#(.*)\[(.*)\]", line)[0]
            print(category)
            titles = []
        else:
            title = line
        titles.append(title)

    category_map[category] = titles
    
    print(category_map)


template = """
---
title: %(title)s
date: 2019-01-01 00:00
tags: %(category)s
categories: 基础技术
---

# %(title)s

TODO 


--- 

# 专题文章

%(link)s

""".strip()

for category, titles in category_map.items():
    links = []
    count = 0
    for title in titles:
        path = "/%s_%s" % (category, count)
        links.append("[%s](%s)" % (title, path))
        count += 1
    link = "\n".join(links)

    count = 0
    for title in titles:
        content = template % {"title": title, "link": link, "category": category}
        path = "/%s_%s.md" % (category, count)
        posts_path = "/Users/yangyongli/Blogs/yongli82/source/_posts" + path
        print("=" * 80)
        print(posts_path)
        print(content)
        print()

        with open(posts_path, "w") as f:
            f.write(content)
            f.flush()
        
        count += 1

