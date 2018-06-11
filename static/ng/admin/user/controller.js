/**
 * Created by achais on 15/10/19.
 */
'use strict';

angular.module('Admin.user', ['ngRoute'])

    .config(['$routeProvider', function ($routeProvider) {
        $routeProvider.when('/developer/check', {
            templateUrl: '/static/ng/admin/user/developer_check.html',
            controller: 'DeveloperCheckCtrl'
        })
        .when('/developer/list', {
            templateUrl: '/static/ng/admin/user/developer_list.html',
            controller: 'DeveloperListCtrl'
        })
        .when('/user/list', {
            templateUrl: '/static/ng/admin/user/user_list.html',
            controller: 'UserListCtrl'
        });
    }])

    .controller('DeveloperCheckCtrl', ['$scope', "$http", function ($scope, $http) {
        $scope.checkFormData = {
            "csrfmiddlewaretoken": $scope.csrf_token,
            "developer_id": "",
            "remark": ""
        };
        $scope.failDeveloper = function (event) {
            $scope.checkFormData.developer_id = $(event.target).attr("data-id");
            $scope.checkFormData.action = "fail_developer";
            $http({
                method: "POST",
                url: location.href,
                data: $.param($scope.checkFormData),
                headers: {'Content-Type': 'application/x-www-form-urlencoded' }
            }).success(function (data) {
                if(data.code == 10000) {
                    mmg.removeRow($(event.target).attr("data-row"));
                    $("#failModal").modal("hide");
                }
            }).error(function (error) {
                alert(error);
            })

        };
        $scope.passDeveloper = function (event) {
            $scope.checkFormData.developer_id = $(event.target).attr("data-id");
            $scope.checkFormData.action = "pass_developer";
            $http({
                method: "POST",
                url: location.href,
                data: $.param($scope.checkFormData),
                headers: {'Content-Type': 'application/x-www-form-urlencoded' }
            }).success(function (data) {
                if(data.code == 10000) {
                    mmg.removeRow($(event.target).attr("data-row"));
                    $("#passModal").modal("hide");
                }
            }).error(function (error) {
                console.log(error);
            })

        }
    }])

    .controller('DeveloperListCtrl', ['$scope', "$http", function ($scope, $http) {
        $scope.forbidFormData = {
            "csrfmiddlewaretoken": $scope.csrf_token,
            "developer_id": ""
        };
        $scope.toggleForbidDeveloper = function (event) {
            $scope.forbidFormData.developer_id = $(event.target).attr("data-id");
            $scope.forbidFormData.action = "toggle_forbid_developer";
            $http({
                method: "POST",
                url: location.href,
                data: $.param($scope.forbidFormData),
                headers: {'Content-Type': 'application/x-www-form-urlencoded' }
            }).success(function (data) {
                if(data.code == 10000) {
                    mmg.load();
                    $("#toggleForbidModal").modal("hide");
                }
            }).error(function (error) {
                alert(error);
            })

        };
    }])

    .controller('UserListCtrl', ['$scope', "$http", function ($scope, $http) {
        $scope.forbidFormData = {
            "csrfmiddlewaretoken": $scope.csrf_token,
            "user_id": ""
        };
        $scope.toggleForbidUser = function (event) {
            $scope.forbidFormData.user_id = $(event.target).attr("data-id");
            $scope.forbidFormData.action = "toggle_forbid_user";
            $http({
                method: "POST",
                url: location.href,
                data: $.param($scope.forbidFormData),
                headers: {'Content-Type': 'application/x-www-form-urlencoded' }
            }).success(function (data) {
                if(data.code == 10000) {
                    mmg.load();
                    $("#toggleForbidModal").modal("hide");
                }
            }).error(function (error) {
                alert(error);
            })

        };
    }])
;