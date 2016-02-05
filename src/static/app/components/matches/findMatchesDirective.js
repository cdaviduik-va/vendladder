angular.module('starcraft2')

.directive('scFindMatches', function() {
    return {
        scope: {
            allowCreateMatch: '=',
            includePlayers: '=',
            excludePlayers: '=',
            ignoreOpen: '='
        },
        templateUrl: '/static/app/components/matches/findMatchesDirective.html',
        restrict: 'E',
        controller: FindMatchesController,
        controllerAs: 'ctrl',
        bindToController: true
    }
});

function FindMatchesController(PlayerFactory, MatchFactory, $mdDialog) {
    var self = this;
    self.players = null;
    self.matches = null;
    self.promise = null;
    self.includePlayers = self.includePlayers || [];
    self.excludePlayers = self.excludePlayers || [];
    self.isCreatingMatch = false;

    self.queryPlayers = queryPlayers;
    self.querySuggestedMatches = querySuggestedMatches;
    self.createMatch = createMatch;

    PlayerFactory.query(function(players) {
        self.players = players;
    });

    function queryPlayers(query) {
        return query ? self.players.filter( createFilterFor(query) ) : self.players;
    }

    function createFilterFor(query) {
        var lowercaseQuery = angular.lowercase(query);
        return function filterFn(player) {
            var isMatch = (angular.lowercase(player.battle_net_name).indexOf(lowercaseQuery) === 0);
            if (!isMatch && player.name) {
                isMatch = (angular.lowercase(player.name).indexOf(lowercaseQuery) === 0);
            }
            return isMatch;
        };
    }

    function querySuggestedMatches() {
        var includePlayerBattleNetNames = self.includePlayers.map(function(player) { return player.battle_net_name; });
        var excludePlayerBattleNetNames = self.excludePlayers.map(function(player) { return player.battle_net_name; });
        self.promise = MatchFactory.querySuggested({
            includePlayers: includePlayerBattleNetNames,
            excludePlayers: excludePlayerBattleNetNames,
            ignoreOpen: self.ignoreOpen
        }, function(data) {
            self.matches = data;
        }).$promise;
    }

    function createMatch(match, ev) {
        self.isCreatingMatch = true;

        var confirmDialog = getConfirmCreateMatchDialog(ev);
        $mdDialog.show(confirmDialog).then(function() {
            MatchFactory.create({match: match}, function() {
                self.isCreatingMatch = false;
                self.matches = null;
                self.querySuggestedMatches();

                var alertDialog = getAlertDialog(ev);
                $mdDialog.show(alertDialog);
            });
        });
    }

    function getConfirmCreateMatchDialog(ev) {
        return $mdDialog.confirm()
            .title('Confirm Create Match')
            .textContent('Would you like to create this match?')
            .clickOutsideToClose(true)
            .targetEvent(ev)
            .ok('Create Match')
            .cancel('Cancel');
    }

    function getAlertDialog(ev) {
        return $mdDialog.alert()
            .title('Success')
            .textContent('The match was created.')
            .clickOutsideToClose(true)
            .targetEvent(ev)
            .ok('Okay');
    }
}
