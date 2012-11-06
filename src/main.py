#!/usr/bin/env python

from google.appengine.ext import webapp
from google.appengine.ext.webapp import util

from controller.MainController import MainController
from controller.SettingController import SettingController

def main():
	application = webapp.WSGIApplication(
											[
												('/', MainController), 
												('/setting', SettingController)
											],
										 debug=False)
	util.run_wsgi_app(application)


if __name__ == '__main__':
	main()
