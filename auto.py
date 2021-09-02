import os,requests,getpass,json,io,time, random
from datetime import datetime
import re, string, uuid, hashlib, hmac, urllib
from time import sleep
from bs4 import BeautifulSoup as bs

header = {"Host": "i.instagram.com",
          'accept' : '*/*',
          'referer': 'https://www.instagram.com/',
          'accept-language': 'id-ID,id;q=0.9,en-US;q=0.8,en;q=0.7',
          'user-agent':'Mozilla/5.0 (iPhone; CPU iPhone OS 12_3_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 Instagram 105.0.0.11.118 (iPhone11,8; iOS 12_3_1; en_US; en-US; scale=2.00; 828x1792; 165586599)'}

url = 'https://i.instagram.com/api/v1/'
device = {
'manufacturer'      : 'Xiaomi',
'model'             : 'HM 1SW',
'android_version'   : 18,
'android_release'   : '4.3'
}
useragent = 'Instagram 9.2.0 Android ({android_version}/{android_release}; 320dpi; 720x1280; {manufacturer}; {model}; armani; qcom; en_US)'.format(**device)
ig_sig_key = '012a54f51c49aa8c5c322416ab1410909add32c966bbaa0fe3dc58ac43fd7ede'
sig_key_versi = '4'

BASE_URL = "https://www.instagram.com/"
LOGIN_URL = BASE_URL + "accounts/login/ajax/"
USER_AGENT = 'Mozilla/5.0 (X11; CrOS i686 4319.74.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/29.0.1547.57 Safari/537.36'
CHANGE_URL = "https://www.instagram.com/accounts/web_change_profile_picture/"
CHNAGE_DATA = {"Content-Disposition": "form-data", "name": "profile_pic", "filename":"profilepic.jpg","Content-Type": "image/jpeg"}
headers = {
    "Host": "www.instagram.com",
    "Accept": "*/*",
    "Accept-Language": "en-US,en;q=0.5",
    "Accept-Encoding": "gzip, deflate, br",
    "Referer": "https://www.instagram.com/accounts/edit/",
    "X-IG-App-ID": "936619743392459",
    "X-Requested-With": "XMLHttpRequest",
    "DNT": "1",
    "Connection": "keep-alive",
}

headerr = {
                        'Accept-Encoding': 'gzip, deflate',
                        'Accept-Language': 'en-US,en;q=0.8',
                        'Connection': 'keep-alive',
                        'Host': 'www.instagram.com',
                        'Referer': 'https://www.instagram.com/',
                        'User-Agent': 'Mozilla/5.0 (X11; CrOS i686 4319.74.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/29.0.1547.57 Safari/537.36',
                        'X-Instagram-AJAX': '1',
                        'X-Requested-With': 'XMLHttpRequest'
                        }

def get_id(username):
        urla = "https://www.instagram.com/web/search/topsearch/?context=blended&query="+username+"&rank_token=0.3953592318270893&count=1"
        response = requests.get(urla, headers=headerr)
        respJSON = response.json()
        try:
                user_id = str( respJSON['users'][0].get("user").get("pk") )
                return user_id
        except:
                print(respJSON)
                return "Unexpected error"

