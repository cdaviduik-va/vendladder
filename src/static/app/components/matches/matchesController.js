angular.module('starcraft2')

.controller('MatchesController', function($mdDialog, MatchFactory) {
    var self = this;
    self.matches = null;
    self.closedMatches = null;

    // open matches
    self.pMatches = MatchFactory.query({isOpen: true}, function(data) {
        self.matches = data;
    }).$promise;

    // historic matches
    self.pClosedMatches = MatchFactory.query({isOpen: false}, function(data) {
        self.closedMatches = data;
    }).$promise;
});
