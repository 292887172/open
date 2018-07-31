'use strict';

angular.module('Product.schedule', ['ngRoute'])

    .config(['$routeProvider', function ($routeProvider) {
        $routeProvider.when('/schedule', {
            templateUrl: '/static/ng/product/schedule/main.html',
            controller: 'ScheduleCtrl'
        });
    }])

    .controller('ScheduleCtrl', ['$scope', "$http", function ($scope, $http) {
        $scope.nav.selected("scheduleMenu");
        $scope.productImgSrc = "";
        var xx = 0;
        console.log('xxx')
        if (xx == 0) {
            $http({
                method: "GET",
                url: "/product/schedule/"+ '?' + "key=" + keysss,
                data: {'key': keysss},
                headers: {'Content-Type': 'application/x-www-form-urlencoded'}
            }).success(function (response) {
                // 获取前端接收到的数据
                $scope.response = response;
                console.log($scope.response)
            })


        }
    }]);
