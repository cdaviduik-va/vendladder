'use strict';

angular
    .module('starcraft2', [
        'ngResource',
        'ui.router',
        'ngMaterial',
        'ngFileUpload',
        'md.data.table'
    ])
    .constant('KingOfTheHill', {
        captain: null,
        sergeant: 'Edindya',
        corporal: 'FutureNights',
        recruit: 'Ferrous'
    })
    .constant('DefaultPlayerImageUrl', 'https://www.vendasta.com/__v965/static/images/team/user-icon.jpg')
    .config(function($stateProvider, $urlRouterProvider, $mdThemingProvider) {

        $stateProvider

            .state('nav', {
                abstract: true,
                templateUrl: '/static/app/components/navigation/navigation.html',
                controller: 'NavigationController as navCtrl'
            })
            .state('nav.rules', {
                url: '/rules',
                templateUrl: '/static/app/components/general/rules.html',
                controller: 'RulesController as ctrl',
                title: 'Rules & Etiquette'
            })
            .state('nav.resources', {
                url: '/resources',
                templateUrl: '/static/app/components/general/resources.html',
                controller: 'ResourcesController as ctrl',
                title: 'Resources'
            })
            .state('nav.dashboard', {
                url: '/dashboard',
                templateUrl: '/static/app/components/player/dashboard.html',
                controller: 'DashboardController as ctrl',
                title: 'Dashboard'
            })
            .state('nav.koth', {
                url: '/koth',
                templateUrl: '/static/app/components/ladder/koth.html',
                controller: 'KothController as ctrl',
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
                controller: 'PlayerDetailsController as ctrl',
                title: 'Player Details'
            })
            .state('nav.upload', {
                url: '/upload',
                templateUrl: '/static/app/components/upload/upload.html',
                controller: 'UploadController as uploadCtrl',
                title: 'Upload A Replay'
            })
            .state('nav.adminCreateMatch', {
                url: '/admin/createMatch',
                templateUrl: '/static/app/components/admin/createMatch.html',
                controller: 'AdminCreateMatchController as cmCtrl',
                title: 'Create Match'
            });

        $urlRouterProvider.otherwise('/matches');

        $mdThemingProvider.theme('default')
            .primaryPalette('blue')
            .accentPalette('blue-grey');

    });
