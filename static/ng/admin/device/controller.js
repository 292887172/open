/**
 * Created by nailuoGG on 15/10/19.
 */


'use strict';


angular.module('Admin.device', ['ngRoute', 'ngDialog'])


    .config(['$routeProvider', function ($routeProvider) {
        $routeProvider.when('/device', {
            templateUrl: '/static/ng/admin/device/device.html',
            controller: 'deviceAddCtrl'
         })
    }])


    .controller('deviceAddCtrl', ['$scope', '$http', "ngDialog", function ($scope, $http, ngDialog) {
        // 对话框

        var orderNum = 0 ;
        $scope.addDeviceFormData = {
            "csrfmiddlewaretoken": $scope.csrf_token,
            "api_id": null,
            "doc_type": 0,
            "doc_name": "",
        };
        $scope.myhide = false;
        $scope.loading = false;
        var dialog = function (a) {
            ngDialog.open({
                template: 'firstDialogId',
                //controller: 'DocAddCtrl',
                className: 'ngdialog-theme-default',
                data: {foo: a}
            });
        };
        //添加子菜单
        $scope.newSubItem = function (scope) {
            var nodeData = scope.$modelValue;
            nodeData.nodes.push({
                id: nodeData.id * 10 + nodeData.nodes.length,
                title: "产品名称",
                url: "#",
                ordernum: "产品key",

            });
        };
        //获取所有菜单
        if (typeof $scope.tree_menu1 == "undefined") {
            $scope.tree_menu1 = [{
                'id': 1,
                'title': '产品名称',
                'url': "#",
                "ordernum": '8位产品key',
                'nodes': []
            }];
            $http({

                method: "GET",
                url: window.location.origin + "/center/doc_device"
            }).success(function (data) {

                /*对数据进行处理
                 1、先取出一级菜单
                 */
                for (var i = 0; i < data.length; i++) {

                    var item1 = data[i];
                        var obj = new Object();
                        obj.id = item1.id;
                        obj.title = item1.name;
                        obj.ordernum = item1.device_key;
                        obj.url = item1.url;
                        obj.sort = item1.sort;
                        obj.nodes = [];
                        $scope.tree_menu1[0].nodes.push(obj);
                    }
                    // 根据obj.sort进行排序
                    $scope.tree_menu1[0].nodes.sort(function (a,b) {
                        return a.sort > b.sort ? 1 : -1;
                    })

            })

        }
        // 保存操作
        $scope.submitDeviceMenuForm = function (scope) {
            if (confirm("确定要保存修改吗？")) {
                $scope.loading = true;
                $http({
                    method: "POST",
                    url: window.location.origin + "/center/doc_device",
                    data: $scope.tree_menu1[0].nodes,
                    headers: {'Content-Type': 'application/x-www-form-urlencoded'}
                }).success(function (res) {
                    if (res.status == 1) {
                        location.reload();
                    } else {
                        alert("操作失败");
                    }
                    $scope.loading = false;
                });
            }
        }
    }]);



