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
    }]);