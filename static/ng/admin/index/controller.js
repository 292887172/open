/**
 * Created by achais on 15/10/15.
 */
'use strict';

angular.module('Admin.index', ['ngRoute'])

    .config(['$routeProvider', function ($routeProvider) {
        $routeProvider.when('/index', {
            templateUrl: '/static/ng/admin/index/index.html',
            controller: 'IndexCtrl'
        });
    }])

    .controller('IndexCtrl', ['$scope', "$http", function ($scope, $http) {

    }]);