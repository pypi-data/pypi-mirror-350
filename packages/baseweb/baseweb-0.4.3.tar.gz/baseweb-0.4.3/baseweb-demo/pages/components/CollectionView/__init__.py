import os
from datetime import datetime, timedelta
import random

from flask import request, abort
from flask_restful import Resource

import logging
logger = logging.getLogger(__name__)

from .... import server

def random_date_between(start, end):
  delta = end - start
  int_delta = (delta.days * 24 * 3600) + delta.seconds
  return start + timedelta(seconds=random.randrange(int_delta))

def random_date():
  return random_date_between(datetime.now(), datetime.now()+timedelta(days=1))

server.register_component("CollectionView.js", os.path.dirname(__file__), route="/components/CollectionView")

# set up an in-memory collection of random names and provide a resource to
# access them with query arguments, emulating a MongoDB collection

first_names = [ "John", "Andy", "Joe" ]
last_names  = [ "Johnson", "Smith", "Williams" ]
data = [
  {
    "id"      : index + 1,
    "name"    : random.choice(first_names) + " " + random.choice(last_names),
    "created" : random_date().isoformat(),
    "updated" : random_date().isoformat()
  } for index in range(100)
]

class Collection(Resource):
  @server.authenticated("app.collection.get")
  def get(self):
    start = int(request.args.get("start", 0))
    limit = int(request.args.get("limit", 5))
    sort  = request.args.get("sort", None)
    order = request.args.get("order", "asc")
    name  = request.args.get("name", None)

    selection = data
    if name:
      selection = filter(lambda item: name in item["name"], selection)
    if sort:
      selection = sorted(selection, key=lambda item: item[sort])
    if order == "desc":
      selection.reverse()

    return { 
      "content"       : selection[start:start+limit],
      "totalElements" : len(data)
    }
    
  @server.authenticated("app.collection.post")
  def post(self):
    return "ok"

  @server.authenticated("app.collection.delete")
  def delete(self):
    id = request.args["id"]
    logger.info(id)
    index = next((i for i, item in enumerate(data) if item["id"] == int(id)), None)
    if index:
      del data[index]
      return "ok"
    else:
      abort(404)

server.api.add_resource(Collection, "/api/collection")
