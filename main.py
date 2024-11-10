
import requests, re, json, os, time, random, pytz, urllib.request
from Tools.friends import AddFriend, ConfirmFriend
from Tools.login import Login, cookiesvalidasi
from Tools.infoprofile import ProfileInfo
from datetime import datetime
from faker import Faker
from rich.console import Console

console = Console()
P = '\033[0m'
H = "\033[32m"
A = "\033[1;30m"
M = '\x1b[1;91m'

POSTS, info = {'STATUS': None}, {}
Ok, Cp, Fail = 0,0,0

class Config:
    
    def kode(self, a):
        for sleep in range(int(a), 0, -1):
            console.print(f' [bold green]#[bold white] Tunggu code verifikasi {sleep}{" "*10}', end='\r')
            time.sleep(1)
            
    def delayy(self, text, a):
        for sleep in range(int(a), 0, -1):
            console.print(f' [bold green]#[bold white] {text} {sleep}{" "*10}', end='\r')
            time.sleep(1)
            
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
    def get_requests_data(req):
        return {
            "__aaid": "0",
            "__user": "0",
            "__a": "1",
            "__req": "6",
            "__hs": re.search('"haste_session":"(.*?)"', str(req)).group(1),
            "dpr": "1",
            "__ccg": "GOOD",
            "__rev": re.search('"__spin_r":(.*?)', str(req)).group(1),
            "__s": "",
            "__hsi": "",
            "__dyn": "",
            "__csr": "",
            "fb_dtsg": re.search('{"dtsg":{"token":"(.*?)"', str(req)).group(1),
            "jazoest": re.search('"jazoest", "(.*?)"', str(req)).group(1),
            "lsd": re.search('"lsd":"(.*?)"', str(req)).group(1),
        }
        
    @staticmethod
    def temp_headers():
        return {
            'host': 'api.internal.temp-mail.io',
            'application-name': 'web',
            'sec-ch-ua-platform': '"Android"',
            'application-version': '2.4.2','sec-ch-ua': '"Google Chrome";v="129", "Not=A?Brand";v="8", "Chromium";v="129"',
            'sec-ch-ua-mobile': '?1',
            'user-agent': 'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Mobile Safari/537.36',
            'accept': 'application/json, text/plain, */*',
            'content-type': 'application/json;charset=UTF-8',
            'origin': 'https://temp-mail.io',
            'sec-fetch-site': 'same-site',
            'sec-fetch-mode': 'cors',
            'sec-fetch-dest': 'empty',
            'referer': 'https://temp-mail.io/',
            'accept-language': 'id-ID,id;q=0.9,en-US;q=0.8,en;q=0.7'
        }
    
    @staticmethod
    def defaultHeadersGet(type: str) -> str:
        if type == 'Get':
            return {
                'host': 'm.facebook.com',
                'cache-control': 'max-age=0',
                'dpr': '2.75',
                'viewport-width': '980',
                'sec-ch-ua': '"Not-A.Brand";v="99", "Chromium";v="124"',
                'sec-ch-ua-mobile': '?1',
                'sec-ch-ua-platform': '"Android"',
                'sec-ch-ua-platform-version': '"9.0.0"',
                'sec-ch-ua-model': '"Redmi Note 8"',
                'sec-ch-ua-full-version-list': '"Not-A.Brand";v="99.0.0.0", "Chromium";v="124.0.6327.4"',
                'sec-ch-prefers-color-scheme': 'light',
                'upgrade-insecure-requests': '1',
                'user-agent': 'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Mobile Safari/537.36',
                'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
                'sec-fetch-site': 'same-origin',
                'sec-fetch-mode': 'navigate',
                'sec-fetch-user': '?1',
                'sec-fetch-dest': 'document',
                'accept-language': 'id-ID,id;q=0.9,en-US;q=0.8,en;q=0.7'
            }
        else:
            return {
                'host': 'm.facebook.com',
                'content-length': '9827',
                'sec-ch-ua-full-version-list': '"Chromium";v="130.0.0.0", "Brave";v="130.0.0.0", "Not?A_Brand";v="99.0.0.0"',
                'sec-ch-ua-platform': '"Android"',
                'sec-ch-ua': '"Chromium";v="130", "Brave";v="130", "Not?A_Brand";v="99"',
                'sec-ch-ua-model': '""',
                'sec-ch-ua-mobile': '?1',
                'user-agent': 'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Mobile Safari/537.36',
                'content-type': 'application/x-www-form-urlencoded;charset=UTF-8',
                'sec-ch-ua-platform-version': '"9.0.0"',
                'accept': '*/*',
                'sec-gpc': '1',
                'accept-language': 'id-ID,id;q=0.7',
                'origin': 'https://m.facebook.com',
                'sec-fetch-site': 'same-origin',
                'sec-fetch-mode': 'cors',
                'sec-fetch-dest': 'empty',
                'referer': 'https://m.facebook.com/reg/',
                'priority': 'u=1, i'
            }

class MainMenu:
	def __init__(self):
		pass
		
	def banner(self):
		print(f""" 
   {A}___               _         ___  ___ 
  / __\ __ ___  __ _| |_ ___  / __\/ __\ 
 / / | '__/ _ \/ _` | __/ _ \/ _\ /__\/\ 
/ /__| | |  __/ (_| | ||  __/ /  / \\/  \\ {P}Source code By {H}Fajarky{P}
{H}\\____/_|  \\___|\\__,_|\\__\\___\\/   \\_____/ {P}Version 0.1""")
	
	def menu(self):
		os.system('cls' if os.name == 'nt' else 'clear')
		self.banner()
		console.print("""
 [bold green]1[bold white]) buat akun facebook
 [bold green]2[bold white]) Add Friend Otomatis
 [bold green]3[bold white]) Komentar Otomatis
 [bold green]4[bold white]) Tambahkan informasi profil
 [bold green]5[bold white]) Cek Akun
 [bold green]6[bold white]) exit
		""")
		choice = console.input(" [bold green]#[bold white] Choose option: ")
		if choice in ['1', '01']:self.create()
		
		elif choice in ['2', '02']:
			console.print("""
 ├─ [bold green]1[bold white] Login menggunakan userID dan password 
 ├─ [bold green]2[bold white] Login menggunakan Cookies
 └─ [bold green]3[bold white] Confirm friend
			""")
			select = console.input(" [bold green]#[bold white] Choose option: ")
			if select in ['1', '01']: 
				try:
				    accounts = self.load_uid_pw('Results/login.txt')
				    userID = self.load_uid('Results/addteman.txt')
				    if not userID:
				        raise ValueError("userID tidak dimuat dengan benar")
				    
				    jumlah_id_per_akun = int(console.input(" [bold green]#[bold white] Masukkan jumlah ID yang ingin di-add per akun: "))
				    
				    for account in accounts:
				        if len(account.split('|')) < 2:
				            continue
				        userid, password = account.split('|')[0], account.split('|')[1]
				        userId, username, cookies = Login(userid, password)
				        console.print(f" [bold green]#[bold white] Login account: [bold green]{username}[bold white]")
				        if not cookies:
				            print("Cookies Tidak dapat dimuat dengan benar")
				            continue
				        console.print(f" [bold green]#[bold white] Memulai proses permintaan pertemanan untuk {jumlah_id_per_akun} pengguna...\n")
				        
				        for uid in userID[:jumlah_id_per_akun]:
				            result = AddFriend().run(cookies, uid)
				            console.print(f" [bold green]#[bold white] Userid: {uid} - Status: {result['status']} - Message: {result['message']}")
				except Exception as e:
					pass
					
			elif select in ['2', '02']:
				try:
					accounts = self.load_cookie('Results/LoginCookies.txt')
					for coki in accounts:
						userID = self.load_uid('Results/addteman.txt')
						userid, username, cookies = cookiesvalidasi(coki)
						console.print(f" [bold green]#[bold white] Login account: [bold green]{username}[bold white]")
						if not userID or not cookies:
							raise ValueError("userID atau cookie tidak dapat dimuat dengan benar. Harap periksa berkas Anda.")
						console.print(f" [bold green]#[bold white] Memulai proses permintaan pertemanan untuk {len(userID)} pengguna...\n")
						for uid in userID:
							result = AddFriend().run(cookies, uid)
							console.print(f" [bold green]#[bold white] Userid: {uid} - Status: {result['status']} - Message: {result['message']}")
						Config().delayy(15)
				except Exception as e:
					pass
			
			elif select in ['3', '03']:
				console.print("""
 ├─ [bold green]1[bold white] Login menggunakan userID dan password 
 └─ [bold green]2[bold white] Login menggunakan Cookies
				""")
				query  = console.input(" [bold green]#[bold white] Choose option: ")
				if query in ['1', '01']:
					pass
				elif query in ['2', '02']:
					pass
						
		elif choice in ['3', '03']: pass
		elif choice in ['5', '05']:
			with open('Results/FacebookNewAcc.json', 'r') as file:
				json_data = json.load(file)
			for i, data in enumerate(json_data, start=1):
				name = data.get("Name")
				userID = data.get("Userid")
				email = data.get("Email")
				password = data.get("Password")
				cookies = data.get("Cookies")
				token = data.get("Token")
				tanggal_lahir = data.get("Tanggal lahir")
				print(f"""
 Account ke {i}
 Name         : {name}
 UserID       : {userID}
 Email        : {email}
 Password     : {password}
 Cookies      : {cookies}
 Token        : {token}
 Tanggal Lahir: {tanggal_lahir}
				""")
	
	def load_uid(self, filename):
		with open(filename, 'r') as file:
			uids = file.read().splitlines()
		return uids
	
	def load_cookie(self, filename):
		with open(filename, 'r') as file:
			cookie = file.read().splitlines()
		return cookie
	
	def load_uid_pw(self, filename):
		with open(filename, 'r') as file:
			acc = file.read().splitlines()
		return acc
		
	def create(self):
		try:
			total = int(console.input('\n [bold green]#[bold white] Mau berapa akun yang di buat (default 5): ') or 5)
			delay = int(console.input(" [bold green]#[bold white] Masukkan waktu delay antar requests (default 60 detik): ") or 60)
			console.print(" [bold green]#[bold white] Apakah kamu ingin langsung membuat postingan pertama (skip=enter)")
			konten_postingan = console.input(" [bold green]#[bold white] Masukkan konten postingan: ")
			if konten_postingan:
				POSTS.update({'STATUS': f'{konten_postingan}'})
			else:
				POSTS.update({'STATUS': None})
		except ValueError:
			total = 5
			delay = 60
		
		for i in range(total):
			AccountCreator()
			self.progres(i+1, total, delay)
		time.sleep(1.5)
		self.results()
	
	def progres(self, current, total, delay):
		for sleep in range(int(delay), 0, -1):
			console.print(f' [bold green]#[bold white] Progress: {current}/{total} success: [bold green]{Ok}[bold white] failed: [bold red]{Fail}[bold white] check: [bold yellow]{Cp}[bold white] Next: {sleep}s', end='\r')
			time.sleep(1)
			if current == total:
				break

	def results(self):
		console.print(f"""
 [bold white]Final Results
 ├─ Success: [bold green]{Ok}[/]
 ├─ Failed: [bold red]{Fail}[/]
 └─ Checkpoint: [bold yellow]{Cp}[/]

Hasil disimpan ke: Results/FacebookAccounts.json""")
		
