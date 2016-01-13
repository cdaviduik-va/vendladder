'use strict';

angular.module('starcraft2', [
        'ngResource',
        'ui.router',
        'ngMaterial',
        'ngFileUpload',
        'md.data.table'
    ])
    .config(function($stateProvider, $urlRouterProvider, $mdThemingProvider) {

        $stateProvider

            .state('nav', {
                abstract: true,
                templateUrl: '/static/app/components/navigation/navigation.html',
                controller: 'NavigationController as navCtrl'
            })
            .state('nav.koth', {
                url: '/koth',
                templateUrl: '/static/app/components/ladder/koth.html',
                controller: 'KothController as kothCtrl',
                title: 'King of the Hill'
            })
            .state('nav.matches', {
                url: '/matches',
                templateUrl: '/static/app/components/matches/matches.html',
                controller: 'MatchesController as matchesCtrl',
                title: 'Matches'
            })
            .state('nav.ladder', {
                url: '/ladder',
                templateUrl: '/static/app/components/ladder/ladder.html',
                controller: 'LadderController as ladderCtrl',
                title: 'Ladder'
            })
            .state('nav.playerDetails', {
                url: '/player/{battleNetName}',
                templateUrl: '/static/app/components/player/playerDetails.html',
                controller: 'PlayerDetailsController as pdCtrl',
                title: 'Player Details'
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
