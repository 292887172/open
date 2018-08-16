'use strict';

angular.module('Product.protocol', ['ngRoute'])

    .config(['$routeProvider', function ($routeProvider) {
        $routeProvider.when('/protocol', {
            templateUrl: '/static/ng/product/protocol/protocol.html',

        })
    }])
    .controller('ProtocolCtrl', ['$scope', "$http", "$location", "$anchorScroll", function ($scope, $http, $location, $anchorScroll) {
        $scope.nav.selected("protocolMenu");
        $scope.frame_length = [1, 2,3,4]; //站位用的长度范围
        $scope.Algorithm = [{"name": "sum", "title": "SUM和校验"}, {"title": "CRC16校验", "name": "crc16"}]; //站位用的长度范围
        $scope.protocol_zdy = false;
        $scope.protocol_type = 0;   // 协议类型， 0：下行， 1：上行
        $scope.protocol_endian = 1;   // 编码规则  1：大端编码，0：小端编码，默认大端编码
        $scope.cur_frame_type_length = '';  // 当前页面上 帧组成部分的个数，比如帧包含 帧头，数据域，校验，则该值为3，主要用于标记新增时候编号累加
        $scope.being = true;    // “+”号是否显示标记
        $scope.frame_data = [
            {"id": 1,"name": "head", "title": "帧头", "length":1, "value": "A5"},
            {"id": 2, "name": "data", "title": "数据域", "length": 4, "value": [{"id": 1, "length":1, "title": "大风"},{"id":2, "length":2, "title":"电源"}]},
            {"id": 3, "name": "check", "title": "校验", "length": 2, "value": {"check_algorithm": "sum", "check_start": 1,"check_end": 2}}
        ];
        $scope.data_menu = '';
        $http({
            method: "GET",
            url: "/product/protocol/" + '?' + "key=" + $scope.$parent.$parent.key + "&action=get_frame_data",
            data: {},
            headers: {'Content-Type': 'application/x-www-form-urlencoded'}
        }).success(function (response) {
                if(response['code']==2){
                    // 标准协议
                    $scope.protocol_zdy=false;
                }
                else{
                    $scope.protocol_zdy=true;
                }
                console.log(response);
                $scope.frame_data=response['data']['frame_content'];
                $scope.protocol_endian = response['data']['endian_type']
            });
        $http({
            method: "GET",
            url: "/product/protocol/" + '?' + "key=" + $scope.$parent.$parent.key + "&action=get_data_content",
            data: {},
            headers: {'Content-Type': 'application/x-www-form-urlencoded'}
        }).success(function (response) {
                $scope.data_menu = response;
                for(var i=0;i<$scope.data_menu.length;i++){
                    if (!$scope.protocol_zdy){
                        $scope.data_menu[i].content=true;
                        for(var j=0;j<$scope.frame_data.length;j++){
                            if ($scope.frame_data[j].name=='data'){
                                $scope.frame_data[j].value=$scope.data_menu;
                            }
                        }
                    }
                }
            });
        $scope.$on("ngRepeatFinished", function () {
            // 监听angular页面渲染完成

            layui.use('form', function () {
                var form = layui.form;
                form.render('select');
            });
            layui.use('form', function () {
                var form = layui.form;
                form.render('radio');
            });
             $(".layui-form-item").delegate('.del-btn',"click", function () {
                 var item_name = $(this).parents(".ui-frame-item").attr('id').split("-")[1];
                 for(var i=0;i<$scope.frame_data.length;i++){
                     if($scope.frame_data[i].name == item_name){
                         $scope.frame_data.splice(i, 1)
                     }
                 }
                $(this).parents(".ui-frame-item").remove();
            });
        });
        $scope.editData=function () {
            tmp_checked_id = [];
            tmp_unchecked_id = [];
            var is_check_all = true;  // 默认全选， 只要有一个选项不选中则置为false
            //处理复选框参数
            var check_content = "";
            console.log($scope.data_menu, $scope.frame_data);
            for(var i=0;i<$scope.frame_data.length;i++){
                if($scope.frame_data[i]['name']=='data'){
                    for(var j=0; j< $scope.data_menu.length;j++){
                        for (var z=0;z<$scope.frame_data[i]['value'].length;z++){
                            if($scope.data_menu[j]['id']== $scope.frame_data[i]['value'][z].id && $scope.frame_data[i]['value'][z].content){
                                $scope.data_menu[j]['content'] = true
                            }
                        }
                    }
                }
            }

            for (var i=0;i<$scope.data_menu.length;i++) {
                if ($scope.data_menu[i].content) {
                    check_content = check_content + '<input class="data-checkbox" lay-filter="data-domain" type="checkbox" name="" value="' + $scope.data_menu[i].id + '" title="' + $scope.data_menu[i].title + '" lay-skin="primary" checked>'
                } else {
                    is_check_all = false
                    check_content = check_content + '<input class="data-checkbox" lay-filter="data-domain" type="checkbox" name="" value="' + $scope.data_menu[i].id + '" title="' + $scope.data_menu[i].title + '" lay-skin="primary">'
                }
            }
            if(is_check_all){
               var check_all_content = '<input type="checkbox" name="" title="全选" lay-filter="click_all" lay-skin="primary" checked>'
            }
            else{
                check_all_content = '<input type="checkbox" name="" title="全选" lay-filter="click_all" lay-skin="primary">'
            }

            layer.open({
                type:1,
                area: ['420px', '260px'], //宽高
                content: '<div class="data-content-item"><form class="layui-form popup-open" action="">\n' +
                check_content +
                '    </form></div><div class="data-all-item"> <form class="layui-form" action="">' + check_all_content +
                '</form></div><div class="data-control-item"><button class="layui-layer-btn0 layui-btn layui-btn-normal" onclick="checkData()">确认</button><button class="layui-layer-btn1 layui-btn layui-btn-primary" onclick="editFunction()">功能不匹配?</button></div>',

                success: function(layero, index){
                    // 弹出成功后回调，
                    layui.use('form', function() {
                        var form = layui.form;
                        // 监听checkbox选择状态
                        form.on('checkbox(data-domain)', function (data) {
                            //console.log(data.elem); //得到checkbox原始DOM对象
                            //console.log(data.elem.checked); //是否被选中，true或者false
                            //console.log(data.value); //复选框value值，也可以通过data.elem.value得到
                            //console.log(data.othis); //得到美化后的DOM对象
                            if(data.elem.checked){
                                tmp_checked_id.push(data.value);
                                var index = tmp_unchecked_id.indexOf(data.value);
                                if(index>=0){
                                    tmp_unchecked_id.splice(index, 1)
                                }
                            }
                            else{
                                tmp_unchecked_id.push(data.value);
                                var index = tmp_checked_id.indexOf(data.value);
                                if(index>=0){
                                    tmp_checked_id.splice(index, 1)
                                }
                            }
                            console.log(tmp_checked_id, tmp_unchecked_id)

                        });
                        form.on('checkbox(click_all)',function (data) {
                            console.log("全选");
                            tmp_checked_id = [];
                            tmp_unchecked_id = [];
                            $(".data-checkbox").each(function () {
                                this.checked = data.elem.checked;
                                if(data.elem.checked){
                                    tmp_checked_id.push(this.value)
                                }
                                else{tmp_unchecked_id.push(this.value)}

                            });
                            form.render('checkbox');
                        })

                    })
                  },

            });
            layui.use('form', function () {
                var form2 = layui.form;
                form2.render('checkbox');
            });

        };
        $scope.editMouseOn=function ($event) {
           // console.log("0n", $event)
            if ($scope.being) {
                $($event.target).children(".add-btn").fadeIn(200, function () {
                    $scope.being = false
                })
            }
        };
        $scope.editMouseLeave=function ($event) {
            //console.log("0ff", $event)
            $($event.target).children(".add-btn").fadeOut(200, function () {
                $scope.being = true
            })

        };
        $scope.addFrameData=function ($event) {
            if($scope.cur_frame_type_length==''){
                $scope.cur_frame_type_length= $(".ui-frame-item").length + $(".new-frame-item").length
            }
            var data_name = $($event.target).parents(".layui-form-item").attr('id').split("-")[1];
            var length = $scope.cur_frame_type_length+1;
            var found_list = new EJS({url: config.url["frame"]}).render({"id": length, "data_name": data_name});
            // console.log(found_list);
            $($event.target).parents(".layui-form-item").append(found_list);
            $scope.cur_frame_type_length+=1;
            layui.use('form', function () {
                var form = layui.form;
                form.render('select');
            });
            $(".layui-form-item").delegate('.del-btn',"click", function () {
                $(this).parents(".new-frame-item").remove();
            });
        };
        $scope.valueKeyUp=function ($event) {
            var n = $($event.target).attr('name').split("-")[1];
            console.log(n, $($event.target).attr('name'), $($event.target).val());
            for (var j = 0; j < $scope.frame_data.length; j++) {
                    if($scope.frame_data[j].name==n){
                        $scope.frame_data[j].value=$($event.target).val();
                    }
                }
        };
        $scope.SubmitData=function () {

            var new_item = $(".new-frame-item").length;
            var tmp_frame_data = {}; // tmp_frame_data = {"head": [{"id": "", "length": "", "name": "", "title": "", "value" :""}]}
            if (new_item > 0){
                $(".new-frame-item").each(function () {
                   var t_id = $(this).attr('id').split("-")[1];
                   var data_name = $(this).attr('data-name');
                   if(tmp_frame_data[data_name]==undefined){
                       tmp_frame_data[data_name] = [];
                   }

                   var t_title =  $('#new-frame-title-'+t_id).find("option:selected").text();      // 中文名称
                   var t_name =  $('#new-frame-title-'+t_id).val();     // 英文标识
                   if(t_name=='other'){
                       t_title = $('#new-frame-tmptitle-'+t_id).children('input').val();
                       t_name = $('#new-frame-bs-'+t_id).children('input').val()
                   }

                   var t_length = parseInt($("#new-frame-length-"+t_id).val());
                   var t_val = $("#new-frame-value-"+t_id).val();
                   var tmp_s = {
                        "id": t_id,
                        "length": t_length,
                        "name": t_name,
                        "title": t_title,
                        "value": t_val,
                        "is_enable": true
                    };
                   tmp_frame_data[data_name].push(tmp_s);
                   // $scope.frame_data.push(tmp_s)
                });
                console.log(tmp_frame_data, "______tmp_frame_data");
                for (var i=0;i <$scope.frame_data.length;i++){
                    var d = tmp_frame_data[$scope.frame_data[i].name];
                    if(d){
                        for (var j=0;j<d.length;j++){
                            $scope.frame_data.splice(i+1+j, 0, d[j]);

                        }
                    }
                }
                $(".new-frame-item").remove();
                setTimeout(function () {
                    // 避免页面还没渲染完，页面上还没有该元素
                    layui.use('form', function () {
                            var form = layui.form;
                            form.render('select');
                        });
                    // 删除按钮绑定事件
                    $(".layui-form-item").delegate('.del-btn',"click", function () {
                         var item_name = $(this).parents(".ui-frame-item").attr('id').split("-")[1];
                         for(var i=0;i<$scope.frame_data.length;i++){
                             if($scope.frame_data[i].name == item_name){
                                 $scope.frame_data.splice(i, 1)
                             }
                         }
                        $(this).parents(".ui-frame-item").remove();
                    });
                }, 500)

            }
            console.log($scope.frame_data);
            $http({
                method: "POST",
                url: "/product/protocol/" + '?' + "key=" + $scope.$parent.$parent.key,
                data: {"action": "update_protocol", "protocol_type": $scope.protocol_type,
                    "protocol_endian": $scope.protocol_endian, "key": $scope.$parent.$parent.key,
                    "frame_content":$scope.frame_data},
                headers: {'Content-Type': 'application/x-www-form-urlencoded'}
            }).success(function (response) {
                    $scope.data_menu = response;
                    // layer.msg('保存成功', {icon: 6, time: 2000});
                    var c = '<div id="" class="layui-layer-padding lay-confirm"><i class="layui-layer-ico layui-layer-ico3 lay-confirm-icon3"></i>协议定义完成，是否生成工程包？</div>' +
                        '<div class="layui-progress lay-my-progress" lay-filter="progress-filter" lay-showPercent="true"><div class="layui-progress-bar" lay-percent="0%"></div></div>' +
                        '<div class="down-control-item"><a class="down-a">下载工程</a><button class="layui-layer-btn0 layui-btn layui-btn-normal" onclick="getProject()">生成工程</button>' +
                        '<button class="layui-layer-btn1 layui-btn layui-btn-primary" onclick="cancelF()">取消</button></div>';
                    layer.open({
                      type: 1,
                      area: ['420px', '240px'], //宽高
                      content: c
                    });

            });
        };
        $scope.getFrameData=function (data_type, frame_zdy) {
            if(frame_zdy){
                var url = "/product/protocol/" + '?' + "key=" + $scope.$parent.$parent.key + "&action=get_frame_data&protocol_type="+data_type+"&zdy="+frame_zdy
            }
            else{
                url = "/product/protocol/" + '?' + "key=" + $scope.$parent.$parent.key + "&action=get_frame_data&protocol_type="+data_type
            }
            $http({
                method: "GET",
                url: url,
                data: {},
                headers: {'Content-Type': 'application/x-www-form-urlencoded'}
            }).success(function (response) {
                console.log(response['data']);
                    if(response['data']!=""){
                        $scope.frame_data=response['data']['frame_content'];
                        //$scope.$apply();
                        console.log($scope.frame_data, '-------');
                        console.log($scope.protocol_zdy)
                            for(var i=0;i<$scope.data_menu.length;i++){
                            if (!$scope.protocol_zdy){
                                // 非自定义
                                console.log("1111111")
                                $scope.data_menu[i].content=true;
                                for(var j=0;j<$scope.frame_data.length;j++){
                                    if ($scope.frame_data[j].name=='data'){
                                        $scope.frame_data[j].value=$scope.data_menu;

                                    }
                                }
                            }
                            else{
                                // 自定义协议
                                for(var i=0;i<$scope.data_menu.length;i++){
                                    $scope.data_menu[i].content=false;
                                }
                            }
                        }


                    }


                });
        }
    }])
    .directive('onFinishRenderFilters', function ($timeout) {
        return {
            restrict: 'A',
            link: function (scope, element, attr) {
                if (scope.$last === true) {    //判断是否是最后一条数据
                    $timeout(function () {
                        scope.$emit('ngRepeatFinished'); //向父级scope传送ngRepeatFinished命令
                    });
                }
            }
        };
    });
