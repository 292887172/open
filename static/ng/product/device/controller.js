/**
 * Created by achais on 15/9/8.
 */
'use strict';

angular.module('Product.device', ['ngRoute'])
    .config(['$routeProvider', function ($routeProvider) {
        $routeProvider.when('/device', {
            templateUrl: "/static/ng/product/device/main.html",
            controller: "deviceCtrl"
        });
    }])

    .controller('deviceCtrl', ['$scope', "$http", function ($scope, $http) {
        $scope.nav.selected("deviceMenu");
        $http({
                method: "POST",
                url: location.href,
                data: $.param({'name': 'device_table'}),
                headers: { 'Content-Type': 'application/x-www-form-urlencoded' }
            }).success(function (data) {
                $scope.data_list = data.data;
                $scope.key = data.key;
                $scope.state = data.check_state;
                $(".loading").css("display",'none');
                console.log("加载完成....");
                if(! $scope.data_list){
                    $("#device-info").css("display","none");
                    $("#barcon").css("display","none");
                    $("#no-info").css("display","block");
                 }
                 else{
                    load_table($scope.data_list,$scope.state)
                }

            }).error(function (error) {
                console.log("请等待加载:",error)
            })
    }]);