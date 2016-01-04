'use strict';

angular.module('starcraft2', [
        'ui.router',
        'ngMaterial',
        'ngFileUpload'
    ])
    .config(function($stateProvider, $urlRouterProvider, $mdThemingProvider) {

        $stateProvider

            .state('nav', {
                abstract: true,
                templateUrl: '/static/app/components/navigation/navigation.html',
                controller: 'NavigationController as navCtrl'
            })
            .state('nav.matches', {
                url: '/matches',
                templateUrl: '/static/app/components/matches/matches.html',
                controller: 'MatchesController as matchesCtrl',
                title: 'Matches'
            })
            .state('nav.ladder', {
                url: '/ladder',
                templateUrl: '/static/app/components/matches/matches.html',
                controller: 'MatchesController as matchesCtrl',
                title: 'Ladder'
            })
            .state('nav.upload', {
                url: '/upload',
                templateUrl: '/static/app/components/upload/upload.html',
                controller: 'UploadController as uploadCtrl',
                title: 'Upload A Replay'
            });

        $urlRouterProvider.otherwise('/matches');

        $mdThemingProvider.theme('default')
            .primaryPalette('blue')
            .accentPalette('green');

    });
