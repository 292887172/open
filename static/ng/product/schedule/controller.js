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





    }]);