class igeh:
      def __init__(self, user, pas):
            self.cok = None
            self.status = 0
            self.username_id = None
            self.rank_token = None
            self.token = None
            self.fullname = None
            self.phone = None
            self.username = user
            self.password = pas
            m = hashlib.md5()
            m.update(user.encode('utf-8') + pas.encode('utf-8'))
            self.device_id = self.getDeviceId(m.hexdigest())
            self.uuid = self.getUUID(True)

      def update(self):
            return (self.session, self.status, self.password, self.username, self.token, self.cok, self.uuid, self.username_id)

      def login(self):
            self.session = requests.Session()
            self.session.headers.update ({'Connection' : 'close',
                                'Accept' : '*/*',
                                'Content-type' : 'application/x-www-form-urlencoded; charset=UTF-8',
                                'Cookie2' : '$Version=1',
                                'Accept-Language' : 'en-US',
                                'User-Agent' : useragent})
            response = self.session.get(f'{url}si/fetch_headers/?challenge_type=signup&guid={self.getUUID(False)}')
            if response.status_code == 200:
                 data = {'phone_id'   : self.getUUID(True),
                        '_csrftoken' : response.cookies['csrftoken'],
                        'username'   : self.username,
                        'guid'       : self.uuid,
                        'device_id'  : self.device_id,
                        'password'   : self.password,
                        'login_attempt_count' : '0'}
                 response = self.session.post(f'{url}accounts/login/', data=self.getSignature(json.dumps(data)))
                 load = json.loads(response.text)
                 if "logged_in_user" in str(response.text):
                         self.id = load["logged_in_user"]["pk"]
                         self.rank_token = "%s_%s" % (self.id, self.uuid)
                         self.token = response.cookies["csrftoken"]
                         self.username_id = self.id
                         self.phone = load["logged_in_user"]["phone_number"]
                         self.fullname = load["logged_in_user"]["full_name"]
                         self.cok = response.cookies
                         self.status = 1

                 elif "checkpoint_required" in str(response.text):
                         self.status = 2
                 elif "Please wait a few minutes before you try again." in str(response.text):
                         self.status = 3
                 elif "ip_block" in str(response.text):
                         self.status = 4
                 else:
                         self.status = 5

      def getSignature(self, data):
             try:
                  parse = urllib.parse.quote(data)
             except AttributeError:
                  parse = urllib.quote(data)

             return f'ig_sig_key_version={sig_key_versi}&signed_body={hmac.new(ig_sig_key.encode("utf-8"), data.encode("utf-8"), hashlib.sha256).hexdigest()}.{parse}'

      def getUUID(self, type):
             generated_uuid = str(uuid.uuid4())
             if (type):
                 return generated_uuid
             else:
                 return generated_uuid.replace('-', '')

      def getDeviceId(self, seed):
             volatile_seed = "12345"
             m = hashlib.md5()
             m.update(seed.encode('utf-8') + volatile_seed.encode('utf-8'))
             return 'android-' + m.hexdigest()[:16]

def sessionLog(user, pas):
      sesi = igeh(user, pas)
      sesi.login()
      session, status, password, username, token, cok, uid, user_id = sesi.update()
      if status == 1:
           cookies = f'csrftoken={cok["csrftoken"]};ds_user_id={cok["ds_user_id"]};rur={cok["rur"]};sessionid={cok["sessionid"]}'
           with open("akun-cookies.log","a") as f:
                 f.write(cookies+"\n")
           return (session, username, password, token, cookies)

      elif status == 2:
           print("(!) CHECKPOINT, PERIKSA AKUN ANDA!!")
      elif status == 3:
           print("(!) LIMIT, TUNGGU BEBERAPA MENIT LAGI / GUNAKAN AKUN LAIN!!")
      elif status == 4:
           print("(!) IP BLOCK, TUNGGU BEBERAPA MENIT!!")
      else:
           print("(!) USERNAME / PASSWORD SALAH!!")

