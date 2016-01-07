angular.module('starcraft2')

.controller('PlayerDetailsController', function($stateParams, PlayerFactory) {
    var self = this;
    self.player = null;

    PlayerFactory.get($stateParams, function(player) {
        self.player = player;
    });
});
