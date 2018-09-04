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
        $scope.process="0%";
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
            });
        $scope.get_product = function () {
            console.log('1111');
            $(".item-tips").hide();
            var p = 10;
            $(".progress").show();
            var t = setInterval(function () {
                p = p+5+Math.round(Math.random()*10);
                if (p>90){
                    clearInterval(t);
                    return true
                }
                $scope.process = p+"%";
                $(".progress-bar").css("width", p+"%");
                $(".sr-only").text(p+"%")
            }, 500);
            $http({
                method: "GET",
                url: '/product/protocol/?action=get_project&key='+$scope.key,
                data: $.param({'action': 'get_product'}),
                headers: { 'Content-Type': 'application/x-www-form-urlencoded' }
            }).success(function (data) {
                console.log(data);
                if(data['code']==0){
                    $(".item-download").attr('download','WiFiIot.zip');
                    $(".item-download").attr('href', data['url']).show();
                    clearInterval(t);
                    $scope.process = "100%";
                $(".progress-bar").css("width", "100%");
                $(".sr-only").text("100%")

                }
                else{
                    $(".item-download").hide();
                    $(".item-tips").show()
                }

             })
        }
        $scope.get_products = function () {
            console.log('1111');
            $(".item-tips").hide();
            var p = 10;
            $(".progress").show();
            var t = setInterval(function () {
                p = p+5+Math.round(Math.random()*10);
                if (p>90){
                    clearInterval(t);
                    return true
                }
                $scope.process = p+"%";
                $(".progress-bar").css("width", p+"%");
                $(".sr-only").text(p+"%")
            }, 500);
            $http({
                method: "GET",
                url: '/product/protocol/?action=get_projects&key='+$scope.key,
                data: $.param({'action': 'get_products'}),
                headers: { 'Content-Type': 'application/x-www-form-urlencoded' }
            }).success(function (data) {
                console.log(data);
                if(data['code']==0){
                    // /product/download?url={[{x.url}]}&name=DCIOT.pkg
                    console.log('ssss',data['url'])
                    $(".item-download").attr('download', 'main.lua').show();
                    $(".item-download").attr('href', data['url']).show();
                    clearInterval(t);
                    $scope.process = "100%";
                $(".progress-bar").css("width", "100%");
                $(".sr-only").text("100%")

                }
                else{
                    $(".item-download").hide();
                    $(".item-tips").show()
                }

             })
        }
    }]);