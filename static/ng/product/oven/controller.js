/**
 * Created by rdy on 17/9/5.
 */
'use strict';

angular.module('Product.oven', ['ngRoute'])
    .config(['$routeProvider', function ($routeProvider) {
        $routeProvider.when('/demo/:type', {
            templateUrl: "/static/ng/product/oven/demo.html",
            controller: "ovenCtrl"


        });
    }])

    .controller('ovenCtrl', ['$scope', "$routeParams", function ($scope, $routeParams) {
        $scope.nav.selected("demoMenu");
        $scope.params=$routeParams;

    }]);