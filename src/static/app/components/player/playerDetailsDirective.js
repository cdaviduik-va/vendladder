angular.module('starcraft2')

.directive('scPlayerDetails', function() {
    return {
        scope: {
            player: '='
        },
        templateUrl: '/static/app/components/player/playerDetailsDirective.html',
        restrict: 'E'
    }
});
