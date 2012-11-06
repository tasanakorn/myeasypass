from MasterController import MasterController

from model import user_prefs
from Crypto.Cipher import ARC4


class SettingController(MasterController):
	def get(self):	
		up = user_prefs.getUserPrefs()
		template_data = {'action':'setting', 'user_prefs': up}
		self.renderTemplate('setting.html', template_data)
	def post(self):
		up = user_prefs.getUserPrefs()
		cmd = self.request.get("cmd")
		if cmd == 'update':
			up.easypass_username = self.request.get("easypass_username")
			if self.request.get("easypass_password") != '':
				up.easypass_password = self.request.get("easypass_password")
			up.put()
			self.redirect('/')