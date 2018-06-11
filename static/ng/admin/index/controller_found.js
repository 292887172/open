'use strict';

angular.module('Admin.index', ['ngRoute'])

    .config(['$routeProvider', function ($routeProvider) {
        $routeProvider.when('/index', {
            templateUrl: '/static/ng/admin/index/index_nofound.html',
            controller: 'IndexCtrl'
        });
    }])

    .controller('IndexCtrl', ['$scope', "$http", function ($scope, $http) {

    }]);