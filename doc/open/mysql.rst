数据库设计
==========
基本信息
-------

* 主机：192.168.0.62
* 数据库名称：ebdb_open
* 帐号：root
* 密码：53iq.com
* 端口号：3306


表结构
-------

.. code-block:: sql

    -- ----------------------------
    -- Table structure for ebt_account
    -- ----------------------------
    DROP TABLE IF EXISTS `ebt_account`;
    CREATE TABLE `ebt_account` (
      `ebf_account_id` varchar(64) NOT NULL COMMENT '用户账号',
      `ebf_account_from_id` varchar(64) DEFAULT NULL,
      `ebf_account_password` varchar(512) NOT NULL COMMENT '密码',
      `ebf_account_type` int(3) NOT NULL DEFAULT '0' COMMENT '账号类型（0：普通账号 ，1：运营账号, 3:微信账号， 4：默认创建）',
      `ebf_account_email` varchar(128) DEFAULT NULL COMMENT '用户邮箱',
      `ebf_account_phone` varchar(32) DEFAULT NULL COMMENT '手机号',
      `ebf_account_status` int(3) NOT NULL DEFAULT '1' COMMENT '用户状态（0：未通过审核，1：可用）',
      `ebf_account_is_forbid` tinyint(1) NOT NULL DEFAULT '0' COMMENT '是否禁用（0：启用，1：禁用）',
      `ebf_account_last_login` datetime NOT NULL COMMENT '上次登录时间',
      `ebf_account_create_date` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
      `ebf_account_pdproducts` varchar(128)  COMMENT '参与开发的产品',
      `ebf_account_number` int(4)  COMMENT '人数',
      `ebf_account_expertise` varchar(128)  COMMENT '专长',
      `ebf_account_sproducts` varchar(128)  COMMENT '已出货的产品',
      `ebf_account_cooperation` varchar(128)  COMMENT '合作方式',
      `ebf_account_relate_account` text COMMENT '用户关联账户',
      PRIMARY KEY (`ebf_account_id`)
    ) ENGINE=ndbcluster DEFAULT CHARSET=utf8 COMMENT='用户表';

    -- --------------------------------------
    -- Table structure for ebt_account_info
    -- --------------------------------------
    DROP TABLE IF EXISTS `ebt_account_info`;
    CREATE TABLE `ebt_account_info` (
      `ebf_account_info_id` int(11) NOT NULL AUTO_INCREMENT COMMENT '用户信息编号',
      `ebf_account_id`  varchar(64) NOT NULL COMMENT '用户账号',
      `ebf_account_contact_name` varchar(64) DEFAULT NULL COMMENT '用户联系人姓名',
      `ebf_account_contact_phone` varchar(32) NOT NULL COMMENT '用户联系人电话',
      `ebf_account_contact_address` varchar(512) NOT NULL COMMENT '用户联系人地址',
      `ebf_account_info_create_date` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
      PRIMARY KEY (`ebf_account_info_id`),
      KEY `Index_12` (`ebf_account_id`),
      CONSTRAINT `FK_Reference_9` FOREIGN KEY (`ebf_account_id`) REFERENCES `ebt_account` (`ebf_account_id`) ON DELETE NO ACTION ON UPDATE NO ACTION
    ) ENGINE=ndbcluster DEFAULT CHARSET=utf8 COMMENT='用户信息表';

    -- ----------------------------
    -- Table structure for ebt_api
    -- ----------------------------
    DROP TABLE IF EXISTS `ebt_api`;
    CREATE TABLE `ebt_api` (
      `ebf_api_id` int(11) NOT NULL AUTO_INCREMENT COMMENT '接口编号',
      `ebf_api_url` text NOT NULL COMMENT '接口地址',
      `ebf_api_type` int(3) NOT NULL DEFAULT '0' COMMENT '接口类型（0：普通接口）',
      `ebf_api_request_type` varchar(64) DEFAULT NULL COMMENT '请求方式',
      `ebf_api_params` text COMMENT '接口参数（json字符串）',
      `ebf_api_name` varchar(64) DEFAULT NULL COMMENT '接口名称',
      `ebf_api_return` text COMMENT '接口返回值（json字符串）',
      `ebf_api_describe` varchar(2048) DEFAULT NULL COMMENT '接口描述',
      `ebf_api_doc_url` varchar(128) DEFAULT NULL COMMENT '文档地址',
      `ebf_api_action_url` varchar(128) DEFAULT NULL COMMENT '未获得时链接到的操作地址',
      `ebf_api_port` int(11) NOT NULL DEFAULT '80' COMMENT '端口号',
      `ebf_api_classify` varchar(64) DEFAULT NULL COMMENT '接口分类',
      `ebf_api_function` varchar(64) DEFAULT NULL COMMENT '接口功能',
      `ebf_api_level` int(3) NOT NULL DEFAULT '0' COMMENT '接口等级（0：普通接口，1：高级接口，2：内部接口）',
      `ebf_api_group` int(8) NOT NULL DEFAULT '0' COMMENT '接口分类（0：普通应用,1：内部接口,2：某某合作伙伴应用,',
      `ebf_api_invoke_total` bigint(20) NOT NULL DEFAULT '0' COMMENT '每日调用次数（0：未限制，其他表示具体次数）',
      `ebf_api_is_forbid` tinyint(4) NOT NULL DEFAULT '0' COMMENT '是否禁用（0：未禁用，1：禁用）',
      `ebf_api_create_date` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
      PRIMARY KEY (`ebf_api_id`),
      KEY `Index_1` (`ebf_api_level`)
    ) ENGINE=ndbcluster AUTO_INCREMENT=16 DEFAULT CHARSET=utf8 COMMENT='接口表';

    -- ----------------------------
    -- Table structure for ebt_api_auth
    -- ----------------------------
    DROP TABLE IF EXISTS `ebt_api_auth`;
    CREATE TABLE `ebt_api_auth` (
      `ebf_aa_id` int(11) NOT NULL AUTO_INCREMENT COMMENT '接口权限编号',
      `ebf_api_id` int(11) DEFAULT NULL COMMENT '接口编号',
      `ebf_app_id` int(11) DEFAULT NULL COMMENT '应用编号',
      `ebf_aa_invoke_total` bigint(20) NOT NULL DEFAULT '0' COMMENT '每次调用次数（0：未限制，其他表示具体次数）',
      `ebf_aa_is_forbid` tinyint(4) NOT NULL DEFAULT '0' COMMENT '是否禁用（0：未禁用，1：禁用）',
      `ebf_aa_create_date` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '授权时间',
      PRIMARY KEY (`ebf_aa_id`),
      KEY `Index_1` (`ebf_api_id`),
      KEY `Index_2` (`ebf_app_id`),
      KEY `Index_3` (`ebf_aa_invoke_total`),
      CONSTRAINT `FK_Reference_4` FOREIGN KEY (`ebf_api_id`) REFERENCES `ebt_api` (`ebf_api_id`) ON DELETE NO ACTION ON UPDATE NO ACTION,
      CONSTRAINT `FK_Reference_5` FOREIGN KEY (`ebf_app_id`) REFERENCES `ebt_app` (`ebf_app_id`) ON DELETE NO ACTION ON UPDATE NO ACTION
    ) ENGINE=ndbcluster DEFAULT CHARSET=utf8 COMMENT='接口权限表';

    -- ----------------------------
    -- Table structure for ebt_app
    -- ----------------------------
    DROP TABLE IF EXISTS `ebt_app`;
    CREATE TABLE `ebt_app` (
      `ebf_app_id` int(11) NOT NULL AUTO_INCREMENT COMMENT '应用编号',
      `ebf_developer_id` varchar(128) DEFAULT NULL COMMENT '开发者账号（开发者来源+下划线+账号拼接起来）',
      `ebf_app_name` varchar(64) NOT NULL COMMENT '应用名称',
      `ebf_app_describe` text COMMENT '应用描述',
      `ebf_app_site` varchar(512) DEFAULT '' COMMENT '应用描述网站',
      `ebf_app_logo` text COMMENT '应用图标',
      `ebf_app_action` int(3) DEFAULT NULL COMMENT '操作类型（1：添加，2：修改，3：删除）',
      `ebf_app_check_status` int(3) NOT NULL DEFAULT '0' COMMENT '审核状态（0：审核中，1：审核通过，-1：审核未通过）',
      `ebf_app_check_remarks` text COMMENT '审核备注',
      `ebf_app_appid` varchar(512) NOT NULL COMMENT 'appid',
      `ebf_app_appsecret` varchar(1024) NOT NULL COMMENT 'appsecret',
      `ebf_app_is_forbid` tinyint(1) NOT NULL DEFAULT '0' COMMENT '是否禁用（0：未禁用，1：禁用）',
      `ebf_app_brand` varchar(64) DEFAULT NULL COMMENT '设备品牌',
      `ebf_app_category` varchar(64) DEFAULT NULL COMMENT '设备类别',
      `ebf_app_model` varchar(64) DEFAULT NULL COMMENT '设备型号',
      `ebf_app_level` int(3) NOT NULL DEFAULT '0' COMMENT '接口等级（0：普通接口，1：高级接口，2：内部接口',
      `ebf_app_group` int(8) NOT NULL DEFAULT '0' COMMENT '接口分类（0：普通应用,1：内部接口,2：某某合作伙伴应用,',
      `ebf_app_push_url` text COMMENT '设备消息推送地址',
      `ebf_app_screen_size` int(2) NOT NULL DEFAULT '0' COMMENT '屏幕尺寸'
      `ebf_app_push_token` varchar(1024) DEFAULT NULL COMMENT '设备消息推送验证Token',
      `ebf_app_device_type` int(3) NOT NULL DEFAULT '0' COMMENT '设备类型（0：未知,1：油烟机，2：集成灶，3：冰柜，4：洗衣机）',
      `ebf_app_protocol_type` int(3) NOT NULL DEFAULT '1' COMMENT '协议类型（1:53iq协议，2：阿里小智协议，3：京东协议）',
      `ebf_app_create_date` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
      `ebf_app_update_date` datetime NOT NULL COMMENT '更新时间',
      `ebf_app_is_cloudmenu_device` tinyint(1) NOT NULL DEFAULT '0' COMMENT '是否是云菜谱产品（0：否，1：是）',
      `ebf_app_create_source` tinyint(1) NOT NULL DEFAULT '0' COMMENT 'App创建来源（0：手动创建，1：模板创建）',
      `ebf_group_id` int(11) NOT NULL DEFAULT '0' COMMENT '项目所属组id',
      PRIMARY KEY (`ebf_app_id`),
      KEY `Index_1` (`ebf_developer_id`),
      CONSTRAINT `FK_Reference_6` FOREIGN KEY (`ebf_developer_id`) REFERENCES `ebt_developer` (`ebf_developer_id`) ON DELETE NO ACTION ON UPDATE NO ACTION
    ) ENGINE=ndbcluster AUTO_INCREMENT=74 DEFAULT CHARSET=utf8 COMMENT='应用表';

    -- ----------------------------
    -- Table structure for ebt_app_history
    -- ----------------------------
    DROP TABLE IF EXISTS `ebt_app_history`;
    CREATE TABLE `ebt_app_history` (
      `ebf_app_id` int(11) NOT NULL AUTO_INCREMENT COMMENT '应用编号',
      `ebf_developer_id` varchar(128) DEFAULT NULL COMMENT '开发者账号（开发者来源+下划线+账号拼接起来）',
      `ebf_app_name` varchar(64) NOT NULL COMMENT '应用名称',
      `ebf_app_describe` text COMMENT '应用描述',
      `ebf_app_site` varchar(512) DEFAULT '' COMMENT '应用描述网站',
      `ebf_app_logo` text COMMENT '应用图标',
      `ebf_app_action` int(3) DEFAULT NULL COMMENT '操作类型（1：添加，2：修改，3：删除）',
      `ebf_app_check_status` int(3) NOT NULL DEFAULT '0' COMMENT '审核状态（0：审核中，1：审核通过，-1：审核未通过）',
      `ebf_app_check_remarks` text COMMENT '审核备注',
      `ebf_app_appid` varchar(512) NOT NULL COMMENT 'appid',
      `ebf_app_appsecret` varchar(1024) NOT NULL COMMENT 'appsecret',
      `ebf_app_is_forbid` tinyint(1) NOT NULL DEFAULT '0' COMMENT '是否禁用（0：未禁用，1：禁用）',
      `ebf_app_brand` varchar(64) DEFAULT NULL COMMENT '设备品牌',
      `ebf_app_category` varchar(64) DEFAULT NULL COMMENT '设备类别',
      `ebf_app_model` varchar(64) DEFAULT NULL COMMENT '设备型号',
      `ebf_app_level` int(3) NOT NULL DEFAULT '0' COMMENT '接口等级（0：普通接口，1：高级接口，2：内部接口',
      `ebf_app_group` int(8) NOT NULL DEFAULT '0' COMMENT '接口分类（0：普通应用,1：内部接口,2：某某合作伙伴应用,',
      `ebf_app_push_url` text COMMENT '设备消息推送地址',
      `ebf_app_push_token` varchar(1024) DEFAULT NULL COMMENT '设备消息推送验证Token',
      `ebf_app_device_type` int(3) NOT NULL DEFAULT '0' COMMENT '设备类型（0：未知,1：油烟机，2：集成灶，3：冰柜，4：洗衣机）',
      `ebf_app_protocol_type` int(3) NOT NULL DEFAULT '1' COMMENT '协议类型（1:53iq协议，2：阿里小智协议，3：京东协议）',
      `ebf_group_id` int(11) NOT NULL DEFAULT '0' COMMENT '项目所属组id',
      `ebf_app_create_date` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
      `ebf_app_update_date`6px datetime NOT NULL COMMENT '更新时间',
      `ebf_app_delete_date` datetime NOT NULL COMMENT '删除时间',
      `ebf_app_is_cloudmenu_device` tinyint(1) NOT NULL DEFAULT '0' COMMENT '是否是云菜谱产品（0：否，1：是）',
      `ebf_app_create_source` tinyint(1) NOT NULL DEFAULT '0' COMMENT 'App创建来源（0：手动创建，1：模板创建）',
      `ebf_group_id` int(11) NOT NULL DEFAULT '0' COMMENT '项目所属组id',

      PRIMARY KEY (`ebf_app_id`)
    ) ENGINE=ndbcluster AUTO_INCREMENT=63 DEFAULT CHARSET=utf8 COMMENT='应用历史表';

    -- ----------------------------
    -- Table structure for ebt_app_version
    -- ----------------------------
    DROP TABLE IF EXISTS `ebt_app_version`;
    CREATE TABLE `ebt_app_version` (
      `ebf_av_id` int(11) NOT NULL AUTO_INCREMENT COMMENT '版本编号',
      `ebf_app_id` int(11) DEFAULT NULL COMMENT 'app编号',
      `ebf_av_version_code` varchar(256) NOT NULL COMMENT '版本号',
      `ebf_av_version_name` varchar(256) NOT NULL COMMENT '版本名称',
      `ebf_av_download_url` text COMMENT '下载地址',
      `ebf_av_is_notify` varchar(16) NOT NULL DEFAULT 'yes' COMMENT '是否提示(yes提示，no不提示)',
      `ebf_av_is_force` varchar(16) NOT NULL DEFAULT 'no' COMMENT '是否强制升级(yes强制，no不强制)',
      `ebf_av_size` varchar(32) DEFAULT NULL COMMENT '文件大小(bytes)',
      `ebf_av_remarks` text COMMENT '更新备注',
      `ebf_av_updatedate` datetime NOT NULL COMMENT '更新时间',
      `ebf_av_createdate` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
      `ebf_av_md5` varchar(128) NOT NULL COMMENT '版本签名',
      `ebf_file_md5` varchar(128) NOT NULL COMMENT 'apk文件md5值',
      `ebf_av_type` int(3) DEFAULT '0' COMMENT '版本类型（0：外部版本，1：内部版本）',
      `ebf_min_version` int(11) DEFAULT '0',
      PRIMARY KEY (`ebf_av_id`),
      KEY `FK_Reference_1` (`ebf_app_id`),
      CONSTRAINT `FK_Reference_1` FOREIGN KEY (`ebf_app_id`) REFERENCES `ebt_app` (`ebf_app_id`) ON DELETE NO ACTION ON UPDATE NO ACTION
    ) ENGINE=ndbcluster AUTO_INCREMENT=247 DEFAULT CHARSET=utf8 COMMENT='app版本信息';

    -- ----------------------------
    -- Table structure for ebt_developer
    -- ----------------------------
    DROP TABLE IF EXISTS `ebt_developer`;
    CREATE TABLE `ebt_developer` (
      `ebf_developer_id` varchar(128) NOT NULL COMMENT '开发者账号（开发者来源+下划线+账号拼接起来）',
      `ebf_developer_account` varchar(512) NOT NULL COMMENT '用户账号',
      `ebf_developer_factory` varchar(128) DEFAULT NULL COMMENT '厂商名称',
      `ebf_developer_symbol` varchar(1024) NOT NULL COMMENT '厂商标识（这个一定不能为空哦）',
      `ebf_developer_from` int(3) NOT NULL DEFAULT '1' COMMENT '开发者来源（1：平台用户，2：设备管理系统厂商，3：qq）',
      `ebf_developer_inc` varchar(64) NOT NULL COMMENT '公司/团队名称',
      `ebf_developer_is_forbid` tinyint(1) NOT NULL DEFAULT '0' COMMENT '是否禁用（0：未禁用，1：禁用）',
      `ebf_developer_site` text COMMENT '公司/团队网址',
      `ebf_developer_address` varchar(2048) DEFAULT NULL COMMENT '公司/团队所在地',
      `ebf_developer_person` int(11) DEFAULT NULL COMMENT '开发团队人数',
      `ebf_developer_realname` varchar(32) NOT NULL COMMENT '联系人姓名',
      `ebf_developer_job` varchar(64) DEFAULT NULL COMMENT '联系人职务',
      `ebf_developer_mobile` varchar(32) NOT NULL COMMENT '手机',
      `ebf_developer_email` varchar(128) DEFAULT NULL COMMENT '邮箱',
      `ebf_developer_action` int(3) DEFAULT NULL COMMENT '操作类型（1：添加，2：修改，3：删除）',
      `ebf_developer_check_status` int(11) NOT NULL DEFAULT '0' COMMENT '审核状态（0：审核中，1：审核通过，-1：审核未通过）',
      `ebf_developer_check_remarks` text COMMENT '审核备注',
      `ebf_developer_update_date` datetime NOT NULL COMMENT '更新时间',
      `ebf_developer_create_date` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
      PRIMARY KEY (`ebf_developer_id`)
    ) ENGINE=ndbcluster DEFAULT CHARSET=utf8 COMMENT='开发者表';

    -- ----------------------------
    -- Table structure for ebt_developer_hostory
    -- ----------------------------
    DROP TABLE IF EXISTS `ebt_developer_hostory`;
    CREATE TABLE `ebt_developer_hostory` (
      `ebf_developer_id` varchar(128) NOT NULL COMMENT '开发者账号（开发者来源+下划线+账号拼接起来）',
      `ebf_developer_account` varchar(512) NOT NULL COMMENT '用户账号',
      `ebf_developer_factory` varchar(128) DEFAULT NULL COMMENT '厂商名称',
      `ebf_developer_symbol` varchar(1024) NOT NULL COMMENT '厂商标识（这个一定不能为空哦）',
      `ebf_developer_from` int(3) NOT NULL DEFAULT '1' COMMENT '开发者来源（1：平台用户，2：设备管理系统厂商，3：qq）',
      `ebf_developer_inc` varchar(64) NOT NULL COMMENT '公司/团队名称',
      `ebf_developer_is_forbid` tinyint(1) NOT NULL DEFAULT '0' COMMENT '是否禁用（0：未禁用，1：禁用）',
      `ebf_developer_site` text COMMENT '公司/团队网址',
      `ebf_developer_address` varchar(2048) DEFAULT NULL COMMENT '公司/团队所在地',
      `ebf_developer_person` int(11) DEFAULT NULL COMMENT '开发团队人数',
      `ebf_developer_realname` varchar(32) NOT NULL COMMENT '联系人姓名',
      `ebf_developer_job` varchar(64) DEFAULT NULL COMMENT '联系人职务',
      `ebf_developer_mobile` varchar(32) NOT NULL COMMENT '手机',
      `ebf_developer_email` varchar(128) DEFAULT NULL COMMENT '邮箱',
      `ebf_developer_action` int(3) DEFAULT NULL COMMENT '操作类型（1：添加，2：修改，3：删除）',
      `ebf_developer_check_status` int(11) NOT NULL DEFAULT '0' COMMENT '审核状态（0：审核中，1：审核通过，-1：审核未通过）',
      `ebf_developer_check_remarks` text COMMENT '审核备注',
      `ebf_developer_update_date` datetime NOT NULL COMMENT '更新时间',
      `ebf_developer_create_date` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
      `ebf_developer_delete_date` datetime NOT NULL COMMENT '删除时间',
      PRIMARY KEY (`ebf_developer_id`)
    ) ENGINE=ndbcluster DEFAULT CHARSET=utf8 COMMENT='开发者表历史表';

    -- ----------------------------
    -- Table structure for ebt_doc
    -- ----------------------------
    DROP TABLE IF EXISTS `ebt_doc`;
    CREATE TABLE `ebt_doc` (
      `ebf_doc_id` int(11) NOT NULL AUTO_INCREMENT COMMENT '文档编号',
      `ebf_api_id` int(11) DEFAULT NULL COMMENT '接口编号（只有接口文档此项不为空）',
      `ebf_doc_markdown` text COMMENT '接口文档（Markdown源码，保存示例代码和详细说明）',
      `ebf_doc_html` text COMMENT '生成的html',
      `ebf_doc_type` int(3) NOT NULL DEFAULT '0' COMMENT '文档类型（0：接口文档，1：介绍文档，2：内部加密文档）',
      `ebf_doc_create_date` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
      `ebf_doc_update_date` datetime DEFAULT NULL COMMENT '更新时间',
      `ebf_doc_name` varchar(64) DEFAULT NULL COMMENT '文档名称',
      PRIMARY KEY (`ebf_doc_id`),
      KEY `FK_Reference_2` (`ebf_api_id`),
      CONSTRAINT `FK_Reference_2` FOREIGN KEY (`ebf_api_id`) REFERENCES `ebt_api` (`ebf_api_id`) ON DELETE NO ACTION ON UPDATE NO ACTION
    ) ENGINE=ndbcluster AUTO_INCREMENT=22 DEFAULT CHARSET=utf8 COMMENT='文档表';

    -- ----------------------------
    -- Table structure for ebt_doc_menu
    -- ----------------------------
    DROP TABLE IF EXISTS `ebt_doc_menu`;
    CREATE TABLE `ebt_doc_menu` (
      `ebf_dm_id` int(11) NOT NULL AUTO_INCREMENT COMMENT '文档菜单编号',
      `ebf_doc_id` int(11) DEFAULT NULL COMMENT '文档编号',
      `ebf_dm_name` varchar(64) NOT NULL COMMENT '菜单名称',
      `ebf_dm_is_parent` tinyint(1) NOT NULL DEFAULT '0' COMMENT '是否为目录菜单（0：非目录菜单，1：目录菜单）',
      `ebf_dm_url` varchar(2048) NOT NULL DEFAULT '#' COMMENT '菜单url地址',
      `ebf_dm_class` varchar(64) DEFAULT NULL COMMENT '菜单样式',
      `ebf_dm_depth` int(2) NOT NULL DEFAULT '1' COMMENT '菜单深度（1：一级菜单，2：二级菜单）',
      `ebf_dm_ordernum` int(11) DEFAULT NULL,
      `ebf_dm_parent_id` int(11) NOT NULL DEFAULT '0' COMMENT '上级菜单编号（根目录的上级菜单为0）',
      PRIMARY KEY (`ebf_dm_id`),
      KEY `Index_1` (`ebf_doc_id`),
      CONSTRAINT `FK_Reference_7` FOREIGN KEY (`ebf_doc_id`) REFERENCES `ebt_doc` (`ebf_doc_id`) ON DELETE NO ACTION ON UPDATE NO ACTION
    ) ENGINE=ndbcluster AUTO_INCREMENT=194 DEFAULT CHARSET=utf8 COMMENT='文档菜单表';

    -- ----------------------------
    -- Table structure for ebt_auto_login
    -- ----------------------------
    DROP TABLE IF EXISTS `ebt_auto_login`;
    CREATE TABLE `ebt_auto_login` (
      `ebf_al_id` int(11) NOT NULL AUTO_INCREMENT COMMENT 'id',
      `ebf_al_account_id` varchar(64) NOT NULL COMMENT '用户账号',
      `ebf_al_account_password` varchar(512) NOT NULL COMMENT '用户密码',
      `ebf_al_token` varchar(64) NOT NULL COMMENT '自动登录的token',
      `ebf_al_login_ip` varchar(32) NOT NULL COMMENT '自动登录的ip',
      `ebf_al_update_date` datetime NOT NULL COMMENT '更新时间',
      `ebf_al_create_date` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
      PRIMARY KEY (`ebf_al_id`)
    ) ENGINE=InnoDB AUTO_INCREMENT=194 DEFAULT CHARSET=utf8 COMMENT='自动登录表';

    -- ----------------------------
    -- Table structure for ebt_message
    -- ----------------------------
    DROP TABLE IF EXISTS `ebt_message`;
    CREATE TABLE `ebt_message` (
      `ebf_message_id` int(11) NOT NULL AUTO_INCREMENT COMMENT 'id',
      `ebf_message_content` varchar(512) NOT NULL COMMENT '消息内容',
      `ebf_message_type` int(2) NOT NULL DEFAULT '1' COMMENT '消息类型（1：一般消息，2：系统消息）',
      `ebf_message_sender` varchar(64) NOT NULL COMMENT '消息发送者id',
      `ebf_message_target` varchar(64) NOT NULL COMMENT '消息目标接受者id',
      `ebf_message_is_read` int(2) NOT NULL DEFAULT '0' COMMENT '是否阅读（1：已读，0：未读）',
      `ebf_message_handler_type` int(2) NOT NULL DEFAULT '0' COMMENT '操作类型（0：无， 1：功能编辑， 2：协议编辑，3：UI编辑）',
      `ebf_device_key` varchar(8)  COMMENT '设备产品key',
      `ebf_message_update_date` datetime NOT NULL COMMENT '更新时间',
      `ebf_message_create_date` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
      PRIMARY KEY (`ebf_message_id`)
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='消息表';

    -- ----------------------------
    -- Table structure for ebt_device_function
    -- ----------------------------
    DROP TABLE IF EXISTS `ebt_device_function`;
    CREATE TABLE `ebt_device_function` (
      `ebf_df_id` int(11) NOT NULL AUTO_INCREMENT COMMENT 'id',
      `ebf_device_key` varchar(10) NOT NULL COMMENT '产品唯一key',
      `ebf_device_function` varchar(1024) NOT NULL COMMENT '产品新增功能内容',
      `ebf_df_check_status` int(2) NOT NULL DEFAULT '0' COMMENT '审核状态(0:待审核，1：审核通过，2：审核不通过)',
      `ebf_df_update_date` datetime NOT NULL COMMENT '更新时间',
      `ebf_df_create_date` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
      PRIMARY KEY (`ebf_df_id`)
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='新增产品功能审核表';

    -- ----------------------------
    -- Table structure for ebt_device_function
    -- ----------------------------
    DROP TABLE IF EXISTS `ebt_factory_protocol`;
    CREATE TABLE `ebt_factory_protocol` (
      `ebf_fp_id` int(11) NOT NULL AUTO_INCREMENT COMMENT 'id',
      `ebf_device_key` varchar(10) NOT NULL COMMENT '产品唯一key',
      `ebf_factory_protocol_type` int(2) NOT NULL DEFAULT '0' COMMENT '协议类型(0:标准协议，1：厂家自定义协议)',
      `ebf_factory_protocol_content` text COMMENT '协议具体内容',
      `ebf_df_update_date` datetime NOT NULL COMMENT '更新时间',
      `ebf_df_create_date` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
      PRIMARY KEY (`ebf_fp_id`)
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='厂家协议定义表';

    -- ----------------------------
    -- Table structure for ebt_group
    -- ----------------------------
    DROP TABLE IF EXISTS `ebt_group`;
    CREATE TABLE `ebt_group` (
      `ebf_group_id` int(11) NOT NULL AUTO_INCREMENT COMMENT '组id',
      `ebf_create_user` varchar(64) NOT NULL COMMENT '创建者id',
      `ebf_relate_project_id` int(11) NOT NULL DEFAULT '0' COMMENT '关联项目id',
      `ebf_group_update_date` datetime NOT NULL COMMENT '更新时间',
      `ebf_group_create_date` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
      PRIMARY KEY (`ebf_group_id`)
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='自定义组表';

    -- ----------------------------
    -- Table structure for ebt_user_group
    -- ----------------------------
    DROP TABLE IF EXISTS `ebt_user_group`;
    CREATE TABLE `ebt_user_group` (
      `ebf_ug_id` int(11) NOT NULL AUTO_INCREMENT COMMENT '用户组id',
      `ebf_group_id` int(11) NOT NULL COMMENT '组id',
      `ebf_user_account` varchar(64) NOT NULL COMMENT '用户账号',
      `ebf_ug_update_date` datetime NOT NULL COMMENT '更新时间',
      `ebf_ug_create_date` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
      PRIMARY KEY (`ebf_ug_id`),
      KEY `Index_13` (`ebf_group_id`),
      CONSTRAINT `FK_Reference_10` FOREIGN KEY (`ebf_group_id`) REFERENCES `ebt_group` (`ebf_group_id`) ON DELETE NO ACTION ON UPDATE NO ACTION
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='用户组关联表';

    -- ----------------------------
    --  Table structure for `ebt_doc_ui`
    -- ----------------------------
    DROP TABLE IF EXISTS `ebt_doc_ui`;
    CREATE TABLE `ebt_doc_ui` (
      `ebf_ui_id` int(11) NOT NULL AUTO_INCREMENT COMMENT 'ui产品编号',
      `ebf_ui_key` varchar(8) NOT NULL COMMENT 'ui产品key',
      `ebf_ui_content` text COMMENT 'ui上传内容',
      `ebf_ui_type` varchar(8) DEFAULT NULL COMMENT 'ui上传类型',
      `ebf_ui_title` varchar(64) DEFAULT '1.0' COMMENT 'ui上传说明（版本v1，v2）',
      `ebf_ui_create_date` datetime DEFAULT NULL COMMENT '创建时间',
      `ebf_ui_update_date` datetime DEFAULT NULL COMMENT '更新时间',
      `ebf_ui_upload_id` int(2) DEFAULT '0' COMMENT 'ui上传编号',
      `ebf_ui_ack` int(2) DEFAULT '0' COMMENT 'ack 确认',
      `ebf_ui_time_stemp` text COMMENT '时间戳',
      `ebf_ui_remark` varchar(64) DEFAULT NULL COMMENT '备注信息',
      `ebf_ui_party` varchar(16) DEFAULT NULL COMMENT '负责方',
      `ebf_ui_plan` varchar(64) DEFAULT NULL COMMENT '计划名称',
      PRIMARY KEY (`ebf_ui_id`)
    ) ENGINE=InnoDB AUTO_INCREMENT=324 DEFAULT CHARSET=utf8;

    -- ----------------------------
    --  Table structure for `ebt_app_info`
    -- ----------------------------
    DROP TABLE IF EXISTS `ebt_app_info`;
    CREATE TABLE `ebt_app_info` (
      `ebf_ai_id` int(11) NOT NULL AUTO_INCREMENT COMMENT '产品信息编号',
      `ebf_app_id` int(11) DEFAULT NULL COMMENT 'app编号',
      `ebf_responsible_party` text COMMENT '负责方',
      `ebf_responsible_people` varchar(64) DEFAULT NULL COMMENT '负责人',
      `ebf_ai_create_date` datetime DEFAULT NULL COMMENT '创建时间',
      `ebf_ai_update_date` datetime DEFAULT NULL COMMENT '更新时间',
      PRIMARY KEY (`ebf_ai_id`)
    ) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8 COMMENT='App信息完善表';;