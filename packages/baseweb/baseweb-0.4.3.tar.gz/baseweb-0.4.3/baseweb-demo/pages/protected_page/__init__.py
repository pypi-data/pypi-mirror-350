import os

from flask import Response
from flask_restful import Resource

import oatk.js
from oatk import OAuthToolkit

from ... import server

# register the Vue component for the UI
server.register_component("protected_page.js", os.path.dirname(__file__), route="/protected_page")

# expose discovery url and client_id settings loaded from from env
server.settings["oauth"] = {
  "provider" : os.environ.get("OAUTH_PROVIDER"),
  "client_id": os.environ.get("OAUTH_CLIENT_ID")
}

# route for oatk.js from the oatk package
@server.route("/oatk.js")
def oatk_script():
  return Response(oatk.js.as_src(), mimetype="application/javascript")

# and have it included in the HTML
server.register_external_script("/oatk.js")

# create an oauth protected API endpoint
oauth = OAuthToolkit()
oauth.using_provider(os.environ["OAUTH_PROVIDER"])
oauth.with_client_id(os.environ["OAUTH_CLIENT_ID"])

class HelloWorld(Resource):
  @oauth.authenticated
  def get(self):
    return {
      "message": "hello protected world"
    }

server.api.add_resource(HelloWorld, "/api/protected/hello")
