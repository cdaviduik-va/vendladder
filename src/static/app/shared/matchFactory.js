angular.module('starcraft2')

.service('MatchFactory', function($resource) {
    var baseUrl = '/sc2/api/match/';
    return $resource(baseUrl + ':action',
        {matchId: '@match_id'},
        {
            close: {method: 'POST', params:{action: 'close'}},
            create: {method: 'POST', params:{action: 'create'}},
            querySuggested: {url: baseUrl + 'suggested', method: 'GET', isArray: true},
            queryForPlayer: {url: baseUrl + 'forPlayer/:battleNetName', method: 'GET', isArray: true}
        });
});
