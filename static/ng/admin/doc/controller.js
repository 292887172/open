/**
 * Created by nailuoGG on 15/10/19.
 */


'use strict';


angular.module('Admin.doc', ['ngRoute', 'ngDialog'])


    .config(['$routeProvider', function ($routeProvider) {
        $routeProvider.when('/doc', {
            templateUrl: '/static/ng/admin/doc/index.html',
            controller: 'DocIndexCtrl'
        }).when('/doc/menu', {
            templateUrl: '/static/ng/admin/doc/menu.html',
            controller: 'DocMenuCtrl'
        }).when('/doc/change', {
            templateUrl: '/static/ng/admin/doc/change.html',
            controller: 'DocChangeCtrl'
        }).when('/doc/list_doc', {
            templateUrl: '/static/ng/admin/doc/list_doc.html',
            controller: 'DocListCtrl'
        }).when('/doc/add', {
            templateUrl: '/static/ng/admin/doc/add.html',
            controller: 'DocAddCtrl'
        })

    }])

    .controller('DocIndexCtrl', ['$scope', '$http', function ($scope, $http) {
        //console.log($scope);
    }])
    .controller('DocMenuCtrl', ['$scope', '$http', function ($scope, $http) {
        //文档菜单处理

        var orderNum = 0;
        $scope.remove = function (scope) {
            scope.remove();
        };

        $scope.toggle = function (scope) {
            scope.toggle();
        };
        //添加子菜单
        $scope.newSubItem = function (scope) {
            var nodeData = scope.$modelValue;
            nodeData.nodes.push({
                id: nodeData.id * 10 + nodeData.nodes.length,
                title: "新节点" + '.' + (nodeData.nodes.length + 1),
                url: "#",
                ordernum: ++orderNum,
                nodes: []
            });
        };
        //获取所有菜单
        if (typeof $scope.tree_menu == "undefined") {
            $scope.tree_menu = [{
                'id': 1,
                'title': '根节点',
                'url': "#",
                "ordernum": 0,
                'nodes': []
            }];
            $http({
                method: "GET",
                url: window.location.origin + "/center/doc_menu"
            }).success(function (data) {
                console.log("data", data);
                /*对数据进行处理
                 1、先取出一级菜单
                 */
                for (var i = 0; i < data.length; i++) {
                    var item = data[i];
                    if (item.parent_id == 0) {
                        var obj = new Object();
                        obj.id = item.id;
                        obj.title = item.name;
                        obj.ordernum = item.ordernum;
                        obj.url = item.url;
                        obj.nodes = [];
                        $scope.tree_menu[0].nodes.push(obj);
                    }
                }
                //根据ordernum对数组进行排序
                $scope.tree_menu[0].nodes.sort(function (a, b) {
                    return a.ordernum > b.ordernum ? 1 : -1;
                });
                //根据一级菜单，寻找二级菜单
                for (var i = 0; i < $scope.tree_menu[0].nodes.length; i++) {
                    var catalog = $scope.tree_menu[0].nodes[i];
                    for (var j = 0; j < data.length; j++) {
                        var item = data[j];
                        if (item.parent_id == catalog.id) {
                            var obj = new Object();
                            obj.id = item.id;
                            obj.title = item.name;
                            obj.ordernum = item.ordernum;
                            obj.url = item.url;
                            obj.nodes = [];
                            $scope.tree_menu[0].nodes[i].nodes.push(obj);
                        }
                    }
                    //对二级菜单进行排序
                    $scope.tree_menu[0].nodes[i].nodes.sort(function (a, b) {
                        return a.ordernum > b.ordernum ? 1 : -1;
                    });
                }
            })

        }
        $scope.submitDocMenuForm = function (scope) {
            if (confirm("确定要保存修改吗？")) {
                $scope.loading = true;
                $http({
                    method: "POST",
                    url: window.location.origin + "/center/doc_menu",
                    data: $scope.tree_menu[0].nodes,
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
    }])
    .controller('DocAddCtrl', ['$scope', '$http', "ngDialog", function ($scope, $http, ngDialog) {
        // 对话框
        $scope.addDocFormData = {
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
        if (typeof $scope.apis == "undefined") {
            $scope.apis = null;
            $http({
                method: "GET",
                url: window.location.origin + "/center/admin/doc/add?action=get-api"
            }).success(function (data) {
                $scope.apis = data.data;
            }).error(function (error) {
                alert("Failed");
            });
        }
        //显示或隐藏api信息
        $scope.hideApi = function (event) {

            if ($scope.addDocFormData.doc_type != 0) {
                $scope.myhide = true;
            } else {
                $scope.myhide = false;
            }
        }
        // 点击下一步
        $scope.submitDocForm = function (event) {
            //检查数据的合法性
            if ($scope.addDocFormData.doc_type == 0 && $scope.addDocFormData.api_id == null) {
                dialog("请选择要操作的api");
                return false;
            }
            $scope.loading = true;
            $http({
                method: "POST",
                url: window.location.origin + "/center/admin/doc/add",
                data: $.param($scope.addDocFormData),
                headers: {'Content-Type': 'application/x-www-form-urlencoded'}
            }).success(function (data) {
                console.log(data);
                var status = data["status"];
                if (status == 1) {
                    location.href = location.origin + "/center/editormd?doc_id=" + data["data"];
                } else if (status == 2) {
                    alert(data["msg"]);//用alert可以阻塞js执行
                    location.href = location.origin + "/center/editormd?doc_id=" + data["data"];
                } else {
                    dialog(data["msg"]);
                }
                $scope.loading = false;
            }).error(function (error) {
                alert("Failed");
                //window.location.reload();
            })

        };
    }])
    .controller('DocListCtrl', ['$scope', '$http', function ($scope, $http) {
        $scope.delDocData = {
            "csrfmiddlewaretoken": $scope.csrf_token,
            "doc_id": ""
        };
        $scope.delDoc = function (event) {
            $scope.delDocData.doc_id = $(event.target).attr("data-id");
            $http({
                method: "POST",
                url: window.location.origin + "/center/admin/doc/delete",
                data: $.param($scope.delDocData),
                headers: {'Content-Type': 'application/x-www-form-urlencoded'}
            }).success(function (data) {
                if (data['status'] == 1) {
                    mmg.removeRow($(event.target).attr("data-row"));
                    $("#delDocModal").modal("hide");
                } else {
                    alert('failed');
                    $("#delDocModal").modal("hide");
                }
            }).error(function (error) {
                if (data['status'] == 0) {
                    alert('failed');
                    $("#delDocModal").modal("hide");
                }

            })

        };
    }])
    .controller('DocChangeCtrl', ['$scope', '$http', function ($scope, $http) {
    }]);
