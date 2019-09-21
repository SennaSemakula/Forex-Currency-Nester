"""This module is responsible for setting up the
   routing for requests to nesting dictionaries"""
import logging
import tornado
from tornado import ioloop
from tornado.web import RequestHandler, Application
from tornado.httpclient import HTTPClientError
import json
from nest import update_dict

logger = logging.getLogger(__name__)

class MainHandler(RequestHandler):
    """Class to handle requests to index page"""
    def initialize(self, input_json):
        """Set up variables"""
        self.input_json = input_json

    def get(self):
        """Process GET requests index"""
        self.write("test")
        #return self.render("admin.html", status=status, repo_list=self.repo_list,
                           #frozen_state=FrozenState)

class JSONHandler(RequestHandler):
    """Class to handle incoming JSON requests"""
    async def get(self):
        """Process GET requests issued to /nest"""
        self.write({"state": "json state"})

    async def post(self):
        """Process POST requests issued to /nest"""
        try:
            data = json.loads(self.request.body)
        except ValueError:
            raise HTTPClientError(code=400,
                                  message="Request only accepts "
                                           "valid json. Please use JSON as payload data.")

        # Get the request parameters
        params = json.dumps({ k: self.get_argument(k) for k in self.request.arguments })
        arg_list = [ v for v in json.loads(params).values() ]
        print(data)
        nested_dict = update_dict(data, arg_list)
        self.redirect("/")

def configure_app():
    """Configure routes with their associated request handlers"""
    routes = [(r"/", MainHandler, dict(input_json=[])),
              (r"/nest", JSONHandler),]
    return Application(routes)


def start(port):
    """Start the server"""
    logger.info("Starting server...")
    app = configure_app()
    try:
        app.listen(port)
    except Exception:
        logger.error("HTTP Server could not be started")
        raise

if __name__ == '__main__':
    start(8080)
    ioloop.IOLoop.current().start()