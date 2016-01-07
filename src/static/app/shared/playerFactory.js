angular.module('starcraft2')

.service('PlayerFactory', function($resource) {
    return $resource('/sc2/api/player/:battleNetName');
});
