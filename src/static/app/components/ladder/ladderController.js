angular.module('starcraft2')

.controller('LadderController', function(PlayerFactory) {
    var self = this;

    self.promise = PlayerFactory.query(function(data) {
        self.players = data;
    }).$promise;
});
