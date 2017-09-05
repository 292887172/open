/**
 * Created by rdy on 17/9/5.
 */
'use strict';

angular.module('Product.oven', ['ngRoute'])
    .config(['$routeProvider', function ($routeProvider) {
        $routeProvider.when('/智能烤箱', {
            templateUrl: "/static/ng/product/oven/demo.html",
            controller: "deviceCtrl"


        });
    }])

    .controller('deviceCtrl', ['$scope', "$http", function ($scope, $http) {
        $scope.nav.selected("demoMenu");

    }]);