"""
-
"""
import json
from app.sc2.models.player import PlayerModel
from app.sc2.utils import jsonDateTimeHandler
from app.sc2.views import UserView
from ...domain.player import create_player, player_info

class PlayerAdminView(UserView):
    """
    Allows for the scheduling of matches
    """
    def get(self):
        """
        Handles the display of the match creation form
        """
        data = {}

        #Handle edits
        id = self.request.GET.get('id')
        if id:
            player = PlayerModel.get_by_id(id)
            data['playerJson'] = json.dumps('player', default=jsonDateTimeHandler)
            data['isUpdate'] = True
        else:
            data['isUpdate'] = False

        self.render_response('/sc2/admin/player/create.html', **data)

    def post(self):
        """
        Handles creating (or at least passing off to the creating of) users
        """
        realname = self.request.POST["realname"]
        vendemail = self.request.POST.get("vendemail")
        bnetname = self.request.POST.get("bnetname")
        skill = self.request.POST.get("skill")
        season = self.request.POST.get("season")
        player_key = create_player(realname, vendemail, bnetname, skill, season)

        data = {
            "player_created": True if player_key else False,
            "name": realname
        }

        self.render_response('/sc2/admin/player/create.html', **data)

