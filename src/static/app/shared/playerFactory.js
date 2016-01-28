angular.module('starcraft2')

.service('PlayerFactory', function($resource) {
    var baseUrl = '/sc2/api/player/';

    return $resource(baseUrl + ':battleNetName',
        {battleNetName: '@battle_net_name'},
        {
            getAuthed: {url: baseUrl + 'getAuthed'}
        }
    );
});