class web:
      def __init__(self, u, p):
           self.username = u
           self.password = p
           self.session = requests.Session()
           self.session.headers.update({
                        'Accept-Encoding': 'gzip, deflate',
                        'Accept-Language': 'en-US,en;q=0.8',
                        'Connection': 'keep-alive',
                        'Host': 'www.instagram.com',
                        'Referer': 'https://www.instagram.com/',
                        'User-Agent': 'Mozilla/5.0 (X11; CrOS i686 4319.74.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/29.0.1547.57 Safari/537.36',
                        'X-Instagram-AJAX': '1',
                        'X-Requested-With': 'XMLHttpRequest'
                    })

      def login(self):
             enc_pass = '#PWD_INSTAGRAM_BROWSER:0:{}:{}'.format(int(time.time()), self.password)
             self.session.cookies.update({
                        'sessionid': '', 'mid': '', 'ig_pr': '1',
                        'ig_vw': '1920', 'csrftoken': '',
                        's_network': '', 'ds_user_id': ''
                    })
             self.session.get('https://www.instagram.com/web/__mid')
             self.session.headers.update({'X-CSRFToken': self.session.cookies.get_dict()['csrftoken']})
             login_data = {'username':self.username,"enc_password":enc_pass}
             login_resp = self.session.post(LOGIN_URL, data=login_data, allow_redirects=True)
             if login_resp.json()['authenticated']:
                    return True, self.username
             else:
                    return False, self.username

             self.session.headers.update({'X-CSRFToken': self.session.cookies.get_dict()['csrftoken']})


      def change(self, cookies):
           self.session.get('https://www.instagram.com/web/__mid')
           self.session.headers.update(headers)
           self.session.headers.update({'X-CSRFToken': self.session.cookies.get_dict()['csrftoken']})
           try:
                 resp = requests.get('https://source.unsplash.com/random/320x320').content
                 p_pic = bytes(resp)
                 p_pic_s = len(p_pic)
                 self.session.headers.update({'Content-Length' : str(p_pic_s)})
                 files = {'profile_pic': p_pic}
                 r = self.session.post(CHANGE_URL, files=files, data=CHNAGE_DATA, cookies={"cookie":cookies})
                 if r.json()['changed_profile']:
                      return True
                 else:
                      return False
           except:
                  pass

      def post_photo(self):
           status = 0
           stop = 0
           try:
               sesi, username, password, token, cookies = sessionLog(self.username, self.password)
               while (stop < 3):
                    stop += 1
                    resp = requests.get('https://source.unsplash.com/random/320x320').content
                    p_pic = bytes(resp)
                    p_pic_s = len(p_pic)
                    microtime = int(datetime.now().timestamp())
                    sesi.headers.update({
                         "content-type": "image / jpg",
                         "X-Entity-Name" : f"fb_uploader_{microtime}",
                         "Offset": "0",
                         "User-Agent": useragent,
                         "x-entity-length": str(p_pic_s),
                         "X-Instagram-Rupload-Params": f'{{"media_type": 1, "upload_id": {microtime}, "upload_media_height": 1080, "upload_media_width": 1080}}',
                         "x-csrftoken": token,
                         "x-ig-app-id": "1217981644879628"
                    })
                    upload = sesi.post(f"https://i.instagram.com/rupload_igphoto/fb_uploader_{microtime}", data=p_pic).json()
                    if upload["status"] == "ok":
                          sesi.headers.update({
                              'Content-Length': str(p_pic_s),
                              'content-type': 'application/x-www-form-urlencoded',
                              "origin": "https://www.instagram.com",
                              "referer": "https://www.instagram.com/create/details/",
                              'user-agent': useragent,
                              "x-csrftoken": token,
                              "x-ig-app-id": "1217981644879628",
                              "X-Requested-With": "XMLHttpRequest"
                          })
                          data = {
                              "source_type":"library",
                              "caption":"",
                              "upcoming_event":"",
                              "upload_id":microtime,
                              "usertags":"",
                              "custom_accessibility_caption":"",
                              "disable_comments":"0",
                          }
                          config = sesi.post("https://i.instagram.com/api/v1/media/configure/", data=data).json()
                          if config["status"] == "ok":
                                status += 1

               if status != 0:
                   if self.change(cookies):
                        print(f"\x1b[32;1m(\x1b[31;1m+\x1b[32;1m) \x1b[36;1mPROFILE PICTURE CHANGED \x1b[32;1m& \x1b[36;1mUPLOADED \x1b[32;1m{status} \x1b[36;1mPHOTOS  \x1b[37;1m(\x1b[32;1mDONE\x1b[37;1m)")
                   else:
                        print (f"\x1b[32;1m(\x1b[31;1m+\x1b[32;1m) \x1b[36;1mUPLOADED \x1b[32;1m{status} PHOTOS \x1b[37;1m(\x1b[32;1mDONE\x1b[37;1m)")
               else:
                   if self.change(cookies):
                        print (f"\x1b[32;1m(\x1b[31;1m+\x1b[32;1m) \x1b[36;1mPROFILE PICTURE CHANGED \x1b[37;1m(\x1b[32;1mDONE\x1b[37;1m)")
                   else:
                        print(f"\x1b[32;1m(\x1b[31;1m!\x1b[32;1m) \x1b[31;1mSOMETHING WENT WRONG")

           except: pass

