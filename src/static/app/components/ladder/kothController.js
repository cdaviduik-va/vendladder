angular.module('starcraft2')

.controller('KothController', function(DefaultPlayerImageUrl, KingOfTheHill, PlayerFactory) {
    var self = this;
    self.defaultPlayerImageUrl = DefaultPlayerImageUrl;
    self.captain = null;
    if (KingOfTheHill.captain) {
        self.captain = PlayerFactory.get({battleNetName: KingOfTheHill.captain})
    }
    self.sergeant = PlayerFactory.get({battleNetName: KingOfTheHill.sergeant});
    self.corporal = PlayerFactory.get({battleNetName: KingOfTheHill.corporal});
    self.recruit = PlayerFactory.get({battleNetName: KingOfTheHill.recruit});
});
