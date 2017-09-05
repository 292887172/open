pc_conf = {
    'name': "wifi烤箱",
    'model': "STX1",
    'key': "xxxxxxxxxxxxxxxxxxxxx",
    'secret': "yyyyyyyy",
    'functions': [
        {
            'id': 1,
            'no': 1,
            'name': "FAST_HEAT",
            'title': "快热",
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
            'name': "WIND_BAKING",
            'title': "风焙烤",
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
            'name': "BAKE",
            'title': "焙烤",
            'length': 8,
            'values': [
                0,1
            ],
            'value_des': {
                 0: "关",
                1: "开"
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
            'name': "BOTTOM_HEAT",
            'title': "底加热",
            'length': 8,
            'values': [
                0,1
            ],
            'value_des': {
                0: "关",
                1: "开"
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
            'id': 6,
            'no': 6,
            'name': "FAN_GRILL",
            'title': "风扇烤",
            'link':'WASH_TIME',
            'length': 8,
            'value_des': {
                0: "关",
                1: "开"
            },
            'values': [
                0,1
            ],
            'value': 0,
            'unit': "",
            'type': "int",
            'widget': "button",
            'permission': "777"
        },
        {
            'id': 8,
            'no': 8,
            'name': "BARBECUE",
            'title': "烧烤",
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
            'id': 9,
            'no': 9,
            'name': "STRONG_ROAST",
            'title': "强烧烤",
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
            'id': 10,
            'no': 10,
            'name': "CAKE",
            'title': "蛋糕",
            'length': 8,
            'values': [
                0,
                1

            ],
            'value_des': {
                0: "关",
                1: "开"            },
            'value': 0,
            'unit': "",
            'type': "int",
            'widget': "button",
            'permission': "777",
            'triggers': [
            ]
        },
        {
            'id': 11,
            'no': 11,
            'name': "BREAD",
            'title': "面包",
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
            'type': "int",
            'widget': "button",
            'permission': "777",
            'triggers': [
            ]
        },
        {
            'id': 12,
            'no': 12,
            'name': "MEAT",
            'title': "肉类",
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
        }
    ],
    'faults': [
        
    ],
    'params': [
        
    ]
};