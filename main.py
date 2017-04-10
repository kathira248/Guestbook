#!/usr/bin/env python
import os
import jinja2
import webapp2
from models import Message
from google.appengine.ext import ndb

template_dir = os.path.join(os.path.dirname(__file__), "templates")
jinja_env = jinja2.Environment(loader=jinja2.FileSystemLoader(template_dir), autoescape=False)


class BaseHandler(webapp2.RequestHandler):

    def write(self, *a, **kw):
        return self.response.out.write(*a, **kw)

    def render_str(self, template, **params):
        t = jinja_env.get_template(template)
        return t.render(params)

    def render(self, template, **kw):
        return self.write(self.render_str(template, **kw))

    def render_template(self, view_filename, params=None):
        if not params:
            params = {}
        template = jinja_env.get_template(view_filename)
        return self.response.out.write(template.render(params))


class MainHandler(BaseHandler):
    def get(self):
        return self.render_template("home.html")

class AboutHandler(BaseHandler):
    def get(self):
        return self.render_template("about.html")


class GuestBookHandler (BaseHandler):

    def get(self):
        messages = Message.query().fetch()
        params = {"messages": messages}

        return self.render_template("guestbook.html", params=params)

    def post(self):
        author = self.request.get("name")
        email = self.request.get("email")
        message = self.request.get("message")

        if not author:
            author = "Anonymous"

        if "<script>" in message:
            return self.write("You no hack me")

        msg_object = Message(author_name=author, email=email, message_text=message.replace("<script>", ""))
        msg_object.put()  # save message into database

        return self.redirect_to("guestbook-site")

class BookingHandler (BaseHandler):
    def get(self):
        return self.render_template("booking.html")

class ContactHandler(BaseHandler):
    def get(self):
        return self.render_template("contact.html")


app = webapp2.WSGIApplication([
    webapp2.Route('/', MainHandler),
    webapp2.Route('/about', AboutHandler),
    webapp2.Route('/guestbook', GuestBookHandler, name="guestbook-site"),
    webapp2.Route('/booking', BookingHandler),
    webapp2.Route('/contact', ContactHandler),

], debug=True)
