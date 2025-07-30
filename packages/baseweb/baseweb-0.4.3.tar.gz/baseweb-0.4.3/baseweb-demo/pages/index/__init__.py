import logging

import os

from flask import request

from flask_restful import Resource

from ... import server

logger = logging.getLogger(__name__)

# register the Vue component for the UI
server.register_component("index.js", os.path.dirname(__file__))

# log all messages both to logging infrastructure and connected clients

def log(msg):
  logger.info(msg)
  server.socketio.emit("log", msg)

# set up socketio event handlers to handle events from the UI

@server.socketio.on("hello")
@server.authenticated("app.io.hello")
def on_hello(name):
  log("received hello from {0} ({1}) via socketio".format(name, request.sid))
  return "Hello {0} from socketio!".format(name)

# set up a REST resource to handle requests from the UI

class Hello(Resource):
  @server.authenticated("app.hello.get")
  def get(self):
    name = request.args["name"]
    log("received hello from {0} via rest/get".format(name))
    return "Hello {0} from REST/GET".format(name)
    
  @server.authenticated("app.hello.post")
  def post(self):
    name = request.get_json()["name"]
    log("received hello from {0} via rest/post".format(name))
    return "Hello {0} from REST/POST".format(name)

server.api.add_resource(Hello, "/api/hello")
