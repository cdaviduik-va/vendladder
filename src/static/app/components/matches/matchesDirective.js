angular.module('starcraft2')

.directive('scMatches', function($mdDialog, MatchFactory) {
    return {
        scope: {
            promise: '=',
            matches: '='
        },
        templateUrl: '/static/app/components/matches/matchesDirective.html',
        restrict: 'E',
        link: function($scope) {
            $scope.close = function(ev, match) {
                match.is_closing = true;
                var confirmDialog = getConfirmCloseDialog(ev);
                $mdDialog.show(confirmDialog).then(function() {
                    match.$close(function() {
                        match.is_closing = false;
                        match.is_open = false;
                        // remove match from list
                        $scope.matches.splice($scope.matches.indexOf(match), 1);

                        var alertDialog = getAlertDialog(ev);
                        return $mdDialog.show(alertDialog);
                    }, function() {
                        match.is_closing = false;
                    });
                });
            };

            var getConfirmCloseDialog = function(ev) {
                return $mdDialog.confirm()
                    .title('Would you like to close this match?')
                    .textContent('Player scores will be updated and replays can no longer be uploaded.')
                    .clickOutsideToClose(true)
                    .targetEvent(ev)
                    .ok('Close Match')
                    .cancel('Cancel');
            }

            var getAlertDialog = function(ev) {
                return $mdDialog.alert()
                    .title('Success')
                    .textContent('Match closed. Player scores have been updated.')
                    .clickOutsideToClose(true)
                    .targetEvent(ev)
                    .ok('Okay');
            }
        }
    }
});
