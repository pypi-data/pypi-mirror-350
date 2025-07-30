import os

from .... import server

# register the Vue component for the UI
server.register_component("ProcessDiagramDemoBody.js", os.path.dirname(__file__))
server.register_component("ProcessDiagram.js", os.path.dirname(__file__), route="/components/ProcessDiagram")
