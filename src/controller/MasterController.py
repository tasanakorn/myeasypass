import os
from google.appengine.ext import webapp
from google.appengine.ext.webapp import template


class MasterController(webapp.RequestHandler):
	def renderTemplate(self, template_name, template_data):
		path = os.path.join(os.path.dirname(__file__),'..','template', template_name)
		self.response.out.write(template.render(path, template_data))