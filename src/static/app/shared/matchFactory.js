angular.module('starcraft2')

.service('MatchFactory', function($resource) {
    return $resource('/sc2/api/match/:matchId',
        {matchId: '@match_id'},
        {
            close: {method: 'POST', params:{close: true}}
        });
});
