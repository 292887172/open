'use strict';

angular.module('Product.argue', ['ngRoute'])

    .config(['$routeProvider', function ($routeProvider) {
        $routeProvider.when('/argue', {
            templateUrl: "/static/ng/product/argue/list.html",
            controller: "argueCtrl"
        });
    }])
    .controller('argueCtrl', ['$scope', "$http", function ($scope, $http) {
        $scope.dis = true;

        // if(device_type == 20 || device_type == 27 || device_type == 11 ){
        //     title = ['功能序号','功能标识', '长度', '功能名称','参数个数','是否可控', '卡片显示','显示到UI','云菜谱可控','操作'];
        // }
    }])


