---
title: Django 项目集成xadmin
date: 2016-06-24 17:26:51
tags: Django
categories: Python
---

django自带的admin很不错，但是界面风格当下流行的`bootstrap`风格不一致。既然前台使用了`bootstrap`风格的样式，那么后台admin也期望很有类似的风格。[`django-admin-bootstrapped`](https://github.com/django-admin-bootstrapped/django-admin-bootstrapped), [grappelli](https://github.com/sehmaschine/django-grappelli), [djangosuit](http://djangosuit.com/)都是admin的bootstrap风格封装。但`xadmin`更为激进，重新打造了一套`admin`系统，使用`xadmin.py`文件来注册需要管理的`model`。

xadmin的主要特性：

* 兼容 Django Admin
* 使用 Bootstrap 作为 UI 框架
* 编辑页面灵活布局
* 主页面仪表盘及小部件
* 过滤器强化
* 数据导出
* 强大的插件机制
项目主页：[http://sshwsfc.github.io/django-xadmin/](http://sshwsfc.github.io/django-xadmin/)
在线demo: [http://demo.xadmin.io/](http://demo.xadmin.io/)

参考： [Django1.9开发博客（14）- 集成Xadmin](http://www.pycoding.com/2015/04/21/simpleblog-14.html)

在Django项目中引入xadmin的步骤：
1、 引入xadmin依赖包
通常采用如下方式：
```
pip install django-xadmin
pip install django-reversion
```
因为版本的原因，可以使用参考文档中的方式： 在requirements.txt中添加如下的依赖，注意：要用到xadmin的django1.9分支
```
django-reversion==1.8.5
xlwt==0.7.5
git+https://github.com/sshwsfc/django-xadmin.git@django1.9
```
在参考项目[vmaig_blog](https://github.com/billvsme/vmaig_blog/tree/xadmin) 中为了解决xadmin的一些BUG，作者将xadmin整个源码包拷贝到工程中，为了一些定制化的修改，在xadmin未稳定的时候，这也是一种合适的方式。

2、在`settings.py`中增加xadmin配置
```
ADMINS = (
    # ('Your Name', 'your_email@example.com'),
)
MANAGERS = ADMINS

# Application definition
INSTALLED_APPS = (
    # ...
    'xadmin',
    'crispy_forms',
    'reversion',
    # ...
)
```
3、在`urls.py`中增加`xadmin`管理页面链接
```
from django.conf.urls import patterns, include, url
# version模块自动注册需要版本控制的 Model
from xadmin.plugins import xversion
import xadmin
xversion.register_models()

urlpatterns = patterns(
    '',
    url(r'xadmin/', include(xadmin.site.urls), name='xadmin'),
    # ...
)
```

4、 使用xadmin管理models，在app中创建`adminx.py`文件

有首页，Dashboard和普通的model管理页面等。
vmaig_blog中的示例：
```
import xadmin
from xadmin.layout import Main, Fieldset

class CategoryAdmin(object):
    search_fields = ('name',)
    list_filter = ('status','create_time')
    list_display = ('name','parent','rank','status')
    fields = ('name','parent','rank','status')



class ArticleAdmin(object):
    search_fields = ('title','summary')
    list_filter = ('status','category','is_top','create_time','update_time','is_top')
    list_display = ('title','category','author','status','is_top','update_time')

    form_layout = (
        Fieldset(u'基本信息',
                    'title','en_title','img','category','tags','author','is_top','rank','status'
                    ),
        Fieldset(u'内容',
                    'content'
                    ),
        Fieldset(u'摘要',
                    'summary'
                    ),
        Fieldset(u'时间',
                    'pub_time'
                    )
    )

class GlobalSetting(object):
    site_title = u"Vmaig后台管理"
    site_footer = u"vmaig.com"


class MainDashboard(object):
    widgets = [
        [
            {"type": "html", "title": "欢迎",
            "content": "<h3> Welcome to Vmaig! </h3>\
                        <p>欢迎来到 Vmaig ,如果有任何问题可以加:<br/>\
                        我的QQ：994171686<br/>\
                        QQ群：458788510 <br/><br/>\
                        后台中，可以<br/>\
                        通过“轮播”添加首页的轮播<br/>\
                        通过“导航条”添加首页nav中的项目<br/>\
                        通过“专栏” 添加博客专栏（可以和导航条结合起来）<br/>\
                        通过“资讯” 添加转载的新闻<br/>\
                        通过“分类” “文章” 添加分类跟文章<br/>\
                        通过“用户” 对用户进行操作<br/>\
                        <h3>注意</h3>\
                        左边的Revisions没用，不用管它<br/>\
                        首页的便签云中的内容，在后台不能修改。 请修改 blog/templates/blog/widgets/tags_cloud.html 中的 tags数组的内容。<br/><br/>"},
        ],
    ]


xadmin.site.register(xadmin.views.CommAdminView,GlobalSetting)
xadmin.site.register(xadmin.views.website.IndexView, MainDashboard)

xadmin.site.register(Category,CategoryAdmin)
xadmin.site.register(Article,ArticleAdmin)
```
参考文档中的示例：
```
#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
Topic: adminx定制类
Desc :
"""
import xadmin
import xadmin.views as xviews
from .models import Tag, Category, Post, Comment, Evaluate, Page
from xadmin.layout import Main, TabHolder, Tab, Fieldset, Row, Col, AppendedText, Side

class BaseSetting(object):
    enable_themes = True
    use_bootswatch = True
xadmin.site.register(xviews.BaseAdminView, BaseSetting)


class AdminSettings(object):
    # 设置base_site.html的Title
    site_title = '博客管理后台'
    # 设置base_site.html的Footer
    site_footer = 'Winhong Inc.'
    menu_style = 'default'

    # 菜单设置
    def get_site_menu(self):
        return (
            {'title': '博客管理', 'perm': self.get_model_perm(Page, 'change'), 'menus': (
                {'title': '所有页面', 'icon': 'fa fa-vimeo-square'
                    , 'url': self.get_model_url(Page, 'changelist')},
                {'title': '分类目录', 'icon': 'fa fa-vimeo-square'
                    , 'url': self.get_model_url(Category, 'changelist')},
            )},
        )
xadmin.site.register(xviews.CommAdminView, AdminSettings)

xadmin.site.register(Page)
xadmin.site.register(Category)
# xadmin.site.register(Tag)
# xadmin.site.register(Post)
# xadmin.site.register(Comment)
# xadmin.site.register(Evaluate)
```

5、 模板页面定制
拷贝xadmin中的模板文件到项目对应的template目录下，进行修改。


遇到的问题：
启动时：

按照vmaig_blog的方式，修改xadmin的models.py, 增加判断条件`and django.VERSION[1] < 7`
```
if django.VERSION[1] > 4 and django.VERSION[1] < 7:
    AUTH_USER_MODEL = django.contrib.auth.get_user_model()
else:
    AUTH_USER_MODEL = getattr(settings, 'AUTH_USER_MODEL', 'auth.User')
```
