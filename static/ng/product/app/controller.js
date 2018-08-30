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
         var x = 0;
         var xx = 0;
         $scope.sss = 0;
         console.log('s')
         if (x == 0) {
            console.log(x)
            $http({
                method: "GET",
                url: "/product/app/"+ '?' + "num=2&id=" + $scope.$parent.app_id,

                headers: {'Content-Type': 'application/x-www-form-urlencoded'}
            }).success(function (response) {
                // 获取前端接收到的数据
                console.log(response.length)
                if (response.length>0){
                     $scope.responses = response;
                    $scope.sssed = 1;
                }else {
                    console.log($scope.responses)
                }


            })


        }
         if (xx == 0) {
            console.log(xx)
            $http({
                method: "GET",
                url: "/product/app/"+ '?' + "num=1&id=" + $scope.$parent.app_id,

                headers: {'Content-Type': 'application/x-www-form-urlencoded'}
            }).success(function (response) {
                // 获取前端接收到的数据
                console.log(response.length)
                if (response.length>0){
                     $scope.response = response;
                    $scope.sss = 1;
                }else {
                    console.log($scope.response)
                }


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
         };
         $scope.Deletes = function (a,b,c) {
             var ids = location.href.split("=")[1].split("#")[0];
             layer.confirm('确定删除工程包？', {
                btn: ['确定', '取消'] //按钮
                }, function (index) {
                 layer.close(index);
                 if (a == '1') {
                     $http({
                         method: "POST",
                         url: "/product/app/" + '?' + "num=1&version=" + b + "&action=del&id=" + ids,

                     }).success(function (responses) {
                         $(c.target).parent().parent().remove()

                     })
                 } else {
                     $http({
                         method: "POST",
                         url: "/product/app/" + '?' + "num=2&version=" + b + "&action=del&id=" + ids,
                     }).success(function (responsess) {

                         $(c.target).parent().parent().remove()

                     })
                 }
             }, function () {
                        console.log("取消");
                    }
             );
         }
     }]);
