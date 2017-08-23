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
        // flag标记判断是否有设备管理的数据
        $scope.nav.selected("deviceMenu");
        if(! $scope.flag){
            $("#device-info").css("display","none");
            $("#no-info").css("display","block");
        }
        //分页显示
        $scope.pageSize=20;　　
/*
            console.log("分页显示");
            var item = $scope.flag;
            $scope.data = item;
            $scope.pages = Math.ceil($scope.data.rows[0].cells.length / $scope.pageSize); //分页数
            $scope.newPages = $scope.pages > 5 ? 5 : $scope.pages;
            $scope.pageList = [];
            $scope.selPage = 1;
            //设置表格数据源(分页)
            $scope.setData = function () {
                $scope.items = $scope.data.slice(($scope.pageSize * ($scope.selPage - 1)), ($scope.selPage * $scope.pageSize));//通过当前页数筛选出表格当前显示数据
            };
            $scope.items = $scope.data.slice(0, $scope.pageSize);
            //分页要repeat的数组
            for (var i = 0; i < $scope.newPages; i++) {
                $scope.pageList.push(i + 1);
            }
            //打印当前选中页索引
            $scope.selectPage = function (page) {
             //不能小于1大于最大
                if (page < 1 || page > $scope.pages) return;
             //最多显示分页数5
                if (page > 2) {
                 //因为只显示5个页数，大于2页开始分页转换
                    var newpageList = [];
                    for (var i = (page - 3); i < ((page + 2) > $scope.pages ? $scope.pages : (page + 2)); i++) {
                        newpageList.push(i + 1);
                 }
                 $scope.pageList = newpageList;
             }
             $scope.selPage = page;
             $scope.setData();
             $scope.isActivePage(page);
             //console.log("选择的页：" + page);
            };
            //设置当前选中页样式
            $scope.isActivePage = function (page) {
                return $scope.selPage == page;
            };
            //上一页
            $scope.Previous = function () {
                $scope.selectPage($scope.selPage - 1);
            };
            //下一页
            $scope.Next = function () {
                $scope.selectPage($scope.selPage + 1);
            };
*/

    }]);