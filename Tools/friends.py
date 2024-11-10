import requests, json, os, re

class Assets:
	def __init__(self):
		pass

	def get_data(self, req):
		return {
			"av": re.search(r'"USER_ID":"(\d+)"', str(req)).group(1),
			"__aaid": "0",
			"__user": re.search(r'"USER_ID":"(\d+)"', str(req)).group(1),
			"__a": "1",
			"__req": "v",
			"__hs": re.search('"haste_session":"(.*?)"', str(req)).group(1),
			"dpr": "3",
			"__ccg": re.search('"connectionClass":"(.*?)"', str(req)).group(1),
			"__rev": re.search('"rev":(\d+)', str(req)).group(1),
			"__s": "lw7s33:uqlsku:83ks21",
			"__hsi": re.search('"hsi":"(\d+)"', str(req)).group(1),
			"__dyn": "",
			"__csr": "",
			"__comet_req": re.search('&__comet_req=(.*?)', str(req)).group(1),
			"fb_dtsg": re.search('"DTSGInitialData",\[\],{"token":"(.*?)"}', str(req)).group(1),
			"jazoest": re.search('&jazoest=(\d+)', str(req)).group(1),
			"lsd": re.search('"LSD",\[\],{"token":"(.*?)"', str(req)).group(1),
			"__spin_r": re.search('"__spin_r":(\d+),', str(req)).group(1),
			"__spin_b": "trunk",
			"__spin_t": re.search('"__spin_t":(\d+),', str(req)).group(1),
			'fb_api_caller_class': 'RelayModern'
		}
		
	def HeadersGet(self):
		return {
            'User-Agent': "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
            'Accept': "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
            'cache-control': "max-age=0",
            'dpr': "2.75",
            'viewport-width': "980",
            'sec-ch-ua': "\"Not-A.Brand\";v=\"99\", \"Chromium\";v=\"124\"",
            'sec-ch-ua-mobile': "?0",
            'sec-ch-ua-platform': "\"Linux\"",
            'sec-ch-ua-platform-version': "\"\"",
            'sec-ch-ua-model': "\"\"",
            'sec-ch-ua-full-version-list': "\"Not-A.Brand\";v=\"99.0.0.0\", \"Chromium\";v=\"124.0.6327.4\"",
            'sec-ch-prefers-color-scheme': "light",
            'upgrade-insecure-requests': "1",
            'sec-fetch-site': "same-origin",
            'sec-fetch-mode': "navigate",
            'sec-fetch-user': "?1",
            'sec-fetch-dest': "document",
            'accept-language': "id-ID,id;q=0.9,en-US;q=0.8,en;q=0.7"
		}
	
	def HeadersPost(self):
		return {
			'host': 'web.facebook.com',
			'sec-ch-ua': '"Not-A.Brand";v="99", "Chromium";v="124"',
			'sec-ch-ua-mobile': '?0',
			'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36',
			'sec-ch-ua-platform-version': '""',
			'content-type': 'application/x-www-form-urlencoded',
			'x-asbd-id': '129477',
			'sec-ch-ua-full-version-list': '"Not-A.Brand";v="99.0.0.0", "Chromium";v="124.0.6327.4"',
			'sec-ch-ua-model': '""',
			'sec-ch-prefers-color-scheme': 'light',
			'sec-ch-ua-platform': '"Linux"',
			'accept': '*/*',
			'origin': 'https://web.facebook.com',
			'sec-fetch-site': 'same-origin',
			'sec-fetch-mode': 'cors',
			'sec-fetch-dest': 'empty',
			'accept-language': 'id-ID,id;q=0.9,en-US;q=0.8,en;q=0.7'
		}
		
