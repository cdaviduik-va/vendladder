"""
-
"""
import json
from google.appengine.ext import ndb
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
            player = ndb.Key(PlayerModel._get_kind(), int(id)).get()
            data['playerJson'] = json.dumps(player, default=jsonDateTimeHandler)
            data['isUpdate'] = True
        else:
            data['playerJson'] = json.dumps({'season':'Winter 1'})
            data['isUpdate'] = False


        self.render_response('/sc2/admin/player/create.html', **data)

    def post(self):
        """
        Handles creating (or at least passing off to the creating of) users
        """
        player_id = self.request.POST['player_id']
        realname = self.request.POST["realname"]
        vendemail = self.request.POST.get("vendemail")
        bnetname = self.request.POST.get("bnetname")
        skill = self.request.POST.get("skill")
        season = self.request.POST.get("season")
        player_key = create_player(realname, vendemail, bnetname, skill, season, player_id)

        data = {}
        player = player_key.get()
        data['playerJson'] = json.dumps(player, default=jsonDateTimeHandler)
        data['isUpdate'] = True

        self.render_response('/sc2/admin/player/create.html', **data)

