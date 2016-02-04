angular.module('starcraft2')

.controller('DashboardController', function($stateParams, KingOfTheHill, PlayerFactory, MatchFactory) {
    var self = this;
    self.player = null;
    self.pMatches = null;
    self.matches = null;

    PlayerFactory.getAuthed(function(player) {
        self.player = player;

        // get suggested 1v1 opponents
        self.opponents = PlayerFactory.queryOpponentsForPlayer({battleNetName: self.player.battle_net_name}, function(data) {
            console.log('opponents')
            console.log(data)
        });

        self.koth = PlayerFactory.get({battleNetName: KingOfTheHill[self.player.league.toLowerCase()]});

        PlayerFactory.get({battleNetName: self.player.battle_net_name}, function(player) {
            self.player = player;

            self.nemesis = PlayerFactory.get({battleNetName: self.player.stats.nemesis.battle_net_name});
        });

        self.pMatches = MatchFactory.queryForPlayer({battleNetName: self.player.battle_net_name}, function(data) {
            self.matches = data;
        }).$promise;
    });
});
