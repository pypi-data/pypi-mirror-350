import os

from ... import server

# register the Vue component for the UI
server.register_component("page6.js", os.path.dirname(__file__), route="/page6")
server.register_stylesheet("calendar.css", os.path.dirname(__file__))
