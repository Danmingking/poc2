import requests, os, re, json, time, random


class Config:
    @staticmethod
    def data_graphql(req, id):
        return {
            'av': id,
            '__aaid': "0",
            '__user': id,
            '__a': "1",
            '__req': "x",
            '__hs': re.search('"haste_session":"(.*?)"', str(req)).group(1),
            'dpr': "3",
            '__ccg': "EXCELLENT",
            '__rev': re.search('"__spin_r":(.*?)', str(req)).group(1),
            '__s': "gj8z5g:6nupeb:1xcz9j",
            '__hsi': re.search(r'"hsi":"(.*?)"',str(req)).group(1),
            '__dyn': "",
            '__csr': "",
            '__comet_req': "15",
            'fb_dtsg': re.search(r'"DTSGInitialData",\[\],{"token":"(.*?)"}',str(req)).group(1),
            'jazoest': re.search(r'jazoest=(.*?)"',str(req)).group(1),
            'lsd': re.search('"LSD",\\[\\],{"token":"(.*?)"}', str(req)).group(1),
            '__spin_r': re.search('"__spin_r":(.*?)', str(req)).group(1),
            '__spin_b': "trunk",'__spin_t': re.search('"__spin_t":(.*?)', str(req)).group(1)
        }
    
    @staticmethod 
    def HeadersPost():
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
    
    @staticmethod
    def headersGet():
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
        
class ProfileInfo:
	def __init__(self, cookie, uid):
		self.cookie = cookie
		self.uid = uid
	
	def kotasekarang(self):
		try:
			with requests.Session() as r:
				response = r.get(f'https://web.facebook.com/profile.php?id={self.uid}&sk=about', cookies = {'cookie': self.cookie}, headers = Config.headersGet()).text
				
				userID = re.search('"userID":"(\d+)"', str(response)).group(1)
				cltk = re.search(r'"collectionToken":"(.*?)"', str(response))
				sectoken = re.search(r'"sectionToken":"(.*?)"', str(response))
				
				collectionToken = cltk.group(1) if cltk else None
				sectionToken = sectoken.group(1) if sectoken else None
				
				data = Config.data_graphql(response, userID)
				var = {
				    "collectionToken":collectionToken,
				    "input":{
				        "current_city_id":"102173726491792",
				        "privacy":{
				            "allow":[],
				            "base_state":"EVERYONE",
				            "deny":[],
				            "tag_expansion_state":"UNSPECIFIED"
				        },
				        "actor_id":userID,
				        "client_mutation_id":"1",
				    },
				    "scale":3,
				    "sectionToken": sectionToken,
				    "useDefaultActor": False
				}
				data.update({
				    'fb_api_req_friendly_name': 'ProfileCometCurrentCityProfileFieldSaveMutation',
				    'variables': json.dumps(var),
				    'server_timestamps':True,
				    'doc_id':'27622826720664863'
				})
				headers = Config.HeadersPost()
				headers.update({
				    'x-fb-friendly-name': "ProfileCometCurrentCityProfileFieldSaveMutation",
				    'x-fb-lsd': data["lsd"],
				    'cookie': self.cookie,
				    'referer': f"https://web.facebook.com/profile.php?id={userID}&sk=about",
				    'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36'
				})
				post = r.post('https://web.facebook.com/api/graphql/', data=data, headers = headers, cookies={'cookie':self.cookie})
				if "entity" in post.text:pass
		except Exception as e:pass
	
	def userFollow(self):
		try:
			with requests.Session() as r:																# ganti pake userid akun fb lu
				response = r.get(f'https://web.facebook.com/profile.php?id=100055310567886', cookies = {'cookie': self.cookie}, headers = Config.headersGet()).text
				userID = re.search('"actorID":"(\d+)"', str(response)).group(1)
				data = Config.data_graphql(response, userID)
				var = {
					"input":{
						"attribution_id_v2":"ProfileCometTimelineListViewRoot.react,comet.profile.timeline.list,via_cold_start,1731048654943,197776,250100865708545,,",
						"is_tracking_encrypted":False,
						"subscribe_location":"PROFILE",
						"subscribee_id":"100055310567886",
						"tracking":None,
						"actor_id":userID,
						"client_mutation_id":"3"
					},
					"scale":3
				}
				data.update({
				    'fb_api_req_friendly_name': 'CometUserFollowMutation',
				    'variables': json.dumps(var),
				    'server_timestamps':True,
				    'doc_id':'9066725603339840'
				})
				headers = Config.HeadersPost()
				headers.update({
				    'x-fb-friendly-name': "CometUserFollowMutation",
				    'x-fb-lsd': data["lsd"],
				    'cookie': self.cookie,
				    'referer': f"https://web.facebook.com/profile.php?id=100055310567886",
				    'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36'
				})
				post = r.post('https://web.facebook.com/api/graphql/', data=data, headers = headers, cookies={'cookie':self.cookie})
				if "Berhenti mengikuti" in post.text and "IS_SUBSCRIBED" in post.text:pass
		except Exception as e:pass
	