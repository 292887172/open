'use strict';

// Declare product level module which depends on views, and components
angular.module('Product', [
    "ngRoute",
    "Product.base",
    "Product.main",
    // 产品信息
    "Product.info",
    // 产品服务
    // 生产测试
    // 开发者
    "Product.dev"
])
.config(['$routeProvider', "$interpolateProvider", function ($routeProvider, $interpolateProvider) {
    $interpolateProvider.startSymbol('{[{');
    $interpolateProvider.endSymbol('}]}');
    $routeProvider.otherwise({redirectTo: '/info'});
}])
.filter('trustHtml', function ($sce) {
    return function (input) {
        return $sce.trustAsHtml(input);
    }
});