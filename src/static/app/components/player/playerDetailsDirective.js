angular.module('starcraft2')

.directive('scPlayerDetails', function($state) {
    return {
        scope: {
            player: '='
        },
        templateUrl: '/static/app/components/player/playerDetailsDirective.html',
        restrict: 'E',
        link: function($scope) {
            $scope.goToDetails = function(player) {
                $state.transitionTo('nav.playerDetails', {battleNetName: player.battle_net_name});
            }
        }
    }
});
