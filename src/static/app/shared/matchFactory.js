angular.module('starcraft2')

.service('MatchFactory', function($resource) {
    return $resource('/sc2/api/match/:action',
        {matchId: '@match_id'},
        {
            close: {method: 'POST', params:{action: 'close'}},
            create: {method: 'POST', params:{action: 'create'}},
            querySuggested: {method: 'GET', isArray: true, params:{action: 'suggested'}}
        });
});
