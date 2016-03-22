'use strict';

angular.module('Product.dev', ['ngRoute'])

    .config(['$routeProvider', function ($routeProvider) {
        $routeProvider.when('/dev', {
            templateUrl: "/static/ng/product/dev/main.html",
            controller: "DevCtrl"
        });
    }])

    .controller('DevCtrl', ['$scope', "$http", function ($scope, $http) {
        $scope.nav.selected("devMenu");

        /**
         * 提交配置信息表单
         * @constructor
         */
        $scope.SubmitConfigForm = function () {
            $scope.configFormData.action = "update_config";
            $http({
                method: "POST",
                url: location.href,
                data: $.param($scope.configFormData),
                headers: { 'Content-Type': 'application/x-www-form-urlencoded' }
            }).success(function (data) {
                if(data.code == 10000) {
                    window.location.reload();
                }else if(data.code == -2){
                    $.notify({
                        message: "服务器推送地址验证失败"
                    }, {
                        type: 'danger',
                        animate: {
                            enter: 'animated fadeInDown',
                            exit: 'animated fadeOutUp'
                        },
                        offset: 50,
                        spacing: 10,
                        z_index: 1031,
                        delay: 2000,
                        timer: 1000,
                        placement: {
                            from: "top",
                            align: "center"
                        }
                    });
                }
            }).error(function (error) {
                alert(error);
            })
        };

        /**
         * 提交重置AppSecret表单
         * @constructor
         */
        $scope.ResetAppSecret = function () {
            $scope.resetSecretFormData.action = "reset_app_secret";
            $http({
                method: "POST",
                url: location.href,
                data: $.param($scope.resetSecretFormData),
                headers: { 'Content-Type': 'application/x-www-form-urlencoded' }
            }).success(function (data) {
                if(data.code == 10000) {
                    window.location.reload();
                }
            }).error(function (error) {
                alert(error);
            })
        };
    }]);