list_mail = ["vintomaper.com","tovinit.com","mentonit.net"]
url_ = "https://cryptogmail.com/"
header_ = {'Connection' : 'close',
           'Accept' : '*/*',
           'Content-type' : 'application/x-www-form-urlencoded; charset=UTF-8',
           'Cookie2' : '$Version=1',
           'Accept-Language' : 'en-US',
           'User-Agent' : useragent}

class cokis:
        def __init__(self, coki):
               self.cookies = coki

        def lognin(self):
                self.sesi = requests.Session()
                self.sesi.headers.update(headerr)
                self.sesi.cookies.update({
                        'sessionid': '', 'mid': '', 'ig_pr': '1',
                        'ig_vw': '1920', 'csrftoken': '',
                        's_network': '', 'ds_user_id': ''
                })
                self.sesi.get('https://www.instagram.com/web/__mid')
                self.sesi.headers.update({'X-CSRFToken': self.sesi.cookies.get_dict()['csrftoken']})
                req = self.sesi.get("https://www.instagram.com/", cookies={'cookie': self.cookies})
                if "ds_user_id" in req.cookies:
                        return True, self.sesi

                else:
                        return False, self.sesi

def banner():
     os.system("clear")
     print("""
     \x1b[35;1m___\x1b[35;1m______\x1b[35;1m______\x1b[35;1m___  __
    \x1b[35;1m/  _\x1b[35;1m/ ____\x1b[35;1m/ ____\x1b[35;1m/ / / /\x1b[100m\x1b[32;1mA\x1b[0m
    \x1b[35;1m/ /\x1b[35;1m/ / __\x1b[35;1m/ __/ \x1b[35;1m/ /_/ /\x1b[100m\x1b[32;1mS\x1b[0m
  \x1b[35;1m_/ /\x1b[35;1m/ /_/ \x1b[35;1m/ /___\x1b[35;1m/ __  /\x1b[100m\x1b[32;1mE\x1b[0m
 \x1b[35;1m/___/\x1b[35;1m\____/\x1b[35;1m_____\x1b[35;1m/_/ /_/\x1b[100m\x1b[32;1mX\x1b[0m
\x1b[31;1m──────────────────────────────""")

def get_teks(accept, key):
        cek = requests.get(url_+"api/emails/"+key, headers={"accept": accept}).text
        if "error" in cek:
                return "-"
        else:
                return cek

def get_random(digit):
        lis = list("abcdefghijklmnopqrstuvwxyz0123456789")
        dig = [random.choice(lis) for _ in range(digit)]
        return "".join(dig), random.choice(list_mail)

def run(email):
        result = []
        no = 0
        while True:
                no += 1
                try:
                        raun = requests.get(url_+"api/emails?inbox="+email).text
                        if "404" in raun:
                                continue
                        elif "data" in raun:
                                z = json.loads(raun)
                                for data in z["data"]:
                                        res = get_teks("text/html,text/plain",data["id"])
                                        sc = bs(res.encode("utf-8"), "html.parser")
                                        cs = sc.find("td", attrs={"style":"padding:10px;color:#565a5c;font-size:32px;font-weight:500;text-align:center;padding-bottom:25px;"}).text
                                        result.append(str(cs))
                                        requests.delete(url_+"api/emails/"+data["id"])
                                break
                        else:
                                continue
                except (KeyboardInterrupt,EOFError):
                                break
                if no >= 10:
                     break
        return result
