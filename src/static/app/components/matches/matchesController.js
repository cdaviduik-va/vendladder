angular.module('starcraft2')

.controller('MatchesController', function($mdDialog, MatchService) {
    var self = this;
    self.matches = null;

    MatchService.lookup().then(function(data) {
        self.matches = data;
    });

    self.close = function(ev, match) {
        match.isClosing = true;
        MatchService.close(match.match_id, ev).then(function() {
            match.isClosing = false;
            match.is_open = false;

            var confirm = $mdDialog.alert()
                .title('Success')
                .textContent('Match closed. Player scores have been updated.')
                .clickOutsideToClose(true)
                .targetEvent(ev)
                .ok('Okay');
            return $mdDialog.show(confirm);
        }, function() {
            match.isClosing = false;
        });
    };
});
