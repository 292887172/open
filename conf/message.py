# 系统账号
SYS_SENDER = '53iqadmin'

# 系统发布消息
SYS_CONTENT = '厨电自助开发平台V1.0发布'

# 普通账号
USER_TYPE = 'user'

# 系统账号

SYS_TYPE = 'sys'

# 开发者资料审核通过
DEVELOPER_PUBLISHED = "开发者资料审核通过"

# 创建产品
CREATE_APP = "产品添加"

# 删除产品
DEL_APP = "产品删除"

# 更新产品基本信息
UPDATE_APP = "最新编辑"

# 更新产品配置信息
UPDATE_APP_CONFIG = "配置信息更新"

# 重置应用的AppSecret
RESET_APP_SECRET = "重置应用的AppSecret"

# 申请发布产品
RELEASE_APP = "提交审核"

# 取消发布产品
CANCEL_RELEASE_APP = "取消审核"

# 下架产品
OFF_APP = "下架"

# 审核通过
PASS_APP = "审核通过"

# 审核不通过
DENIED_APP = "审核不通过"

# 创建产品功能
CREATE_FUN = "功能创建"

# 修改产品功能
UPDATE_FUN = "功能编辑"

# 修改功能状态
UPDATE_FUN_OPEN = "功能启用"
UPDATE_FUN_CLOSE = "功能关闭"

# 删除产品功能
DEL_FUN = "功能删除"

# 设备存到redis
DEVICE = "DEVICE"

# 计划书
BOOK = {
    '1': '提交蒸烤箱详细技术功能规划书',
    '2': '提交电控板功能协议文档',
    '3': '提交正式蒸烤箱UI和UE',
    '4': '制定项目进度计划书',
    '5': '蒸烤箱应用程序开发',
    '6': '提供正式电控版',
    '7': '蒸烤箱控制协议对接',
    '8': '提供蒸烤箱整机',
    '9': '整机联调、老化测试'

}

