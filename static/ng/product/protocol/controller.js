'use strict';

angular.module('Product.protocol', ['ngRoute'])

    .config(['$routeProvider', function ($routeProvider) {
        $routeProvider.when('/protocol', {
            templateUrl: '/static/ng/product/protocol/protocol.html',

        })
    }])
    .controller('ProtocolCtrl', ['$scope', "$http", "$location", "$anchorScroll", function ($scope, $http, $location, $anchorScroll) {
        $scope.nav.selected("protocolMenu");
        $scope.frame_length = 0;
        var xx = 0;
        $scope.list_mode = [{"val": "A55A", "title": "帧头", "number": 1}, {
            "val": "00",
            "title": "流水号",
            "number": 2
        }, {"val": "00", "title": "协议版本", "number": 3},
            {"val": "00", "title": "数据类型", "number": 4}, {"val": "00", "title": "帧长", "number": 5}, {
                "val": "00x15",
                "title": "帧数据",
                "number": 6
            },
            {"val": "00", "title": "校验", "number": 7}];
        $scope.data_menu = [{
            'id': 1,
            'title': 'power',
            'length': 2
        }, {
            'id': 2,
            'title': 'wind',
            'length': 2
        }, {
            'id': 3,
            'title': 'light',
            'length': 2
        }, {
            'id': 4,
            'title': 'dry',
            'length': 2
        }, {
            'id': 5,
            'title': 'time',
            'length': 8
        }, {
            'id': 6,
            'title': 'temp',
            'length': 16
        }, {
            'id': 7,
            'title': 'wind_left',
            'length': 8
        }];

        for (var j = 0; j < $scope.data_menu.length; j++) {
            $scope.frame_length += $scope.data_menu[j].length
        }
        if (xx == 0) {
            $http({
                method: "GET",
                url: "/product/protocol/" + '?' + "key=" + $scope.$parent.$parent.key,
                data: {'key': $scope.$parent.$parent.key},
                headers: {'Content-Type': 'application/x-www-form-urlencoded'}
            })
                .success(function (response) {
                    // 获取前端接收到的数据
                    $scope.response = response.data;
                    console.log($scope.response.frame_content[0]['length'])
                    $scope.response.protocol_type = response.protocol_type;
                    if (response.code == 1) {
                        // 非标协议
                        document.getElementById("custom-item").checked = true;
                        console.log('非标')
                        setTimeout(function () {
                            show_or_hide($scope.response.frame_content[0]['length'])
                        }, 100)
                    }
                    else {
                        // 标准协议
                        document.getElementById("standard-item").checked = true;

                    }
                    //上下行判断

                    if (response.protocol_type == 1) {
                        // 下行被选中
                        document.getElementById("x_x").selected = true;
                        //$scope.response.frame_content[0]['code']=[{"desc": "发送码", "value": "5AA5", "type": "response"}]

                    }
                    else {
                        //上行被选中
                        document.getElementById("s_x").selected = true;
                        //$scope.response.frame_content[0]['code']=[{"desc": "发送码", "value": "A55A", "type": "send"}]

                    }

                    $scope.list_mode = [];
                    for (var i = 0; i < $scope.response.frame_content.length; i++) {
                        if ($scope.response.frame_content[i]['code'] && $scope.response.frame_content[i]['code'].length > 0) {
                            var tmp = {
                                "title": $scope.response.frame_content[i]['title'],
                                "val": $scope.response.frame_content[i]['code'][0]['value'],
                                'number': $scope.response.frame_content[i]['number']
                            }
                        } else {
                            if (parseInt($scope.response.frame_content[i]['length']) > 1) {
                                var t_val = "00*" + $scope.response.frame_content[i]['length']
                            }

                            else {
                                t_val = "00*N"
                            }

                            tmp = {
                                "title": $scope.response.frame_content[i]['title'],
                                "val": t_val,
                                'number': $scope.response.frame_content[i]['number']
                            }
                        }

                        $scope.list_mode.push(tmp)

                    }
                });
            setTimeout(function () {
                foo();

            }, 200)

            $http({
                method: "GET",
                url: "/product/protocol/" + '?' + "key=" + $scope.$parent.$parent.key + "&action=get_data_content",
                data: {},
                headers: {'Content-Type': 'application/x-www-form-urlencoded'}
            })
                .success(function (response) {

                    $scope.data_menu = response;
                    console.log($scope.data_menu)
                    $scope.frame_length = 0;
                    for (var j = 0; j < $scope.data_menu.length; j++) {
                        console.log($scope.data_menu[j].length);
                        $scope.frame_length += parseInt($scope.data_menu[j].length)
                    }
                })


        }
        $scope.BzProtocol = function (scope) {
            $http({
                method: "GET",
                url: "/product/protocol/" + '?' + "key=" + $scope.$parent.$parent.key,
                data: {'key': $scope.$parent.$parent.key},
                headers: {'Content-Type': 'application/x-www-form-urlencoded'}
            })
                .success(function (response) {
                    // 获取前端接收到的数据
                    $scope.response = response.data;
                    $scope.response.protocol_type = response.protocol_type;
                    //上下行判断

                    if (response.protocol_type == 1) {
                        // 下行被选中
                        document.getElementById("x_x").selected = true;


                    }
                    else {
                        //上行被选中
                        document.getElementById("s_x").selected = true;

                    }

                    $scope.list_mode = [];
                    for (var i = 0; i < $scope.response.frame_content.length; i++) {
                        if ($scope.response.frame_content[i]['code'] && $scope.response.frame_content[i]['code'].length > 0) {
                            var tmp = {
                                "title": $scope.response.frame_content[i]['title'],
                                "val": $scope.response.frame_content[i]['code'][0]['value'],
                                'number': $scope.response.frame_content[i]['number']
                            }
                        } else {
                            if (parseInt($scope.response.frame_content[i]['length']) / 8 > 1) {
                                var t_val = "00*" + parseInt($scope.response.frame_content[i]['length']) / 8
                            }

                            else if (String($scope.response.frame_content[i]['length']).indexOf("*") > 0) {
                                t_val = "00*N"
                            }
                            else {
                                t_val = "00"
                            }
                            tmp = {
                                "title": $scope.response.frame_content[i]['title'],
                                "val": t_val,
                                'number': $scope.response.frame_content[i]['number']
                            }
                        }

                        $scope.list_mode.push(tmp)

                    }
                    setTimeout(function () {
                        foo();
                        console.log('标准点击')
                        try {
                            show_or_hide($scope.response.frame_content[0]['length'])
                        }
                        catch (err) {
                            console.log('错误pass')
                        }
                    }, 100)
                })
        }
        $scope.ZdyProtocol = function (scope) {
            $scope.response.protocol_type = $("#select_id option:selected").val();
            $http({
                method: "GET",
                url: "/product/protocol/" + '?' + "key=" + $scope.$parent.$parent.key + '&zdy=' + $scope.response.protocol_type,
                data: {'key': $scope.$parent.$parent.key},
                headers: {'Content-Type': 'application/x-www-form-urlencoded'}
            })
                .success(function (response) {
                    // 获取前端接收到的数据
                    $scope.response = response.data;
                    $scope.response.protocol_type = response.protocol_type;
                    //上下行判断
                    console.log($scope.response.frame_content[0]);
                    //new add data list
                    var new_data_list = response.data.frame_content[2]["code"];
                    console.log(new_data_list)
                    if (response.protocol_type == 1) {
                        // 下行被选中
                        document.getElementById("x_x").selected = true;
                        $scope.response.frame_content[0]['code'] = [{
                            "desc": "发送码",
                            "value": "5AA5",
                            "type": "response"
                        }]

                    }
                    else {
                        //上行被选中
                        document.getElementById("s_x").selected = true;
                        $scope.response.frame_content[0]['code'] = [{"desc": "发送码", "value": "A55A", "type": "send"}]

                    }

                    $scope.list_mode = [];
                    for (var i = 0; i < $scope.response.frame_content.length; i++) {
                        if ($scope.response.frame_content[i]['code'] && $scope.response.frame_content[i]['code'].length > 0) {
                            var tmp = {
                                "title": $scope.response.frame_content[i]['title'],
                                "val": $scope.response.frame_content[i]['code'][0]['value'],
                                'number': $scope.response.frame_content[i]['number']
                            }
                        } else {
                            if (parseInt($scope.response.frame_content[i]['length']) / 8 > 1) {
                                var t_val = "00*" + parseInt($scope.response.frame_content[i]['length']) / 8
                            }

                            else if (String($scope.response.frame_content[i]['length']).indexOf("*") > 0) {
                                t_val = "00*N"
                            }
                            else {
                                t_val = "00"
                            }
                            tmp = {
                                "title": $scope.response.frame_content[i]['title'],
                                "val": t_val,
                                'number': $scope.response.frame_content[i]['number']
                            }
                        }
                        console.log(tmp)
                        $scope.list_mode.push(tmp)

                    }
                })
            setTimeout(function () {
                foo();
                show_or_hide($scope.response.frame_content[0]['length'])
            }, 100)
        };
        $scope.TypeProtocol = function (scope) {
            console.log('weishenmebuhaishi')
            $scope.response.key = $scope.$parent.$parent.key;
            $scope.response.action = "update_protocol";
            $scope.response.heart_rate = "500";
            $scope.response.repeat_rate = "500";
            $scope.response.repeat_count = "3";
            $scope.response.fivechoose = ["true", "true", "true", "true", "true"];
            // 获取循环体的value
            // 根据是否启用获取响应的value 启用则获取value 不启用这

            var list_1 = [];
            $(".x1x input[value]").each(function () {
                var v = $(this).val();
                list_1.push(v);
            });
            console.log(list_1)
            var list_2 = [];
            var for2 = document.getElementsByClassName("taf");
            for (var g = 0, lll2 = for2.length; g < lll2; g++) {
                var obj1 = for2[g].checked;
                console.log(obj1);
                list_2.push(obj1)
            }
            console.log(list_2)
            // 终极循环
            var li = [];
            var z1 = document.getElementsByClassName("x1x");
            console.log(z1)
            for (var ze = 0; ze < z1.length; ze++) {
                console.log("循环开始");
                var list_code = [];
                var dict_1 = {};

                var z2 = z1[ze].getElementsByTagName("input");
                var codeItem = z1[ze].getElementsByClassName("code-item");
                var select_1 = z1[ze].getElementsByTagName("select");
                dict_1["name"] = $(z1[ze]).data("name");
                dict_1["title"] = z2[0].value;
                dict_1["is_enable"] = z2[1].checked;
                dict_1["number"] = z2[2].value;
                //$("#select_option option:selected").val()

                dict_1["length"] = $(select_1).children("option:selected").val();
                console.log(dict_1)
                for (var k = 0; k < codeItem.length; k++) {
                    var tmp = {"type": $(codeItem[k]).data('type'), "desc": $(codeItem[k]).children("span").text()};
                    var lengtt = codeItem[k].getElementsByTagName("input").length;
                    console.log(lengtt)
                    if (lengtt) {
                        var v_aa = '';
                        for (var zz = 0; zz < parseInt($(select_1).children("option:selected").val()); zz++) {
                            if (codeItem[k].getElementsByTagName("input").length > 1) {
                                var v_z = codeItem[k].getElementsByTagName("input")[zz].value;
                                console.log(v_z)
                                v_aa += v_z
                            } else {
                                var v_z = codeItem[k].getElementsByTagName("input")[0].value;
                                console.log(v_z)
                                v_aa = v_z

                            }

                        }
                    }

                    tmp['value'] = v_aa
                    console.log(tmp)
                    list_code.push(tmp)
                }
                console.log(list_code)
                dict_1['code'] = list_code;
                console.log(dict_1)
                li.push(dict_1);
                // 获取新增code
                var new_class_data = z1[ze].getElementsByClassName("new_class");
                if (new_class_data) {
                    for (var v = 0, list_new_data = new_class_data.length; v < list_new_data; v++) {
                        var dict_class_list = {};
                        var new_data_class = new_class_data[v].getElementsByTagName("input")
                        dict_class_list["desc"] = new_data_class[0].value;
                        dict_class_list["type"] = "new_data";
                        dict_class_list["value"] = new_data_class[1].value;
                        list_code.push(dict_class_list);
                        console.log(list_code);
                    }
                } else {
                    console.log('无新政家数据')
                }
            }

            var zdy_data = document.getElementsByClassName("x11x");
            for (var i = 0, list_zdy = zdy_data.length; i < list_zdy; i++) {
                var zdy_input = zdy_data[i].getElementsByTagName("input");
                var dict_2 = {"code": []};
                dict_2["title"] = zdy_input[0].value;
                dict_2["is_enable"] = "true";
                dict_2["number"] = zdy_input[1].value;
                dict_2["length"] = zdy_input[2].value;
                dict_2["code"].push({"desc": zdy_input[3].value, "value": zdy_input[4].value});
                console.log(dict_2.length);
                if (dict_2.length > 0) {
                    li.push(dict_2)
                } else {
                    console.log(dict_2)
                }
            }
            $scope.response.typesss = "change";
            $scope.response.frame_taf = list_2;
            $scope.response.frame_content = li;
            $scope.response.start_check_number = $("#input_04").val();
            $scope.response.end_check_number = $("#input_05").val();
            $scope.response.checkout_algorithm = $("#select_option option:selected").val();
            //上下行传参
            $scope.response.protocol_type = $("#select_id option:selected").val();
            console.log($scope.response)
            $http({
                method: "POST",
                url: "/product/protocol/" + '?' + "key=" + $scope.$parent.$parent.key,
                data: $scope.response,
                headers: {'Content-Type': 'application/x-www-form-urlencoded'}
            }).success(function (response1) {
               // console.log('拿回的数据',response1)
                $scope.response = response1;

                $scope.response.protocol_type = response1.protocol_type;
                //上下行判断
                console.log($scope.response.frame_content[0]);
                //new add data list
                var new_data_list = response1.frame_content[2]["code"];
                console.log(new_data_list)
                if (response1.protocol_type == 1) {
                    // 下行被选中
                    document.getElementById("x_x").selected = true;


                }
                else {
                    //上行被选中
                    document.getElementById("s_x").selected = true;


                }

                $scope.list_mode = [];
                for (var i = 0; i < $scope.response.frame_content.length; i++) {
                    if ($scope.response.frame_content[i]['code'] && $scope.response.frame_content[i]['code'].length > 0) {
                        var tmp = {
                            "title": $scope.response.frame_content[i]['title'],
                            "val": $scope.response.frame_content[i]['code'][0]['value'],
                            'number': $scope.response.frame_content[i]['number']
                        }
                    } else {
                        if (parseInt($scope.response.frame_content[i]['length']) / 8 > 1) {
                            var t_val = "00*" + parseInt($scope.response.frame_content[i]['length']) / 8
                        }

                        else if (String($scope.response.frame_content[i]['length']).indexOf("*") > 0) {
                            t_val = "00*N"
                        }
                        else {
                            t_val = "00"
                        }
                        tmp = {
                            "title": $scope.response.frame_content[i]['title'],
                            "val": t_val,
                            'number': $scope.response.frame_content[i]['number']
                        }
                    }
                    console.log(tmp)
                    $scope.list_mode.push(tmp)

                }
            });
        custom();
        setTimeout(function () {
                foo();

                show_or_hide($scope.response.frame_content[0]['length'])
            }, 200);
        };
        $scope.SubmitProtocol = function (scope) {
            $scope.response.key = $scope.$parent.$parent.key;
            $scope.response.action = "update_protocol";
            $scope.response.heart_rate = "500";
            $scope.response.repeat_rate = "500";
            $scope.response.repeat_count = "3";
            $scope.response.fivechoose = ["true", "true", "true", "true", "true"];
            // 获取循环体的value
            // 根据是否启用获取响应的value 启用则获取value 不启用这

            var list_1 = [];
            $(".x1x input[value]").each(function () {
                var v = $(this).val();
                list_1.push(v);
            });
            console.log(list_1)
            var list_2 = [];
            var for2 = document.getElementsByClassName("taf");
            for (var g = 0, lll2 = for2.length; g < lll2; g++) {
                var obj1 = for2[g].checked;
                console.log(obj1);
                list_2.push(obj1)
            }
            console.log(list_2)
            // 终极循环
            var li = [];
            var z1 = document.getElementsByClassName("x1x");
            console.log(z1)
            for (var ze = 0; ze < z1.length; ze++) {
                console.log("循环开始");
                var list_code = [];
                var dict_1 = {};

                var z2 = z1[ze].getElementsByTagName("input");
                var codeItem = z1[ze].getElementsByClassName("code-item");
                var select_1 = z1[ze].getElementsByTagName("select");
                dict_1["name"] = $(z1[ze]).data("name");
                dict_1["title"] = z2[0].value;
                dict_1["is_enable"] = z2[1].checked;
                dict_1["number"] = z2[2].value;
                //$("#select_option option:selected").val()
                if(dict_1['name'] == 'data_domain'){
                    dict_1["length"] = $("#data_domain_length").data("length")
                }else{
                    dict_1["length"] = $(select_1).children("option:selected").val();
                }

                console.log(dict_1)
                for (var k = 0; k < codeItem.length; k++) {
                    var tmp = {"type": $(codeItem[k]).data('type'), "desc": $(codeItem[k]).children("span").text()};
                    var lengtt = codeItem[k].getElementsByTagName("input").length;
                    console.log(lengtt)
                    if (lengtt) {
                        var v_aa = '';
                        for (var zz = 0; zz < parseInt($(select_1).children("option:selected").val()); zz++) {
                            if (codeItem[k].getElementsByTagName("input").length > 1) {
                                var v_z = codeItem[k].getElementsByTagName("input")[zz].value;
                                console.log(v_z)
                                v_aa += v_z
                            } else {
                                var v_z = codeItem[k].getElementsByTagName("input")[0].value;
                                console.log(v_z)
                                v_aa = v_z

                            }

                        }
                    }

                    tmp['value'] = v_aa
                    console.log(tmp)
                    list_code.push(tmp)
                }
                console.log(list_code)
                dict_1['code'] = list_code;
                console.log(dict_1)
                li.push(dict_1);
                // 获取新增code
                var new_class_data = z1[ze].getElementsByClassName("new_class");
                if (new_class_data) {
                    for (var v = 0, list_new_data = new_class_data.length; v < list_new_data; v++) {
                        var dict_class_list = {};
                        var new_data_class = new_class_data[v].getElementsByTagName("input")
                        dict_class_list["desc"] = new_data_class[0].value;
                        dict_class_list["type"] = "new_data";
                        dict_class_list["value"] = new_data_class[1].value;
                        list_code.push(dict_class_list);
                        console.log(list_code);
                    }
                } else {
                    console.log('无新政家数据')
                }
            }

            var zdy_data = document.getElementsByClassName("x11x");
            for (var i = 0, list_zdy = zdy_data.length; i < list_zdy; i++) {
                var zdy_input = zdy_data[i].getElementsByTagName("input");
                var dict_2 = {"code": []};
                dict_2["title"] = zdy_input[0].value;
                dict_2["is_enable"] = "true";
                dict_2["number"] = zdy_input[1].value;
                dict_2["length"] = zdy_input[2].value;
                dict_2["code"].push({"desc": zdy_input[3].value, "value": zdy_input[4].value});
                console.log(dict_2.length);
                if (dict_2.length > 0) {
                    li.push(dict_2)
                } else {
                    console.log(dict_2)
                }
            }
            $scope.response.frame_taf = list_2;
            $scope.response.frame_content = li;
            $scope.response.start_check_number = $("#input_04").val();
            $scope.response.end_check_number = $("#input_05").val();
            $scope.response.checkout_algorithm = $("#select_option option:selected").val();
            //上下行传参
            $scope.response.protocol_type = $("#select_id option:selected").val();
            console.log($scope.response)
            $http({
                method: "POST",
                url: "/product/protocol/" + '?' + "key=" + $scope.$parent.$parent.key,
                data: $scope.response,
                headers: {'Content-Type': 'application/x-www-form-urlencoded'}
            }).success(function (response1) {
               // console.log('拿回的数据',response1)

                jQuery.extend({
                        alertWindow:function(e,n){var e=e,r;n===undefined?r="#00a8b7":r=n;
                        if($("body").find(".alertWindow1").length===0){
                            var i='<div class="alertWindow1" style="width: 100%;height: 100%; background:rgba(0,0,0,0.5);position: fixed; left:0px; top: 0px; z-index: 9999;"><div  style="width: 360px; height: 170px;background: #FFF;margin: 300px auto;border: 2px solid #CFCFCF;">'+'<div  style="width: inherit;height: 20px;">'+'<div class="alertWindowCloseButton1" style="float: right; width: 10px; height: 30px;margin-right:5px;font-family:\'microsoft yahei\';color:'+r+';cursor: pointer;"></div>'+"</div>"+'<div id="successImg" class="alertWindowTitle" style="margin-top:10px;width:100px;text-align:center;font-family:\'Verdana, Geneva, Arial, Helvetica, sans-serif\';font-size: 18px;font-weight: normal;color: '+r+';">'+"</div>"+'<div class="alertWindowContent" style="width:360px;height: 40px;text-align:center;font-size: 18px;color: #7F7F7F;margin-top:10px;">'+e+"</div>"+"</div>"+"</div>";
                            $("body").append(i);
                            var s=$(".alertWindow1");
                            //2秒后自动关闭窗口
                            setTimeout(function(){s.hide()},1000);
                        }
                        else {$(".alertWindowContent").text(e),$(".alertWindow1").show(),setTimeout(function(){$(".alertWindow1").hide()},1000);}
                        }
                        })
                jQuery.alertWindow("保存成功");
                $scope.response = response1;

                $scope.response.protocol_type = response1.protocol_type;
                //上下行判断
                console.log($scope.response.frame_content[0]);
                //new add data list
                var new_data_list = response1.frame_content[2]["code"];
                console.log(new_data_list)
                if (response1.protocol_type == 1) {
                    // 下行被选中
                    document.getElementById("x_x").selected = true;


                }
                else {
                    //上行被选中
                    document.getElementById("s_x").selected = true;


                }

                $scope.list_mode = [];
                for (var i = 0; i < $scope.response.frame_content.length; i++) {
                    if ($scope.response.frame_content[i]['code'] && $scope.response.frame_content[i]['code'].length > 0) {
                        var tmp = {
                            "title": $scope.response.frame_content[i]['title'],
                            "val": $scope.response.frame_content[i]['code'][0]['value'],
                            'number': $scope.response.frame_content[i]['number']
                        }
                    } else {
                        if (parseInt($scope.response.frame_content[i]['length']) / 8 > 1) {
                            var t_val = "00*" + parseInt($scope.response.frame_content[i]['length']) / 8
                        }

                        else if (String($scope.response.frame_content[i]['length']).indexOf("*") > 0) {
                            t_val = "00*N"
                        }
                        else {
                            t_val = "00"
                        }
                        tmp = {
                            "title": $scope.response.frame_content[i]['title'],
                            "val": t_val,
                            'number': $scope.response.frame_content[i]['number']
                        }
                    }
                    $scope.list_mode.push(tmp)

                }
            });
        custom();
        setTimeout(function () {
                foo();
                show_or_hide($scope.response.frame_content[0]['length'])
            }, 200)
        };


$scope.gotoPosition = function (positionId) {
    console.log(positionId)

    // 将location.hash的值设置为
    // 你想要滚动到的元素的id
    $location.hash("protocolx" + positionId + "x");

    // 调用 $anchorScroll()
    $anchorScroll();
    xx = 1

    };

$scope.range = function (n) {
    return new Array(n);
    };

    }])
    ;