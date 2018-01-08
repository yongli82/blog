---
title: 天玑权限管理
date: 2016-06-24 17:26:51
tags: 架构设计
categories: 架构设计
---

天玑权限管理
==========


权限功能
--------

- 限制用户是否能够访问天玑某个页面或Ajax
- 限制用户是否能够看到和使用某个按钮
- 限制用户是否能够访问某个产品线、某个公司的数据
- 在实现中，通过`权限`或`角色`进行限制

管理功能
--------

- 在系统中管理`权限`，字符串
- 在系统中管理`角色`，包括为`角色`分配`权限`，查看其`权限`
- 在系统中管理`角色组`，增删`角色`，查询其`权限`
- 在系统中管理`用户`的`角色`，`角色组`，`权限`


权限控制
--------

#### 1  菜单

天玑的菜单在subnav.xml文件中配置

例如：

```xml
<tags>
    <set name="收款管理">
        <link name="收款单" url="http://${ba-finance-exchange-web.Domain}/exchange/receiveorder/orderlist"/>
        <link name="收款通知单" url="http://${ba-finance-exchange-web.Domain}/exchange/receivenotify/orderlist"/>
    </set>
 ......

 </tags>

```

为了控制菜单是否显示，在配置文件中添加权限属性"menu:receive"

```xml
<tags>
    <set name="收款管理" permission="menu:receive">
        <link name="收款单" url="http://${ba-finance-exchange-web.Domain}/exchange/receiveorder/orderlist"/>
        <link name="收款通知单" url="http://${ba-finance-exchange-web.Domain}/exchange/receivenotify/orderlist"/>
    </set>
 ......

 </tags>

```

在portal-header渲染菜单的时候，通过检查当前访问人是否拥有权限"menu:receive"来决定是否显示"收款管理菜单"。


#### 2  页面组件

比如一个按钮"导出支付", 在页面ftl文件中

```html
   <a id="order-export" class="btn btn-primary btn-fs-normal btn-fs-sm ajaxdisabledbutton" style="display: none">
   <span class="glyphicon glyphicon-save"></span>导出支付
   </a>
```

使用ftl的自定义标签进行权限控制

```html
<@finance.hasRole name="operator">

    <a id="order-export" class="btn btn-primary btn-fs-normal btn-fs-sm ajaxdisabledbutton" style="display: none">
   <span class="glyphicon glyphicon-save"></span>导出支付
   </a>

</@finance.hasRole>
```
只有当前用户具有角色'operator'才会渲染改html组件。


#### 3  下拉框选项

比如产品线下拉框，在枚举上添加自定义注解来标识需要的权限或角色

```java
public enum BusinessType {

    /**
     * 错误
     */
    DEFAULT(0),
    /**
     * 团购
     */
    @NeedPermission("group:trade")
    GROUP_PURCHASE(1),
    /**
     * 预约预订
     */
    @NeedPermission("group:trade")
    BOOKING(2),
    /**
     * 结婚亲子
     */
    @NeedPermission("group:trade")
    WEDDING(3),
    /**
     * 储值卡
     */
    @NeedPermission("group:trade")
    PREPAID_CARD(4),
}
```

在下拉框Ajax的实现代码中, 判断当前用户是否具有对应的权限

```java
public String loadBusinessTypeOption() {
        FinanceSubject subject = StaffPermissionUtils.getSubject();
        BusinessType[] values = BusinessType.values();
        for (BusinessType value : values) {
            if(isAllowed(value, subject)){
                option.put(value.getBusinessType(), value.toString());
            }
        }

        msg.put("option", option);
        code = SUCCESS_CODE;
        return SUCCESS;
    }

    public <T extends Enum>  boolean isAllowed(T value, FinanceSubject subject){
        String name = value.name();
        boolean allowed = true;
        try {
            Annotation[] annotations = value.getClass().getField(name).getDeclaredAnnotations();
            if(annotations != null) {
                for (Annotation annotation : annotations) {
                    if(annotation instanceof NeedRole){
                        //需要所有的角色
                        String[] roleNames = ((NeedRole) annotation).value();
                        for (String roleName : roleNames) {
                            if(!subject.hasRole(roleName)){
                                allowed = false;
                                return allowed;
                            }
                        }
                    }else if(annotation instanceof NeedPermission){
                        //需要所有的权限
                        String[] permissionNames = ((NeedPermission) annotation).value();
                        for (String permissionName : permissionNames) {
                            if(!subject.isPermitted(permissionName)){
                                allowed = false;
                                return allowed;
                            }
                        }
                    }
                }
            }
        } catch (NoSuchFieldException e) {

        }
        return allowed;
    }
```

#### 4  Ajax请求

在Ajax请求对应的Action函数上使用自定义注解，在PermissionInterceptor拦截器中判断当前用户是否具有对应的权限或角色。
