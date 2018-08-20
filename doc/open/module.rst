主要模块
========

::

    ├── api
    │  
    ├── app
    │   ├── center
    │   │  
    │   ├── debug
    │   │  
    │   ├── home
    │   │  
    │   ├── product
    │   │  
    │   └── wiki
    │  
    ├── base
    │  
    ├── common
    │  
    ├── conf
    │  
    ├── doc
    │  
    ├── idl
    ├── log
    ├── model
    │  
    ├── open
    ├── static
    │   ├── angular
    │   │  
    │   ├── common
    │   │  
    │   ├── css
    │   │  
    │   ├── image
    │   │  
    │   ├── js
    │   │  
    │   ├── layui
    │   │  
    │   ├── ng
    │   │   ├── admin
    │   │   │  
    │   │   └── product
    │   │  
    │   ├── sdk
    │   │  
    │   └── tpl
    ├── templates
    │   ├── admin
    │   ├── center
    │   ├── component
    │   ├── debug
    │   ├── home
    │   ├── product
    │   ├── UI
    │   └── wiki
    │  
    ├── test
    │  
    └── util

#. api 主要存放纯接口部分内容，例如：获取UI配置，保存邮寄地址等
#. app 主要是页面相关全部路由表和具体实现，包括管理后台和开发平台
#. base 主要是基础通用部分内容，包括数据库连接器，静态固定变量定义，标准默认模板等
#. common 通用部分内容，数据库具体读写操作封装， 异步任务，发送邮件短信服务，生成lua脚本文件替换
#. conf 配置文件存放路径
#. doc 项目相关文档存放路径
#. idl 服务配置存放路径，例如：设备在线状态
#. log 项目运行日志
#. model 数据库模型文件
#. static 项目使用的静态资源文件路径，包括angularjs文件，bootstrap文件,markdown编辑器文件，layui框架文件，sdk文件存放，ejs模板存放
#. templates 前端页面模板存放，主要是django前端模板存放路径，包括管理后台页面
#. util 通用工具类封装，邮件发送，短信发送等
