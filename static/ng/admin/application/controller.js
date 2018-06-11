/**
 * Created by achais on 15/10/15.
 */
'use strict';

angular.module('Admin.application', ['ngRoute'])

    .config(['$routeProvider', function ($routeProvider) {
        $routeProvider.when('/application', {
            templateUrl: '/static/ng/admin/application/index.html',
            controller : 'ApplicationIndexCtrl'
        }).when('/application/list', {
            templateUrl: '/static/ng/admin/application/list.html',
            controller : 'ApplicationListCtrl'
        }).when('/application/check', {
            templateUrl: '/static/ng/admin/application/check.html',
            controller : 'ApplicationCheckCtrl'
        }).when('/application/published', {
            templateUrl: '/static/ng/admin/application/published.html',
            controller : 'ApplicationPublishedCtrl'
        });
    }])

    .controller('ApplicationIndexCtrl', ['$scope', "$http", function ($scope, $http) {

    }])

/**
 * 应用列表控制器
 */
    .controller('ApplicationListCtrl', ['$scope', "$http", function ($scope, $http) {
        $scope.checkFormData = {
            "csrfmiddlewaretoken": $scope.csrf_token,
            "app_id"             : "",
            "remark"             : ""
        };
        $scope.failProduct = function (event) {
            $scope.checkFormData.app_id = $(event.target).attr("data-id");
            $scope.checkFormData.action = "fail_product";
            $http({
                method : "POST",
                url    : location.href,
                data   : $.param($scope.checkFormData),
                headers: {'Content-Type': 'application/x-www-form-urlencoded'}
            }).success(function (data) {
                if (data.code == 10000) {
                    mmg.removeRow($(event.target).attr("data-row"));
                    $("#failModal").modal("hide");
                }
            }).error(function (error) {
                alert(error);
            })
        };
    }])

/**
 * 应用审核控制器
 */
    .controller('ApplicationCheckCtrl', ['$scope', "$http", function ($scope, $http) {
        $scope.checkFormData = {
            "csrfmiddlewaretoken": $scope.csrf_token,
            "app_id"             : "",
            "remark"             : ""
        };
        $scope.failProduct = function (event) {
            $scope.checkFormData.app_id = $(event.target).attr("data-id");
            $scope.checkFormData.action = "fail_product";
            $http({
                method : "POST",
                url    : location.href,
                data   : $.param($scope.checkFormData),
                headers: {'Content-Type': 'application/x-www-form-urlencoded'}
            }).success(function (data) {
                if (data.code == 10000) {
                    mmg.removeRow($(event.target).attr("data-row"));
                    $("#failModal").modal("hide");
                }
            }).error(function (error) {
                alert(error);
            })
        };
        $scope.passProduct = function (event) {
            $scope.checkFormData.app_id = $(event.target).attr("data-id");
            $scope.checkFormData.action = "pass_product";
            $http({
                method : "POST",
                url    : location.href,
                data   : $.param($scope.checkFormData),
                headers: {'Content-Type': 'application/x-www-form-urlencoded'}
            }).success(function (data) {
                if (data.code == 10000) {
                    mmg.removeRow($(event.target).attr("data-row"));
                    $("#passModal").modal("hide");
                }
            }).error(function (error) {
                alert(error);
            })
        };
    }])

    /**
 * 已审核通过应用列表控制器
 */
    .controller('ApplicationPublishedCtrl', ['$scope', "$http", function ($scope, $http) {
        $scope.checkFormData = {
            "csrfmiddlewaretoken": $scope.csrf_token,
            "app_id"             : "",
            "remark"             : ""
        };
        $scope.failProduct = function (event) {
            $scope.checkFormData.app_id = $(event.target).attr("data-id");
            $scope.checkFormData.action = "fail_product";
            $http({
                method : "POST",
                url    : location.href,
                data   : $.param($scope.checkFormData),
                headers: {'Content-Type': 'application/x-www-form-urlencoded'}
            }).success(function (data) {
                if (data.code == 10000) {
                    mmg.removeRow($(event.target).attr("data-row"));
                    $("#failModal").modal("hide");
                }
            }).error(function (error) {
                alert(error);
            })
        };
    }]);