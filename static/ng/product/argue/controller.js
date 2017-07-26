'use strict';

angular.module('Product.argue', ['ngRoute'])

    .config(['$routeProvider', function ($routeProvider) {
        $routeProvider.when('/argue', {
            templateUrl: '/static/ng/product/argue/list.html',
            controller: 'argueCtrl'
        });
    }]);




