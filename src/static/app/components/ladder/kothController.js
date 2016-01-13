angular.module('starcraft2')

.controller('KothController', function(PlayerFactory) {
    var self = this;
    self.sergeant = PlayerFactory.get({battleNetName: 'Edindya'});
    self.corporal = PlayerFactory.get({battleNetName: 'FutureNights'});
    self.recruit = PlayerFactory.get({battleNetName: 'Ferrous'});
});
