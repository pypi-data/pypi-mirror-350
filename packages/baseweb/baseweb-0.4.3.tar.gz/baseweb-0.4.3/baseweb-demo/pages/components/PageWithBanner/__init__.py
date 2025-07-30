import os

from .... import server

# register the Vue component for the UI
server.register_component("PageWithBanner.js", os.path.dirname(__file__), route="/components/PageWitBanner")
