angular.module('starcraft2')

.controller('AdminCreateMatchController', function($mdDialog, MatchFactory, PlayerFactory) {
    var self = this;
    self.players = null;
    self.matches = null;
    self.closedMatches = null;
    self.includePlayers = [];
    self.excludePlayers = [];
    self.isCreatingMatch = false;
    self.ignoreOpen = false;

    PlayerFactory.query(function(players) {
        self.players = players
    });

    self.querySuggestedMatches = function() {
        var includePlayerBattleNetNames = self.includePlayers.map(function(player) { return player.battle_net_name; });
        var excludePlayerBattleNetNames = self.excludePlayers.map(function(player) { return player.battle_net_name; });
        self.promise = MatchFactory.querySuggested({
            includePlayers: includePlayerBattleNetNames,
            excludePlayers: excludePlayerBattleNetNames,
            ignoreOpen: self.ignoreOpen
        }, function(data) {
            self.matches = data;
        }).$promise;
    };

    self.queryPlayers = function(query) {
        return query ? self.players.filter( createFilterFor(query) ) : self.players;
    };

    self.createMatch = function(match) {
        self.isCreatingMatch = true;
        MatchFactory.create({match: match}, function() {
            self.isCreatingMatch = false;
            self.querySuggestedMatches();
        });
    };

    function createFilterFor(query) {
        var lowercaseQuery = angular.lowercase(query);
        return function filterFn(player) {
            var isMatch = (angular.lowercase(player.battle_net_name).indexOf(lowercaseQuery) === 0);
            if (!isMatch && player.name) {
                isMatch = (angular.lowercase(player.name).indexOf(lowercaseQuery) === 0);
            }
            return isMatch;
        };
    };
});
