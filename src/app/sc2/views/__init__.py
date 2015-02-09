"""
-
"""

from google.appengine.api import users
from webapp2 import RequestHandler, cached_property
from webapp2_extras import jinja2
from app.sc2.domain.season import lookup_current_season


class UserView(RequestHandler):

    @cached_property
    def jinja2(self):
        return jinja2.get_jinja2(app=self.app)

    def render_response(self, template, **context):
        """
        Pass a template (html) and a dictionary :)
        :param alerts: List of alert type (one of "error", "success", or "info") and corresponding text tuples
        """
        user = users.get_current_user()
        context['user'] = user
        if "logout" not in context.keys() or "login" not in context.keys():
            if user:
                if users.is_current_user_admin():
                    context["is_admin"] = True
                context["logout"] = users.create_logout_url("/")
            else:
                context["login"] = users.create_login_url("/")
        # Seasonal constants
        context['current_season'] = self.current_season
        content = self.jinja2.render_template(template, **context)
        self.response.write(content)

    @cached_property
    def current_season(self):
        return lookup_current_season()
