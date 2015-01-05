"""
-
"""
import json
from app.sc2.domain.player import create_player, get_player_details, update_player
from app.sc2.utils import jsonDateTimeHandler
from app.sc2.views import UserView
import constants


class PlayerCreateView(UserView):
    """
    Create a player
    """
    def get(self):
        """
        Handles the display of the match creation form
        """
        data = {
            'playerJson': json.dumps({
                'score': constants.DEFAULT_SCORE
            })
        }
        return self.render_response('/sc2/admin/player/create_or_update.html', **data)

    def post(self):
        """
        Handles creating (or at least passing off to the creating of) users
        """
        battle_net_name = self.request.POST.get("battle_net_name", '').strip()
        if not battle_net_name:
            return self.abort(400, 'Battle.net Username is required.')

        real_name = self.request.POST["real_name"]
        vendasta_email = self.request.POST.get("vendasta_email")
        score = self.request.POST.get("score")

        try:
            create_player(battle_net_name, real_name=real_name, vendasta_email=vendasta_email, score=score)
        except ValueError, e:
            return self.abort(400, e.message)

        return self.redirect_to('sc2-player')


class PlayerEditView(UserView):

    def get(self, battle_net_name):
        player_details = get_player_details(battle_net_name)
        data = {
            'is_update': True,
            'playerJson': json.dumps(player_details, default=jsonDateTimeHandler)
        }
        return self.render_response('/sc2/admin/player/create_or_update.html', **data)

    def post(self, battle_net_name):
        kwargs = {
            'name': self.request.POST["real_name"],
            'vendasta_email': self.request.POST.get("vendasta_email"),
            'image_url': self.request.POST.get("image_url"),
            'score': self.request.POST.get("score"),
            'is_participating': self.request.POST.get("is_participating") == 'on'
        }
        update_player(battle_net_name, **kwargs)

        return self.redirect_to('sc2-player')
