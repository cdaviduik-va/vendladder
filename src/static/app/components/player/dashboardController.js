angular.module('starcraft2')

.controller('DashboardController', function($stateParams, PlayerFactory) {
    var self = this;
    self.player = null;

    PlayerFactory.getAuthed(function(player) {
        self.player = player;
    });
});
