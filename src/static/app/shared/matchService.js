angular.module('starcraft2')

.service('MatchService', function($http, $mdDialog) {
    var self = this;

    self.lookup = function(limit) {
        return $http.get('/sc2/api/match/lookup/', {
            params: {limit: limit}
        }).then(function success(response) {
            return response.data;
        })
    };

    self.lookupOpen = function() {
        return $http.get('/sc2/api/match/lookupOpen/')
            .then(function success(response) {
                return response.data;
            })
    };

    //self.close = function(matchId) {
    //    return $http.post('/sc2/api/match/close/', {
    //        matchId: matchId
    //    });
    //};

    self.close = function(matchId, ev) {
        var confirm = $mdDialog.confirm()
            .title('Would you like to close this match?')
            .textContent('Player scores will be updated and replays can no longer be uploaded.')
            .clickOutsideToClose(true)
            .targetEvent(ev)
            .ok('Close Match')
            .cancel('Cancel');
        return $mdDialog.show(confirm).then(function() {
            return $http.post('/sc2/api/match/close/', {
                matchId: matchId
            });
        });
    };
});
