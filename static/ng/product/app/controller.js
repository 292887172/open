'use strict';
angular.module('Product.app', ['ngRoute'])

    .config(['$routeProvider', function ($routeProvider) {
        $routeProvider.when('/app', {
            templateUrl: "/static/ng/product/app/main.html",
            controller: "AppCtrl"
        });
    }])


     .controller('AppCtrl', ['$scope', "$http", function ($scope, $http) {

         $scope.nav.selected("appMenu");
         var xx = 0;
         $scope.sss = 0;
         console.log('s')
         if (xx == 0) {
            console.log(xx)
            $http({
                method: "GET",
                url: "/product/app/"+ '?' + "id=" + $scope.$parent.app_id,

                headers: {'Content-Type': 'application/x-www-form-urlencoded'}
            }).success(function (response) {
                // 获取前端接收到的数据

                $scope.response = response;
                $scope.sss = 1;
                console.log($scope.response)
            })


        }
         $scope.block_mac = function () {

             $scope.app_appid = $("#controlId").attr('data-appid');
             $scope.app_appid = $scope.app_appid.slice(-8);
             console.log($scope.app_appid);
             $scope.data = {'key':$scope.app_appid,'sign':1};
             $http({
                 method: "GET",
                 url: 'https://oven.53iq.com/api/produce/base_html',
                 data: $.param($scope.data),
                 headers: { 'Content-Type': 'application/x-www-form-urlencoded' }
             }).success(function () {
                console.log("请求成功！");
                location.href="https://oven.53iq.com/static/html/move.html?id="+$scope.app_appid+".html";
             }).error(function() {
                console.log("请求失败！");
                location.href="https://oven.53iq.com/static/html/move.html?id="+$scope.app_appid+".html";
             });
         }
     }]);
