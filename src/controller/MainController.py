from MasterController import MasterController
from model import user_prefs
from service import easypass

class MainController(MasterController):
	def get(self):
		template_data = {}
		up = user_prefs.getUserPrefs()
		if not up:
			print "NO User"
			return
		
		if not (up.easypass_username  or up.easypass_password):
			#self.renderTemplate('setting.html', template_data)
			self.redirect('/setting')
			return
		
		template_data['balance'] = easypass.getBalance(up.easypass_username, up.easypass_password)
		self.renderTemplate('index.html', template_data)