angular.module('starcraft2')

.controller('NavigationController', function($window, $state, $rootScope, UserService) {
    var self = this;
    self.pageTitle = $state.current.title;
    self.user = null;
    self.authLinks = null;
    UserService.getAuthLinks().then(function(data) {
        self.authLinks = data;
    });
    UserService.getUser().then(function(data) {
        console.log('user')
        console.log(data)
        self.user = data;
    });

    self.navigateTo = function(link) {
        $window.location = link;
    };

    $rootScope.$on("$stateChangeStart", function(event, toState, toParams, fromState, fromParams){
        self.pageTitle = toState.title;
        //if (toState.authenticate && !AuthService.isAuthenticated()){
        //    // User isn’t authenticated
        //    $state.transitionTo("login");
        //    event.preventDefault();
        //}
    });
});