class AddFriend:
	def __init__(self) -> None:
		pass
		
	def run(self, cookie, uid):
		self.cookies = cookie
		self.userid = uid
		try:
			res = {'status': 'gagal', 'userID': None, 'message': 'Terjadi kesalahan'}
			with requests.Session() as r:
				q = Assets()
				req = r.get(f'https://web.facebook.com/profile.php?id={self.userid}', headers=q.HeadersGet(), cookies = {'cookie': self.cookies}).text
				userID = re.search('"userID":"(\d+)"', str(req)).group(1)
				data = q.get_data(req)
				var = {"input":{"attribution_id_v2":"ProfileCometTimelineListViewRoot.react,comet.profile.timeline.list,via_cold_start,1730479732860,423160,190055527696468,,","friend_requestee_ids":[userID],"friending_channel":"PROFILE_BUTTON","warn_ack_for_ids":[],"actor_id":data["__user"],"client_mutation_id":"1"},"scale":3}
				data.update({'fb_api_req_friendly_name': 'FriendingCometFriendRequestSendMutation', 'variables': json.dumps(var),'server_timestamps':True,'doc_id':'9088602351172612'})
				headers = q.HeadersPost()
				headers.update({'x-fb-friendly-name': "FriendingCometFriendRequestSendMutation",'x-fb-lsd': data["lsd"], 'cookie': self.cookies, 'referer': f"https://web.facebook.com/profile.php?id={userID}", 'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36'})
				post = r.post('https://web.facebook.com/api/graphql/', data=data, headers = headers, cookies={'cookie':self.cookies}).text
				if 'friendship_status' in post and 'OUTGOING_REQUEST' in post:
					res = {'status': 'berhasil add', 'userID': userID, 'message': None}
				elif 'ARE_FRIENDS' in post:
					res = {'status': 'gagal add', 'userID': userID, 'message': 'Akun Sudah Berteman'}
				elif 'Apa orang ini mengenal Anda?' in post and '"path":["friend_request_send"]' in post:
					vari = {"input":{"attribution_id_v2":"ProfileCometTimelineListViewRoot.react,comet.profile.timeline.list,via_cold_start,1730447894107,790673,190055527696468,,","friend_requestee_ids":[userID],"friending_channel":"PROFILE_BUTTON","warn_ack_for_ids":[userID],"actor_id":data["__user"],"client_mutation_id":"2"},"scale":3}
					data.update({"__req": "m",'fb_api_req_friendly_name': 'FriendingCometFriendRequestSendMutation', 'variables': json.dumps(vari),'server_timestamps':True,'doc_id':'9088602351172612'})
					headers.update({'x-fb-friendly-name': "FriendingCometFriendRequestSendMutation",'x-fb-lsd': data["lsd"], 'cookie': self.cookies, 'referer': f"https://web.facebook.com/profile.php?id={userID}", 'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36'})
					post2 = r.post('https://web.facebook.com/api/graphql/', data=data, headers = headers, cookies={'cookie':self.cookies}).text
					if 'friendship_status' in post2 or 'Sorry, something went wrong.' in post2:
						res = {'status': 'berhasil add', 'userID': userID, 'message': None}
					elif 'ARE_FRIENDS' in post2:
						res = {'status': 'gagal add', 'userID': userID, 'message': 'Akun Sudah Berteman'}
					else:
						res = {'status': 'gagal add', 'userID': userID, 'message': 'Akun Spam atau Cookie Tidak Valid'}
				elif 'Sorry, something went wrong.' in post:
					res = {'status': 'berhasil add', 'userID': userID, 'message': None}
				else:
					res = {'status': 'gagal add', 'userID': userID, 'message': 'Akun Spam atau Cookie Tidak Valid'}
		except Exception as e:
			res = {'status': 'gagal', 'userID': None, 'message': f'Error: {str(e)}'}
		return res

# belum jadi
class ConfirmFriend:
	def __init__(self) -> None:
		pass
		
	def confirmFriend(self, cookie):
		self.cookies = cookie
		try:
			with requests.Session() as r:
				req = r.get('https://web.facebook.com/friends/requests', headers=headers_get, cookies = {'cookie': self.cookies}).text
				data = Assets().get_data(req)
				cursor = re.search(r'"cursor":"(\d+)"', str(req)).group(1)
				print(cursor)
				self.kumpulkan_id(r, data, self.cookies, cursor)
		except Exception as e:
			raise e
	
	def kumpulkan_id(self, r, data, cookie, next):
		pass