/**
 * Created by achais on 15/10/15.
 */
'use strict';

angular.module('Admin.function', ['ngRoute'])

    .config(['$routeProvider', function ($routeProvider) {
        $routeProvider.when('/function', {
            templateUrl: '/static/ng/admin/function/index.html',
            controller : 'FunctionIndexCtrl'
        }).when('/function/list', {
            templateUrl: '/static/ng/admin/function/list.html',
            controller : 'FunctionListCtrl'
        }).when('/function/check', {
            templateUrl: '/static/ng/admin/function/check.html',
            controller : 'FunctionCheckCtrl'
        }).when('/function/published', {
            templateUrl: '/static/ng/admin/function/published.html',
            controller : 'FunctionPublishedCtrl'
        });
    }])

    .controller('FunctionIndexCtrl', ['$scope', "$http", function ($scope, $http) {

    }])

/**
 * 应用列表控制器
 */
    .controller('FunctionListCtrl', ['$scope', "$http", function ($scope, $http) {
        $scope.checkFormData = {
            "csrfmiddlewaretoken": $scope.csrf_token,
            "key"             : ""
        };
        $scope.failFunction = function (event) {
            $scope.checkFormData.key = $(event.target).attr("data-key");
            $scope.checkFormData.id = $(event.target).attr("data-id");
            $scope.checkFormData.action = "fail_function";
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
    .controller('FunctionCheckCtrl', ['$scope', "$http", function ($scope, $http) {
        $scope.checkFormData = {
            "csrfmiddlewaretoken": $scope.csrf_token,
            "key"             : "",
        };
        $scope.failFunction = function (event) {
            $scope.checkFormData.key = $(event.target).attr("data-key");
            $scope.checkFormData.id = $(event.target).attr("data-id");
            $scope.checkFormData.action = "fail_function";
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
        $scope.passFunction = function (event) {
            $scope.checkFormData.key = $(event.target).attr("data-key");
            $scope.checkFormData.id = $(event.target).attr("data-id");
            $scope.checkFormData.action = "pass_function";
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
    .controller('FunctionPublishedCtrl', ['$scope', "$http", function ($scope, $http) {
        $scope.checkFormData = {
            "csrfmiddlewaretoken": $scope.csrf_token,
            "key"             : "",
        };
        $scope.failFunction = function (event) {
            $scope.checkFormData.key = $(event.target).attr("data-key");
            $scope.checkFormData.id = $(event.target).attr("data-id");
            $scope.checkFormData.action = "fail_function";
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