var tmp_checked_id = [];
var tmp_unchecked_id = [];
function checkData() {

    //通过controller来获取Angular应用
    var appElement = document.querySelector('[ng-controller=ProtocolCtrl]');
      //获取$scope变量
    var $scope = angular.element(appElement).scope();
    console.log(tmp_checked_id, tmp_unchecked_id, '++++++');
    //清空内容
    $(".btn-active").empty();
    for(var j =0;j<$scope.data_menu.length;j++ ){
        console.log(tmp_unchecked_id, tmp_checked_id, $scope.data_menu[j].id);
        if (tmp_unchecked_id.indexOf(String($scope.data_menu[j].id))>-1) {
            $scope.data_menu[j].content = false;
        }

        else if(tmp_checked_id.indexOf(String($scope.data_menu[j].id))>-1){
            $scope.data_menu[j].content=true;

        }
        if($scope.data_menu[j].content==true){
             $(".btn-active").append("<span class='layui-badge layui-bg-gray'>" + $scope.data_menu[j].title + " </span>")
        }

    }
    for(var z=0;z<$scope.frame_data.length;z++){
        if($scope.frame_data[z].name=='data'){
            $scope.frame_data[z].value=$scope.data_menu
        }
    }
    console.log($scope.data_menu, $scope.frame_data,'------1');
    layer.closeAll('page');
}
function editFunction() {
    layer.closeAll('page');
    window.location.href='#/argue'
}
function getProject() {
    $(".lay-my-progress").show();
     var p = 10;
    layui.use('element', function(){
      var element = layui.element;
      var t = setInterval(function () {
        p = p+5+Math.round(Math.random()*10);
        if (p>90){
            clearInterval(t);
            return true
        }
        element.progress('progress-filter', p+"%");
    }, 300);
         $.ajax({
             type: "GET",
             url: '/product/protocol/?action=get_project&key='+keysss,
             dataType: "json",
             success: function(data){
                 console.log(data);
                if(data['code']==0){
                    $(".down-a").attr('href', data['url']).show();
                    clearInterval(t);
                    element.progress('progress-filter', "100%");
                $(".progress-bar").css("width", "100%");


                }
                else{
                    $(".down-a").hide();
                    $(".item-tips").show()
                }
             }
         });
    });

}
function cancelF() {
    layer.closeAll('page');
}