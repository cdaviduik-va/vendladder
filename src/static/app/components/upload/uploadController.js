angular.module('starcraft2')

.controller('UploadController', function($mdToast, $mdDialog, MatchService, Upload) {
    var self = this;
    self.isUploading = false;
    self.selectedMatch = null;
    self.selectedMatches = [];

    self.lookupMatches = function() {
        self.matches = null;
        self.promise = MatchService.lookupOpen().then(function(data) {
            self.matches = data;
        });
    };

    self.onSelect = function(item, key) {
        if (self.selectedMatches.length >= 2) {
            self.selectedMatches.shift();
        }
        self.selectedMatch = self.selectedMatches.length > 0 ? self.selectedMatches[0] : null;
    };

    self.upload = function() {
        self.isUploading = true;
        console.log('submit')
        console.log(self.replay)
        console.log(self.selectedMatch)
        var matchId = undefined;
        if (self.selectedMatch) {
            matchId = self.selectedMatch.match_id
        }
        self.replay.upload = Upload.upload({
            url: '/sc2/api/game/submit/',
            data: {file: self.replay, matchId: matchId},
        });

        self.replay.upload.then(function (response) {
            self.isUploading = false;
            console.log('response')
            console.log(response)
            self.game = JSON.stringify(response.data.game, null, "  ");
            self.winningTeam = response.data.winning_team;
            self.losingTeam = response.data.losing_team;
        }, function (response) {
            self.isUploading = false;
            console.log('error response')
            console.log(response)
            if (response.status > 0) {
                console.log(response.status + ': ' + response.data);
                var message = 'Unable to upload replay. Please try again.';
                if (response.data.message) {
                    message = response.data.message;
                }
                self.showMessage(message, 'Error');
            }
        });
    };

    self.reset = function() {
        self.replay = null;
        self.game = null;
        self.winningTeam = null;
        self.losingTeam = null;
        self.lookupMatches();
    };

    self.close = function(ev, match) {
        match.isClosing = true;
        MatchService.close(match.match_id, ev).then(function() {
            match.isClosing = false;
            match.is_open = false;
        }, function() {
            match.isClosing = false;
        });
    };

    self.showMessage = function(message, title, okText) {
        okText = okText || 'Okay';
        var confirm = $mdDialog.alert()
            .title(title)
            .textContent(message)
            .clickOutsideToClose(true)
            .ok(okText);
        $mdDialog.show(confirm)
    };

    self.lookupMatches();
});
