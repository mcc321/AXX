# AXX说明文档

### 数据库结构

##### 1.表

* User
* Message
* Role
* Comment
* Search_information
* User_search
* Course

##### 2.简介

* User表，其构建连带包含Message ，Comment , Search_information
* Role表用来存储用户类型
* Course表用来存储课程
* User_search主要是做多对多的关联的一个表

> 总结：
>
> User表和Search_information是多对多，因此增加了一个User_search表关联两者
>
> User与Message，Comment，Course是一对多
>
> Role是固定不变的表
>
> Course与Comment是一对多

详细的数据库信息[demo](https://mcc321.github.io/mysql.html)

##### 3.逻辑实现

数据库操作的主要逻辑是基于两个中兴：User和Course，根据User表构建Search_information

基于Course构建Comment，Message，这样的结构主要是出于后续的Message添加以及Search_information的计数，排序。

##### 4.功能简介

* 认证功能简介

认证可以基于cookie认证，也可以基于JWT认证

> cookie认证
>
> 通过设置login_requre,admin_require,super_admin_require三个修饰器，限定用户的访问
>
> 基于JWT认证
>
> 首先前端需要行一个路由发送请求，申请到一个已注册的用户的toke，再将这个token加在每个请求的header里面，作为用户的表示，基于的是request_loader

注册登录的附加功能，邮件验证功能，只有确认后用户才能登陆[demo]()

* 基本信息反馈，通过相应的路由实现[demo]()
* 全部测试示例[demo](https://documenter.getpostman.com/view/6263986/S17qTpnT)

##### 项目总结

[AXX项目总结](https://mcc321.github.io/2019/03/21/axx-xiang-mu-zong-jie/)

![mcc](https://github.com/mcc321/mcc/blob/master/img/3.jpg?raw=true)