# 功能标准库
PROTOCOL_KU = [
    {'isControl': 1, 'state': 1, 'isDisplay': 1, 'isCloudMenu': 0, 'isShow': 0, 'time': '2017-08-01 09:20:19',
     'name': '开关', 'corpMark': '', 'widget': 'button', 'min': 0, 'max': 255,
     'mxsNum': '2', 'mxs': [{'desc': '关', 'trigger': [], 'data': '0'}, {'desc': '开', 'trigger': [], 'data': '1'}],
     'corpName': '', 'paramType': 4,
     'mxsLength': '8', 'id': '1', 'Stream_ID': 'POWER', 'toSwitch': '0', 'isFunction': '1'},
    {'isControl': 1, 'state': 1, 'isDisplay': 1, 'isCloudMenu': 0, 'isShow': 0, 'time': '2017-08-01 09:20:19',
     'name': '预约', 'corpMark': '', 'widget': 'button', 'min': 0, 'max': 255,
     'mxsNum': '2', 'corpName': '', 'paramType': 4,
     'mxs': [{'desc': '无', 'trigger': [], 'data': '0'}, {'desc': '预约·', 'trigger': [], 'data': '1'}],
     'mxsLength': '8', 'id': '2', 'Stream_ID': 'APPOINT', 'toSwitch': '0', 'isFunction': '1'},
    {'isControl': 1, 'state': 1, 'isDisplay': 1, 'isCloudMenu': 0, 'isShow': 0, 'time': '2017-08-01 09:20:19',
     'name': '童锁', 'corpMark': '', 'widget': 'button', 'min': 0, 'max': 255,
     'mxsNum': '2', 'corpName': '', 'paramType': 4,
     'mxs': [{'desc': '关', 'trigger': [], 'data': '0'}, {'desc': '开·', 'trigger': [], 'data': '1'}],
     'mxsLength': '8', 'id': '3', 'Stream_ID': 'BODY_LOCK', 'toSwitch': '0', 'isFunction': '1'},
    {'isControl': 1, 'state': 1, 'isDisplay': 1, 'isCloudMenu': 0, 'isShow': 0, 'time': '2017-08-01 09:20:19',
     'name': '照明', 'corpMark': '', 'widget': 'button', 'min': 0, 'max': 255,
     'mxsNum': '2', 'corpName': '', 'paramType': 4,
     'mxs': [{'desc': '关', 'trigger': [], 'data': '0'}, {'desc': '开·', 'trigger': [], 'data': '1'}],
     'mxsLength': '8', 'id': '4', 'Stream_ID': 'LAMP', 'toSwitch': '0', 'isFunction': '1'},
    {'isControl': 1, 'state': 1, 'isDisplay': 1, 'isCloudMenu': 0, 'isShow': 0, 'time': '2017-08-01 09:20:19',
     'name': '工作状态', 'corpMark': '', 'widget': 'button', 'min': 0, 'max': 255,
     'mxsNum': '2', 'corpName': '', 'paramType': 4,
     'mxs': [{'desc': '停止', 'trigger': [], 'data': '2'}, {'desc': '关', 'data': '0'}, {'desc': '工作', 'data': '1'},
             {'desc': '暂停', 'trigger': [], 'data': '3'}],
     'mxsLength': '8', 'id': '5', 'Stream_ID': 'STATE', 'toSwitch': '0', 'isFunction': '1'},
    {'isControl': 1, 'state': 1, 'isDisplay': 1, 'isCloudMenu': 0, 'isShow': 0, 'time': '2017-08-01 09:20:19',
     'name': '模式', 'corpMark': '', 'widget': 'button', 'min': 0, 'max': 255,
     'mxsNum': '2', 'mxs': [
        {
            "desc": "解冻",
            "data": "1"
        },
        {
            "desc": "发酵",
            "data": "2"
        },
        {
            "desc": "杀菌",
            "data": "3"
        },
        {
            "desc": "清洗",
            "data": "4"
        },
        {
            "desc": "高温",
            "data": "5"
        },
        {
            "desc": "保温",
            "data": "6"
        },
        {
            "desc": "蔬菜",
            "trigger": [

            ],
            "data": "256"
        },
        {
            "desc": "水果",
            "trigger": [

            ],
            "data": "512"
        },
        {
            "desc": "肉类",
            "trigger": [

            ],
            "data": "768"
        },
        {
            "desc": "鱼类",
            "trigger": [

            ],
            "data": "1024"
        },
        {
            "desc": "蛋类",
            "trigger": [

            ],
            "data": "1280"
        },
        {
            "desc": "米饭",
            "trigger": [

            ],
            "data": "1536"
        },
        {
            "desc": "面食",
            "trigger": [

            ],
            "data": "1792"
        },
        {
            "desc": "快热",
            "trigger": [

            ],
            "data": "4096"
        },
        {
            "desc": "风焙烤",
            "trigger": [

            ],
            "data": "4097"
        },
        {
            "desc": "焙烤",
            "trigger": [

            ],
            "data": "4098"
        },
        {
            "desc": "底加热",
            "trigger": [

            ],
            "data": "4099"
        },
        {
            "desc": "风扇烤",
            "trigger": [

            ],
            "data": "4100"
        },
        {
            "desc": "烧烤",
            "trigger": [

            ],
            "data": "4101"
        },
        {
            "desc": "强烧烤",
            "trigger": [

            ],
            "data": "4102"
        },
        {
            "desc": "增强烧烤",
            "trigger": [

            ],
            "data": "4103"
        },
        {
            "desc": "发酵",
            "trigger": [

            ],
            "data": "4104"
        },
        {
            "desc": "蛋糕",
            "trigger": [

            ],
            "data": "4352"
        },
        {
            "desc": "家禽",
            "trigger": [

            ],
            "data": "4608"
        },
        {
            "desc": "面包",
            "trigger": [

            ],
            "data": "4864"
        },
        {
            "desc": "烤肉",
            "trigger": [

            ],
            "data": "5120"
        },
        {
            "desc": "烤鱼",
            "trigger": [

            ],
            "data": "5376"
        },
        {
            "desc": "披萨",
            "trigger": [

            ],
            "data": "5632"
        },
        {
            "desc": "饼干",
            "trigger": [

            ],
            "data": "5888"
        }

    ], 'corpName': '', 'paramType': 4,
     'mxsLength': '8', 'id': '6', 'Stream_ID': 'MODEL', 'toSwitch': '0', 'isFunction': '1'},
    {'isControl': 1, 'state': 1, 'isDisplay': 1, 'isCloudMenu': 0, 'isShow': 0, 'time': '2017-08-01 09:20:19',
     'name': '当前温度', 'corpMark': '', 'widget': 'input', 'min': 0, 'max': 255,
     'mxsNum': '2', 'corpName': '', 'paramType': 4,
     'mxs': [],
     'mxsLength': '8', 'id': '7', 'Stream_ID': 'CUR_TEMPE', 'toSwitch': '0', 'isFunction': '1'},
    {'isControl': 1, 'state': 1, 'isDisplay': 1, 'isCloudMenu': 0, 'isShow': 0, 'time': '2017-08-01 09:20:19',
     'name': '故障', 'corpMark': '', 'widget': 'button', 'min': 0, 'max': 255,
     'mxsNum': '2', 'corpName': '', 'paramType': 4,
     'mxs': [
         {
             "desc": "无",
             "trigger": [

             ],
             "data": "0"
         },
         {
             "desc": "高水位",
             "trigger": [

             ],
             "data": "2"
         },
         {
             "desc": "加热异常",
             "trigger": [

             ],
             "data": "4"
         },
         {
             "desc": "温度传感器故障",
             "trigger": [

             ],
             "data": "8"
         },
         {
             "desc": "浊度传感器异常",
             "trigger": [

             ],
             "data": "16"
         },
         {
             "desc": "上盖没压紧",
             "trigger": [

             ],
             "data": "32"
         },
         {
             "desc": "溢流",
             "trigger": [

             ],
             "data": "1"
         }],
     'mxsLength': '8', 'id': '8', 'Stream_ID': 'ERROR', 'toSwitch': '0', 'isFunction': '1'},
    {'isControl': 1, 'state': 1, 'isDisplay': 1, 'isCloudMenu': 0, 'isShow': 0, 'time': '2017-08-01 09:20:19',
     'name': '状态反馈', 'corpMark': '', 'widget': 'button', 'min': 0, 'max': 255,
     'mxsNum': '2', 'corpName': '', 'paramType': 4,
     'mxs': [
         {
             "desc": "门关",
             "trigger": [

             ],
             "data": "0"
         },
         {
             "desc": "门开",
             "trigger": [

             ],
             "data": "1"
         },
         {
             "desc": "水位",
             "trigger": [

             ],
             "data": "2"
         },
         {
             "desc": "水箱",
             "trigger": [

             ],
             "data": "4"
         },
         {
             "desc": "童锁开",
             "trigger": [

             ],
             "data": "8"
         },
         {
             "desc": "缺盐",
             "trigger": [

             ],
             "data": "16"
         }],
     'mxsLength': '8', 'id': '9', 'Stream_ID': 'System_Status', 'toSwitch': '0', 'isFunction': '1'},
    {'isControl': 1, 'state': 1, 'isDisplay': 1, 'isCloudMenu': 0, 'isShow': 0, 'time': '2017-08-01 09:20:19',
     'name': '设定温度', 'corpMark': '', 'widget': 'input', 'min': 0, 'max': 255,
     'mxsNum': '2', 'mxs': [], 'corpName': '', 'paramType': 4,
     'mxsLength': '8', 'id': '10', 'Stream_ID': 'SET_TEMPE', 'toSwitch': '0', 'isFunction': '1'},
    {'isControl': 1, 'state': 1, 'isDisplay': 1, 'isCloudMenu': 0, 'isShow': 0, 'time': '2017-08-01 09:20:19',
     'name': '建议温度下限', 'corpMark': '', 'widget': 'input', 'min': 0, 'max': 255,
     'mxsNum': '2', 'mxs': [], 'corpName': '', 'paramType': 4,
     'mxsLength': '8', 'id': '11', 'Stream_ID': 'Suggest_Temp_Down', 'toSwitch': '0', 'isFunction': '1'},
    {'isControl': 1, 'state': 1, 'isDisplay': 1, 'isCloudMenu': 0, 'isShow': 0, 'time': '2017-08-01 09:20:19',
     'name': '建议温度上限', 'corpMark': '', 'widget': 'input', 'min': 0, 'max': 255,
     'mxsNum': '2', 'mxs': [], 'corpName': '', 'paramType': 4,
     'mxsLength': '8', 'id': '12', 'Stream_ID': 'Suggest_Temp_Up', 'toSwitch': '0', 'isFunction': '1'},
    {'isControl': 1, 'state': 1, 'isDisplay': 1, 'isCloudMenu': 0, 'isShow': 0, 'time': '2017-08-01 09:20:19',
     'name': '设定工作时间', 'corpMark': '', 'widget': 'input', 'min': 0, 'max': 255,
     'mxsNum': '2', 'mxs': [], 'corpName': '', 'paramType': 4,
     'mxsLength': '8', 'id': '13', 'Stream_ID': 'SET_WORK_TIME', 'toSwitch': '0', 'isFunction': '1'},
    {'isControl': 1, 'state': 1, 'isDisplay': 1, 'isCloudMenu': 0, 'isShow': 0, 'time': '2017-08-01 09:20:19',
     'name': '建议工作时间下限', 'corpMark': '', 'widget': 'input', 'min': 0, 'max': 255,
     'mxsNum': '2', 'mxs': [], 'corpName': '', 'paramType': 4,
     'mxsLength': '8', 'id': '14', 'Stream_ID': 'Suggest_Time_Down', 'toSwitch': '0', 'isFunction': '1'},
    {'isControl': 1, 'state': 1, 'isDisplay': 1, 'isCloudMenu': 0, 'isShow': 0, 'time': '2017-08-01 09:20:19',
     'name': '建议工作时间上限', 'corpMark': '', 'widget': 'input', 'min': 0, 'max': 255,
     'mxsNum': '2', 'mxs': [], 'corpName': '', 'paramType': 4,
     'mxsLength': '8', 'id': '15', 'Stream_ID': 'Suggest_Time_Up', 'toSwitch': '0', 'isFunction': '1'},
    {'isControl': 1, 'state': 1, 'isDisplay': 1, 'isCloudMenu': 0, 'isShow': 0, 'time': '2017-08-01 09:20:19',
     'name': '剩余工作时间', 'corpMark': '', 'widget': 'button', 'min': 0, 'max': 255,
     'mxsNum': '2', 'mxs': [], 'corpName': '', 'paramType': 4,
     'mxsLength': '8', 'id': '16', 'Stream_ID': 'REMAIN_WORK_TIME', 'toSwitch': '0', 'isFunction': '1'},

]
