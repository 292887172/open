pc_conf = {
    'name': "油烟机",
    'model': "jcz1",
    'key': "xxxxxxxxxxxxxxxxxxxxx",
    'secret': "yyyyyyyy",
    'functions': [
        {
            'id': 1,
            'no': 1,
            'name': "POWER",
            'title': "电源",
            'length': 8,
            'values': [
                0,
                1
            ],
            'value_des': {
                0: "关",
                1: "开"
            },
            'value': 0,
            'unit': "",
            'type': "bool",
            'widget': "button",
            'permission': "777",
            'triggers': [
            ]
        },

        {
            'id': 2,
            'no': 2,
            'name': "LIGHT",
            'title': "照明",
            'length': 8,
            'values': [
                0,
                1
            ],
            'value_des': {
                0: "关",
                1: "开"
            },
            'value': 0,
            'unit': "",
            'type': "bool",
            'widget': "button",
            'permission': "777",
            'triggers': [
            ]
        },{
            'id': 3,
            'no': 3,
            'name': "TIME_OFF",
            'title': "延时",
            'length': 8,
            'values': [
                0,3
            ],
            'value_des': {
                1:"延时10秒",
                2: "延时30秒",
                3: "延时1分钟"
            },
            'value': 0,
            'unit': "",
            'type': "int",
            'widget': "button",
            'permission': "777",
            'triggers': [
            ]
        },
        {
            'id': 4,
            'no': 4,
            'name': "SMALL_WIND",
            'title': "小风",
            'length': 8,
            'values': [
                0,
                3

            ],
            'value_des': {
                0: "关",
                1: "小风"
            },
            'value': 0,
            'unit': "",
            'type': "int",
            'widget': "button",
            'permission': "777",
            'triggers': [
            ]
        },
        {
            'id': 5,
            'no': 5,
            'name': "MIDDLE_WIND",
            'link':"",
            'title': "中风",
            'length': 8,
            'values': [
                0,2,4
            ],
            'value_des': {
                0: "关",
                1: "中风"
            },
            'value': 0,
            'unit': "",
            'type': "enum",
            'widget': "button",
            'permission': "777",
            'triggers': [
            ]
        },
        {
            'id': 6,
            'no': 6,
            'name': "BIG_WIND",
            'link':"",
            'title': "大风",
            'length': 8,
            'values': [
                0,2,4
            ],
            'value_des': {
                0: "关",
                1: "大风"
            },
            'value': 0,
            'unit': "",
            'type': "enum",
            'widget': "button",
            'permission': "777",
            'triggers': [
            ]
        }
    ],
    'faults': [
        {
            'code': "1",
            'title': "烟雾报警"
        },
        {
            'code': "2",
            'title': "电机故障"
        }
    ],
    'params': [
        {
            'id': 1,
            'no': 1,
            'name': "AIR_THRESHOLD",
            'title': "气敏阈值",
            'length': 1,
            'value': "0.6"
        }
    ]
};