def create():
            session = requests.Session()
            sesi = requests.Session()
            session.headers.update(header_)
            while True:
              try:
                 set_name, set_email = get_random(3)
                 ran = requests.get("https://randomuser.me/api/").json()
                 set_name = f'{str(ran["results"][0]["name"]["first"])}_{set_name}'.upper()
                 sesi.headers.update(headerr)
                 sesi.cookies.update({
                        'sessionid': '', 'mid': '', 'ig_pr': '1',
                        'ig_vw': '1920', 'csrftoken': '',
                        's_network': '', 'ds_user_id': ''
                       })
                 sesi.get('https://www.instagram.com/web/__mid')
                 sesi.headers.update({'X-CSRFToken': sesi.cookies.get_dict()['csrftoken']})
                 suges = sesi.post("https://www.instagram.com/accounts/username_suggestions/", data={"email": set_name+"@"+set_email, "name": str(ran["results"][0]["name"]["first"]).upper()}).json()
                 usernam = suges["suggestions"][0]
                 uudi = random.choice(["YCMpBgABAAEI3BpsACCjB0aLRmYC"])
                 dat = {
                     "device_id": str(uudi),
                     "email": set_name+"@"+set_email
                     }
                 send = session.post(f"{url}accounts/send_verify_email/", data=dat).json()
                 try:
                     if send["email_sent"]:
                         print ("\x1b[32;1m(\x1b[31;1m*\x1b[32;1m) \x1b[36;1mWaiting for OTP code....")
                         codec = run(set_name+"@"+set_email)[0]
                         check = session.post(f"{url}accounts/check_confirmation_code/", data={"code":codec,"device_id": str(uudi),"email":set_name+"@"+set_email}).json()
                         print (f"\x1b[32;1m(\x1b[31;1m+\x1b[32;1m) \x1b[36;1mVerification successful with code\x1b[32;1m(\x1b[37;1m{codec}\x1b[32;1m)")
                         enc_pass = '#PWD_INSTAGRAM_BROWSER:0:{}:{}'.format(int(time.time()), "sabar123")
                         sesi.post("https://www.instagram.com/web/consent/check_age_eligibility/", data={"day":"12", "mont":"3", "year":"1999"})
                         data = {
                                  "email": set_name+"@"+set_email,
                                  "enc_password": enc_pass,
                                  "username": usernam,
                                  "first_name": str(ran["results"][0]["name"]["first"]).upper(),
                                  "month": "3",
                                  "day": "12",
                                  "year": "1999",
                                  "client_id": str(uudi),
                                  "seamless_login_enabled":"1",
                                  "tos_version":"row",
                                  "force_sign_up_code": check["signup_code"],
                                  }
                         buat = sesi.post("https://www.instagram.com/accounts/web_create_ajax/", data=data).json()
                         try:
                               if buat["account_created"] == True:
                                   with open("akun1.txt","a") as f:
                                         f.write(usernam+" | "+set_name+"@"+set_email+" | sabar123\n")
                                   print ("\x1b[32;1m(\x1b[31;1m+\x1b[32;1m) \x1b[36;1mSTATUS   \x1b[31;1m: \x1b[35;1mLOGIN")
                                   print (f"\x1b[32;1m(\x1b[31;1m+\x1b[32;1m) \x1b[36;1mUSERNAME \x1b[31;1m: \x1b[37;1m{usernam}")
                                   print (f"\x1b[32;1m(\x1b[31;1m+\x1b[32;1m) \x1b[36;1mPASSWORD \x1b[31;1m: \x1b[37;1msabar123")
                                   print (f"\x1b[32;1m(\x1b[31;1m+\x1b[32;1m) \x1b[36;1mEMAIL    \x1b[31;1m: \x1b[37;1m{set_name}@{set_email}")
                                   web(usernam, "sabar123").post_photo()
                                   print (f"\x1b[31;1m──────────────────────────────\n")
                                   break

                         except KeyError:
                               if "checkpoint_required" in str(buat):
                                   print ("\x1b[32;1m(\x1b[31;1m+\x1b[32;1m) \x1b[36;1mSTATUS   \x1b[31;1m: \x1b[33;1mCHECKPOINT")
                                   print (f"\x1b[32;1m(\x1b[31;1m+\x1b[32;1m) \x1b[36;1mUSERNAME \x1b[31;1m: \x1b[37;1m{usernam}")
                                   print (f"\x1b[32;1m(\x1b[31;1m+\x1b[32;1m) \x1b[36;1mPASSWORD \x1b[31;1m: \x1b[37;1msabar123")
                                   print (f"\x1b[32;1m(\x1b[31;1m+\x1b[32;1m) \x1b[36;1mEMAIL    \x1b[31;1m: \x1b[37;1m{set_name}@{set_email}")
                                   print (f"\x1b[31;1m──────────────────────────────\n")
                                   with open("akun-cp.txt","a") as f:
                                        f.write(usernam+" | "+set_name+"@"+set_email+" | sabar123"+" | "+buat['checkpoint_url']+"\n") 
                                   break

                               else:
                                   print ("\x1b[32;1m(\x1b[31;1m+\x1b[32;1m) \x1b[36;1mSTATUS   \x1b[31;1m: \x1b[31;1mFAILLED")
                                   print (buat)
                                   print (f"\x1b[31;1m──────────────────────────────\n")
                                   sleep(200)
                                   break

                 except KeyError:
                       pass
                 except:
                       print (f"\x1b[31;1m──────────────────────────────\n")
                       pass

              except json.decoder.JSONDecodeError:
                     print (f"\x1b[31;1m──────────────────────────────\n")
                     pass
              except requests.exceptions.ConnectionError:
                     print ("\x1b[31;1mJaringan Tidak Stabil ....")
                     sleep(5)
              #except: pass

            create()

