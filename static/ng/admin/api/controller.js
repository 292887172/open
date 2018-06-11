/**
 * Created by achais on 15/10/15.
 */
'use strict';

angular.module('Admin.api', ['ngRoute'])

    .config(['$routeProvider', function ($routeProvider) {
        $routeProvider.when('/api', {
            templateUrl: '/static/ng/admin/api/index.html',
            controller: 'ApiIndexCtrl'
        }).when('/api/list', {
            templateUrl: '/static/ng/admin/api/list.html',
            controller: 'ApiListCtrl'
        }).when('/api/add', {
            templateUrl: '/static/ng/admin/api/add.html',
            controller: 'ApiAddCtrl'
        }).when('/api/edit', {
            templateUrl: '/static/ng/admin/api/edit.html',
            controller: 'ApiEditCtrl'
        });
    }])

    .controller('ApiIndexCtrl', ['$scope', "$http", function ($scope, $http) {

    }])

/**
 * api列表控制器
 */
    .controller('ApiListCtrl', ['$scope', "$http", function ($scope, $http) {
        $scope.delApiFormData = {
            "csrfmiddlewaretoken": $scope.csrf_token,
            "app_id": "",
            "remark": ""
        };
        $scope.delApi = function (event) {
            $scope.delApiFormData.api_id = $(event.target).attr("data-id");
            $scope.delApiFormData.action = "del_api";
            $http({
                method: "POST",
                url: location.href,
                data: $.param($scope.delApiFormData),
                headers: {'Content-Type': 'application/x-www-form-urlencoded'}
            }).success(function (data) {
                if (data.code == 10000) {
                    mmg.removeRow($(event.target).attr("data-row"));
                    $("#delModal").modal("hide");
                }
            }).error(function (error) {
                alert(error);
            })
        }
    }])

/**
 * api添加控制器
 */
    .controller('ApiAddCtrl', ['$scope', "$http", function ($scope, $http) {
        $scope.apiParamsSelectItems = [
            {
                "name": "请选择",
                "value": ""
            },
            {
                "name": "String",
                "value": "String"
            },
            {
                "name": "Integer",
                "value": "Integer"
            }
        ];
        $scope.addApiFormData = {
            "csrfmiddlewaretoken": $scope.csrf_token,
            "api_name": "",
            "api_url": "",
            "api_type": "",
            "api_request_type": "",
            "api_params": "",
            "api_describe": "",
            "api_return": "",
            "api_doc_url": "",
            "api_action_url": "",
            "api_port": 80,
            "api_classify": "",
            "api_function": "",
            "api_level": 0,
            "api_group": 0,
            "api_invoke_total": 0
        };
        $scope.submitApiForm = function (event) {
            $scope.addApiFormData.action = "add_api";
            $scope.addApiFormData.api_params = [];
            //遍历API参数
            var api_params = $(".api-params .row");
            api_params.each(function (index, element) {
                var param = {};
                param.name = $(this).find(".param-name").eq(0).val().trim();
                param.type = $(this).find(".param-type").eq(0).val().trim();
                param.example = $(this).find(".param-example").eq(0).val().trim();
                param.remark = $(this).find(".param-remark").eq(0).val().trim();
                param.required = $(this).find(".param-required").eq(0)[0].checked ? "true" : "false";
                if (param.name != "" && param.type != "" && param.example != "" && param.required != ""){
                    $scope.addApiFormData.api_params.push(param);
                }
            });
            $scope.addApiFormData.api_params = JSON.stringify($scope.addApiFormData.api_params);
            $http({
                method: "POST",
                url: location.href,
                data: $.param($scope.addApiFormData),
                headers: {'Content-Type': 'application/x-www-form-urlencoded'}
            }).success(function (data) {
                if (data.code == 10000) {
                    window.location.reload();
                }else{
                    alert("内容不够完整请补充");
                }
            }).error(function (error) {
                console.log($scope.addApiFormData);
                alert(error);
            })
        };
    }])

/**
 * api编辑控制器
 */
    .controller('ApiEditCtrl', ['$scope', "$http", "$location", function ($scope, $http, $location) {
        $scope.editApiFormData = {};
        // 获取接口信息
        $scope.api_id = $location.search().id;
        if($scope.api_id){
            $scope.request_url = "/center/admin/api/data?id="+$scope.api_id;
            $http({
                method: "GET",
                url: $scope.request_url,
                headers: {'Content-Type': 'application/x-www-form-urlencoded'}
            }).success(function (ret) {
                if (ret.code == 10000) {
                    $scope.editApiFormData = ret.data;
                    $scope.editApiFormData.csrfmiddlewaretoken = $scope.csrf_token;
                    $scope.api_params = $.parseJSON(ret.data.api_params);
                    $scope.api_params_html = template('params_template', {"list": $scope.api_params});
                    jQuery("#params").append($scope.api_params_html);
                    //遍历API参数
                    var api_params = $(".api-params .row");
                    api_params.each(function (index, element) {
                        if ($scope.api_params[index].required == "true"){
                            $(this).find(".param-required").eq(0).attr("checked", "true");
                        }
                        $(this).find(".param-type").eq(0).find("option").each(function (j, e) {
                            if($(e).val() == $scope.api_params[index].type){$(e).attr("selected", "true");}
                        })
                    });
                }
            }).error(function (error) {
                window.location  = "#/api/list";
            });
        }else{
            window.location = "#/api/list";
        }
        $scope.apiParamsSelectItems = [
            {
                "name": "请选择",
                "value": ""
            },
            {
                "name": "String",
                "value": "String"
            },
            {
                "name": "Integer",
                "value": "Integer"
            }
        ];
        $scope.submitApiForm = function (event) {
            $scope.editApiFormData.action = "update_api";
            $scope.editApiFormData.api_id = $scope.api_id;
            $scope.editApiFormData.api_params = [];
            //遍历API参数
            var api_params = $(".api-params .row");
            api_params.each(function (index, element) {
                var param = {};
                param.name = $(this).find(".param-name").eq(0).val().trim();
                param.type = $(this).find(".param-type").eq(0).val().trim();
                param.example = $(this).find(".param-example").eq(0).val().trim();
                param.remark = $(this).find(".param-remark").eq(0).val().trim();
                param.required = $(this).find(".param-required").eq(0)[0].checked ? "true" : "false";
                if (param.name != "" && param.type != "" && param.example != "" && param.required != ""){
                    $scope.editApiFormData.api_params.push(param);
                }
            });
            $scope.editApiFormData.api_params = JSON.stringify($scope.editApiFormData.api_params);
            $http({
                method: "POST",
                url: location.href,
                data: $.param($scope.editApiFormData),
                headers: {'Content-Type': 'application/x-www-form-urlencoded'}
            }).success(function (data) {
                if (data.code == 10000) {
                    window.location = "#/api/list"
                }else{
                    alert("内容不够完整请补充");
                }
            }).error(function (error) {
                console.log($scope.editApiFormData);
                alert(error);
            })
        };
    }]);