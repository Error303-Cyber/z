import os
import json
import time
import random
import requests
from concurrent.futures import ThreadPoolExecutor
from fake_useragent import UserAgent

ua_chrome = UserAgent().chrome
file_cookie = "cookie.txt"
try:
	cok_zxc = open(file_cookie, "r").read()
	cookie = {"cookie": cok_zxc}
except FileNotFoundError:
	pass

ua_api = "Mozilla/5.0 (Linux; Android 10; SM-G973F Build/QP1A.190711.020; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/86.0.4240.198 Mobile Safari/537.36 Instagram 166.1.0.42.245 Android (29/10; 420dpi; 1080x2042; samsung; SM-G973F; beyond1; exynos9820; en_GB; 256099204)"
header_api = {"User-Agent": ua_api}
header_zxc = {"User-Agent": ua_chrome}

data_foll = {"foll_saya": [], "foll_orang": []}

def csrftoken_zxc():
	for spl in cok_zxc.split(";"):
		if "csrftoken=" in spl:
			csrftoken_zxc_ = spl.replace("csrftoken=", "")
			return csrftoken_zxc_.strip()
def may_id():
	for spl in cok_zxc.split(";"):
		if "ds_user_id=" in spl:
			may_id_zxc_ = spl.replace("ds_user_id=", "")
			return may_id_zxc_.strip()
def masuk_cookie():
	c = input(" Masukkan Cookie: ")
	with open(file_cookie, "w") as tul:
		tul.write(c)
		print(" Sukses...")

def login():
	print("\n\tLogin Instagram..\n")
	username = input(" ? Username: ")
	password = input(" ? Password: ")
	with requests.Session() as ses_zxc:
		headerz = {
					"Accept-Encoding": "gzip, deflate, br",
					"User-Agent": ua_chrome,
					"X-CSRFToken": ses_zxc.get("https://www.instagram.com/").cookies.get("csrftoken"),
				   }
		payload = {
					"enc_password": f"#PWD_INSTAGRAM_BROWSER:0:{int(time.time())}:{password.strip()}",
					"username": username.strip(),
					"queryParams": {},
				   }
		res_log = ses_zxc.post("https://www.instagram.com/accounts/login/ajax/", data=payload, headers=headerz)
		jes_log = json.loads(res_log.content)
		cok_log = res_log.cookies.get_dict()
		if "userId" in str(jes_log):
			print("\n Berhasil Login..")
			with open(file_cookie, "w") as h:
				h.write("")
			for zxc in cok_log:
				with open(file_cookie, "a") as w:
					w.write(zxc+"="+cok_log[zxc]+";")

		else:
			print("\n Login Gagal...")

def get_info_acount(user, key):
	url = f"https://www.instagram.com/{user}/?__a=1"
	with requests.Session() as ses_zxc:
		req = ses_zxc.get(url, headers={"User-Agent": ua_chrome})
		data = req.json()["graphql"]["user"]
		return data[key]

def may_followers_list(may_id, opsi_foll):
	url = f"https://i.instagram.com/api/v1/friendships/{may_id}/{opsi_foll}/?count=100000"
	with requests.Session() as ses_zxc:
		req = ses_zxc.get(url, cookies=cookie, headers=header_api)
		for zxc in req.json()["users"]:
			data_foll["foll_saya"]+=[{
									  "id":zxc["pk"], 
									  "username": zxc["username"], 
									  "nama": zxc["full_name"],
									  "private": zxc["is_private"]
									}]

def get_followers_list(id_user, limit, opsi):
	url = f"https://i.instagram.com/api/v1/friendships/{id_user}/{opsi}/?count={limit}"
	animasi = ["\\","/","-"]
	with requests.Session() as ses_zxc:
		req = ses_zxc.get(url, cookies=cookie, headers=header_api)
		for i, zxc in enumerate(req.json()['users']):
			print("\r",i,random.choice(animasi),zxc['username'],end="____________"),
			if zxc["pk"] == int(may_id()):
				continue
			data_foll["foll_orang"]+=[{
									  "id":zxc["pk"], 
									  "username": zxc["username"], 
									  "nama": zxc["full_name"],
									  "private": zxc["is_private"]
									 }]
			time.sleep(0.01)

