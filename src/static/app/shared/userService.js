angular.module('starcraft2')

.service('UserService', function($http) {
    var self = this;
    self.currentUser = null;

    self.getAuthLinks = function() {
        return $http.get('/sc2/api/user/getAuthLinks/').then(function success(response) {
            return response.data;
        });
    };

    self.getUser = function() {
        return $http.get('/sc2/api/user/get/').then(function success(response) {
            return response.data;
        });
    }
});
