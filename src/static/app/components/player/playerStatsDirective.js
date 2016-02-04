angular.module('starcraft2')

    .directive('scPlayerStats', function() {
        return {
            scope: {
                player: '='
            },
            templateUrl: '/static/app/components/player/playerStatsDirective.html',
            restrict: 'E'
        }
    });