def follow(_user_, opsi, c):
	global berhenti
	try:
		berhenti = False
		id_user = _user_["id"]
		username = _user_["username"]
		w = random.choice([27,10,15,20,25,30])
		url = f"https://www.instagram.com/web/friendships/{id_user}/{opsi}/"
		with requests.Session() as ses_zxc:
			headerz = {"User-Agent": ua_chrome, "X-CSRFToken": csrftoken_zxc()}
			req = ses_zxc.post(url, cookies=cookie, headers=headerz).content
			print(f"\r {c} >--[time:{w}]--< Sukses {opsi} -- {username} ")
			while w != 0:
				print(f"\r +-- Tunggu {w} detik...", end="")
				time.sleep(1)
				w -= 1

	except requests.exceptions.ConnectionError:
		follow(_user_, opsi, c)

	except KeyboardInterrupt:
		try:
			input("\n Jeda....")
		except KeyboardInterrupt:
			berhenti = True

def main():
	# login()
	data_cek = []
	print("\n\n ( 1 ) Auto Follow.")
	print(" ( 2 ) Auto Unfollow")
	print(" ( 3 ) Ganti Cookie")
	print(" ( 4 ) Login Ulang")
	print("------------------------")
	pil = input(" ? Pilih: ")
	if pil == "1":
		username = input("\n ? Input Username Target: ")
		limit = input(" ? Masukkan Limit: ")
		try:
			with open(username+".json", "r") as cek:
				for iq in json.load(cek):
					data_cek.append(iq)
				ada = True
		except FileNotFoundError:
				ada = False
		while True:
			opsi = input(" ? Opsi 1.Followers, 2.Following: ")
			if opsi == "1":
				opsi = "followers"
				break
			elif opsi == "2":
				opsi = "following"
				break
			else:
				pass
		may_followers_list(may_id(), "following")
		get_followers_list(get_info_acount(username, "id"), "10000", opsi)
		print("\n"+35*"=")

		count = 1
		unfollow_ = []
		try:
			for iq in data_foll["foll_orang"]:
				if iq in data_foll["foll_saya"]: # or iq["private"] == True:
					continue
				if count >= int(limit)+1:
					break

				follow(iq, "follow", count)
				if ada == True:
					def tulis(data, file_name=username+".json"):
						with open(file_name, "w") as f:
							json.dump(data, f, indent=4)
					with open(username+".json") as json_file:
						data = json.load(json_file)
						isi_ = data
						isi_+=[iq]

					if iq not in data_cek:
						tulis(data)

				if ada == False:
					unfollow_.append(iq)

				if berhenti == True:
					break

				count += 1

		except KeyboardInterrupt:
			pass

		if ada == False:
			try:
				with open(username+".json", "w") as tul:
					json.dump(unfollow_, tul, indent=4)

				input("\n>>>>\n")	
				count = 1
				for iq in unfollow_:
					follow(iq, "unfollow", count)
					count += 1
				os.remove(username+".json")
			except KeyboardInterrupt:
				exit()

	elif pil == "2":
		try:
			count = 1
			username = input("\n Input Username Target: ")
			nama_file = username+".json"
			with open(nama_file, "r") as file_foll_orang:
				may_followers_list(may_id(), "followers")
				for iq in json.load(file_foll_orang):
					if iq in data_foll["foll_saya"]: 
						continue
					follow(iq, "unfollow", count)
					if berhenti == True:
						break
					count+=1
			if berhenti == False:
				os.remove(nama_file)
				
		except FileNotFoundError:
			print("\n Tidak ada file",nama_file), exit()
	elif pil == "3":
		masuk_cookie()
	elif pil == "4":
		login()

if __name__=="__main__":
	main()
