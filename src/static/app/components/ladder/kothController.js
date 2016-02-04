angular.module('starcraft2')

.controller('KothController', function(KingOfTheHill, PlayerFactory) {
    var self = this;
    self.sergeant = PlayerFactory.get({battleNetName: KingOfTheHill.sergeant});
    self.corporal = PlayerFactory.get({battleNetName: KingOfTheHill.corporal});
    self.recruit = PlayerFactory.get({battleNetName: KingOfTheHill.recruit});
});
