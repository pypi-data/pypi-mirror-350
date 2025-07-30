import os

from ... import server

# register the Vue component for the UI
server.register_component("page3.js", os.path.dirname(__file__), route="/page3")

# add some additional settings
server.settings["baseweb-demo"] = {
  "a few" : "app specific",
  "configuration" : "settings"
}
