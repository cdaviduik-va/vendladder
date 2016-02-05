angular.module('starcraft2')

.directive('scPlayer', function($state) {
    return {
        scope: {
            players: '=',
            disabled: '=',
            showScore: '=',
            diffWithScore: '='
        },
        templateUrl: '/static/app/components/player/playerDirective.html',
        restrict: 'E',
        link: function($scope) {
            $scope.playerList = $scope.players;
            if (!angular.isArray($scope.players)) {
                $scope.playerList = [$scope.players];
            }
            $scope.goToDetails = function(player) {
                $state.transitionTo('nav.playerDetails', {battleNetName: player.battle_net_name});
            }
            $scope.scoreDiff = function(player) {
                return player.score - $scope.diffWithScore;
            }
        }
    }
});
