'use strict';

angular.module('Product.portal', ['ngRoute'])

    .config(['$routeProvider', function ($routeProvider) {
        $routeProvider.when('/portal', {
            templateUrl: '/static/ng/product/portal/main.html',
            controller: 'PortalCtrl'
        });
    }])

    .controller('PortalCtrl', ['$scope', "$http", function ($scope, $http) {
        $scope.nav.selected("portalMenu");
        $scope.productImgSrc = "";





    }]);
