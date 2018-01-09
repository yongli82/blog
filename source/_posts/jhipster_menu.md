---
title: Jhipster 菜单管理
date: 2016-08-23
tags: JHipster, SpringMVC
categories: 框架学习
---


### 模型

![jhipster_菜单数据模型](/images/jhipster_菜单数据模型.png)

### JDL

为了[创建实体](http://jhipster.cn/creating-an-entity/)，
JHipster有一个强大的模型设计工具[jdl-studio](https://jhipster.github.io/jdl-studio/)和模型语言[jdl](http://jhipster.cn/jdl/)。

我为菜单创建的模型用jdl语言编写如下

```jdl

entity SystemModule {
    moduleCode String required maxlength(256),
    moduleName String required maxlength(256),
    moduleNameEn String required maxlength(256),
    description String required maxlength(2048),
    createdTime ZonedDateTime,
    createdBy Long,
    updatedTime ZonedDateTime,
    updatedBy Long
}

entity Menu {
    systemModuleId Long required,
    parentMenuId Long,
    resourceId Long,
    name String required maxlength(256),
    nameEn String required maxlength(256),
    tagName String required maxlength(256),
    iconClass String required maxlength(256),
    helpText String maxlength(2048),
    link String required maxlength(256),
    displayOrder Integer,
    createdTime ZonedDateTime,
    createdBy Long,
    updatedTime ZonedDateTime,
    updatedBy Long
}

relationship ManyToOne {
    Menu{systemModuleId} to SystemModule
}

relationship ManyToOne {
    Menu{parentMenuId} to Menu
}

relationship ManyToOne {
    SystemModule{createdBy} to User
}

relationship ManyToOne {
    SystemModule{updatedBy} to User
}

relationship ManyToOne {
    Menu{createdBy} to User
}

relationship ManyToOne {
    Menu{updatedBy} to User
}


// Set pagination options
paginate Menu with pagination

dto * with mapstruct

// Set service options to all except few
service all with serviceImpl

```

放到[jdl-studio](https://jhipster.github.io/jdl-studio/)中显示为


### 生成实体

按照[创建实体](http://jhipster.cn/creating-an-entity/)的方法，使用如下命令生成实体。进行该动作前，先提交git，之后生成的代码不满意，方便回滚修改。

```
yo jhipster:import-jdl model/menu.jdl

```

如果语法不对，可能会遇到如下错误

```
The jdl is being parsed.
Error jhipster:import-jdl model/menu.jdl

ERROR! Error while parsing entities from JDL
[object Object]
```

类似的问题在stackoverflow.com上有[How to define a relationship with builtin User entity in jhipster jdl?](http://stackoverflow.com/questions/38749825/how-to-define-a-relationship-with-builtin-user-entity-in-jhipster-jdl)

通过分段执行的方式，发现是关联到User的语句有问题

```
relationship ManyToOne {
    SystemModule{createdBy} to User
}
```

参考[managing-relationships](https://jhipster.github.io/managing-relationships/)中的说明：

> Tip: the User entity

> Please note that the User entity, which is handled by JHipster, is specific. You can do:

> *  many-to-one relationships to this entity (a Car can have a many-to-one relationship to a User). This will generate a specific query in your new entity repository, so you can filter your entity on the current security user, which is a common requirement. On the generated AngularJS client UI you will have a dropdown in Car to select a User.

> * many-to-many and one-to-one relationships to the User entity, but the other entity must be the owner of the relationship (a Team can have a many-to-many relationship to User, but only the team can add/remove users, and a user cannot add/remove a team). On the AngularJS client UI, you will also be able to select a User in a multi-select box.



使用jdl-uml

在github上找到一个[示例Keep的keep-jdl.jh](https://github.com/bminciu/keep/blob/master/keep-jdl.jh)

```
entity Checklist {
  name String required
}

entity Item {
  name String required,
  description String,
  done Boolean,
  dueDate LocalDate
}

relationship ManyToOne {
  Checklist{user} to User
}

relationship OneToMany {
  Checklist{item} to Item
}

paginate all with pagination
service all with serviceClass


```

使用jhipster-uml导入：

`jhipster-uml model/checklist.jdl -db sql`


```
✗ jhipster-uml model/checklist.jdl -db sql
In the One-to-Many relationship from Checklist to Item, only bidirectionality is supported for a One-to-Many association. The other side will be automatically added.
Warning:  An Entity called 'User' was defined: 'User' is an entity created by default by JHipster. All relationships toward it will be kept but all attributes and relationships from it will be disregarded.
Creating:
	Checklist
	Item

Found the .jhipster/Checklist.json configuration file, entity can be automatically generated!


The entity Checklist is being updated.

   create src/main/java/com/yangyongli/phoenix/domain/Checklist.java
   create src/main/java/com/yangyongli/phoenix/repository/ChecklistRepository.java
   create src/main/java/com/yangyongli/phoenix/web/rest/ChecklistResource.java
   create src/main/java/com/yangyongli/phoenix/service/ChecklistService.java
   create src/main/resources/config/liquibase/changelog/20160823230547_added_entity_Checklist.xml
   create src/main/resources/config/liquibase/changelog/20160823230547_added_entity_constraints_Checklist.xml
 conflict src/main/resources/config/liquibase/master.xml
? Overwrite src/main/resources/config/liquibase/master.xml? overwrite

.......
```

更改menu.jdl如下

```jdl

entity SystemModule {
    moduleCode String required maxlength(256),
    moduleName String required maxlength(256),
    moduleNameEn String required maxlength(256),
    description String required maxlength(2048),
    createdTime ZonedDateTime,
    createdBy Long,
    updatedTime ZonedDateTime,
    updatedBy Long
}

entity Menu {
    systemModuleId Long required,
    resourceId Long,
    name String required maxlength(256),
    nameEn String required maxlength(256),
    tagName String required maxlength(256),
    iconClass String required maxlength(256),
    link String required maxlength(256),
    displayOrder Integer,
    helpText String maxlength(2048),
    createdTime ZonedDateTime,
    createdBy Long,
    updatedTime ZonedDateTime,
    updatedBy Long
}

relationship ManyToOne {
    Menu{parentMenuId} to Menu
}

dto * with mapstruct

paginate all with pagination
service all with serviceClass

```
现在可以用jhipster-uml生成代码。

```
jhipster-uml model/menu.jdl -db sql
```

生成的代码，默认的字段标签名是根据字段名生成的
比如Module Name En，是"模块英文名"，我们可以找到他，修改在webapp/i18n的语言模块下的`systemModule.json`中的标签名。

![](/images/jhipster_gen_label.png)

修改zh-cn目录下的文件

```javascript
{
    "avonApp": {
        "systemModule" : {
            "home": {
                "title": "System Modules",
                "createLabel": "Create a new System Module",
                "createOrEditLabel": "Create or edit a System Module",
                "search": "Search for System Module"
            },
            "created": "A new System Module is created with identifier {{ param }}",
            "updated": "A System Module is updated with identifier {{ param }}",
            "deleted": "A System Module is deleted with identifier {{ param }}",
            "delete": {
                "question": "Are you sure you want to delete System Module {{ id }}?"
            },
            "detail": {
                "title": "System Module"
            },
            "moduleCode": "Module Code",
            "moduleName": "Module Name",
            "moduleNameEn": "Module Name En",
            "description": "Description",
            "createdTime": "Created Time",
            "createdBy": "Created By",
            "updatedTime": "Updated Time",
            "updatedBy": "Updated By"
        }
    }
}

```

为

```javascript
{
    "avonApp": {
        "systemModule" : {
            "home": {
                "title": "系统模块",
                "createLabel": "创建新系统模块",
                "createOrEditLabel": "创建或编辑系统模块",
                "search": "查询"
            },
            "created": "系统模块 {{ param }} 已创建",
            "updated": "系统模块 {{ param }} 已更新",
            "deleted": "系统模块 {{ param }} 已删除",
            "delete": {
                "question": "是否确认删除系统模块 {{ id }}?"
            },
            "detail": {
                "title": "系统模块"
            },
            "moduleCode": "模块代码",
            "moduleName": "模块名称",
            "moduleNameEn": "模块英语名称",
            "description": "描述",
            "createdTime": "创建时间",
            "createdBy": "创建人",
            "updatedTime": "更新时间",
            "updatedBy": "更新人"
        }
    }
}

```




