"""
-
"""
import json
from app.sc2.domain.match import get_suggested_matches, create_match
from app.sc2.domain.player import lookup_players_for_season
from app.sc2.utils import jsonDateTimeHandler
from app.sc2.views import UserView


class MatchCreateView(UserView):
    """
    Allows for the scheduling of matches
    """
    def get(self, **kwargs):
        """
        Handles the display of the match creation form
        """
        exclude_players = self.request.GET.get('exclude_players', '')
        data = {
            'is_debug': self.request.GET.get('is_debug'),
            'exclude_players': exclude_players,
            'suggested_matches_json': json.dumps([match.to_dict() for match in get_suggested_matches(exclude_players=exclude_players.split(' '))[:20]]),
            'players': json.dumps([player.to_dict() for player in lookup_players_for_season()], default=jsonDateTimeHandler)
        }
        if self.request.GET.get('success'):
            data['alerts'] = [('success', 'Match created successfully!')]
        data.update(kwargs)
        self.render_response('/sc2/admin/matches/create.html', **data)

    def post(self):
        team1_player1 = self.request.POST.get('team1player1')
        team1_player2 = self.request.POST.get('team1player2')
        team2_player1 = self.request.POST.get('team2player1')
        team2_player2 = self.request.POST.get('team2player2')

        try:
            create_match([team1_player1, team1_player2], [team2_player1, team2_player2])
        except ValueError as e:
            alerts = [
                ('error', e.message)
            ]
            return self.get(alerts=alerts)

        self.redirect_to('sc2-admin-match-create', success=True)
