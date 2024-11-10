import re, requests, random
from time import time

def cookiesvalidasi(cokie):
	try:
		with requests.Session() as r:
			req = r.get('https://www.facebook.com/profile.php', cookies={'cookie': cokie})
			userID_match = re.search('"actorID":"(\d+)"', req.text)
			username_match = re.search('"NAME":"(.*?)"', req.text)
			if userID_match and username_match:
				return userID_match.group(1), username_match.group(1), cokie
			else:
				return None, None
	except Exception as e:
		return None, None 
            
def Login(userid, password):
	try:
		with requests.Session() as r:
			enpas = '#PWD_BROWSER:0:{}:{}'.format(int(time()), password)
			headersGET = {'host': 'm.facebook.com','cache-control': 'max-age=0','dpr': '2.75','viewport-width': '980','sec-ch-ua': '"Not-A.Brand";v="99", "Chromium";v="124"','sec-ch-ua-mobile': '?1','sec-ch-ua-platform': '"Android"','sec-ch-ua-platform-version': '"9.0.0"','sec-ch-ua-model': '"Redmi Note 8"','sec-ch-ua-full-version-list': '"Not-A.Brand";v="99.0.0.0", "Chromium";v="124.0.6327.4"','sec-ch-prefers-color-scheme': 'light','upgrade-insecure-requests': '1','user-agent': 'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Mobile Safari/537.36','accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7','sec-fetch-site': 'same-origin','sec-fetch-mode': 'navigate','sec-fetch-user': '?1','sec-fetch-dest': 'document','referer': 'https://m.facebook.com/bookmarks/','accept-language': 'id-ID,id;q=0.9,en-US;q=0.8,en;q=0.7'}
			response = r.get('https://m.facebook.com/login/', headers = headersGET).text
			userData = {"__aaid": "0","__user": "0","__a": "1","__req": "1j","__hs": re.search(r'"haste_session":"(.*?)"', str(response)).group(1),"dpr": "1","__ccg": "GOOD","__rev": re.search(r'"__spin_r":(\d+)', str(response)).group(1),"__s": ":vsy60g:p01voh","__hsi": re.search(r'"hsi":"(\d+)"', str(response)).group(1),"__dyn": "","__csr": "","fb_dtsg": re.search(r'"dtsg":{"token":"(.*?)"', str(response)).group(1),"jazoest": re.search(r'"jazoest", "(\d+)"', str(response)).group(1),"lsd": re.search(r'"lsd":"(.*?)"', str(response)).group(1),"params": "{\"params\":\"{\\\"server_params\\\":{\\\"credential_type\\\":\\\"password\\\",\\\"username_text_input_id\\\":\\\"s0853g:70\\\",\\\"password_text_input_id\\\":\\\"s0853g:71\\\",\\\"login_source\\\":\\\"Login\\\",\\\"login_credential_type\\\":\\\"none\\\",\\\"server_login_source\\\":\\\"login\\\",\\\"ar_event_source\\\":\\\"login_home_page\\\",\\\"should_trigger_override_login_success_action\\\":0,\\\"should_trigger_override_login_2fa_action\\\":0,\\\"is_caa_perf_enabled\\\":1,\\\"reg_flow_source\\\":\\\"aymh_multi_profiles_native_integration_point\\\",\\\"caller\\\":\\\"gslr\\\",\\\"is_from_landing_page\\\":0,\\\"is_from_empty_password\\\":0,\\\"is_from_password_entry_page\\\":0,\\\"is_from_assistive_id\\\":0,\\\"INTERNAL__latency_qpl_marker_id\\\":36707139,\\\"INTERNAL__latency_qpl_instance_id\\\":\\\"169343278000404\\\",\\\"device_id\\\":null,\\\"family_device_id\\\":null,\\\"waterfall_id\\\":\\\"0af5a326-07b8-4380-b860-155cf8394202\\\",\\\"offline_experiment_group\\\":null,\\\"layered_homepage_experiment_group\\\":null,\\\"is_platform_login\\\":0,\\\"is_from_logged_in_switcher\\\":0,\\\"is_from_logged_out\\\":0,\\\"access_flow_version\\\":\\\"F2_FLOW\\\",\\\"INTERNAL_INFRA_THEME\\\":\\\"harm_f\\\"},\\\"client_input_params\\\":{\\\"machine_id\\\":\\\"\\\",\\\"contact_point\\\":\\\""+userid+"\\\",\\\"password\\\":\\\""+enpas+"\\\",\\\"accounts_list\\\":[],\\\"fb_ig_device_id\\\":[],\\\"secure_family_device_id\\\":\\\"\\\",\\\"encrypted_msisdn\\\":\\\"\\\",\\\"headers_infra_flow_id\\\":\\\"\\\",\\\"try_num\\\":3,\\\"login_attempt_count\\\":1,\\\"event_flow\\\":\\\"login_manual\\\",\\\"event_step\\\":\\\"home_page\\\",\\\"openid_tokens\\\":{},\\\"auth_secure_device_id\\\":\\\"\\\",\\\"client_known_key_hash\\\":\\\"\\\",\\\"has_whatsapp_installed\\\":0,\\\"sso_token_map_json_string\\\":\\\"\\\",\\\"should_show_nested_nta_from_aymh\\\":1,\\\"password_contains_non_ascii\\\":\\\"false\\\",\\\"has_granted_read_contacts_permissions\\\":0,\\\"has_granted_read_phone_permissions\\\":0,\\\"lois_settings\\\":{\\\"lois_token\\\":\\\"\\\",\\\"lara_override\\\":\\\"\\\"}}}\"}"}
			headersPOST = {'host': 'm.facebook.com','content-length': str(len(userData)),'sec-ch-ua': '"Not-A.Brand";v="99", "Chromium";v="124"','sec-ch-ua-mobile': '?1','user-agent': 'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Mobile Safari/537.36','content-type': 'application/x-www-form-urlencoded;charset=UTF-8','sec-ch-ua-platform-version': '"9.0.0"','sec-ch-ua-full-version-list': '"Not-A.Brand";v="99.0.0.0", "Chromium";v="124.0.6327.4"','sec-ch-ua-model': '"Redmi Note 8"','sec-ch-prefers-color-scheme': 'light','sec-ch-ua-platform': '"Android"','accept': '*/*','origin': 'https://m.facebook.com','sec-fetch-site': 'same-origin','sec-fetch-mode': 'cors','sec-fetch-dest': 'empty','referer': 'https://m.facebook.com/login/','accept-language': 'id-ID,id;q=0.9,en-US;q=0.8,en;q=0.7'}
			cokie = '; '.join(f"{key}={value}" for key, value in r.cookies.get_dict().items())
			versioning = re.search(r'"WebBloksVersioningID",\[\],{versioningID:"(.*?)"', str(response))
			versioningID = versioning.group(1) if versioning else 'b187aeb6992d725d2f0fee8885c98f6b6f26079006a06093954f6628d1977a9a'
			request = r.post('https://m.facebook.com/async/wbloks/fetch/?appid=com.bloks.www.bloks.caa.login.async.send_login_request&type=action&__bkv={}'.format(versioningID), data = userData, headers=headersPOST, cookies = {'cookie': cokie})
			cookie = '; '.join(f"{key}={value}" for key, value in r.cookies.get_dict().items())
			if 'c_user' in str(cookie) or 'com.bloks.www.caa.login.save-credentials' in str(request):
				userID, username, cookies = cookiesvalidasi(cookie)
				return(userID, username, cookies)
			elif 'com.bloks.www.ap.two_step_verification.entrypoint_async' in str(request.text):
				return("Login gagal, Periksa email anda", False, False)
			else:return("Login gagal", False, False)
	except Exception as e:
		return(e)