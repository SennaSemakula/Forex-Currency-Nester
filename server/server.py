"""This module is responsible for setting up the
   routing for requests to nesting dictionaries"""
import nest
import logging
import tornado
from tornado import ioloop
from tornado.web import RequestHandler, Application
from tornado.httpclient import HTTPClientError
import json

logging.basicConfig(level=logging.INFO)

class BaseHandler(tornado.web.RequestHandler):
    def get_current_user(self):
        return self.get_secure_cookie("user")

class MainHandler(BaseHandler):
    """Class to handle requests to index page"""
    def get(self):
        """Process GET requests index"""
        self.clear_cookie("user")
        if not self.current_user:
            self.redirect("/login")
        else:
            self.write("Welcome to Nesting API ")

class LoginHandler(BaseHandler):
    def get(self):
        self.render("login.html", msg="")

    def post(self):
        username = self.get_argument("username", "")
        password = self.get_argument("password", "")
        if username == "admin" and password == "challenge123":
            self.set_secure_cookie("user", username)
            self.redirect("/")
        else:
            msg = "Invalid login credentials. Please try again"
            self.render("login.html", msg=msg)


class JSONHandler(RequestHandler):
    """Class to handle incoming JSON requests"""
    def get(self):
        """Process GET requests issued to /nest"""
        self.write("Send me some POST requests!")

    def post(self):
        """Process POST requests issued to /nest"""
        try:
            data = json.loads(self.request.body)
        except ValueError:
            raise HTTPClientError(code=400,
                                  message="Request only accepts "
                                  "valid json. Please use JSON as "
                                  "payload data.")

        # retrieve the request parameters
        params = json.dumps({k: self.get_argument(k) for k in self.request.arguments})
        arg_list = [v for v in json.loads(params).values()]
        nest.update_dict(data, arg_list)
        self.redirect("/")


def configure_app():
    """Configure routes with their associated request handlers"""
    routes = [(r"/", MainHandler),
              (r"/login", LoginHandler),
              (r"/nest", JSONHandler),]
    return Application(routes, cookie_secret="0Nvv1W4EWbhNRnWm0LZmnAkhJd4CZde/3vDWw9ndxWE=")


def start(port):
    """Start the server"""
    logging.info("Starting server...")
    app = configure_app()
    try:
        app.listen(port)
    except Exception:
        logging.error("HTTP Server could not be started")
        raise


if __name__ == '__main__':
    start(8080)
    tornado.ioloop.IOLoop.instance().start()