def follow():
       user = input("(+) Username : ")
       id = get_id(user)
       for i, val in enumerate(open("akun1.txt").read().splitlines(), start=1):
             try:
                if i > 88:
                  cek = 0
                  try:
                     for va in open(user+".txt").read().splitlines():
                          if val.split(" | ")[0] == va:
                               cek += 1
                               break
                  except: pass
                  if cek == 0:
                      six = igeh(val.split(" | ")[0], "sabar123")
                      six.login()
                      session, status, password, username, token, cok, uid, user_id = six.update()
                      if status == 1:
                            data = json.dumps({
                                     '_uuid'         : uid,
                                     '_uid'          : user_id,
                                     'user_id'       : id,
                                     '_csrftoken'    : token
                                     })
                            res = session.post(f'{url}friendships/create/{str(id)}/', data=six.getSignature(data)).json()
                            try:
                               if res["friendship_status"]["following"] == True:
                                     with open(user+".txt","a") as f:
                                          f.write(username+"\n")
                                     print (f"({i}) {username} : FOLLOW {user} SUCCESS")
                               else:
                                     print (f"({i}) {username} : FOLLOW {user} FAILLED")
                            except KeyError:
                                 if res['spam']:
                                      print ("kena limut om....")
                                      sleep(10)
                                 else: pass
                      else: print (status)

             except requests.exceptions.ChunkedEncodingError:
                sleep(5)
                pass
             #except KeyError: pass
             except requests.exceptions.ConnectionError:
                sleep(5)
                pass

def follow_cookie(val):
     user = input("(+) Username : ")
     id = get_id(user)
     for i, val in enumerate(open("akun-cookies.log").read().splitlines(), start=1):
         try:
           if i > 430:
                try:
                   cek = 0
                   for va in open(user+".txt").read().splitlines():
                       if val == va:
                            cek += 1
                            break
                except: pass
                if cek == 0:
                     login, sesi = cokis(val).lognin()
                     if login:
                         try:
                             follow = sesi.post(f'https://www.instagram.com/web/friendships/{str(id)}/follow/', cookies={'cookie': val}).json()
                             if follow["status"] == "ok":
                                  with open(user+".txt","a") as f:
                                       f.write(val+"\n")
                                  print (f"({i}) FOLLOW {user} SUCCESS")
                             else:
                                  print (f"({i}) FOLLOW {user} FAILLED")
                         except json.decoder.JSONDecodeError:
                              sleep(3)

         except requests.exceptions.ChunkedEncodingError:
                 sleep(5)
                 pass

         except requests.exceptions.ConnectionError:
                 sleep(5)
                 pass


if __name__ == "__main__":
        banner()
        create()
        #follow_cookie()
