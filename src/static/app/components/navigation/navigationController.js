angular.module('starcraft2')

.controller('NavigationController', function($window, $state, $rootScope, $mdSidenav, UserService, PlayerFactory) {
    var self = this;
    self.pageTitle = $state.current.title;
    self.user = null;
    self.player = null;
    self.authLinks = null;

    UserService.getAuthLinks().then(function(data) {
        self.authLinks = data;
    });
    UserService.getUser().then(function(data) {
        console.log('user')
        console.log(data)
        self.user = data;
    });

    PlayerFactory.getAuthed(function(player) {
        self.player = player;
    });

    self.navigateTo = function(link) {
        $window.location = link;
    };

    self.toggleMenu = function() {
        $mdSidenav('left').toggle();
    };

    self.goToPlayerDetails = function(player) {
        $state.transitionTo('nav.playerDetails', {battleNetName: player.battle_net_name});
    };

    $rootScope.$on("$stateChangeStart", function(event, toState) {
        self.pageTitle = toState.title;
    });
});
