import requests
import json
import random
import string
from requests_toolbelt import MultipartEncoder
from PIL import Image
from io import BytesIO


class TohyoTalk:
    def __init__(self, debug=False):
        self.headers = {
            'authority': 'tohyotalk.com',
            'accept': 'application/json, text/javascript, */*; q=0.01',
            'accept-language': 'ja',
            'content-keep': 'on',
            'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'origin': 'https://tohyotalk.com',
            'referer': 'https://tohyotalk.com',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'user-agent': 'Mozilla/5.0 (iPad; CPU OS 13_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) CriOS/87.0.4280.77 Mobile/15E148 Safari/604.1 Edg/112.0.0.0',
            'x-requested-with': 'XMLHttpRequest',
        }
        self.debug = debug
        self.data = None

    def get_fueldid(self, proxy=None):
        proxies = {
            "http": proxy,
            "https": proxy,
        }
        r = requests.get('https://tohyotalk.com/', proxies=proxies)
        return r.cookies.get('fueldid')

    def create_account(self, userId, userName, password="password", proxy=None):
        self.fueldid = self.get_fueldid(proxy)
        proxies = {
            "http": proxy,
            "https": proxy,
        }
        cookies = {
            'sf': '4',
            'fueldid': self.fueldid
        }
        data = {
            'tt_id': userId,
            'tt_name': userName,
            'mode': 'set_id_name'
        }

        r = requests.post('https://tohyotalk.com/api/updateaccount.json',
                          cookies=cookies, headers=self.headers, data=data, proxies=proxies)
        if self.debug:
            print(r.text)
        if json.loads(r.text)["status"] == 0:
            user_id = r.cookies.get("user_id")
            phpsessid = r.cookies.get("PHPSESSID")
            d4 = r.cookies.get("d4")
            cookies = {
                'sf': '4',
                'PHPSESSID': phpsessid,
                'user_id': user_id,
                'd4': d4,
                'fueldid': self.fueldid}
            data = {
                'tt_id': userId,
                'tt_pw': password,
            }
            r = requests.post('https://tohyotalk.com/api/updatepassword.json',
                              cookies=cookies, headers=self.headers, data=data, proxies=proxies)
            self.data = {
                "PHPSESSID": phpsessid,
                "d4": d4,
                "user_id": user_id,
                "userId": userId,
                "password": password
            }
            if self.debug:
                print({
                    "status": True,
                    "userName": userName,
                    "userId": userId,
                    "password": password
                })
            return {
                "status": True,
                "userName": userName,
                "userId": userId,
                "password": password
            }

        else:
            if self.debug:
                print({
                    "status": False,
                })
            return {
                "status": False
            }

    def login(self, userId, password, proxy=None):
        self.fueldid = self.get_fueldid(proxy)
        proxies = {
            "http": proxy,
            "https": proxy,
        }
        cookies = {
            'sf': '4',
            'fueldid': self.fueldid
        }
        data = {
            'tt_id': userId,
            'tt_pw': password,
        }
        r = requests.post('https://tohyotalk.com/api/idrenkei.json',
                          cookies=cookies, headers=self.headers, data=data, proxies=proxies)
        if self.debug:
            print(r.text)
        if json.loads(r.text)["status"] == 0:
            self.data = {
                "PHPSESSID": r.cookies.get("PHPSESSID"),
                "d4": r.cookies.get("d4"),
                "user_id": r.cookies.get("user_id"),
                "userId": userId,
                "password": password
            }
            if self.debug:
                print({
                    "status": True,
                })
            return {
                "status": True,
            }
        else:
            if self.debug:
                print({
                    "status": False,
                })
            return {
                "status": False,
            }

    def vote(self, vote_id, target, proxy=None):
        if not self.data == None:
            fueldid = self.fueldid
            proxies = {
                "http": proxy,
                "https": proxy,
            }
            cookies = {
                'sf': '4',
                'PHPSESSID': self.data["PHPSESSID"],
                'user_id': self.data["user_id"],
                'd4': self.data["d4"],
                'fueldid': fueldid
            }
            data = {
                'id': vote_id,
                'target': target,
            }
            r = requests.post('https://tohyotalk.com/api/vote.json',
                              cookies=cookies, headers=self.headers, data=data, proxies=proxies)
            if self.debug:
                print(r.text)
            if json.loads(r.text)["status"] == 0:
                if self.debug:
                    print({
                        "status": True
                    })
                return {
                    "status": True
                }
            else:
                if self.debug:
                    print({
                        "status": False
                    })
                return {
                    "status": False
                }
        else:
            if self.debug:
                print({
                    "status": False
                })
            return {
                "status": False
            }

    def tweet(self, content, proxy=None):
        if not self.data == None:
            fueldid = self.fueldid
            proxies = {
                "http": proxy,
                "https": proxy,
            }
            cookies = {
                'sf': '4',
                'PHPSESSID': self.data["PHPSESSID"],
                'user_id': self.data["user_id"],
                'd4': self.data["d4"],
                'fueldid': fueldid
            }
            data = {
                'question_id': '-380',
                'content': content,
            }
            r = requests.post('https://tohyotalk.com/api/createmsg2.json',
                              cookies=cookies, headers=self.headers, data=data, proxies=proxies)
            if self.debug:
                print(r.text)
            if json.loads(r.text)["status"] == 0:
                if self.debug:
                    print({
                        "status": True,
                        "msgId": json.loads(r.text)["msgId"]
                    })
                return {
                    "status": True,
                    "msgId": json.loads(r.text)["msgId"]
                }
            else:
                if self.debug:
                    print({
                        "status": False
                    })
                return {
                    "status": False
                }
        else:
            if self.debug:
                print({
                    "status": False
                })
            return {
                "status": False
            }

    def follow(self, id, proxy=None):
        if not self.data == None:
            fueldid = self.fueldid
            proxies = {
                "http": proxy,
                "https": proxy,
            }
            cookies = {
                'sf': '4',
                'PHPSESSID': self.data["PHPSESSID"],
                'user_id': self.data["user_id"],
                'd4': self.data["d4"],
                'fueldid': fueldid
            }
            data = {
                'tt_id': id,
                'followed': "",
            }
            r = requests.post('https://tohyotalk.com/api/saveuserfollowuser.json',
                              cookies=cookies, headers=self.headers, data=data, proxies=proxies)
            if self.debug:
                print(r.text)
            if json.loads(r.text)["status"] == 0:
                if self.debug:
                    print({
                        "status": True
                    })
                return {
                    "status": True
                }
            else:
                if self.debug:
                    print({
                        "status": False
                    })
                return {
                    "status": False
                }
        else:
            if self.debug:
                print({
                    "status": False
                })
            return {
                "status": False
            }

    def like(self, msgId, proxy=None):
        if not self.data == None:
            fueldid = self.get_fueldid(proxy)
            proxies = {
                "http": proxy,
                "https": proxy,
            }
            cookies = {
                'sf': '4',
                'PHPSESSID': self.data["PHPSESSID"],
                'user_id': self.data["user_id"],
                'd4': self.data["d4"],
                'fueldid': fueldid
            }
            data = {
                'msg_id': msgId,
                'eval_mode': 'plus',
            }
            r = requests.post('https://tohyotalk.com/api/evalmsg.json',
                              cookies=cookies, headers=self.headers, data=data, proxies=proxies)
            if self.debug:
                print(r.text)
            if json.loads(r.text)["status"] == 0:
                if self.debug:
                    print({
                        "status": True
                    })
                return {
                    "status": True
                }
            else:
                if self.debug:
                    print({
                        "status": False
                    })
                return {
                    "status": False
                }
        else:
            if self.debug:
                print({
                    "status": False
                })
            return {
                "status": False
            }

    def game(self, score, proxy=None):
        if not self.data == None:
            fueldid = self.fueldid
            proxies = {
                "http": proxy,
                "https": proxy,
            }
            cookies = {
                'sf': '4',
                'PHPSESSID': self.data["PHPSESSID"],
                'user_id': self.data["user_id"],
                'd4': self.data["d4"],
                'fueldid': fueldid
            }
            data = {
                'game_id': '1',
                'game_version': '1',
                'score': score,
                'play_id': '',
            }
            r = requests.post('https://tohyotalk.com/api/saveusergamescore.json',
                              cookies=cookies, headers=self.headers, data=data, proxies=proxies)
            if self.debug:
                print(r.text)
            if json.loads(r.text)["status"] == 0:
                if self.debug:
                    print({
                        "status": True,
                        "rank": json.loads(r.text)["this_rank"]
                    })
                return {
                    "status": True,
                    "rank": json.loads(r.text)["this_rank"]
                }
            else:
                if self.debug:
                    print({
                        "status": False
                    })
                return {
                    "status": False
                }
        else:
            if self.debug:
                print({
                    "status": False
                })
            return {
                "status": False
            }

    def icon(self, icon_path, proxy=None):
        if not self.data == None:
            fueldid = self.fueldid
            proxies = {
                "http": proxy,
                "https": proxy,
            }
            cookies = {
                'sf': '4',
                'PHPSESSID': self.data["PHPSESSID"],
                'user_id': self.data["user_id"],
                'd4': self.data["d4"],
                'fueldid': fueldid
            }
            fields = {
                'file': (icon_path, open(icon_path, 'rb'), "image/png"),
                'file_id': "0"
            }
            boundary = '----WebKitFormBoundary' \
                + ''.join(random.sample(string.ascii_letters + string.digits, 16))
            data = MultipartEncoder(
                fields=fields, boundary=boundary)
            headers = {
                'authority': 'tohyotalk.com',
                'accept': 'application/json, text/javascript, */*; q=0.01',
                'accept-language': 'ja',
                'content-keep': 'on',
                'content-type': data.content_type,
                'origin': 'https://tohyotalk.com',
                'referer': 'https://tohyotalk.com/account/id',
                'sec-fetch-dest': 'empty',
                'sec-fetch-mode': 'cors',
                'sec-fetch-site': 'same-origin',
                'user-agent': 'Mozilla/5.0 (iPad; CPU OS 13_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) CriOS/87.0.4280.77 Mobile/15E148 Safari/604.1 Edg/112.0.0.0',
                'x-requested-with': 'XMLHttpRequest',
            }
            r = requests.post('https://tohyotalk.com/api/uploadimg.json',
                              cookies=cookies, headers=headers, data=data, proxies=proxies
                              )
            if json.loads(r.text)["status"] == 0:
                x, y = Image.open(BytesIO(requests.get(
                    json.loads(r.text)["uploaded_file_url"]).content)).size
                data = {
                    'uploaded_file_name': json.loads(r.text)["uploaded_file_name"],
                    'zoom': '0.1667',
                    'x1': '0',
                    'y1': '0',
                    'x2': x,
                    'y2': y,
                }
                r = requests.post('https://tohyotalk.com/api/cropimg.json',
                                  cookies=cookies, headers=self.headers, data=data, proxies=proxies)
                if json.loads(r.text)["status"] == 0:
                    if self.debug:
                        print({
                            "status": True
                        })
                    return {
                        "status": True
                    }
                else:
                    if self.debug:
                        print({
                            "status": False
                        })
                    return {
                        "status": False
                    }
            else:
                if self.debug:
                    print({
                        "status": False
                    })
                return {
                    "status": False
                }
        else:
            if self.debug:
                print({
                    "status": False
                })
            return {
                "status": False
            }

    def profile(self, content, proxy=None):
        if not self.data == None:
            fueldid = self.fueldid
            proxies = {
                "http": proxy,
                "https": proxy,
            }
            cookies = {
                'sf': '4',
                'PHPSESSID': self.data["PHPSESSID"],
                'user_id': self.data["user_id"],
                'd4': self.data["d4"],
                'fueldid': fueldid
            }
            data = {
                'tt_id': self.data["userId"],
                'content': content
            }
            r = requests.post('https://tohyotalk.com/api/saveprofilecontent.json',
                              cookies=cookies, headers=self.headers, data=data, proxies=proxies)
            if self.debug:
                print(r.text)
            if json.loads(r.text)["status"] == 0:
                if self.debug:
                    print({
                        "status": True
                    })
                return {
                    "status": True
                }
            else:
                if self.debug:
                    print({
                        "status": False
                    })
                return {
                    "status": False
                }
        else:
            if self.debug:
                print({
                    "status": False
                })
            return {
                "status": False
            }
