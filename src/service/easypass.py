# coding=utf-8
import urllib
import re
from google.appengine.api import memcache
import logging
from WebClient import WebClient


from html_entity_decode import html_entity_decode

def getBalance(easypass_username, easypass_password):
	wc = WebClient()
	balance = memcache.get(easypass_username, namespace='easypass_balance')
	if balance:
		logging.info("getBalance cache hit")		
		return balance
	
	balance = 0
	state = 0
	view_state = ''
	easypass_account_no = ''
	
	while state >= 0:
		if state == 0:
			data = wc.request('http://thaieasypass.com/EPCustInfo/Login.aspx')
			m = re.search('id="__VIEWSTATE" value="(.*)"', data)
			if m :
				view_state = html_entity_decode(m.group(1))
				state += 1
			else :
				state = -2
		elif state == 1:
			p = urllib.urlencode( { 'txtUser': easypass_username, 'txtPWD' : easypass_password, '__VIEWSTATE' : view_state} )
			data = wc.request('http://thaieasypass.com/EPCustInfo/Login.aspx', p, isPost = True)
			if re.search('CustInfoView.aspx', data) :
				state += 1
			else :
				state = -2
		elif state == 2:
			data = wc.request('http://thaieasypass.com/EPCustInfo/CustInfoView.aspx')
			m = re.search('id="__VIEWSTATE" value="(.*)"', data)
			if m :
				view_state = html_entity_decode(m.group(1))
				state += 1
			else :
				state = -2			
		elif state == 3:
			state += 1
			data = wc.request('http://thaieasypass.com/EPCustInfo/Default.aspx')
			m = re.search('id="__VIEWSTATE" value="(.*)"', data)
			if m :
				view_state = html_entity_decode(m.group(1))
				m = re.search('id="__EVENTVALIDATION" value="(.*)"', data)
				if m : 
					event_validation = html_entity_decode(m.group(1))
				else:
					logging.error('__EVENTVALIDATION not found')
					state = -2

				m = re.search('"AccountList"\s*>\s*<option value="([0-9a-zA-Z]*)">', data)
				if m:
					easypass_account_no = m.group(1)
				else:
					state = -2
			else :
				logging.error('__VIEWSTATE not found')
				state = -2		
		elif state == 4:
			req_data = { '__VIEWSTATE' : view_state,
									'__EVENTVALIDATION' : event_validation,
									'AccountList' : easypass_account_no,
									'selMonth' : '07',
									'selYear' : '2011',
									'Button1' : u'ดูรายงาน'.encode('utf-8')
								}
			p = urllib.urlencode(req_data)												
			
			try:
				data = wc.request('http://thaieasypass.com/EPCustInfo/Default.aspx', p, isPost = True)
				m = re.search('<iframe src="(.*)" frameborder', data)
				if m:
					iframe_src = m.group(1)
					m2 = re.search(';ReportUrl=(.*)', iframe_src)
					if m2:
						report_url = urllib.unquote_plus(m2.group(1))
					else:
						state = -5
				else:
					state = -5
			except Exception, e:
				print e
				state = -5
			state += 1
		elif state == 5:
			data = wc.request('http://thaieasypass.com' + report_url)
			m = re.search('<DIV class="[a-zA-Z0-9]+">เงินคงเหลือ<\/DIV><\/TD><TD COLSPAN="3" class="[a-zA-Z0-9]+"><DIV class="[a-zA-Z0-9]+">([,.0-9]+)<\/DIV>', data)
			if m:
				balance = m.group(1)
			state += 1
		elif state == 6:
			state += 1
		else:
			state = -3
	memcache.set(easypass_username, balance, 300, namespace="easypass_balance")
	logging.info("getBalance online")
	return balance