'use strict';

// Declare product level module which depends on views, and components
angular.module('Admin', [
    "ngRoute",
    "ngDialog",
    "ui.tree",
    "Admin.base",
    "Admin.main",
    "Admin.index",
    "Admin.user",
    "Admin.application",
    "Admin.api",
    "Admin.doc"
])
    .config(['$routeProvider', "$interpolateProvider", function ($routeProvider, $interpolateProvider) {
        $interpolateProvider.startSymbol('{[{');
        $interpolateProvider.endSymbol('}]}');
        $routeProvider.otherwise({redirectTo: '/index'});
    }])
    .filter('trustHtml', function ($sce) {
        return function (input) {
            return $sce.trustAsHtml(input);
        }
    });