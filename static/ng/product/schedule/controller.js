'use strict';

angular.module('Product.schedule', ['ngRoute'])

    .config(['$routeProvider', function ($routeProvider) {
        $routeProvider.when('/schedule', {
            templateUrl: '/static/ng/product/schedule/main.html',
            // controller:
        });
    }])

    .controller('ScheduleCtrl', ['$scope', "$http", function ($scope, $http) {
        $scope.nav.selected("scheduleMenu");
        $scope.productImgSrc = "";
        var str = 0;
        var strs = 0;
        if (str == 0) {
            $http({
                method: "GET",
                url: "/product/schedule/"+ '?' + "key=" + keysss,
                data: {'key': keysss},
                headers: {'Content-Type': 'application/x-www-form-urlencoded'}
            }).success(function (response) {
                // 获取前端接收到的数据
                $scope.response = response;


                var aaa = []

                var file = $("#plans-users")
                $("#plans-users").empty()
                $("#ul_id_party").empty()
                var attrr = $("<option value=\"\">请选择负责方</option>")
                var ul_li = $("#ul_id_party")
                attrr.appendTo(file)
                if ($scope.response[0]['partys']) {
                    $scope.party_list = $scope.response[0]['partys']
                    for (var i = 0, ss = $scope.party_list.length; i < ss; i++) {

                        var li_list = $(" <li>\n" +
                            "                <input type=\"text\" value=\"" + $scope.party_list[i]['title'] + "\">\n" +
                            "                <button class=\"my-user-del\" onclick='Del_Party(this)'>删除</button>\n" +
                            "            </li>")

                        var addtr = $("<option value=\"" + $scope.party_list[i]['title'] + "\">" + $scope.party_list[i]['title'] + "</option>")
                        addtr.appendTo(file)
                        li_list.appendTo(ul_li)
                    }
                } else {
                    console.log('无上传文件')
                }

                layui.use('form', function () {
                    var form = layui.form;
                    form.render('select');
                });

                $("#ul_id").sortable({update:function (event,ui) {

                        layer.confirm('确认提交计划？', {
                            btn: ['确定', '取消'] //按钮
                        },
                        function (index) {
                            console.log("确定");
                            var arr = $( "#ul_id" ).sortable('toArray');
                            console.log(arr);
                            console.log(arr.length);
                            console.log('sss',$scope.response)
                            ss=[]
                            for (var ir =0,il_len = arr.length;ir<il_len;ir++){

                            ss.push($scope.response[parseInt(arr[ir])-1])

                            console.log($scope.response[ir]['id'],ir + 1,arr[ir])
                        }
                            for (var irr =0,il_lens = ss.length;irr<il_lens;irr++){
                                ss[irr]['id'] = irr + 1
                            }
                            console.log(ss)
                            $scope.response = ss;
                            $scope.$apply();
                            layer.close(index);
                            $.ajax({

                                method: "POST",
                                url: "/product/schedule/"+ '?' + "key=" + keysss,
                                data: {'data': JSON.stringify(arr)},
                                headers: {'Content-Type': 'application/x-www-form-urlencoded'}

                            }).success(function (data) {
                                data = JSON.parse(data)
                                console.log('返回的数据',data)
                                if (data['code']==0){
                                    bootbox.alert('更新成功')
                                }else{
                                    bootbox.alert('更新失败')
                                }

                            })
                            },
                        function () {
                            console.log('取消')
                            console.log('sss',$scope.response);
                            $("#ul_id").sortable("cancel")
                        }
                        )

                    }});



                $("#ul_id").disableSelection();

            })


        }
        //如果右侧标签不隐藏，默认显示第一条数据 该请求不刷新页面的情况下 仅请求一次
        if (strs== 0){
             $(".upfile").empty()
             $(".file").empty()
             document.getElementsByClassName("task-ack-name")[0].innerHTML = ''
             document.getElementsByClassName("task-id-name")[0].innerHTML = ''
             document.getElementsByClassName("task-plan-name")[0].innerHTML = ''
             document.getElementsByClassName("remarks")[0].innerHTML ="备注："
             document.getElementsByClassName("times-text")[0].innerHTML =''

             $.ajax({
                type: "POST",
                url: '/product/schedule',
                data: {'key': keysss, "action": "get_detail_plan", "id": 1},
                success: function (data) {
                    data = JSON.parse(data)
                    $scope.responses = data;
                    console.log(data)
                    console.log(data['id'])
                    console.log(data['plan'])
                    console.log($scope.responses['content'])
                    document.getElementsByClassName("task-ack-name")[0].value = data['ack']
                    document.getElementsByClassName("task-id-name")[0].innerHTML = data['id']
                    document.getElementsByClassName("task-plan-name")[0].innerHTML = data['plan']
                    document.getElementsByClassName("names")[0].innerHTML = data['party']
                    document.getElementsByClassName("remarks")[0].innerHTML ="备注："+ data['remark']
                    document.getElementsByClassName("times-text")[0].innerHTML = data['time_stemp']
                    try {
                        var dd = JSON.parse($scope.responses['content'])
                        for (var i = 0, d_length = dd.length; i < d_length; i++) {
                            var file_list = $(".upfile")[0]
                            if (dd[i]['date']){
                                console.log('date')
                            }else{
                                dd[i]['date'] = ''
                            }
                            if (dd[i]['user']){
                                console.log('user')
                            }else{
                                dd[i]['user'] = ''
                            }
                            if (dd[i]['urll']){
                                console.log('urll')
                            }else{
                                dd[i]['urll'] = ''
                            }
                            if (dd[i]['filename']){
                                console.log('filename')
                            }else{
                                dd[i]['filename'] = ''
                            }
                            var addtr = $(
                                "<div class=\"file-list\">\n" +
                                "                    <div class=\"div-flex file-box\">\n" +
                                "                        <a class=\"file-name text-ellipsis\" href=\"/product/download?url=" + dd[i]['urll'] + "&name=" + dd[i]['filename'] + "\">" + dd[i]['filename'] + "</a>\n" +
                                "                        <p class=\"file-user text-ellipsis\">" + dd[i]['user'] + "</p>\n" +
                                "                        <p class=\"file-time\">" + dd[i]['date'] + "</p>\n" +
                                "                        <p class=\"file-dell\" onclick='Deleted(this)'>删除</p>\n" +
                                "                    </div>\n" +
                                "                </div>"
                            )
                            addtr.appendTo(file_list)

                        }
                    }

                    catch (e) {
                        console.log(e)
                    }

                }
            });
        }
             $scope.focus = 0;
        $scope.Show_Detail_Plan = function (that,i_index) {
             $scope.focus = i_index;

             $(".upfile").empty()
             $(".file").empty()
             document.getElementsByClassName("task-ack-name")[0].innerHTML = ''
             document.getElementsByClassName("task-id-name")[0].innerHTML = ''
             document.getElementsByClassName("task-plan-name")[0].innerHTML = ''
             document.getElementsByClassName("remarks")[0].innerHTML ="备注："
             document.getElementsByClassName("times-text")[0].innerHTML =''

             $.ajax({
                type: "POST",
                url: '/product/schedule',
                data: {'key': keysss, "action": "get_detail_plan", "id": that},
                success: function (data) {
                    data = JSON.parse(data)
                    $scope.responses = data;
                    console.log(data)
                    console.log(data['id'])
                    console.log(data['plan'])

                    console.log($scope.responses['content'])
                    document.getElementsByClassName("task-ack-name")[0].value = data['ack']
                    document.getElementsByClassName("task-id-name")[0].innerHTML = data['id']
                    document.getElementsByClassName("task-plan-name")[0].innerHTML = data['plan']
                    document.getElementsByClassName("names")[0].innerHTML = data['party']
                    document.getElementsByClassName("remarks")[0].innerHTML ="备注："+ data['remark']
                    document.getElementsByClassName("times-text")[0].innerHTML = data['time_stemp']
                    try {
                        var dd = JSON.parse($scope.responses['content'])
                        for (var i = 0, d_length = dd.length; i < d_length; i++) {
                            var file_list = $(".upfile")[0]
                            console.log(file_list)
                            if (dd[i]['date']){
                                console.log('date')
                            }else{
                                dd[i]['date'] = ''
                            }
                            if (dd[i]['user']){
                                console.log('user')
                            }else{
                                dd[i]['user'] = ''
                            }
                            if (dd[i]['urll']){
                                console.log('urll')
                            }else{
                                dd[i]['urll'] = ''
                            }
                            if (dd[i]['filename']){
                                console.log('filename')
                            }else{
                                dd[i]['filename'] = ''
                            }
                            var addtr = $(
                                "<div class=\"file-list\">\n" +
                                "                    <div class=\"div-flex file-box\">\n" +
                                "                        <a class=\"file-name text-ellipsis\" href=\"/product/download?url=" + dd[i]['urll'] + "&name=" + dd[i]['filename'] + "\">" + dd[i]['filename'] + "</a>\n" +
                                "                        <p class=\"file-user text-ellipsis\">" + dd[i]['user'] + "</p>\n" +
                                "                        <p class=\"file-time\">" + dd[i]['date'] + "</p>\n" +
                                "                        <p class=\"file-dell\" onclick='Deleted(this)'>删除</p>\n" +
                                "                    </div>\n" +
                                "                </div>"
                            )
                            addtr.appendTo(file_list)

                        }
                    }

                    catch (e) {
                        console.log(e)
                    }

                }
            });

            console.log(that)
        };
        $scope.Save_Plan = function (that) {
            console.log(that);
            layer.confirm('确认提交计划？', {
                btn: ['确定', '取消'] //按钮

            },
                function () {
                console.log("确定");

                $.ajax({
                    type: "POST",
                    url: '/product/schedule',
                    data: {'key': keysss, "action": "save_plan", "num": that},
                    success:function () {
                        layer.msg('已确认', {icon: 1,time:2000});
                        for(var i=0;i<$scope.response.length;i++){
                            if($scope.response[i]['id']==that){

                                $scope.response[i]['ack']=1;
                                $scope.$apply();
                                return
                            }

                        }

                    },
                    error:function (even) {
                        layer.msg('提交失败', {icon: 2,time:2000});
                        console.log(even)
                    }
                })
            },
                function () {
                console.log("取消");
            })
        }
        var being = true;
        $scope.Span_Over = function ($event) {
            if(being){
                let w_span = $($event.target).width();
                if (w_span > 100){
                    w_span = 100
                }
                $($event.target).parent(".text-ellipsis").siblings(".my-tooltip-box").css("left",-(100-w_span)/3 + "px");
                $($event.target).parent(".text-ellipsis").siblings(".my-tooltip-box").fadeIn();
            }
            being = false
        }
        
        $scope.Span_Out = function ($event) {
            being = true;
            $($event.target).parent(".text-ellipsis").siblings(".my-tooltip-box").fadeOut();
        }

    }]);