class AccountCreator:
	def __init__(self):
		self.config = Config()
		self.ses = requests.Session()
		self.data_collection()
		self.create_account()
	
	def get_email_temp_mail(self):
		try:
			mail = requests.Session()
			headers = self.config.temp_headers()
			payload = json.dumps({"min_name_length": 10,"max_name_length": 10})
			headers.update({'content-length': str(len(payload))})
			response = mail.post('https://api.internal.temp-mail.io/api/v3/email/new', data=payload, headers=headers)
			if response.status_code == 200:
				return response.json()['email']
			raise Exception("Gagal membuat email")
		except Exception as e:
			console.print(f"[bold red]Terjadi kesalahan saat menerima email sementara: {str(e)}[/]")
			return None
	
	def get_code_temp_mail(self, email):
		mail = requests.Session()
		headers = self.config.temp_headers()
		response = mail.get(f'https://api.internal.temp-mail.io/api/v3/email/{email}/messages', headers=headers)
		if response.status_code == 200:
			req = response.json()
			if req and isinstance(req, list):
				subject = req[0].get('subject', '')
				kode = re.search(r'(\d{5})', subject)
				code = kode.group(1) if kode else 'Kode tidak ditemukan'
				return code
			else:
				return 'Respon tidak valid'
		return None
	
	def data_collection(self):
		self.nama_depan, self.nama_belakang = self.generate_username()
		self.email = self.get_email_temp_mail()
		self.nomorTlpn = f"08{random.choice(['38', '31', '58'])}{random.randrange(1000,10000)}{random.randrange(10000,100000)}"
		self.tgl_lahir = self.generate_birthday()
		self.password = self.nama_belakang.lower()+"1234"
	
	def generate_username(self):
		fake = Faker("id_ID")
		first_name = fake.first_name_female()
		last_name = fake.last_name_female()
		name = f"{first_name} {last_name}"
		return first_name, last_name
	
	def generate_birthday(self):
		year = random.randint(1980, 2003)
		month = random.randint(1, 12)
		day = random.randint(1, 28)
		return str(f'{day:02d}-{month:02d}-{year}')
	
	def create_account(self):
		try:
			response = self.ses.get('https://m.facebook.com/reg/', headers = self.config.defaultHeadersGet('Get')).text
			version = re.search('\\["WebBloksVersioningID",\\[\\],{versioningID:"(.*?)"}', response)
			self.versioningID = version.group(1) if version else 'b187aeb6992d725d2f0fee8885c98f6b6f26079006a06093954f6628d1977a9a'
			self.data = self.config.get_requests_data(response)
			self.headers = self.config.defaultHeadersGet('Post')
			self.cok = ';'.join([str(x)+"="+str(y) for x,y in self.ses.cookies.get_dict().items()])
			self.name_signup()
		except Exception as e:
			raise e
			return False
	
	def name_signup(self):
		global Fail
		try:
			self.data.update({"params":"{\"server_params\":{\"event_request_id\":\"f838e734-694a-4007-b8e5-f63ec1599c5d\",\"reg_info\":\"{\\\"first_name\\\":null,\\\"last_name\\\":null,\\\"full_name\\\":null,\\\"contactpoint\\\":null,\\\"ar_contactpoint\\\":null,\\\"contactpoint_type\\\":null,\\\"is_using_unified_cp\\\":null,\\\"unified_cp_screen_variant\\\":null,\\\"is_cp_auto_confirmed\\\":false,\\\"is_cp_auto_confirmable\\\":false,\\\"confirmation_code\\\":null,\\\"birthday\\\":null,\\\"did_use_age\\\":null,\\\"gender\\\":null,\\\"use_custom_gender\\\":false,\\\"custom_gender\\\":null,\\\"encrypted_password\\\":null,\\\"username\\\":null,\\\"username_prefill\\\":null,\\\"fb_conf_source\\\":null,\\\"device_id\\\":null,\\\"ig4a_qe_device_id\\\":null,\\\"family_device_id\\\":null,\\\"nta_eligibility_reason\\\":null,\\\"ig_nta_test_group\\\":null,\\\"user_id\\\":null,\\\"safetynet_token\\\":null,\\\"safetynet_response\\\":null,\\\"machine_id\\\":null,\\\"profile_photo\\\":null,\\\"profile_photo_id\\\":null,\\\"profile_photo_upload_id\\\":null,\\\"avatar\\\":null,\\\"email_oauth_token_no_contact_perm\\\":null,\\\"email_oauth_token\\\":null,\\\"email_oauth_tokens\\\":null,\\\"should_skip_two_step_conf\\\":null,\\\"openid_tokens_for_testing\\\":null,\\\"encrypted_msisdn\\\":null,\\\"encrypted_msisdn_for_safetynet\\\":null,\\\"cached_headers_safetynet_info\\\":null,\\\"should_skip_headers_safetynet\\\":null,\\\"headers_last_infra_flow_id\\\":null,\\\"headers_last_infra_flow_id_safetynet\\\":null,\\\"headers_flow_id\\\":null,\\\"was_headers_prefill_available\\\":null,\\\"sso_enabled\\\":null,\\\"existing_accounts\\\":null,\\\"used_ig_birthday\\\":null,\\\"sync_info\\\":null,\\\"create_new_to_app_account\\\":null,\\\"skip_session_info\\\":null,\\\"ck_error\\\":null,\\\"ck_id\\\":null,\\\"ck_nonce\\\":null,\\\"should_save_password\\\":null,\\\"horizon_synced_username\\\":null,\\\"fb_access_token\\\":null,\\\"horizon_synced_profile_pic\\\":null,\\\"is_identity_synced\\\":false,\\\"is_msplit_reg\\\":null,\\\"user_id_of_msplit_creator\\\":null,\\\"dma_data_combination_consent_given\\\":null,\\\"xapp_accounts\\\":null,\\\"fb_device_id\\\":null,\\\"fb_machine_id\\\":null,\\\"ig_device_id\\\":null,\\\"ig_machine_id\\\":null,\\\"should_skip_nta_upsell\\\":null,\\\"big_blue_token\\\":null,\\\"skip_sync_step_nta\\\":null,\\\"caa_reg_flow_source\\\":\\\"login_home_native_integration_point\\\",\\\"ig_authorization_token\\\":null,\\\"full_sheet_flow\\\":false,\\\"crypted_user_id\\\":null,\\\"is_caa_perf_enabled\\\":false,\\\"is_preform\\\":true,\\\"ignore_suma_check\\\":false,\\\"ignore_existing_login\\\":false,\\\"ignore_existing_login_from_suma\\\":false,\\\"ignore_existing_login_after_errors\\\":false,\\\"suggested_first_name\\\":null,\\\"suggested_last_name\\\":null,\\\"suggested_full_name\\\":null,\\\"replace_id_sync_variant\\\":null,\\\"is_redirect_from_nta_replace_id_sync_variant\\\":false,\\\"frl_authorization_token\\\":null,\\\"post_form_errors\\\":null,\\\"skip_step_without_errors\\\":false,\\\"existing_account_exact_match_checked\\\":false,\\\"existing_account_fuzzy_match_checked\\\":false,\\\"email_oauth_exists\\\":false,\\\"confirmation_code_send_error\\\":null,\\\"is_too_young\\\":false,\\\"source_account_type\\\":null,\\\"whatsapp_installed_on_client\\\":false,\\\"confirmation_medium\\\":null,\\\"source_credentials_type\\\":null,\\\"source_cuid\\\":null,\\\"source_account_reg_info\\\":null,\\\"soap_creation_source\\\":null,\\\"source_account_type_to_reg_info\\\":null,\\\"registration_flow_id\\\":\\\"53335e1d-b812-4d0d-b4b6-9d27dcd898ec\\\",\\\"should_skip_youth_tos\\\":false,\\\"is_youth_regulation_flow_complete\\\":false,\\\"is_on_cold_start\\\":false,\\\"email_prefilled\\\":false,\\\"cp_confirmed_by_auto_conf\\\":false,\\\"auto_conf_info\\\":null,\\\"in_sowa_experiment\\\":false,\\\"youth_regulation_config\\\":null,\\\"conf_allow_back_nav_after_change_cp\\\":null,\\\"conf_bouncing_cliff_screen_type\\\":null,\\\"conf_show_bouncing_cliff\\\":null,\\\"eligible_to_flash_call_in_ig4a\\\":false,\\\"flash_call_permissions_status\\\":null,\\\"attestation_result\\\":null,\\\"request_data_and_challenge_nonce_string\\\":null,\\\"confirmed_cp_and_code\\\":null,\\\"notification_callback_id\\\":null,\\\"reg_suma_state\\\":0,\\\"is_msplit_neutral_choice\\\":false,\\\"msg_previous_cp\\\":null,\\\"ntp_import_source_info\\\":null,\\\"youth_consent_decision_time\\\":null,\\\"username_screen_experience\\\":\\\"control\\\",\\\"reduced_tos_test_group\\\":\\\"control\\\",\\\"should_show_spi_before_conf\\\":true,\\\"google_oauth_account\\\":null,\\\"is_reg_request_from_ig_suma\\\":false,\\\"is_igios_spc_reg\\\":false,\\\"device_emails\\\":null,\\\"is_toa_reg\\\":false,\\\"is_threads_public\\\":false,\\\"spc_import_flow\\\":false,\\\"caa_play_integrity_attestation_result\\\":null,\\\"flash_call_provider\\\":null,\\\"name_prefill_variant\\\":\\\"control\\\",\\\"spc_birthday_input\\\":false,\\\"failed_birthday_year_count\\\":null,\\\"user_presented_medium_source\\\":null,\\\"user_opted_out_of_ntp\\\":null}\",\"flow_info\":\"{\\\"flow_name\\\":\\\"new_to_family_fb_default\\\",\\\"flow_type\\\":\\\"ntf\\\"}\",\"current_step\":1,\"INTERNAL__latency_qpl_marker_id\":36707139,\"INTERNAL__latency_qpl_instance_id\":\"25652786500051\",\"device_id\":null,\"family_device_id\":null,\"waterfall_id\":\"fdeeab0b-b282-4a84-99bc-9da462834819\",\"offline_experiment_group\":null,\"layered_homepage_experiment_group\":null,\"is_platform_login\":0,\"is_from_logged_in_switcher\":0,\"is_from_logged_out\":0,\"access_flow_version\":\"F2_FLOW\",\"INTERNAL_INFRA_THEME\":\"harm_f\"},\"client_input_params\":{\"firstname\":\""+self.nama_depan+"\",\"lastname\":\""+self.nama_belakang+"\",\"lois_settings\":{\"lois_token\":\"\",\"lara_override\":\"\"}}}"})
			post = self.ses.post(f'https://m.facebook.com/async/wbloks/fetch/?appid=com.bloks.www.bloks.caa.reg.name.async&type=action&__bkv={self.versioningID}', data=self.data, headers = self.headers, cookies={'cookie': self.cok})
			if "Masukkan nama depan dan belakang Anda." in post.text:
				self.birthday()
				return True
			else:
				Fail+=1
				return False
		except Exception as e:
			pass
	
	def birthday(self):
		global Fail
		try:
			self.data.update({"params":"{\"server_params\":{\"reg_info\":\"{\\\"first_name\\\":\\\""+self.nama_depan+"\\\",\\\"last_name\\\":\\\""+self.nama_belakang+"\\\",\\\"full_name\\\":\\\""+self.nama_depan+"\\\",\\\"contactpoint\\\":null,\\\"ar_contactpoint\\\":null,\\\"contactpoint_type\\\":null,\\\"is_using_unified_cp\\\":null,\\\"unified_cp_screen_variant\\\":null,\\\"is_cp_auto_confirmed\\\":false,\\\"is_cp_auto_confirmable\\\":false,\\\"confirmation_code\\\":null,\\\"birthday\\\":null,\\\"did_use_age\\\":false,\\\"gender\\\":null,\\\"use_custom_gender\\\":false,\\\"custom_gender\\\":null,\\\"encrypted_password\\\":null,\\\"username\\\":null,\\\"username_prefill\\\":null,\\\"fb_conf_source\\\":null,\\\"device_id\\\":null,\\\"ig4a_qe_device_id\\\":null,\\\"family_device_id\\\":null,\\\"nta_eligibility_reason\\\":null,\\\"ig_nta_test_group\\\":null,\\\"user_id\\\":null,\\\"safetynet_token\\\":null,\\\"safetynet_response\\\":null,\\\"machine_id\\\":null,\\\"profile_photo\\\":null,\\\"profile_photo_id\\\":null,\\\"profile_photo_upload_id\\\":null,\\\"avatar\\\":null,\\\"email_oauth_token_no_contact_perm\\\":null,\\\"email_oauth_token\\\":null,\\\"email_oauth_tokens\\\":null,\\\"should_skip_two_step_conf\\\":null,\\\"openid_tokens_for_testing\\\":null,\\\"encrypted_msisdn\\\":null,\\\"encrypted_msisdn_for_safetynet\\\":null,\\\"cached_headers_safetynet_info\\\":null,\\\"should_skip_headers_safetynet\\\":null,\\\"headers_last_infra_flow_id\\\":null,\\\"headers_last_infra_flow_id_safetynet\\\":null,\\\"headers_flow_id\\\":null,\\\"was_headers_prefill_available\\\":null,\\\"sso_enabled\\\":null,\\\"existing_accounts\\\":null,\\\"used_ig_birthday\\\":null,\\\"sync_info\\\":null,\\\"create_new_to_app_account\\\":null,\\\"skip_session_info\\\":null,\\\"ck_error\\\":null,\\\"ck_id\\\":null,\\\"ck_nonce\\\":null,\\\"should_save_password\\\":null,\\\"horizon_synced_username\\\":null,\\\"fb_access_token\\\":null,\\\"horizon_synced_profile_pic\\\":null,\\\"is_identity_synced\\\":false,\\\"is_msplit_reg\\\":null,\\\"user_id_of_msplit_creator\\\":null,\\\"dma_data_combination_consent_given\\\":null,\\\"xapp_accounts\\\":null,\\\"fb_device_id\\\":null,\\\"fb_machine_id\\\":null,\\\"ig_device_id\\\":null,\\\"ig_machine_id\\\":null,\\\"should_skip_nta_upsell\\\":null,\\\"big_blue_token\\\":null,\\\"skip_sync_step_nta\\\":null,\\\"caa_reg_flow_source\\\":\\\"login_home_native_integration_point\\\",\\\"ig_authorization_token\\\":null,\\\"full_sheet_flow\\\":false,\\\"crypted_user_id\\\":null,\\\"is_caa_perf_enabled\\\":false,\\\"is_preform\\\":true,\\\"ignore_suma_check\\\":false,\\\"ignore_existing_login\\\":false,\\\"ignore_existing_login_from_suma\\\":false,\\\"ignore_existing_login_after_errors\\\":false,\\\"suggested_first_name\\\":null,\\\"suggested_last_name\\\":null,\\\"suggested_full_name\\\":null,\\\"replace_id_sync_variant\\\":null,\\\"is_redirect_from_nta_replace_id_sync_variant\\\":false,\\\"frl_authorization_token\\\":null,\\\"post_form_errors\\\":null,\\\"skip_step_without_errors\\\":false,\\\"existing_account_exact_match_checked\\\":false,\\\"existing_account_fuzzy_match_checked\\\":false,\\\"email_oauth_exists\\\":false,\\\"confirmation_code_send_error\\\":null,\\\"is_too_young\\\":false,\\\"source_account_type\\\":null,\\\"whatsapp_installed_on_client\\\":false,\\\"confirmation_medium\\\":null,\\\"source_credentials_type\\\":null,\\\"source_cuid\\\":null,\\\"source_account_reg_info\\\":null,\\\"soap_creation_source\\\":null,\\\"source_account_type_to_reg_info\\\":null,\\\"registration_flow_id\\\":\\\"53335e1d-b812-4d0d-b4b6-9d27dcd898ec\\\",\\\"should_skip_youth_tos\\\":false,\\\"is_youth_regulation_flow_complete\\\":false,\\\"is_on_cold_start\\\":false,\\\"email_prefilled\\\":false,\\\"cp_confirmed_by_auto_conf\\\":false,\\\"auto_conf_info\\\":null,\\\"in_sowa_experiment\\\":false,\\\"youth_regulation_config\\\":null,\\\"conf_allow_back_nav_after_change_cp\\\":null,\\\"conf_bouncing_cliff_screen_type\\\":null,\\\"conf_show_bouncing_cliff\\\":null,\\\"eligible_to_flash_call_in_ig4a\\\":false,\\\"flash_call_permissions_status\\\":null,\\\"attestation_result\\\":null,\\\"request_data_and_challenge_nonce_string\\\":null,\\\"confirmed_cp_and_code\\\":null,\\\"notification_callback_id\\\":null,\\\"reg_suma_state\\\":0,\\\"is_msplit_neutral_choice\\\":false,\\\"msg_previous_cp\\\":null,\\\"ntp_import_source_info\\\":null,\\\"youth_consent_decision_time\\\":null,\\\"username_screen_experience\\\":\\\"control\\\",\\\"reduced_tos_test_group\\\":\\\"control\\\",\\\"should_show_spi_before_conf\\\":true,\\\"google_oauth_account\\\":null,\\\"is_reg_request_from_ig_suma\\\":false,\\\"is_igios_spc_reg\\\":false,\\\"device_emails\\\":null,\\\"is_toa_reg\\\":false,\\\"is_threads_public\\\":false,\\\"spc_import_flow\\\":false,\\\"caa_play_integrity_attestation_result\\\":null,\\\"flash_call_provider\\\":null,\\\"name_prefill_variant\\\":\\\"control\\\",\\\"spc_birthday_input\\\":false,\\\"failed_birthday_year_count\\\":null,\\\"user_presented_medium_source\\\":null,\\\"user_opted_out_of_ntp\\\":null}\",\"flow_info\":\"{\\\"flow_name\\\":\\\"new_to_family_fb_default\\\",\\\"flow_type\\\":\\\"ntf\\\"}\",\"current_step\":2,\"INTERNAL__latency_qpl_marker_id\":36707139,\"INTERNAL__latency_qpl_instance_id\":\"25730902800115\",\"device_id\":null,\"family_device_id\":null,\"waterfall_id\":\"fdeeab0b-b282-4a84-99bc-9da462834819\",\"offline_experiment_group\":null,\"layered_homepage_experiment_group\":null,\"is_platform_login\":0,\"is_from_logged_in_switcher\":0,\"is_from_logged_out\":0,\"access_flow_version\":\"F2_FLOW\",\"INTERNAL_INFRA_THEME\":\"harm_f\"},\"client_input_params\":{\"birthday_timestamp\":"+str(int(time.time()))+",\"should_skip_youth_tos\":0,\"is_youth_regulation_flow_complete\":0,\"lois_settings\":{\"lois_token\":\"\",\"lara_override\":\"\"}}}"})
			cok  = ';'.join([str(x)+"="+str(y) for x,y in self.ses.cookies.get_dict().items()])
			post = self.ses.post(f'https://m.facebook.com/async/wbloks/fetch/?appid=com.bloks.www.bloks.caa.reg.birthday.async&type=action&__bkv={self.versioningID}', data=self.data, headers = self.headers, cookies={'cookie': cok})
			if "Kelihatannya Anda memasukkan info yang salah. Harap pastikan untuk menggunakan tanggal lahir asli Anda." in post.text:
				self.gender()
				return True
			else:
				Fail+=1
				return False
		except Exception as e:
			pass
	
	def gender(self):
		global Fail
		try:
			self.data.update({"params":"{\"server_params\":{\"reg_info\":\"{\\\"first_name\\\":\\\""+self.nama_depan+"\\\",\\\"last_name\\\":\\\""+self.nama_belakang+"\\\",\\\"full_name\\\":\\\""+self.nama_depan+"\\\",\\\"contactpoint\\\":null,\\\"ar_contactpoint\\\":null,\\\"contactpoint_type\\\":null,\\\"is_using_unified_cp\\\":null,\\\"unified_cp_screen_variant\\\":null,\\\"is_cp_auto_confirmed\\\":false,\\\"is_cp_auto_confirmable\\\":false,\\\"confirmation_code\\\":null,\\\"birthday\\\":\\\""+self.tgl_lahir+"\\\",\\\"did_use_age\\\":false,\\\"gender\\\":null,\\\"use_custom_gender\\\":false,\\\"custom_gender\\\":null,\\\"encrypted_password\\\":null,\\\"username\\\":null,\\\"username_prefill\\\":null,\\\"fb_conf_source\\\":null,\\\"device_id\\\":null,\\\"ig4a_qe_device_id\\\":null,\\\"family_device_id\\\":null,\\\"nta_eligibility_reason\\\":null,\\\"ig_nta_test_group\\\":null,\\\"user_id\\\":null,\\\"safetynet_token\\\":null,\\\"safetynet_response\\\":null,\\\"machine_id\\\":null,\\\"profile_photo\\\":null,\\\"profile_photo_id\\\":null,\\\"profile_photo_upload_id\\\":null,\\\"avatar\\\":null,\\\"email_oauth_token_no_contact_perm\\\":null,\\\"email_oauth_token\\\":null,\\\"email_oauth_tokens\\\":null,\\\"should_skip_two_step_conf\\\":null,\\\"openid_tokens_for_testing\\\":null,\\\"encrypted_msisdn\\\":null,\\\"encrypted_msisdn_for_safetynet\\\":null,\\\"cached_headers_safetynet_info\\\":null,\\\"should_skip_headers_safetynet\\\":null,\\\"headers_last_infra_flow_id\\\":null,\\\"headers_last_infra_flow_id_safetynet\\\":null,\\\"headers_flow_id\\\":null,\\\"was_headers_prefill_available\\\":null,\\\"sso_enabled\\\":null,\\\"existing_accounts\\\":null,\\\"used_ig_birthday\\\":null,\\\"sync_info\\\":null,\\\"create_new_to_app_account\\\":null,\\\"skip_session_info\\\":null,\\\"ck_error\\\":null,\\\"ck_id\\\":null,\\\"ck_nonce\\\":null,\\\"should_save_password\\\":null,\\\"horizon_synced_username\\\":null,\\\"fb_access_token\\\":null,\\\"horizon_synced_profile_pic\\\":null,\\\"is_identity_synced\\\":false,\\\"is_msplit_reg\\\":null,\\\"user_id_of_msplit_creator\\\":null,\\\"dma_data_combination_consent_given\\\":null,\\\"xapp_accounts\\\":null,\\\"fb_device_id\\\":null,\\\"fb_machine_id\\\":null,\\\"ig_device_id\\\":null,\\\"ig_machine_id\\\":null,\\\"should_skip_nta_upsell\\\":null,\\\"big_blue_token\\\":null,\\\"skip_sync_step_nta\\\":null,\\\"caa_reg_flow_source\\\":\\\"login_home_native_integration_point\\\",\\\"ig_authorization_token\\\":null,\\\"full_sheet_flow\\\":false,\\\"crypted_user_id\\\":null,\\\"is_caa_perf_enabled\\\":false,\\\"is_preform\\\":true,\\\"ignore_suma_check\\\":false,\\\"ignore_existing_login\\\":false,\\\"ignore_existing_login_from_suma\\\":false,\\\"ignore_existing_login_after_errors\\\":false,\\\"suggested_first_name\\\":null,\\\"suggested_last_name\\\":null,\\\"suggested_full_name\\\":null,\\\"replace_id_sync_variant\\\":null,\\\"is_redirect_from_nta_replace_id_sync_variant\\\":false,\\\"frl_authorization_token\\\":null,\\\"post_form_errors\\\":null,\\\"skip_step_without_errors\\\":false,\\\"existing_account_exact_match_checked\\\":false,\\\"existing_account_fuzzy_match_checked\\\":false,\\\"email_oauth_exists\\\":false,\\\"confirmation_code_send_error\\\":null,\\\"is_too_young\\\":false,\\\"source_account_type\\\":null,\\\"whatsapp_installed_on_client\\\":false,\\\"confirmation_medium\\\":null,\\\"source_credentials_type\\\":null,\\\"source_cuid\\\":null,\\\"source_account_reg_info\\\":null,\\\"soap_creation_source\\\":null,\\\"source_account_type_to_reg_info\\\":null,\\\"registration_flow_id\\\":\\\"53335e1d-b812-4d0d-b4b6-9d27dcd898ec\\\",\\\"should_skip_youth_tos\\\":false,\\\"is_youth_regulation_flow_complete\\\":false,\\\"is_on_cold_start\\\":false,\\\"email_prefilled\\\":false,\\\"cp_confirmed_by_auto_conf\\\":false,\\\"auto_conf_info\\\":null,\\\"in_sowa_experiment\\\":false,\\\"youth_regulation_config\\\":null,\\\"conf_allow_back_nav_after_change_cp\\\":null,\\\"conf_bouncing_cliff_screen_type\\\":null,\\\"conf_show_bouncing_cliff\\\":null,\\\"eligible_to_flash_call_in_ig4a\\\":false,\\\"flash_call_permissions_status\\\":null,\\\"attestation_result\\\":null,\\\"request_data_and_challenge_nonce_string\\\":null,\\\"confirmed_cp_and_code\\\":null,\\\"notification_callback_id\\\":null,\\\"reg_suma_state\\\":0,\\\"is_msplit_neutral_choice\\\":false,\\\"msg_previous_cp\\\":null,\\\"ntp_import_source_info\\\":null,\\\"youth_consent_decision_time\\\":null,\\\"username_screen_experience\\\":\\\"control\\\",\\\"reduced_tos_test_group\\\":\\\"control\\\",\\\"should_show_spi_before_conf\\\":true,\\\"google_oauth_account\\\":null,\\\"is_reg_request_from_ig_suma\\\":false,\\\"is_igios_spc_reg\\\":false,\\\"device_emails\\\":null,\\\"is_toa_reg\\\":false,\\\"is_threads_public\\\":false,\\\"spc_import_flow\\\":false,\\\"caa_play_integrity_attestation_result\\\":null,\\\"flash_call_provider\\\":null,\\\"name_prefill_variant\\\":\\\"control\\\",\\\"spc_birthday_input\\\":false,\\\"failed_birthday_year_count\\\":null,\\\"user_presented_medium_source\\\":null,\\\"user_opted_out_of_ntp\\\":null}\",\"flow_info\":\"{\\\"flow_name\\\":\\\"new_to_family_fb_default\\\",\\\"flow_type\\\":\\\"ntf\\\"}\",\"current_step\":3,\"INTERNAL__latency_qpl_marker_id\":36707139,\"INTERNAL__latency_qpl_instance_id\":\"25777026700115\",\"device_id\":null,\"family_device_id\":null,\"waterfall_id\":\"fdeeab0b-b282-4a84-99bc-9da462834819\",\"offline_experiment_group\":null,\"layered_homepage_experiment_group\":null,\"is_platform_login\":0,\"is_from_logged_in_switcher\":0,\"is_from_logged_out\":0,\"access_flow_version\":\"F2_FLOW\",\"INTERNAL_INFRA_THEME\":\"harm_f\"},\"client_input_params\":{\"gender\":1,\"pronoun\":0,\"custom_gender\":\"\",\"device_phone_numbers\":[],\"lois_settings\":{\"lois_token\":\"\",\"lara_override\":\"\"}}}"})
			cok  = ';'.join([str(x)+"="+str(y) for x,y in self.ses.cookies.get_dict().items()])
			post = self.ses.post(f'https://m.facebook.com/async/wbloks/fetch/?appid=com.bloks.www.bloks.caa.reg.gender.async&type=action&__bkv={self.versioningID}', data=self.data, headers = self.headers, cookies={'cookie': cok})
			if "com.bloks.www.bloks.caa.reg.contactpoint_phone" in post.text:
				self.phone_()
				return True
			else:
				Fail+=1
				return False
		except Exception as e:
			pass
	
	def email_(self):
		global Fail
		try:
			console.print(f" [bold green]#[bold white] email: [bold green]{self.email}[bold white]{' '*20}", end='\r')
			time.sleep(1.5)
			self.data.update({"params":"{\"server_params\":{\"event_request_id\":\"b1ce0a8e-49af-4aba-a73c-dd3593f857bf\",\"cp_funnel\":0,\"cp_source\":0,\"text_input_id\":\"25813308100064\",\"reg_info\":\"{\\\"first_name\\\":\\\""+self.nama_depan+"\\\",\\\"last_name\\\":\\\""+self.nama_belakang+"\\\",\\\"full_name\\\":\\\""+self.nama_depan+"\\\",\\\"contactpoint\\\":null,\\\"ar_contactpoint\\\":null,\\\"contactpoint_type\\\":null,\\\"is_using_unified_cp\\\":null,\\\"unified_cp_screen_variant\\\":null,\\\"is_cp_auto_confirmed\\\":false,\\\"is_cp_auto_confirmable\\\":false,\\\"confirmation_code\\\":null,\\\"birthday\\\":\\\""+self.tgl_lahir+"\\\",\\\"did_use_age\\\":false,\\\"gender\\\":1,\\\"use_custom_gender\\\":false,\\\"custom_gender\\\":null,\\\"encrypted_password\\\":null,\\\"username\\\":null,\\\"username_prefill\\\":null,\\\"fb_conf_source\\\":null,\\\"device_id\\\":null,\\\"ig4a_qe_device_id\\\":null,\\\"family_device_id\\\":null,\\\"nta_eligibility_reason\\\":null,\\\"ig_nta_test_group\\\":null,\\\"user_id\\\":null,\\\"safetynet_token\\\":null,\\\"safetynet_response\\\":null,\\\"machine_id\\\":null,\\\"profile_photo\\\":null,\\\"profile_photo_id\\\":null,\\\"profile_photo_upload_id\\\":null,\\\"avatar\\\":null,\\\"email_oauth_token_no_contact_perm\\\":null,\\\"email_oauth_token\\\":null,\\\"email_oauth_tokens\\\":null,\\\"should_skip_two_step_conf\\\":null,\\\"openid_tokens_for_testing\\\":null,\\\"encrypted_msisdn\\\":null,\\\"encrypted_msisdn_for_safetynet\\\":null,\\\"cached_headers_safetynet_info\\\":null,\\\"should_skip_headers_safetynet\\\":null,\\\"headers_last_infra_flow_id\\\":null,\\\"headers_last_infra_flow_id_safetynet\\\":null,\\\"headers_flow_id\\\":null,\\\"was_headers_prefill_available\\\":null,\\\"sso_enabled\\\":null,\\\"existing_accounts\\\":null,\\\"used_ig_birthday\\\":null,\\\"sync_info\\\":null,\\\"create_new_to_app_account\\\":null,\\\"skip_session_info\\\":null,\\\"ck_error\\\":null,\\\"ck_id\\\":null,\\\"ck_nonce\\\":null,\\\"should_save_password\\\":null,\\\"horizon_synced_username\\\":null,\\\"fb_access_token\\\":null,\\\"horizon_synced_profile_pic\\\":null,\\\"is_identity_synced\\\":false,\\\"is_msplit_reg\\\":null,\\\"user_id_of_msplit_creator\\\":null,\\\"dma_data_combination_consent_given\\\":null,\\\"xapp_accounts\\\":null,\\\"fb_device_id\\\":null,\\\"fb_machine_id\\\":null,\\\"ig_device_id\\\":null,\\\"ig_machine_id\\\":null,\\\"should_skip_nta_upsell\\\":null,\\\"big_blue_token\\\":null,\\\"skip_sync_step_nta\\\":null,\\\"caa_reg_flow_source\\\":\\\"login_home_native_integration_point\\\",\\\"ig_authorization_token\\\":null,\\\"full_sheet_flow\\\":false,\\\"crypted_user_id\\\":null,\\\"is_caa_perf_enabled\\\":false,\\\"is_preform\\\":true,\\\"ignore_suma_check\\\":false,\\\"ignore_existing_login\\\":false,\\\"ignore_existing_login_from_suma\\\":false,\\\"ignore_existing_login_after_errors\\\":false,\\\"suggested_first_name\\\":null,\\\"suggested_last_name\\\":null,\\\"suggested_full_name\\\":null,\\\"replace_id_sync_variant\\\":null,\\\"is_redirect_from_nta_replace_id_sync_variant\\\":false,\\\"frl_authorization_token\\\":null,\\\"post_form_errors\\\":null,\\\"skip_step_without_errors\\\":false,\\\"existing_account_exact_match_checked\\\":false,\\\"existing_account_fuzzy_match_checked\\\":false,\\\"email_oauth_exists\\\":false,\\\"confirmation_code_send_error\\\":null,\\\"is_too_young\\\":false,\\\"source_account_type\\\":null,\\\"whatsapp_installed_on_client\\\":false,\\\"confirmation_medium\\\":null,\\\"source_credentials_type\\\":null,\\\"source_cuid\\\":null,\\\"source_account_reg_info\\\":null,\\\"soap_creation_source\\\":null,\\\"source_account_type_to_reg_info\\\":null,\\\"registration_flow_id\\\":\\\"53335e1d-b812-4d0d-b4b6-9d27dcd898ec\\\",\\\"should_skip_youth_tos\\\":false,\\\"is_youth_regulation_flow_complete\\\":false,\\\"is_on_cold_start\\\":false,\\\"email_prefilled\\\":false,\\\"cp_confirmed_by_auto_conf\\\":false,\\\"auto_conf_info\\\":null,\\\"in_sowa_experiment\\\":false,\\\"youth_regulation_config\\\":null,\\\"conf_allow_back_nav_after_change_cp\\\":null,\\\"conf_bouncing_cliff_screen_type\\\":null,\\\"conf_show_bouncing_cliff\\\":null,\\\"eligible_to_flash_call_in_ig4a\\\":false,\\\"flash_call_permissions_status\\\":null,\\\"attestation_result\\\":null,\\\"request_data_and_challenge_nonce_string\\\":null,\\\"confirmed_cp_and_code\\\":null,\\\"notification_callback_id\\\":null,\\\"reg_suma_state\\\":0,\\\"is_msplit_neutral_choice\\\":false,\\\"msg_previous_cp\\\":null,\\\"ntp_import_source_info\\\":null,\\\"youth_consent_decision_time\\\":null,\\\"username_screen_experience\\\":\\\"control\\\",\\\"reduced_tos_test_group\\\":\\\"control\\\",\\\"should_show_spi_before_conf\\\":true,\\\"google_oauth_account\\\":null,\\\"is_reg_request_from_ig_suma\\\":false,\\\"is_igios_spc_reg\\\":false,\\\"device_emails\\\":null,\\\"is_toa_reg\\\":false,\\\"is_threads_public\\\":false,\\\"spc_import_flow\\\":false,\\\"caa_play_integrity_attestation_result\\\":null,\\\"flash_call_provider\\\":null,\\\"name_prefill_variant\\\":\\\"control\\\",\\\"spc_birthday_input\\\":false,\\\"failed_birthday_year_count\\\":null,\\\"user_presented_medium_source\\\":null,\\\"user_opted_out_of_ntp\\\":null}\",\"flow_info\":\"{\\\"flow_name\\\":\\\"new_to_family_fb_default\\\",\\\"flow_type\\\":\\\"ntf\\\"}\",\"current_step\":4,\"INTERNAL__latency_qpl_marker_id\":36707139,\"INTERNAL__latency_qpl_instance_id\":\"25813308100096\",\"device_id\":null,\"family_device_id\":null,\"waterfall_id\":\"fdeeab0b-b282-4a84-99bc-9da462834819\",\"offline_experiment_group\":null,\"layered_homepage_experiment_group\":null,\"is_platform_login\":0,\"is_from_logged_in_switcher\":0,\"is_from_logged_out\":0,\"access_flow_version\":\"F2_FLOW\",\"INTERNAL_INFRA_THEME\":\"harm_f\"},\"client_input_params\":{\"device_id\":\"\",\"family_device_id\":\"\",\"email\":\""+self.email+"\",\"email_prefilled\":0,\"accounts_list\":[],\"fb_ig_device_id\":[],\"confirmed_cp_and_code\":{},\"is_from_device_emails\":0,\"msg_previous_cp\":\"\",\"switch_cp_first_time_loading\":1,\"switch_cp_have_seen_suma\":0,\"lois_settings\":{\"lois_token\":\"\",\"lara_override\":\"\"}}}"})
			cok  = ';'.join([str(x)+"="+str(y) for x,y in self.ses.cookies.get_dict().items()])
			post = self.ses.post(f'https://m.facebook.com/async/wbloks/fetch/?appid=com.bloks.www.bloks.caa.reg.async.contactpoint_email.async&type=action&__bkv={self.versioningID}', data=self.data, headers = self.headers, cookies={'cookie': cok})
			if 'com.bloks.www.bloks.caa.reg.password' in post.text:
				self.password_()
				return True
			else:
				Fail+=1
				return False
		except Exception as e:
			pass
	
	def phone_(self):
		global Fail
		try:
			console.print(f" [bold green]#[bold white] nomor: [bold green]{self.nomorTlpn.replace('08', '+628')}[bold white]{' '*20}", end='\r')
			time.sleep(1.5)
			self.data.update({"params":"{\"server_params\":{\"event_request_id\":\"ba86e3d3-6cd8-4065-9eef-9c2db35fd5dc\",\"cp_funnel\":0,\"cp_source\":0,\"text_input_id\":\"29225065300073\",\"reg_info\":\"{\\\"first_name\\\":\\\""+self.nama_depan+"\\\",\\\"last_name\\\":\\\""+self.nama_belakang+"\\\",\\\"full_name\\\":\\\""+self.nama_depan+"\\\",\\\"contactpoint\\\":null,\\\"ar_contactpoint\\\":null,\\\"contactpoint_type\\\":null,\\\"is_using_unified_cp\\\":null,\\\"unified_cp_screen_variant\\\":null,\\\"is_cp_auto_confirmed\\\":false,\\\"is_cp_auto_confirmable\\\":false,\\\"confirmation_code\\\":null,\\\"birthday\\\":\\\""+self.tgl_lahir+"\\\",\\\"did_use_age\\\":false,\\\"gender\\\":1,\\\"use_custom_gender\\\":false,\\\"custom_gender\\\":null,\\\"encrypted_password\\\":null,\\\"username\\\":null,\\\"username_prefill\\\":null,\\\"fb_conf_source\\\":null,\\\"device_id\\\":null,\\\"ig4a_qe_device_id\\\":null,\\\"family_device_id\\\":null,\\\"nta_eligibility_reason\\\":null,\\\"ig_nta_test_group\\\":null,\\\"user_id\\\":null,\\\"safetynet_token\\\":null,\\\"safetynet_response\\\":null,\\\"machine_id\\\":null,\\\"profile_photo\\\":null,\\\"profile_photo_id\\\":null,\\\"profile_photo_upload_id\\\":null,\\\"avatar\\\":null,\\\"email_oauth_token_no_contact_perm\\\":null,\\\"email_oauth_token\\\":null,\\\"email_oauth_tokens\\\":null,\\\"should_skip_two_step_conf\\\":null,\\\"openid_tokens_for_testing\\\":null,\\\"encrypted_msisdn\\\":null,\\\"encrypted_msisdn_for_safetynet\\\":null,\\\"cached_headers_safetynet_info\\\":null,\\\"should_skip_headers_safetynet\\\":null,\\\"headers_last_infra_flow_id\\\":null,\\\"headers_last_infra_flow_id_safetynet\\\":null,\\\"headers_flow_id\\\":null,\\\"was_headers_prefill_available\\\":null,\\\"sso_enabled\\\":null,\\\"existing_accounts\\\":null,\\\"used_ig_birthday\\\":null,\\\"sync_info\\\":null,\\\"create_new_to_app_account\\\":null,\\\"skip_session_info\\\":null,\\\"ck_error\\\":null,\\\"ck_id\\\":null,\\\"ck_nonce\\\":null,\\\"should_save_password\\\":null,\\\"horizon_synced_username\\\":null,\\\"fb_access_token\\\":null,\\\"horizon_synced_profile_pic\\\":null,\\\"is_identity_synced\\\":false,\\\"is_msplit_reg\\\":null,\\\"user_id_of_msplit_creator\\\":null,\\\"dma_data_combination_consent_given\\\":null,\\\"xapp_accounts\\\":null,\\\"fb_device_id\\\":null,\\\"fb_machine_id\\\":null,\\\"ig_device_id\\\":null,\\\"ig_machine_id\\\":null,\\\"should_skip_nta_upsell\\\":null,\\\"big_blue_token\\\":null,\\\"skip_sync_step_nta\\\":null,\\\"caa_reg_flow_source\\\":null,\\\"ig_authorization_token\\\":null,\\\"full_sheet_flow\\\":false,\\\"crypted_user_id\\\":null,\\\"is_caa_perf_enabled\\\":false,\\\"is_preform\\\":true,\\\"ignore_suma_check\\\":false,\\\"ignore_existing_login\\\":false,\\\"ignore_existing_login_from_suma\\\":false,\\\"ignore_existing_login_after_errors\\\":false,\\\"suggested_first_name\\\":null,\\\"suggested_last_name\\\":null,\\\"suggested_full_name\\\":null,\\\"replace_id_sync_variant\\\":null,\\\"is_redirect_from_nta_replace_id_sync_variant\\\":false,\\\"frl_authorization_token\\\":null,\\\"post_form_errors\\\":null,\\\"skip_step_without_errors\\\":false,\\\"existing_account_exact_match_checked\\\":false,\\\"existing_account_fuzzy_match_checked\\\":false,\\\"email_oauth_exists\\\":false,\\\"confirmation_code_send_error\\\":null,\\\"is_too_young\\\":false,\\\"source_account_type\\\":null,\\\"whatsapp_installed_on_client\\\":false,\\\"confirmation_medium\\\":null,\\\"source_credentials_type\\\":null,\\\"source_cuid\\\":null,\\\"source_account_reg_info\\\":null,\\\"soap_creation_source\\\":null,\\\"source_account_type_to_reg_info\\\":null,\\\"registration_flow_id\\\":\\\"\\\",\\\"should_skip_youth_tos\\\":false,\\\"is_youth_regulation_flow_complete\\\":false,\\\"is_on_cold_start\\\":false,\\\"email_prefilled\\\":false,\\\"cp_confirmed_by_auto_conf\\\":false,\\\"auto_conf_info\\\":null,\\\"in_sowa_experiment\\\":false,\\\"youth_regulation_config\\\":null,\\\"conf_allow_back_nav_after_change_cp\\\":null,\\\"conf_bouncing_cliff_screen_type\\\":null,\\\"conf_show_bouncing_cliff\\\":null,\\\"eligible_to_flash_call_in_ig4a\\\":false,\\\"flash_call_permissions_status\\\":null,\\\"attestation_result\\\":null,\\\"request_data_and_challenge_nonce_string\\\":null,\\\"confirmed_cp_and_code\\\":null,\\\"notification_callback_id\\\":null,\\\"reg_suma_state\\\":0,\\\"is_msplit_neutral_choice\\\":false,\\\"msg_previous_cp\\\":null,\\\"ntp_import_source_info\\\":null,\\\"youth_consent_decision_time\\\":null,\\\"username_screen_experience\\\":\\\"control\\\",\\\"reduced_tos_test_group\\\":\\\"control\\\",\\\"should_show_spi_before_conf\\\":true,\\\"google_oauth_account\\\":null,\\\"is_reg_request_from_ig_suma\\\":false,\\\"is_igios_spc_reg\\\":false,\\\"device_emails\\\":null,\\\"is_toa_reg\\\":false,\\\"is_threads_public\\\":false,\\\"spc_import_flow\\\":false,\\\"caa_play_integrity_attestation_result\\\":null,\\\"flash_call_provider\\\":null,\\\"name_prefill_variant\\\":\\\"control\\\",\\\"spc_birthday_input\\\":false,\\\"failed_birthday_year_count\\\":null,\\\"user_presented_medium_source\\\":null,\\\"user_opted_out_of_ntp\\\":null,\\\"is_from_registration_reminder\\\":false,\\\"show_youth_reg_in_ig_spc\\\":false}\",\"flow_info\":\"{\\\"flow_name\\\":\\\"new_to_family_fb_default\\\",\\\"flow_type\\\":\\\"ntf\\\"}\",\"current_step\":4,\"INTERNAL__latency_qpl_marker_id\":36707139,\"INTERNAL__latency_qpl_instance_id\":\"29225065300074\",\"device_id\":null,\"family_device_id\":null,\"waterfall_id\":\"eb0e1792-3bfe-4e4c-a5a3-1dfd405a4839\",\"offline_experiment_group\":null,\"layered_homepage_experiment_group\":null,\"is_platform_login\":0,\"is_from_logged_in_switcher\":0,\"is_from_logged_out\":0,\"access_flow_version\":\"F2_FLOW\",\"INTERNAL_INFRA_THEME\":\"harm_f\"},\"client_input_params\":{\"device_id\":\"\",\"family_device_id\":\"\",\"phone\":\""+self.nomorTlpn+"\",\"accounts_list\":[],\"build_type\":\"\",\"encrypted_msisdn\":\"\",\"headers_infra_flow_id\":\"\",\"was_headers_prefill_available\":0,\"was_headers_prefill_used\":0,\"fb_ig_device_id\":[],\"whatsapp_installed_on_client\":0,\"confirmed_cp_and_code\":{},\"msg_previous_cp\":\"\",\"switch_cp_first_time_loading\":1,\"switch_cp_have_seen_suma\":0,\"login_upsell_phone_list\":[],\"country_code\":\"\",\"lois_settings\":{\"lois_token\":\"\",\"lara_override\":\"\"}}}"})
			cok  = ';'.join([str(x)+"="+str(y) for x,y in self.ses.cookies.get_dict().items()])
			post = self.ses.post(f'https://m.facebook.com/async/wbloks/fetch/?appid=com.bloks.www.bloks.caa.reg.async.contactpoint_phone.async&type=action&__bkv={self.versioningID}', data=self.data, headers = self.headers, cookies={'cookie': cok})
			if 'com.bloks.www.bloks.caa.reg.password' in post.text:
				self.password_()
				return True
			else:
				Fail+=1
				return False
		except Exception as e:
			pass
			
	def password_(self):
		global Fail
		try:
			self.enpas = '#PWD_BROWSER:0:{}:{}'.format(int(time.time()), self.password)
			self.data.update({"params":"{\"server_params\":{\"event_request_id\":\"8b0ca18c-94ef-4ca8-95ad-4bdd0f52196d\",\"reg_info\":\"{\\\"first_name\\\":\\\""+self.nama_depan+"\\\",\\\"last_name\\\":\\\""+self.nama_belakang+"\\\",\\\"full_name\\\":\\\""+self.nama_depan+"\\\",\\\"contactpoint\\\":\\\""+self.nomorTlpn.replace('08', '+628')+"\\\",\\\"ar_contactpoint\\\":null,\\\"contactpoint_type\\\":\\\"phone\\\",\\\"is_using_unified_cp\\\":false,\\\"unified_cp_screen_variant\\\":null,\\\"is_cp_auto_confirmed\\\":false,\\\"is_cp_auto_confirmable\\\":false,\\\"confirmation_code\\\":null,\\\"birthday\\\":\\\""+self.tgl_lahir+"\\\",\\\"did_use_age\\\":false,\\\"gender\\\":1,\\\"use_custom_gender\\\":false,\\\"custom_gender\\\":null,\\\"encrypted_password\\\":null,\\\"username\\\":null,\\\"username_prefill\\\":null,\\\"fb_conf_source\\\":null,\\\"device_id\\\":null,\\\"ig4a_qe_device_id\\\":null,\\\"family_device_id\\\":null,\\\"nta_eligibility_reason\\\":null,\\\"ig_nta_test_group\\\":null,\\\"user_id\\\":null,\\\"safetynet_token\\\":null,\\\"safetynet_response\\\":null,\\\"machine_id\\\":null,\\\"profile_photo\\\":null,\\\"profile_photo_id\\\":null,\\\"profile_photo_upload_id\\\":null,\\\"avatar\\\":null,\\\"email_oauth_token_no_contact_perm\\\":null,\\\"email_oauth_token\\\":null,\\\"email_oauth_tokens\\\":null,\\\"should_skip_two_step_conf\\\":null,\\\"openid_tokens_for_testing\\\":null,\\\"encrypted_msisdn\\\":null,\\\"encrypted_msisdn_for_safetynet\\\":null,\\\"cached_headers_safetynet_info\\\":null,\\\"should_skip_headers_safetynet\\\":null,\\\"headers_last_infra_flow_id\\\":null,\\\"headers_last_infra_flow_id_safetynet\\\":null,\\\"headers_flow_id\\\":\\\"615f131a-2ab4-43f5-8052-26fa52758bfa\\\",\\\"was_headers_prefill_available\\\":false,\\\"sso_enabled\\\":null,\\\"existing_accounts\\\":null,\\\"used_ig_birthday\\\":null,\\\"sync_info\\\":null,\\\"create_new_to_app_account\\\":null,\\\"skip_session_info\\\":null,\\\"ck_error\\\":null,\\\"ck_id\\\":null,\\\"ck_nonce\\\":null,\\\"should_save_password\\\":null,\\\"horizon_synced_username\\\":null,\\\"fb_access_token\\\":null,\\\"horizon_synced_profile_pic\\\":null,\\\"is_identity_synced\\\":false,\\\"is_msplit_reg\\\":null,\\\"user_id_of_msplit_creator\\\":null,\\\"dma_data_combination_consent_given\\\":null,\\\"xapp_accounts\\\":null,\\\"fb_device_id\\\":null,\\\"fb_machine_id\\\":null,\\\"ig_device_id\\\":null,\\\"ig_machine_id\\\":null,\\\"should_skip_nta_upsell\\\":null,\\\"big_blue_token\\\":null,\\\"skip_sync_step_nta\\\":null,\\\"caa_reg_flow_source\\\":null,\\\"ig_authorization_token\\\":null,\\\"full_sheet_flow\\\":false,\\\"crypted_user_id\\\":null,\\\"is_caa_perf_enabled\\\":false,\\\"is_preform\\\":true,\\\"ignore_suma_check\\\":false,\\\"ignore_existing_login\\\":false,\\\"ignore_existing_login_from_suma\\\":false,\\\"ignore_existing_login_after_errors\\\":false,\\\"suggested_first_name\\\":null,\\\"suggested_last_name\\\":null,\\\"suggested_full_name\\\":null,\\\"replace_id_sync_variant\\\":null,\\\"is_redirect_from_nta_replace_id_sync_variant\\\":false,\\\"frl_authorization_token\\\":null,\\\"post_form_errors\\\":null,\\\"skip_step_without_errors\\\":false,\\\"existing_account_exact_match_checked\\\":false,\\\"existing_account_fuzzy_match_checked\\\":false,\\\"email_oauth_exists\\\":false,\\\"confirmation_code_send_error\\\":null,\\\"is_too_young\\\":false,\\\"source_account_type\\\":null,\\\"whatsapp_installed_on_client\\\":false,\\\"confirmation_medium\\\":null,\\\"source_credentials_type\\\":null,\\\"source_cuid\\\":null,\\\"source_account_reg_info\\\":null,\\\"soap_creation_source\\\":null,\\\"source_account_type_to_reg_info\\\":null,\\\"registration_flow_id\\\":\\\"\\\",\\\"should_skip_youth_tos\\\":false,\\\"is_youth_regulation_flow_complete\\\":false,\\\"is_on_cold_start\\\":false,\\\"email_prefilled\\\":false,\\\"cp_confirmed_by_auto_conf\\\":false,\\\"auto_conf_info\\\":null,\\\"in_sowa_experiment\\\":false,\\\"youth_regulation_config\\\":null,\\\"conf_allow_back_nav_after_change_cp\\\":null,\\\"conf_bouncing_cliff_screen_type\\\":null,\\\"conf_show_bouncing_cliff\\\":null,\\\"eligible_to_flash_call_in_ig4a\\\":false,\\\"flash_call_permissions_status\\\":null,\\\"attestation_result\\\":null,\\\"request_data_and_challenge_nonce_string\\\":null,\\\"confirmed_cp_and_code\\\":null,\\\"notification_callback_id\\\":null,\\\"reg_suma_state\\\":0,\\\"is_msplit_neutral_choice\\\":false,\\\"msg_previous_cp\\\":null,\\\"ntp_import_source_info\\\":null,\\\"youth_consent_decision_time\\\":null,\\\"username_screen_experience\\\":\\\"control\\\",\\\"reduced_tos_test_group\\\":\\\"control\\\",\\\"should_show_spi_before_conf\\\":true,\\\"google_oauth_account\\\":null,\\\"is_reg_request_from_ig_suma\\\":false,\\\"is_igios_spc_reg\\\":false,\\\"device_emails\\\":null,\\\"is_toa_reg\\\":false,\\\"is_threads_public\\\":false,\\\"spc_import_flow\\\":false,\\\"caa_play_integrity_attestation_result\\\":null,\\\"flash_call_provider\\\":null,\\\"name_prefill_variant\\\":\\\"control\\\",\\\"spc_birthday_input\\\":false,\\\"failed_birthday_year_count\\\":null,\\\"user_presented_medium_source\\\":null,\\\"user_opted_out_of_ntp\\\":null,\\\"is_from_registration_reminder\\\":false,\\\"show_youth_reg_in_ig_spc\\\":false}\",\"flow_info\":\"{\\\"flow_name\\\":\\\"new_to_family_fb_default\\\",\\\"flow_type\\\":\\\"ntf\\\"}\",\"current_step\":5,\"INTERNAL__latency_qpl_marker_id\":36707139,\"INTERNAL__latency_qpl_instance_id\":\"29267608200213\",\"device_id\":null,\"family_device_id\":null,\"waterfall_id\":\"eb0e1792-3bfe-4e4c-a5a3-1dfd405a4839\",\"offline_experiment_group\":null,\"layered_homepage_experiment_group\":null,\"is_platform_login\":0,\"is_from_logged_in_switcher\":0,\"is_from_logged_out\":0,\"access_flow_version\":\"F2_FLOW\",\"INTERNAL_INFRA_THEME\":\"harm_f\"},\"client_input_params\":{\"machine_id\":\"\",\"encrypted_password\":\""+self.enpas+"\",\"safetynet_token\":\"\",\"safetynet_response\":\"\",\"email_oauth_token_map\":{},\"whatsapp_installed_on_client\":0,\"encrypted_msisdn_for_safetynet\":\"\",\"headers_last_infra_flow_id_safetynet\":\"\",\"fb_ig_device_id\":[],\"caa_play_integrity_attestation_result\":\"\",\"lois_settings\":{\"lois_token\":\"\",\"lara_override\":\"\"}}}"})
			cok  = ';'.join([str(x)+"="+str(y) for x,y in self.ses.cookies.get_dict().items()])
			post = self.ses.post(f'https://m.facebook.com/async/wbloks/fetch/?appid=com.bloks.www.bloks.caa.reg.password.async&type=action&__bkv={self.versioningID}', data=self.data, headers = self.headers, cookies={'cookie': cok})
			if 'com.bloks.www.bloks.caa.reg.save-credentials' in post.text:
				self.saveCredentials()
				return True
			else:
				Fail+=1
				return False
		except Exception as e:
			pass
	
	def saveCredentials(self):
		global Fail
		try:
			self.data.update({"params":"{\"server_params\":{\"waterfall_id\":\"eb0e1792-3bfe-4e4c-a5a3-1dfd405a4839\",\"is_platform_login\":0,\"is_from_logged_out\":0,\"access_flow_version\":\"F2_FLOW\",\"reg_info\":\"{\\\"first_name\\\":\\\""+self.nama_depan+"\\\",\\\"last_name\\\":\\\""+self.nama_belakang+"\\\",\\\"full_name\\\":\\\""+self.nama_depan+"\\\",\\\"contactpoint\\\":\\\""+self.nomorTlpn.replace('08', '+628')+"\\\",\\\"ar_contactpoint\\\":null,\\\"contactpoint_type\\\":\\\"phone\\\",\\\"is_using_unified_cp\\\":false,\\\"unified_cp_screen_variant\\\":null,\\\"is_cp_auto_confirmed\\\":false,\\\"is_cp_auto_confirmable\\\":false,\\\"confirmation_code\\\":null,\\\"birthday\\\":\\\""+self.tgl_lahir+"\\\",\\\"did_use_age\\\":false,\\\"gender\\\":1,\\\"use_custom_gender\\\":false,\\\"custom_gender\\\":null,\\\"encrypted_password\\\":\\\""+self.enpas+"\\\",\\\"username\\\":null,\\\"username_prefill\\\":null,\\\"fb_conf_source\\\":null,\\\"device_id\\\":null,\\\"ig4a_qe_device_id\\\":null,\\\"family_device_id\\\":null,\\\"nta_eligibility_reason\\\":null,\\\"ig_nta_test_group\\\":null,\\\"user_id\\\":null,\\\"safetynet_token\\\":null,\\\"safetynet_response\\\":null,\\\"machine_id\\\":null,\\\"profile_photo\\\":null,\\\"profile_photo_id\\\":null,\\\"profile_photo_upload_id\\\":null,\\\"avatar\\\":null,\\\"email_oauth_token_no_contact_perm\\\":null,\\\"email_oauth_token\\\":null,\\\"email_oauth_tokens\\\":[],\\\"should_skip_two_step_conf\\\":null,\\\"openid_tokens_for_testing\\\":null,\\\"encrypted_msisdn\\\":null,\\\"encrypted_msisdn_for_safetynet\\\":null,\\\"cached_headers_safetynet_info\\\":null,\\\"should_skip_headers_safetynet\\\":null,\\\"headers_last_infra_flow_id\\\":null,\\\"headers_last_infra_flow_id_safetynet\\\":null,\\\"headers_flow_id\\\":\\\"615f131a-2ab4-43f5-8052-26fa52758bfa\\\",\\\"was_headers_prefill_available\\\":false,\\\"sso_enabled\\\":null,\\\"existing_accounts\\\":null,\\\"used_ig_birthday\\\":null,\\\"sync_info\\\":null,\\\"create_new_to_app_account\\\":null,\\\"skip_session_info\\\":null,\\\"ck_error\\\":null,\\\"ck_id\\\":null,\\\"ck_nonce\\\":null,\\\"should_save_password\\\":null,\\\"horizon_synced_username\\\":null,\\\"fb_access_token\\\":null,\\\"horizon_synced_profile_pic\\\":null,\\\"is_identity_synced\\\":false,\\\"is_msplit_reg\\\":null,\\\"user_id_of_msplit_creator\\\":null,\\\"dma_data_combination_consent_given\\\":null,\\\"xapp_accounts\\\":null,\\\"fb_device_id\\\":null,\\\"fb_machine_id\\\":null,\\\"ig_device_id\\\":null,\\\"ig_machine_id\\\":null,\\\"should_skip_nta_upsell\\\":null,\\\"big_blue_token\\\":null,\\\"skip_sync_step_nta\\\":null,\\\"caa_reg_flow_source\\\":null,\\\"ig_authorization_token\\\":null,\\\"full_sheet_flow\\\":false,\\\"crypted_user_id\\\":null,\\\"is_caa_perf_enabled\\\":false,\\\"is_preform\\\":true,\\\"ignore_suma_check\\\":false,\\\"ignore_existing_login\\\":false,\\\"ignore_existing_login_from_suma\\\":false,\\\"ignore_existing_login_after_errors\\\":false,\\\"suggested_first_name\\\":null,\\\"suggested_last_name\\\":null,\\\"suggested_full_name\\\":null,\\\"replace_id_sync_variant\\\":null,\\\"is_redirect_from_nta_replace_id_sync_variant\\\":false,\\\"frl_authorization_token\\\":null,\\\"post_form_errors\\\":null,\\\"skip_step_without_errors\\\":false,\\\"existing_account_exact_match_checked\\\":false,\\\"existing_account_fuzzy_match_checked\\\":false,\\\"email_oauth_exists\\\":false,\\\"confirmation_code_send_error\\\":null,\\\"is_too_young\\\":false,\\\"source_account_type\\\":null,\\\"whatsapp_installed_on_client\\\":false,\\\"confirmation_medium\\\":null,\\\"source_credentials_type\\\":null,\\\"source_cuid\\\":null,\\\"source_account_reg_info\\\":null,\\\"soap_creation_source\\\":null,\\\"source_account_type_to_reg_info\\\":null,\\\"registration_flow_id\\\":\\\"\\\",\\\"should_skip_youth_tos\\\":false,\\\"is_youth_regulation_flow_complete\\\":false,\\\"is_on_cold_start\\\":false,\\\"email_prefilled\\\":false,\\\"cp_confirmed_by_auto_conf\\\":false,\\\"auto_conf_info\\\":null,\\\"in_sowa_experiment\\\":false,\\\"youth_regulation_config\\\":null,\\\"conf_allow_back_nav_after_change_cp\\\":null,\\\"conf_bouncing_cliff_screen_type\\\":null,\\\"conf_show_bouncing_cliff\\\":null,\\\"eligible_to_flash_call_in_ig4a\\\":false,\\\"flash_call_permissions_status\\\":null,\\\"attestation_result\\\":null,\\\"request_data_and_challenge_nonce_string\\\":null,\\\"confirmed_cp_and_code\\\":null,\\\"notification_callback_id\\\":null,\\\"reg_suma_state\\\":0,\\\"is_msplit_neutral_choice\\\":false,\\\"msg_previous_cp\\\":null,\\\"ntp_import_source_info\\\":null,\\\"youth_consent_decision_time\\\":null,\\\"username_screen_experience\\\":\\\"control\\\",\\\"reduced_tos_test_group\\\":\\\"control\\\",\\\"should_show_spi_before_conf\\\":true,\\\"google_oauth_account\\\":null,\\\"is_reg_request_from_ig_suma\\\":false,\\\"is_igios_spc_reg\\\":false,\\\"device_emails\\\":[],\\\"is_toa_reg\\\":false,\\\"is_threads_public\\\":false,\\\"spc_import_flow\\\":false,\\\"caa_play_integrity_attestation_result\\\":null,\\\"flash_call_provider\\\":null,\\\"name_prefill_variant\\\":\\\"control\\\",\\\"spc_birthday_input\\\":false,\\\"failed_birthday_year_count\\\":null,\\\"user_presented_medium_source\\\":null,\\\"user_opted_out_of_ntp\\\":null,\\\"is_from_registration_reminder\\\":false,\\\"show_youth_reg_in_ig_spc\\\":false}\",\"flow_info\":\"{\\\"flow_name\\\":\\\"new_to_family_fb_default\\\",\\\"flow_type\\\":\\\"ntf\\\"}\",\"current_step\":6,\"INTERNAL_INFRA_screen_id\":\"4ucbuy:6\"},\"client_input_params\":{\"lois_settings\":{\"lois_token\":\"\",\"lara_override\":\"\"}}}"})
			cok  = ';'.join([str(x)+"="+str(y) for x,y in self.ses.cookies.get_dict().items()])
			post = self.ses.post(f'https://m.facebook.com/async/wbloks/fetch/?appid=com.bloks.www.bloks.caa.reg.save-credentials&type=app&__bkv={self.versioningID}', data=self.data,headers = self.headers, cookies={'cookie': cok})
			if "Simpan" in post.text or "Simpan info login Anda?" in post.text:
				self.kanjut_()
				return True
			else:
				Fail+=1
				return False
		except Exception as e:
			pass
	
	def kanjut_(self):
		global Fail
		try:
			self.data.update({"params":"{\"server_params\":{\"waterfall_id\":\"eb0e1792-3bfe-4e4c-a5a3-1dfd405a4839\",\"is_platform_login\":0,\"is_from_logged_out\":0,\"access_flow_version\":\"F2_FLOW\",\"tos_type\":\"standard\",\"reg_info\":\"{\\\"first_name\\\":\\\""+self.nama_depan+"\\\",\\\"last_name\\\":\\\""+self.nama_belakang+"\\\",\\\"full_name\\\":\\\""+self.nama_depan+"\\\",\\\"contactpoint\\\":\\\""+self.nomorTlpn.replace('08', '+628')+"\\\",\\\"ar_contactpoint\\\":null,\\\"contactpoint_type\\\":\\\"phone\\\",\\\"is_using_unified_cp\\\":false,\\\"unified_cp_screen_variant\\\":null,\\\"is_cp_auto_confirmed\\\":false,\\\"is_cp_auto_confirmable\\\":false,\\\"confirmation_code\\\":null,\\\"birthday\\\":\\\""+self.tgl_lahir+"\\\",\\\"did_use_age\\\":false,\\\"gender\\\":1,\\\"use_custom_gender\\\":false,\\\"custom_gender\\\":null,\\\"encrypted_password\\\":\\\""+self.enpas+"\\\",\\\"username\\\":null,\\\"username_prefill\\\":null,\\\"fb_conf_source\\\":null,\\\"device_id\\\":null,\\\"ig4a_qe_device_id\\\":null,\\\"family_device_id\\\":null,\\\"nta_eligibility_reason\\\":null,\\\"ig_nta_test_group\\\":null,\\\"user_id\\\":null,\\\"safetynet_token\\\":null,\\\"safetynet_response\\\":null,\\\"machine_id\\\":null,\\\"profile_photo\\\":null,\\\"profile_photo_id\\\":null,\\\"profile_photo_upload_id\\\":null,\\\"avatar\\\":null,\\\"email_oauth_token_no_contact_perm\\\":null,\\\"email_oauth_token\\\":null,\\\"email_oauth_tokens\\\":[],\\\"should_skip_two_step_conf\\\":null,\\\"openid_tokens_for_testing\\\":null,\\\"encrypted_msisdn\\\":null,\\\"encrypted_msisdn_for_safetynet\\\":null,\\\"cached_headers_safetynet_info\\\":null,\\\"should_skip_headers_safetynet\\\":null,\\\"headers_last_infra_flow_id\\\":null,\\\"headers_last_infra_flow_id_safetynet\\\":null,\\\"headers_flow_id\\\":\\\"615f131a-2ab4-43f5-8052-26fa52758bfa\\\",\\\"was_headers_prefill_available\\\":false,\\\"sso_enabled\\\":null,\\\"existing_accounts\\\":null,\\\"used_ig_birthday\\\":null,\\\"sync_info\\\":null,\\\"create_new_to_app_account\\\":null,\\\"skip_session_info\\\":null,\\\"ck_error\\\":null,\\\"ck_id\\\":null,\\\"ck_nonce\\\":null,\\\"should_save_password\\\":true,\\\"horizon_synced_username\\\":null,\\\"fb_access_token\\\":null,\\\"horizon_synced_profile_pic\\\":null,\\\"is_identity_synced\\\":false,\\\"is_msplit_reg\\\":null,\\\"user_id_of_msplit_creator\\\":null,\\\"dma_data_combination_consent_given\\\":null,\\\"xapp_accounts\\\":null,\\\"fb_device_id\\\":null,\\\"fb_machine_id\\\":null,\\\"ig_device_id\\\":null,\\\"ig_machine_id\\\":null,\\\"should_skip_nta_upsell\\\":null,\\\"big_blue_token\\\":null,\\\"skip_sync_step_nta\\\":null,\\\"caa_reg_flow_source\\\":null,\\\"ig_authorization_token\\\":null,\\\"full_sheet_flow\\\":false,\\\"crypted_user_id\\\":null,\\\"is_caa_perf_enabled\\\":false,\\\"is_preform\\\":true,\\\"ignore_suma_check\\\":false,\\\"ignore_existing_login\\\":false,\\\"ignore_existing_login_from_suma\\\":false,\\\"ignore_existing_login_after_errors\\\":false,\\\"suggested_first_name\\\":null,\\\"suggested_last_name\\\":null,\\\"suggested_full_name\\\":null,\\\"replace_id_sync_variant\\\":null,\\\"is_redirect_from_nta_replace_id_sync_variant\\\":false,\\\"frl_authorization_token\\\":null,\\\"post_form_errors\\\":null,\\\"skip_step_without_errors\\\":false,\\\"existing_account_exact_match_checked\\\":false,\\\"existing_account_fuzzy_match_checked\\\":false,\\\"email_oauth_exists\\\":false,\\\"confirmation_code_send_error\\\":null,\\\"is_too_young\\\":false,\\\"source_account_type\\\":null,\\\"whatsapp_installed_on_client\\\":false,\\\"confirmation_medium\\\":null,\\\"source_credentials_type\\\":null,\\\"source_cuid\\\":null,\\\"source_account_reg_info\\\":null,\\\"soap_creation_source\\\":null,\\\"source_account_type_to_reg_info\\\":null,\\\"registration_flow_id\\\":\\\"\\\",\\\"should_skip_youth_tos\\\":false,\\\"is_youth_regulation_flow_complete\\\":false,\\\"is_on_cold_start\\\":false,\\\"email_prefilled\\\":false,\\\"cp_confirmed_by_auto_conf\\\":false,\\\"auto_conf_info\\\":null,\\\"in_sowa_experiment\\\":false,\\\"youth_regulation_config\\\":null,\\\"conf_allow_back_nav_after_change_cp\\\":null,\\\"conf_bouncing_cliff_screen_type\\\":null,\\\"conf_show_bouncing_cliff\\\":null,\\\"eligible_to_flash_call_in_ig4a\\\":false,\\\"flash_call_permissions_status\\\":null,\\\"attestation_result\\\":null,\\\"request_data_and_challenge_nonce_string\\\":null,\\\"confirmed_cp_and_code\\\":null,\\\"notification_callback_id\\\":null,\\\"reg_suma_state\\\":0,\\\"is_msplit_neutral_choice\\\":false,\\\"msg_previous_cp\\\":null,\\\"ntp_import_source_info\\\":null,\\\"youth_consent_decision_time\\\":null,\\\"username_screen_experience\\\":\\\"control\\\",\\\"reduced_tos_test_group\\\":\\\"control\\\",\\\"should_show_spi_before_conf\\\":true,\\\"google_oauth_account\\\":null,\\\"is_reg_request_from_ig_suma\\\":false,\\\"is_igios_spc_reg\\\":false,\\\"device_emails\\\":[],\\\"is_toa_reg\\\":false,\\\"is_threads_public\\\":false,\\\"spc_import_flow\\\":false,\\\"caa_play_integrity_attestation_result\\\":null,\\\"flash_call_provider\\\":null,\\\"name_prefill_variant\\\":\\\"control\\\",\\\"spc_birthday_input\\\":false,\\\"failed_birthday_year_count\\\":null,\\\"user_presented_medium_source\\\":null,\\\"user_opted_out_of_ntp\\\":null,\\\"is_from_registration_reminder\\\":false,\\\"show_youth_reg_in_ig_spc\\\":false}\",\"flow_info\":\"{\\\"flow_name\\\":\\\"new_to_family_fb_default\\\",\\\"flow_type\\\":\\\"ntf\\\"}\",\"current_step\":8,\"INTERNAL_INFRA_screen_id\":\"CAA_REG_TERMS_OF_SERVICE\"},\"client_input_params\":{\"lois_settings\":{\"lois_token\":\"\",\"lara_override\":\"\"}}}"})
			cok  = ';'.join([str(x)+"="+str(y) for x,y in self.ses.cookies.get_dict().items()])
			post = self.ses.post(f'https://m.facebook.com/async/wbloks/fetch/?appid=com.bloks.www.bloks.caa.reg.tos&type=app&__bkv={self.versioningID}', data=self.data, headers = self.headers, cookies={'cookie': cok})
			if "Setujui ketentuan dan kebijakan Facebook" in post.text and "Saya setuju" in post.text:
				self.final_create()
				return True
			else:
				Fail+=1
				return False
		except Exception as e:
			pass
	
	def final_create(self):
		global Ok, Cp, Fail
		try:
			self.data.update({"params":"{\"server_params\":{\"event_request_id\":\"299e21d2-6735-4188-af7e-3110775cc653\",\"app_id\":0,\"reg_info\":\"{\\\"first_name\\\":\\\""+self.nama_depan+"\\\",\\\"last_name\\\":\\\""+self.nama_belakang+"\\\",\\\"full_name\\\":\\\""+self.nama_depan+"\\\",\\\"contactpoint\\\":\\\""+self.nomorTlpn.replace('08', '+628')+"\\\",\\\"ar_contactpoint\\\":null,\\\"contactpoint_type\\\":\\\"phone\\\",\\\"is_using_unified_cp\\\":false,\\\"unified_cp_screen_variant\\\":null,\\\"is_cp_auto_confirmed\\\":false,\\\"is_cp_auto_confirmable\\\":false,\\\"confirmation_code\\\":null,\\\"birthday\\\":\\\""+self.tgl_lahir+"\\\",\\\"did_use_age\\\":false,\\\"gender\\\":1,\\\"use_custom_gender\\\":false,\\\"custom_gender\\\":null,\\\"encrypted_password\\\":\\\""+self.enpas+"\\\",\\\"username\\\":null,\\\"username_prefill\\\":null,\\\"fb_conf_source\\\":null,\\\"device_id\\\":null,\\\"ig4a_qe_device_id\\\":null,\\\"family_device_id\\\":null,\\\"nta_eligibility_reason\\\":null,\\\"ig_nta_test_group\\\":null,\\\"user_id\\\":null,\\\"safetynet_token\\\":null,\\\"safetynet_response\\\":null,\\\"machine_id\\\":null,\\\"profile_photo\\\":null,\\\"profile_photo_id\\\":null,\\\"profile_photo_upload_id\\\":null,\\\"avatar\\\":null,\\\"email_oauth_token_no_contact_perm\\\":null,\\\"email_oauth_token\\\":null,\\\"email_oauth_tokens\\\":[],\\\"should_skip_two_step_conf\\\":null,\\\"openid_tokens_for_testing\\\":null,\\\"encrypted_msisdn\\\":null,\\\"encrypted_msisdn_for_safetynet\\\":null,\\\"cached_headers_safetynet_info\\\":null,\\\"should_skip_headers_safetynet\\\":null,\\\"headers_last_infra_flow_id\\\":null,\\\"headers_last_infra_flow_id_safetynet\\\":null,\\\"headers_flow_id\\\":\\\"615f131a-2ab4-43f5-8052-26fa52758bfa\\\",\\\"was_headers_prefill_available\\\":false,\\\"sso_enabled\\\":null,\\\"existing_accounts\\\":null,\\\"used_ig_birthday\\\":null,\\\"sync_info\\\":null,\\\"create_new_to_app_account\\\":null,\\\"skip_session_info\\\":null,\\\"ck_error\\\":null,\\\"ck_id\\\":null,\\\"ck_nonce\\\":null,\\\"should_save_password\\\":true,\\\"horizon_synced_username\\\":null,\\\"fb_access_token\\\":null,\\\"horizon_synced_profile_pic\\\":null,\\\"is_identity_synced\\\":false,\\\"is_msplit_reg\\\":null,\\\"user_id_of_msplit_creator\\\":null,\\\"dma_data_combination_consent_given\\\":null,\\\"xapp_accounts\\\":null,\\\"fb_device_id\\\":null,\\\"fb_machine_id\\\":null,\\\"ig_device_id\\\":null,\\\"ig_machine_id\\\":null,\\\"should_skip_nta_upsell\\\":null,\\\"big_blue_token\\\":null,\\\"skip_sync_step_nta\\\":null,\\\"caa_reg_flow_source\\\":null,\\\"ig_authorization_token\\\":null,\\\"full_sheet_flow\\\":false,\\\"crypted_user_id\\\":null,\\\"is_caa_perf_enabled\\\":false,\\\"is_preform\\\":true,\\\"ignore_suma_check\\\":false,\\\"ignore_existing_login\\\":false,\\\"ignore_existing_login_from_suma\\\":false,\\\"ignore_existing_login_after_errors\\\":false,\\\"suggested_first_name\\\":null,\\\"suggested_last_name\\\":null,\\\"suggested_full_name\\\":null,\\\"replace_id_sync_variant\\\":null,\\\"is_redirect_from_nta_replace_id_sync_variant\\\":false,\\\"frl_authorization_token\\\":null,\\\"post_form_errors\\\":null,\\\"skip_step_without_errors\\\":false,\\\"existing_account_exact_match_checked\\\":false,\\\"existing_account_fuzzy_match_checked\\\":false,\\\"email_oauth_exists\\\":false,\\\"confirmation_code_send_error\\\":null,\\\"is_too_young\\\":false,\\\"source_account_type\\\":null,\\\"whatsapp_installed_on_client\\\":false,\\\"confirmation_medium\\\":null,\\\"source_credentials_type\\\":null,\\\"source_cuid\\\":null,\\\"source_account_reg_info\\\":null,\\\"soap_creation_source\\\":null,\\\"source_account_type_to_reg_info\\\":null,\\\"registration_flow_id\\\":\\\"\\\",\\\"should_skip_youth_tos\\\":false,\\\"is_youth_regulation_flow_complete\\\":false,\\\"is_on_cold_start\\\":false,\\\"email_prefilled\\\":false,\\\"cp_confirmed_by_auto_conf\\\":false,\\\"auto_conf_info\\\":null,\\\"in_sowa_experiment\\\":false,\\\"youth_regulation_config\\\":null,\\\"conf_allow_back_nav_after_change_cp\\\":null,\\\"conf_bouncing_cliff_screen_type\\\":null,\\\"conf_show_bouncing_cliff\\\":null,\\\"eligible_to_flash_call_in_ig4a\\\":false,\\\"flash_call_permissions_status\\\":null,\\\"attestation_result\\\":null,\\\"request_data_and_challenge_nonce_string\\\":null,\\\"confirmed_cp_and_code\\\":null,\\\"notification_callback_id\\\":null,\\\"reg_suma_state\\\":0,\\\"is_msplit_neutral_choice\\\":false,\\\"msg_previous_cp\\\":null,\\\"ntp_import_source_info\\\":null,\\\"youth_consent_decision_time\\\":null,\\\"username_screen_experience\\\":\\\"control\\\",\\\"reduced_tos_test_group\\\":\\\"control\\\",\\\"should_show_spi_before_conf\\\":true,\\\"google_oauth_account\\\":null,\\\"is_reg_request_from_ig_suma\\\":false,\\\"is_igios_spc_reg\\\":false,\\\"device_emails\\\":[],\\\"is_toa_reg\\\":false,\\\"is_threads_public\\\":false,\\\"spc_import_flow\\\":false,\\\"caa_play_integrity_attestation_result\\\":null,\\\"flash_call_provider\\\":null,\\\"name_prefill_variant\\\":\\\"control\\\",\\\"spc_birthday_input\\\":false,\\\"failed_birthday_year_count\\\":null,\\\"user_presented_medium_source\\\":null,\\\"user_opted_out_of_ntp\\\":null,\\\"is_from_registration_reminder\\\":false,\\\"show_youth_reg_in_ig_spc\\\":false}\",\"flow_info\":\"{\\\"flow_name\\\":\\\"new_to_family_fb_default\\\",\\\"flow_type\\\":\\\"ntf\\\"}\",\"current_step\":8,\"INTERNAL__latency_qpl_marker_id\":36707139,\"INTERNAL__latency_qpl_instance_id\":\"29290046600041\",\"device_id\":null,\"family_device_id\":null,\"waterfall_id\":\"eb0e1792-3bfe-4e4c-a5a3-1dfd405a4839\",\"offline_experiment_group\":null,\"layered_homepage_experiment_group\":null,\"is_platform_login\":0,\"is_from_logged_in_switcher\":0,\"is_from_logged_out\":0,\"access_flow_version\":\"F2_FLOW\",\"INTERNAL_INFRA_THEME\":\"harm_f\"},\"client_input_params\":{\"device_id\":\"\",\"waterfall_id\":\"eb0e1792-3bfe-4e4c-a5a3-1dfd405a4839\",\"machine_id\":\"\",\"ck_error\":\"\",\"ck_id\":\"\",\"ck_nonce\":\"\",\"should_ignore_existing_login\":0,\"encrypted_msisdn\":\"\",\"headers_last_infra_flow_id\":\"\",\"reached_from_tos_screen\":1,\"no_contact_perm_email_oauth_token\":\"\",\"failed_birthday_year_count\":\"{}\",\"lois_settings\":{\"lois_token\":\"\",\"lara_override\":\"\"}}}"})
			cok  = ';'.join([str(x)+"="+str(y) for x,y in self.ses.cookies.get_dict().items()])
			post = self.ses.post(f'https://m.facebook.com/async/wbloks/fetch/?appid=com.bloks.www.bloks.caa.reg.create.account.async&type=action&__bkv={self.versioningID}', data=self.data, headers = self.headers, cookies={'cookie': cok})
			if "session_key" in post.text.replace('\\', ''):
				self.confirm_code_phone()
				return True
			elif "Nama pengguna atau kata sandi tidak valid" in post.text.replace('\\', ''):
				Cp+=1
				return False
			else:
				Fail+=1
				return False
		except Exception as e:
			pass
	
	def confirm_code_phone(self):
		global Fail
		try:
			console.print(f" [bold green]#[bold white] email: [bold green]{self.email}[bold white]{' '*20}", end='\r')
			time.sleep(1.5)
			cookie  = ';'.join([str(x)+"="+str(y) for x,y in self.ses.cookies.get_dict().items()])
			uid = re.search(r'c_user=(\d+)', cookie).group(1)
			params = {'reg_info': "{\"contactpoint\":\" "+self.nomorTlpn.replace('08', '+628')+"\",\"contactpoint_type\":\"phone\",\"is_cp_auto_confirmed\":false,\"fb_conf_source\":null,\"confirmation_medium\":null,\"registration_flow_id\":\"\"}",'flow_info': "{\"flow_name\":\"new_to_family_fb_default\",\"flow_type\":\"ntf\"}",'current_step': "10"}
			req = self.ses.get("https://m.facebook.com/caa/reg/confirmation/", params=params, cookies={'cookie': cookie}, headers = self.config.defaultHeadersGet('Get')).text
			data = {
				"__aaid": "0",
				"__user": uid,
				"__a": "1",
				"__req": "x",
				"__hs": re.search('"haste_session":"(.*?)"', str(req)).group(1),
				"dpr": "1",
				"__ccg": "GOOD",
				"__rev": re.search('"__spin_r":(.*?)', str(req)).group(1),
				"__s": ":",
				"__hsi": "",
				"__dyn": "",
				"__csr": "",
				"fb_dtsg": re.search('{"dtsg":{"token":"(.*?)"', str(req)).group(1),
				"jazoest": re.search('"jazoest", "(.*?)"', str(req)).group(1),
				 "lsd": re.search('"LSD",\[\],{"token":"(.*?)"}', str(req)).group(1)
			}
			data.update({"params":"{\"server_params\":{\"waterfall_id\":\"a763fafb-432c-492a-9556-d768833ecc63\",\"is_platform_login\":0,\"is_from_logged_out\":0,\"access_flow_version\":\"F2_FLOW\",\"trigger\":\"upon_failed_conf_attempts\",\"reg_info\":\"{\\\"first_name\\\":\\\""+self.nama_depan+"\\\",\\\"last_name\\\":\\\""+self.nama_belakang+"\\\",\\\"full_name\\\":\\\""+self.nama_depan+"\\\",\\\"contactpoint\\\":\\\""+self.nomorTlpn.replace('08', '+628')+"\\\",\\\"ar_contactpoint\\\":null,\\\"contactpoint_type\\\":\\\"phone\\\",\\\"is_using_unified_cp\\\":false,\\\"unified_cp_screen_variant\\\":null,\\\"is_cp_auto_confirmed\\\":false,\\\"is_cp_auto_confirmable\\\":false,\\\"confirmation_code\\\":null,\\\"birthday\\\":\\\""+self.tgl_lahir+"\\\",\\\"did_use_age\\\":false,\\\"gender\\\":1,\\\"use_custom_gender\\\":false,\\\"custom_gender\\\":null,\\\"encrypted_password\\\":\\\""+self.enpas+"\\\",\\\"username\\\":null,\\\"username_prefill\\\":null,\\\"fb_conf_source\\\":null,\\\"device_id\\\":null,\\\"ig4a_qe_device_id\\\":null,\\\"family_device_id\\\":null,\\\"nta_eligibility_reason\\\":null,\\\"ig_nta_test_group\\\":null,\\\"user_id\\\":null,\\\"safetynet_token\\\":null,\\\"safetynet_response\\\":null,\\\"machine_id\\\":\\\"\\\",\\\"profile_photo\\\":null,\\\"profile_photo_id\\\":null,\\\"profile_photo_upload_id\\\":null,\\\"avatar\\\":null,\\\"email_oauth_token_no_contact_perm\\\":null,\\\"email_oauth_token\\\":null,\\\"email_oauth_tokens\\\":[],\\\"should_skip_two_step_conf\\\":null,\\\"openid_tokens_for_testing\\\":null,\\\"encrypted_msisdn\\\":null,\\\"encrypted_msisdn_for_safetynet\\\":null,\\\"cached_headers_safetynet_info\\\":null,\\\"should_skip_headers_safetynet\\\":null,\\\"headers_last_infra_flow_id\\\":null,\\\"headers_last_infra_flow_id_safetynet\\\":null,\\\"headers_flow_id\\\":\\\"1a1dcad7-55be-4e96-b5ec-dccad18f625a\\\",\\\"was_headers_prefill_available\\\":false,\\\"sso_enabled\\\":null,\\\"existing_accounts\\\":null,\\\"used_ig_birthday\\\":null,\\\"sync_info\\\":null,\\\"create_new_to_app_account\\\":null,\\\"skip_session_info\\\":null,\\\"ck_error\\\":null,\\\"ck_id\\\":null,\\\"ck_nonce\\\":null,\\\"should_save_password\\\":true,\\\"horizon_synced_username\\\":null,\\\"fb_access_token\\\":null,\\\"horizon_synced_profile_pic\\\":null,\\\"is_identity_synced\\\":false,\\\"is_msplit_reg\\\":null,\\\"user_id_of_msplit_creator\\\":null,\\\"dma_data_combination_consent_given\\\":null,\\\"xapp_accounts\\\":null,\\\"fb_device_id\\\":null,\\\"fb_machine_id\\\":null,\\\"ig_device_id\\\":null,\\\"ig_machine_id\\\":null,\\\"should_skip_nta_upsell\\\":null,\\\"big_blue_token\\\":null,\\\"skip_sync_step_nta\\\":null,\\\"caa_reg_flow_source\\\":null,\\\"ig_authorization_token\\\":null,\\\"full_sheet_flow\\\":false,\\\"crypted_user_id\\\":null,\\\"is_caa_perf_enabled\\\":false,\\\"is_preform\\\":false,\\\"ignore_suma_check\\\":false,\\\"ignore_existing_login\\\":false,\\\"ignore_existing_login_from_suma\\\":false,\\\"ignore_existing_login_after_errors\\\":false,\\\"suggested_first_name\\\":null,\\\"suggested_last_name\\\":null,\\\"suggested_full_name\\\":null,\\\"replace_id_sync_variant\\\":null,\\\"is_redirect_from_nta_replace_id_sync_variant\\\":false,\\\"frl_authorization_token\\\":null,\\\"post_form_errors\\\":null,\\\"skip_step_without_errors\\\":false,\\\"existing_account_exact_match_checked\\\":false,\\\"existing_account_fuzzy_match_checked\\\":false,\\\"email_oauth_exists\\\":false,\\\"confirmation_code_send_error\\\":null,\\\"is_too_young\\\":false,\\\"source_account_type\\\":null,\\\"whatsapp_installed_on_client\\\":false,\\\"confirmation_medium\\\":\\\"sms\\\",\\\"source_credentials_type\\\":null,\\\"source_cuid\\\":null,\\\"source_account_reg_info\\\":null,\\\"soap_creation_source\\\":null,\\\"source_account_type_to_reg_info\\\":null,\\\"registration_flow_id\\\":\\\"\\\",\\\"should_skip_youth_tos\\\":false,\\\"is_youth_regulation_flow_complete\\\":false,\\\"is_on_cold_start\\\":false,\\\"email_prefilled\\\":false,\\\"cp_confirmed_by_auto_conf\\\":false,\\\"auto_conf_info\\\":null,\\\"in_sowa_experiment\\\":false,\\\"youth_regulation_config\\\":null,\\\"conf_allow_back_nav_after_change_cp\\\":null,\\\"conf_bouncing_cliff_screen_type\\\":null,\\\"conf_show_bouncing_cliff\\\":null,\\\"eligible_to_flash_call_in_ig4a\\\":false,\\\"flash_call_permissions_status\\\":null,\\\"attestation_result\\\":null,\\\"request_data_and_challenge_nonce_string\\\":null,\\\"confirmed_cp_and_code\\\":null,\\\"notification_callback_id\\\":null,\\\"reg_suma_state\\\":0,\\\"is_msplit_neutral_choice\\\":false,\\\"msg_previous_cp\\\":null,\\\"ntp_import_source_info\\\":null,\\\"youth_consent_decision_time\\\":null,\\\"username_screen_experience\\\":\\\"control\\\",\\\"reduced_tos_test_group\\\":\\\"control\\\",\\\"should_show_spi_before_conf\\\":true,\\\"google_oauth_account\\\":null,\\\"is_reg_request_from_ig_suma\\\":false,\\\"is_igios_spc_reg\\\":false,\\\"device_emails\\\":[],\\\"is_toa_reg\\\":false,\\\"is_threads_public\\\":false,\\\"spc_import_flow\\\":false,\\\"caa_play_integrity_attestation_result\\\":null,\\\"flash_call_provider\\\":null,\\\"name_prefill_variant\\\":\\\"control\\\",\\\"spc_birthday_input\\\":false,\\\"failed_birthday_year_count\\\":\\\"{}\\\",\\\"user_presented_medium_source\\\":null,\\\"user_opted_out_of_ntp\\\":null,\\\"is_from_registration_reminder\\\":false,\\\"show_youth_reg_in_ig_spc\\\":false}\",\"flow_info\":\"{\\\"flow_name\\\":\\\"new_to_family_fb_default\\\",\\\"flow_type\\\":\\\"ntf\\\"}\",\"current_step\":10,\"INTERNAL_INFRA_screen_id\":\"5up49a:214\"},\"client_input_params\":{\"lois_settings\":{\"lois_token\":\"\",\"lara_override\":\"\"}}}"})
			cok  = ';'.join([str(x)+"="+str(y) for x,y in self.ses.cookies.get_dict().items()])
			resp = self.ses.post(f'https://m.facebook.com/async/wbloks/fetch/?appid=com.bloks.www.bloks.caa.reg.confirmation.fb.bottomsheet&type=app&__bkv={self.versioningID}', data=data, headers = self.headers, cookies={'cookie': cok})
			if "com.bloks.www.bloks.caa.reg.confirmation.change.email" in resp.text:
				data.update({"params":"{\"server_params\":{\"event_request_id\":\"8e2332bd-01ee-4afd-a56f-d8565897d3e8\",\"cp_funnel\":1,\"cp_source\":1,\"text_input_id\":\"35541197300062\",\"reg_info\":\"{\\\"first_name\\\":\\\""+self.nama_depan+"\\\",\\\"last_name\\\":\\\""+self.nama_belakang+"\\\",\\\"full_name\\\":\\\""+self.nama_depan+"\\\",\\\"contactpoint\\\":\\\""+self.nomorTlpn.replace('08', '+628')+"\\\",\\\"ar_contactpoint\\\":null,\\\"contactpoint_type\\\":\\\"phone\\\",\\\"is_using_unified_cp\\\":false,\\\"unified_cp_screen_variant\\\":null,\\\"is_cp_auto_confirmed\\\":false,\\\"is_cp_auto_confirmable\\\":false,\\\"confirmation_code\\\":null,\\\"birthday\\\":\\\""+self.tgl_lahir+"\\\",\\\"did_use_age\\\":false,\\\"gender\\\":1,\\\"use_custom_gender\\\":false,\\\"custom_gender\\\":null,\\\"encrypted_password\\\":\\\""+self.enpas+"\\\",\\\"username\\\":null,\\\"username_prefill\\\":null,\\\"fb_conf_source\\\":null,\\\"device_id\\\":null,\\\"ig4a_qe_device_id\\\":null,\\\"family_device_id\\\":null,\\\"nta_eligibility_reason\\\":null,\\\"ig_nta_test_group\\\":null,\\\"user_id\\\":null,\\\"safetynet_token\\\":null,\\\"safetynet_response\\\":null,\\\"machine_id\\\":\\\"\\\",\\\"profile_photo\\\":null,\\\"profile_photo_id\\\":null,\\\"profile_photo_upload_id\\\":null,\\\"avatar\\\":null,\\\"email_oauth_token_no_contact_perm\\\":null,\\\"email_oauth_token\\\":null,\\\"email_oauth_tokens\\\":[],\\\"should_skip_two_step_conf\\\":null,\\\"openid_tokens_for_testing\\\":null,\\\"encrypted_msisdn\\\":null,\\\"encrypted_msisdn_for_safetynet\\\":null,\\\"cached_headers_safetynet_info\\\":null,\\\"should_skip_headers_safetynet\\\":null,\\\"headers_last_infra_flow_id\\\":null,\\\"headers_last_infra_flow_id_safetynet\\\":null,\\\"headers_flow_id\\\":\\\"1a1dcad7-55be-4e96-b5ec-dccad18f625a\\\",\\\"was_headers_prefill_available\\\":false,\\\"sso_enabled\\\":null,\\\"existing_accounts\\\":null,\\\"used_ig_birthday\\\":null,\\\"sync_info\\\":null,\\\"create_new_to_app_account\\\":null,\\\"skip_session_info\\\":null,\\\"ck_error\\\":null,\\\"ck_id\\\":null,\\\"ck_nonce\\\":null,\\\"should_save_password\\\":true,\\\"horizon_synced_username\\\":null,\\\"fb_access_token\\\":null,\\\"horizon_synced_profile_pic\\\":null,\\\"is_identity_synced\\\":false,\\\"is_msplit_reg\\\":null,\\\"user_id_of_msplit_creator\\\":null,\\\"dma_data_combination_consent_given\\\":null,\\\"xapp_accounts\\\":null,\\\"fb_device_id\\\":null,\\\"fb_machine_id\\\":null,\\\"ig_device_id\\\":null,\\\"ig_machine_id\\\":null,\\\"should_skip_nta_upsell\\\":null,\\\"big_blue_token\\\":null,\\\"skip_sync_step_nta\\\":null,\\\"caa_reg_flow_source\\\":null,\\\"ig_authorization_token\\\":null,\\\"full_sheet_flow\\\":false,\\\"crypted_user_id\\\":null,\\\"is_caa_perf_enabled\\\":false,\\\"is_preform\\\":false,\\\"ignore_suma_check\\\":false,\\\"ignore_existing_login\\\":false,\\\"ignore_existing_login_from_suma\\\":false,\\\"ignore_existing_login_after_errors\\\":false,\\\"suggested_first_name\\\":null,\\\"suggested_last_name\\\":null,\\\"suggested_full_name\\\":null,\\\"replace_id_sync_variant\\\":null,\\\"is_redirect_from_nta_replace_id_sync_variant\\\":false,\\\"frl_authorization_token\\\":null,\\\"post_form_errors\\\":null,\\\"skip_step_without_errors\\\":false,\\\"existing_account_exact_match_checked\\\":false,\\\"existing_account_fuzzy_match_checked\\\":false,\\\"email_oauth_exists\\\":false,\\\"confirmation_code_send_error\\\":null,\\\"is_too_young\\\":false,\\\"source_account_type\\\":null,\\\"whatsapp_installed_on_client\\\":false,\\\"confirmation_medium\\\":\\\"sms\\\",\\\"source_credentials_type\\\":null,\\\"source_cuid\\\":null,\\\"source_account_reg_info\\\":null,\\\"soap_creation_source\\\":null,\\\"source_account_type_to_reg_info\\\":null,\\\"registration_flow_id\\\":\\\"\\\",\\\"should_skip_youth_tos\\\":false,\\\"is_youth_regulation_flow_complete\\\":false,\\\"is_on_cold_start\\\":false,\\\"email_prefilled\\\":false,\\\"cp_confirmed_by_auto_conf\\\":false,\\\"auto_conf_info\\\":null,\\\"in_sowa_experiment\\\":false,\\\"youth_regulation_config\\\":null,\\\"conf_allow_back_nav_after_change_cp\\\":true,\\\"conf_bouncing_cliff_screen_type\\\":null,\\\"conf_show_bouncing_cliff\\\":null,\\\"eligible_to_flash_call_in_ig4a\\\":false,\\\"flash_call_permissions_status\\\":null,\\\"attestation_result\\\":null,\\\"request_data_and_challenge_nonce_string\\\":null,\\\"confirmed_cp_and_code\\\":null,\\\"notification_callback_id\\\":null,\\\"reg_suma_state\\\":0,\\\"is_msplit_neutral_choice\\\":false,\\\"msg_previous_cp\\\":null,\\\"ntp_import_source_info\\\":null,\\\"youth_consent_decision_time\\\":null,\\\"username_screen_experience\\\":\\\"control\\\",\\\"reduced_tos_test_group\\\":\\\"control\\\",\\\"should_show_spi_before_conf\\\":true,\\\"google_oauth_account\\\":null,\\\"is_reg_request_from_ig_suma\\\":false,\\\"is_igios_spc_reg\\\":false,\\\"device_emails\\\":[],\\\"is_toa_reg\\\":false,\\\"is_threads_public\\\":false,\\\"spc_import_flow\\\":false,\\\"caa_play_integrity_attestation_result\\\":null,\\\"flash_call_provider\\\":null,\\\"name_prefill_variant\\\":\\\"control\\\",\\\"spc_birthday_input\\\":false,\\\"failed_birthday_year_count\\\":\\\"{}\\\",\\\"user_presented_medium_source\\\":null,\\\"user_opted_out_of_ntp\\\":null,\\\"is_from_registration_reminder\\\":false,\\\"show_youth_reg_in_ig_spc\\\":false}\",\"flow_info\":\"{\\\"flow_name\\\":\\\"new_to_family_fb_default\\\",\\\"flow_type\\\":\\\"ntf\\\"}\",\"current_step\":10,\"INTERNAL__latency_qpl_marker_id\":36707139,\"INTERNAL__latency_qpl_instance_id\":\"35541197300093\",\"device_id\":null,\"family_device_id\":null,\"waterfall_id\":\"a763fafb-432c-492a-9556-d768833ecc63\",\"offline_experiment_group\":null,\"layered_homepage_experiment_group\":null,\"is_platform_login\":0,\"is_from_logged_in_switcher\":0,\"is_from_logged_out\":0,\"access_flow_version\":\"F2_FLOW\",\"INTERNAL_INFRA_THEME\":\"harm_f\"},\"client_input_params\":{\"device_id\":\"\",\"family_device_id\":\"\",\"email\":\""+self.email+"\",\"email_prefilled\":0,\"accounts_list\":[],\"fb_ig_device_id\":[],\"confirmed_cp_and_code\":{},\"is_from_device_emails\":0,\"msg_previous_cp\":\"\",\"switch_cp_first_time_loading\":1,\"switch_cp_have_seen_suma\":0,\"lois_settings\":{\"lois_token\":\"\",\"lara_override\":\"\"}}}"})
				cok  = ';'.join([str(x)+"="+str(y) for x,y in self.ses.cookies.get_dict().items()])
				respn = self.ses.post(f'https://m.facebook.com/async/wbloks/fetch/?appid=com.bloks.www.bloks.caa.reg.async.contactpoint_email.async&type=action&__bkv={self.versioningID}', data=data, headers = self.headers, cookies={'cookie': cok})
				if "com.bloks.www.bloks.caa.reg.confirmation" in respn.text:
					Config().kode(20)
					self.code = self.get_code_temp_mail(self.email)
					self.confirm_code()
			else:
				Fail+=1
				return False
		except Exception as e:
			print(e)
			
	def confirm_code(self):
		global Ok,Cp,Fail
		try:
			print(f" {H}#{P} verification code > {self.code}{' ' *20}", end = '\r')
			time.sleep(1.5)
			cookie  = ';'.join([str(x)+"="+str(y) for x,y in self.ses.cookies.get_dict().items()])
			params = {'reg_info': "{\"contactpoint\":\""+self.email+"\",\"contactpoint_type\":\"email\",\"is_cp_auto_confirmed\":false,\"fb_conf_source\":null,\"confirmation_medium\":null,\"registration_flow_id\":\"53335e1d-b812-4d0d-b4b6-9d27dcd898ec\"}",'flow_info': "{\"flow_name\":\"new_to_family_fb_default\",\"flow_type\":\"ntf\"}",'current_step': "10"}
			req = self.ses.get("https://m.facebook.com/caa/reg/confirmation/", params=params, cookies={'cookie': cookie}, headers = self.config.defaultHeadersGet('Get')).text
			uid = re.search(r'c_user=(\d+)', cookie).group(1)
			data = {
				"__aaid": "0",
				"__user": uid,
				"__a": "1",
				"__req": "x",
				"__hs": re.search('"haste_session":"(.*?)"', str(req)).group(1),
				"dpr": "1",
				"__ccg": "GOOD",
				"__rev": re.search('"__spin_r":(.*?)', str(req)).group(1),
				"__s": ":",
				"__hsi": "",
				"__dyn": "",
				"__csr": "",
				"fb_dtsg": re.search('{"dtsg":{"token":"(.*?)"', str(req)).group(1),
				"jazoest": re.search('"jazoest", "(.*?)"', str(req)).group(1),
				 "lsd": re.search('"LSD",\[\],{"token":"(.*?)"}', str(req)).group(1),
				"params":"{\"server_params\":{\"event_request_id\":\"a5fdd8c0-2505-4e3b-9747-6956ba214149\",\"text_input_id\":\"35563411300047\",\"sms_retriever_started_prior_step\":0,\"wa_timer_id\":\"wa_retriever\",\"reg_info\":\"{\\\"first_name\\\":\\\""+self.nama_depan+"\\\",\\\"last_name\\\":\\\""+self.nama_belakang+"\\\",\\\"full_name\\\":\\\""+self.nama_depan+"\\\",\\\"contactpoint\\\":\\\""+self.email+"\\\",\\\"ar_contactpoint\\\":null,\\\"contactpoint_type\\\":\\\"email\\\",\\\"is_using_unified_cp\\\":false,\\\"unified_cp_screen_variant\\\":null,\\\"is_cp_auto_confirmed\\\":false,\\\"is_cp_auto_confirmable\\\":false,\\\"confirmation_code\\\":null,\\\"birthday\\\":\\\""+self.tgl_lahir+"\\\",\\\"did_use_age\\\":false,\\\"gender\\\":1,\\\"use_custom_gender\\\":false,\\\"custom_gender\\\":null,\\\"encrypted_password\\\":\\\""+self.enpas+"\\\",\\\"username\\\":null,\\\"username_prefill\\\":null,\\\"fb_conf_source\\\":null,\\\"device_id\\\":null,\\\"ig4a_qe_device_id\\\":null,\\\"family_device_id\\\":null,\\\"nta_eligibility_reason\\\":null,\\\"ig_nta_test_group\\\":null,\\\"user_id\\\":null,\\\"safetynet_token\\\":null,\\\"safetynet_response\\\":null,\\\"machine_id\\\":\\\"\\\",\\\"profile_photo\\\":null,\\\"profile_photo_id\\\":null,\\\"profile_photo_upload_id\\\":null,\\\"avatar\\\":null,\\\"email_oauth_token_no_contact_perm\\\":null,\\\"email_oauth_token\\\":null,\\\"email_oauth_tokens\\\":[],\\\"should_skip_two_step_conf\\\":null,\\\"openid_tokens_for_testing\\\":null,\\\"encrypted_msisdn\\\":null,\\\"encrypted_msisdn_for_safetynet\\\":null,\\\"cached_headers_safetynet_info\\\":null,\\\"should_skip_headers_safetynet\\\":null,\\\"headers_last_infra_flow_id\\\":null,\\\"headers_last_infra_flow_id_safetynet\\\":null,\\\"headers_flow_id\\\":\\\"1a1dcad7-55be-4e96-b5ec-dccad18f625a\\\",\\\"was_headers_prefill_available\\\":false,\\\"sso_enabled\\\":null,\\\"existing_accounts\\\":null,\\\"used_ig_birthday\\\":null,\\\"sync_info\\\":null,\\\"create_new_to_app_account\\\":null,\\\"skip_session_info\\\":null,\\\"ck_error\\\":null,\\\"ck_id\\\":null,\\\"ck_nonce\\\":null,\\\"should_save_password\\\":true,\\\"horizon_synced_username\\\":null,\\\"fb_access_token\\\":null,\\\"horizon_synced_profile_pic\\\":null,\\\"is_identity_synced\\\":false,\\\"is_msplit_reg\\\":null,\\\"user_id_of_msplit_creator\\\":null,\\\"dma_data_combination_consent_given\\\":null,\\\"xapp_accounts\\\":null,\\\"fb_device_id\\\":null,\\\"fb_machine_id\\\":null,\\\"ig_device_id\\\":null,\\\"ig_machine_id\\\":null,\\\"should_skip_nta_upsell\\\":null,\\\"big_blue_token\\\":null,\\\"skip_sync_step_nta\\\":null,\\\"caa_reg_flow_source\\\":null,\\\"ig_authorization_token\\\":null,\\\"full_sheet_flow\\\":false,\\\"crypted_user_id\\\":null,\\\"is_caa_perf_enabled\\\":false,\\\"is_preform\\\":false,\\\"ignore_suma_check\\\":false,\\\"ignore_existing_login\\\":false,\\\"ignore_existing_login_from_suma\\\":false,\\\"ignore_existing_login_after_errors\\\":false,\\\"suggested_first_name\\\":null,\\\"suggested_last_name\\\":null,\\\"suggested_full_name\\\":null,\\\"replace_id_sync_variant\\\":null,\\\"is_redirect_from_nta_replace_id_sync_variant\\\":false,\\\"frl_authorization_token\\\":null,\\\"post_form_errors\\\":null,\\\"skip_step_without_errors\\\":false,\\\"existing_account_exact_match_checked\\\":false,\\\"existing_account_fuzzy_match_checked\\\":false,\\\"email_oauth_exists\\\":false,\\\"confirmation_code_send_error\\\":null,\\\"is_too_young\\\":false,\\\"source_account_type\\\":null,\\\"whatsapp_installed_on_client\\\":false,\\\"confirmation_medium\\\":null,\\\"source_credentials_type\\\":null,\\\"source_cuid\\\":null,\\\"source_account_reg_info\\\":null,\\\"soap_creation_source\\\":null,\\\"source_account_type_to_reg_info\\\":null,\\\"registration_flow_id\\\":\\\"\\\",\\\"should_skip_youth_tos\\\":false,\\\"is_youth_regulation_flow_complete\\\":false,\\\"is_on_cold_start\\\":false,\\\"email_prefilled\\\":false,\\\"cp_confirmed_by_auto_conf\\\":false,\\\"auto_conf_info\\\":null,\\\"in_sowa_experiment\\\":false,\\\"youth_regulation_config\\\":null,\\\"conf_allow_back_nav_after_change_cp\\\":true,\\\"conf_bouncing_cliff_screen_type\\\":null,\\\"conf_show_bouncing_cliff\\\":null,\\\"eligible_to_flash_call_in_ig4a\\\":false,\\\"flash_call_permissions_status\\\":null,\\\"attestation_result\\\":null,\\\"request_data_and_challenge_nonce_string\\\":null,\\\"confirmed_cp_and_code\\\":null,\\\"notification_callback_id\\\":null,\\\"reg_suma_state\\\":0,\\\"is_msplit_neutral_choice\\\":false,\\\"msg_previous_cp\\\":null,\\\"ntp_import_source_info\\\":null,\\\"youth_consent_decision_time\\\":null,\\\"username_screen_experience\\\":\\\"control\\\",\\\"reduced_tos_test_group\\\":\\\"control\\\",\\\"should_show_spi_before_conf\\\":true,\\\"google_oauth_account\\\":null,\\\"is_reg_request_from_ig_suma\\\":false,\\\"is_igios_spc_reg\\\":false,\\\"device_emails\\\":[],\\\"is_toa_reg\\\":false,\\\"is_threads_public\\\":false,\\\"spc_import_flow\\\":false,\\\"caa_play_integrity_attestation_result\\\":null,\\\"flash_call_provider\\\":null,\\\"name_prefill_variant\\\":\\\"control\\\",\\\"spc_birthday_input\\\":false,\\\"failed_birthday_year_count\\\":\\\"{}\\\",\\\"user_presented_medium_source\\\":null,\\\"user_opted_out_of_ntp\\\":null,\\\"is_from_registration_reminder\\\":false,\\\"show_youth_reg_in_ig_spc\\\":false}\",\"flow_info\":\"{\\\"flow_name\\\":\\\"new_to_family_fb_default\\\",\\\"flow_type\\\":\\\"ntf\\\"}\",\"current_step\":10,\"INTERNAL__latency_qpl_marker_id\":36707139,\"INTERNAL__latency_qpl_instance_id\":\"35563411300077\",\"device_id\":null,\"family_device_id\":null,\"waterfall_id\":\"a763fafb-432c-492a-9556-d768833ecc63\",\"offline_experiment_group\":null,\"layered_homepage_experiment_group\":null,\"is_platform_login\":0,\"is_from_logged_in_switcher\":0,\"is_from_logged_out\":0,\"access_flow_version\":\"F2_FLOW\",\"INTERNAL_INFRA_THEME\":\"harm_f\"},\"client_input_params\":{\"code\":\""+self.code+"\",\"fb_ig_device_id\":[],\"confirmed_cp_and_code\":{},\"lois_settings\":{\"lois_token\":\"\",\"lara_override\":\"\"}}}"
			}
			cok  = ';'.join([str(x)+"="+str(y) for x,y in self.ses.cookies.get_dict().items()])
			self.headers.update({'referer': f'https://m.facebook.com/caa/reg/confirmation/?reg_info=%7B%22contactpoint%22%3A%22{urllib.request.quote(self.email)}%22%2C%22contactpoint_type%22%3A%22email%22%2C%22is_cp_auto_confirmed%22%3Afalse%2C%22fb_conf_source%22%3Anull%2C%22confirmation_medium%22%3Anull%2C%22registration_flow_id%22%3A%2253335e1d-b812-4d0d-b4b6-9d27dcd898ec%22%7D&flow_info=%7B%22flow_name%22%3A%22new_to_family_fb_default%22%2C%22flow_type%22%3A%22ntf%22%7D&current_step=10','cookie': cok})
			post = self.ses.post(f'https://m.facebook.com/async/wbloks/fetch/?appid=com.bloks.www.bloks.caa.reg.confirmation.async&type=action&__bkv={self.versioningID}', data=data, headers = self.headers, cookies={'cookie': cok})
			if "confirmation_success" in post.text.replace('\\', ''):
				waktu = datetime.now(pytz.timezone('Asia/Jakarta')).strftime("%d-%m-%Y %H:%M:%S")
				cookies = ';'.join([str(x)+"="+str(y) for x,y in self.ses.cookies.get_dict().items()])
				Config().delayy("Sedang upload profile", 20)
				profil = self.postFotoProfile(cookies)
				Config().delayy("Sedang edit profile", 20)
				self.intro_profile(cookies)
				start = ProfileInfo(cookies, uid)
				start.userFollow()
				start.kotasekarang()
				if POSTS["STATUS"] is not None:
					textz = self.posting_pertama(cookies)
					console.print(f"""\r{' ' * 76}
 INFO ACCOUNT

 Status     : [bold green]Success[bold white]
 Timestamp  : [bold green]{waktu}[bold white]
 Name       : [bold green]{self.nama_depan} {self.nama_belakang}[bold white]
 UserID     : [bold green]{uid}[bold white]
 Nomor      : [bold green]{self.nomorTlpn}[bold white]
 Email      : [bold green]{self.email}[bold white]
 Password   : [bold green]{self.password}[bold white]
 Birthday   : [bold green]{self.tgl_lahir}[bold white]
 Profile    : {profil}
 Postingan  : {textz}
 Cookies    : [bold green]{cookies}[bold white]
					""")
				else:
					console.print(f"""\r{' ' * 76}
 INFO ACCOUNT

 Status     : [bold green]Success[bold white]
 Timestamp  : [bold green]{waktu}[bold white]
 Name       : [bold green]{self.nama_depan} {self.nama_belakang}[bold white]
 UserID     : [bold green]{uid}[bold white]
 Nomor      : [bold green]{self.nomorTlpn}[bold white]
 Email      : [bold green]{self.email}[bold white]
 Password   : [bold green]{self.password}[bold white]
 Birthday   : [bold green]{self.tgl_lahir}[bold white]
 Profile    : {profil}
 Cookies    : [bold green]{cookies}[bold white]
					""")
				json_ = {
					'Timestamp': f'{waktu}',
					'Name': f'{self.nama_depan} {self.nama_belakang}',
					'Userid': f'{uid}',
					'Email': f'{self.email}',
					'Password': f'{self.password}',
					'Tanggal lahir': f'{self.tgl_lahir}',
					'Cookies': f'{cookies}',
				}
				file_path = 'Results/FacebookNewAcc.json'
				os.makedirs(os.path.dirname(file_path), exist_ok=True)
				if os.path.exists(file_path):
					with open(file_path, 'r') as file:
						try:
							data = json.load(file)
						except json.JSONDecodeError:
							data = []
				else:
					data = []
				data.append(json_)
				with open(file_path, 'w') as file:
					json.dump(data, file, indent=4)
				Ok+=1
				return True
			elif "errorSummary" in post.text and "Coba muat ulang halaman, atau tutup dan buka kembali jendela browser Anda." in post.text:
				Cp+=1
				return False
			Fail+=1
			return False
		except Exception as e:
			pass
		
	def postFotoProfile(self, cookie):
		img = open('Data/pinterest.txt', 'r').read().splitlines()
		image_url = random.choice(img)
		try:
			with requests.Session() as r:
				id = re.search('c_user=(\\d+)', str(cookie)).group(1)
				req = r.get(f'https://web.facebook.com/profile.php?id={id}', cookies={'cookie': cookie}).text
				params = self.config.data_graphql(req, id)
				params.update({
					'profile_id': id,
					'photo_source': "57",
				})
				files = {'file':('image.jpg',urllib.request.urlopen(image_url).read())}
				pos = r.post("https://web.facebook.com/profile/picture/upload/", cookies={'cookie': cookie}, params=params,  files=files).text
				fbid = re.search('"fbid":"(\d+)"', str(pos)).group(1)
				data = self.config.data_graphql(req, id)
				data.update({
					"fb_api_caller_class": "RelayModern",
					"fb_api_req_friendly_name": "ProfileCometProfilePictureSetMutation",
					"variables": json.dumps({"input":{"attribution_id_v2":"ProfileCometTimelineListViewRoot.react,comet.profile.timeline.list,via_cold_start,1729674295794,691444,190055527696468,,","caption":"","existing_photo_id":fbid,"expiration_time":None,"profile_id":id,"profile_pic_method":"EXISTING","profile_pic_source":"TIMELINE","scaled_crop_rect":{"height":1,"width":1,"x":0,"y":0},"skip_cropping": True,"actor_id":id,"client_mutation_id":"2"},"isPage":False,"isProfile":True,"sectionToken":"UNKNOWN","collectionToken":"UNKNOWN","scale":3,"__relay_internal__pv__ProfileGeminiIsCoinFlipEnabledrelayprovider":False}),
					"server_timestamps": "true",
					"doc_id": "28132579203008372"
				})
				post = r.post('https://web.facebook.com/api/graphql/', data=data, cookies = {'cookie':cookie})
				if 'profilePhoto' in post.text:
					return f"[bold green]Berhasil memperbarui foto profil[bold white]"
				else:
					return f"[bold red]Gagal memperbarui foto profil[bold white]"
					
		except Exception as e:
			return f"[bold red]Gagal memperbarui foto profil[bold red]"
	
	def intro_profile(self, cookie):
		try:
			with requests.Session() as r:
				id = re.search('c_user=(\d+)', str(cookie)).group(1)
				response = r.get(f'https://web.facebook.com/profile.php?id={id}&sk=about_work_and_education', cookies={'cookie': cookie}).text
				
				cltk = re.search(r'"collectionToken":"(.*?)"', str(response))
				sectoken = re.search(r'"sectionToken":"(.*?)"', str(response))
				collectionToken = cltk.group(1) if cltk else None
				sectionToken = sectoken.group(1) if sectoken else None
				
				data = self.config.data_graphql(response, id)
				data.update({
					"fb_api_caller_class": "RelayModern",
					"fb_api_req_friendly_name": "ComposerStoryCreateMutation",
					"variables": json.dumps({"collectionToken":collectionToken,"input":{"description":None,"employer_id":"1953170501618069","employer_name":None,"end_date":{},"is_current":True,"location_id":"102173726491792","mutation_surface":"PROFILE","position_id":"186213662204063","position_name":None,"privacy":{"allow":[],"base_state":"EVERYONE","deny":[],"tag_expansion_state":"UNSPECIFIED"},"start_date":{"day":int(random.randint(1,28)),"month":int(random.randint(1,12)),"year":int(random.randint(1980,2024))},"actor_id":id,"client_mutation_id":"5"},"scale":3,"sectionToken":sectionToken,"useDefaultActor":False}),
					"server_timestamps": "true",
					"doc_id": "8496075440505870"
				})
				post = r.post('https://web.facebook.com/api/graphql/', data=data, cookies = {'cookie':cookie})
				if 'entity' in post.text:pass
		except Exception as e:pass
			
	def posting_pertama(self, cookie):
		try:
			with requests.Session() as r:
				id = re.search('c_user=(\\d+)', str(cookie)).group(1)
				req = r.get(f'https://web.facebook.com/profile.php?id={id}', cookies={'cookie': cookie}).text
				data = self.config.data_graphql(req, id)
				data.update({
					"fb_api_caller_class": "RelayModern",
					"fb_api_req_friendly_name": "ComposerStoryCreateMutation",
					"variables": json.dumps({"input":{"composer_entry_point":"inline_composer","composer_source_surface":"timeline","idempotence_token":"437cba73-b0e3-4655-aada-38dfd789008e_FEED","source":"WWW","attachments":[],"audience":{"privacy":{"allow":[],"base_state":"EVERYONE","deny":[],"tag_expansion_state":"UNSPECIFIED"}},"message":{"ranges":[],"text":POSTS['STATUS']},"with_tags_ids":None,"inline_activities":[],"text_format_preset_id":"0","publishing_flow":{"supported_flows":["ASYNC_SILENT","ASYNC_NOTIF","FALLBACK"]},"logging":{"composer_session_id":"437cba73-b0e3-4655-aada-38dfd789008e"},"navigation_data":{"attribution_id_v2":"ProfileCometTimelineListViewRoot.react,comet.profile.timeline.list,unexpected,1730202783968,840602,190055527696468,,;CometErrorRoot.react,comet.error,via_cold_start,1730202779383,997568,,,"},"tracking":[None],"event_share_metadata":{"surface":"timeline"},"actor_id":id,"client_mutation_id":"3"},"feedLocation":"TIMELINE","feedbackSource":0,"focusCommentID":None,"gridMediaWidth":230,"groupID":None,"scale":3,"privacySelectorRenderLocation":"COMET_STREAM","checkPhotosToReelsUpsellEligibility":True,"renderLocation":"timeline","useDefaultActor":False,"inviteShortLinkKey":None,"isFeed":False,"isFundraiser":False,"isFunFactPost":False,"isGroup":False,"isEvent":False,"isTimeline":True,"isSocialLearning":False,"isPageNewsFeed":False,"isProfileReviews":False,"isWorkSharedDraft":False,"hashtag":None,"canUserManageOffers":False,"__relay_internal__pv__CometUFIShareActionMigrationrelayprovider":True,"__relay_internal__pv__GHLShouldChangeSponsoredDataFieldNamerelayprovider":False,"__relay_internal__pv__GHLShouldChangeAdIdFieldNamerelayprovider":False,"__relay_internal__pv__IncludeCommentWithAttachmentrelayprovider":True,"__relay_internal__pv__CometUFIReactionsEnableShortNamerelayprovider":False,"__relay_internal__pv__CometImmersivePhotoCanUserDisable3DMotionrelayprovider":False,"__relay_internal__pv__IsWorkUserrelayprovider":False,"__relay_internal__pv__IsMergQAPollsrelayprovider":False,"__relay_internal__pv__FBReelsMediaFooter_comet_enable_reels_ads_gkrelayprovider":True,"__relay_internal__pv__StoriesArmadilloReplyEnabledrelayprovider":False,"__relay_internal__pv__EventCometCardImage_prefetchEventImagerelayprovider":False,"__relay_internal__pv__GHLShouldChangeSponsoredAuctionDistanceFieldNamerelayprovider":True}),
					"server_timestamps": "true",
					"doc_id": "8941629622565537"
				})
				post = r.post('https://web.facebook.com/api/graphql/', data=data, cookies = {'cookie':cookie})
				if "story_create" in post.text:
					return f"[bold green]berhasil posting {POSTS['STATUS']}[bold white]"
				else:
					return f"[bold red]gagal posting {POSTS['STATUS']}[bold white]"
		except Exception as e:
			return f"[bold red]gagal posting {POSTS['STATUS']}[bold white]"


if __name__ == "__main__":
	try:
		creator = MainMenu()
		creator.menu()
	except KeyboardInterrupt:
		console.print("\n\n[bold red] Proses diganggu oleh pengguna. Keluar...[/]")
	except Exception as e:
		console.print(f"\n\n[bold red] Terjadi kesalahan: {str(e)}[/]")
