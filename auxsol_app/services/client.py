import requests
import os


class AuxsolClient:
    BASE_URL = "https://eu.auxsolcloud.com/auxsol-api"
    HOME_URL = "https://www.auxsolcloud.com/"

    def __init__(self):
        self.username = os.getenv("AUX_USER", "").strip()
        self.password = os.getenv("AUX_PASS", "").strip()
        self.session = requests.Session()

        # Sarlavhalarni brauzer bilan bir xil qilamiz
        self.session.headers.update({
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:147.0) Gecko/20100101 Firefox/147.0",
            "Accept": "application/json, text/plain, */*",
            "Accept-Language": "en-US,en;q=0.5",
            "Content-Type": "application/json;charset=utf-8",
            "Origin": "https://www.auxsolcloud.com",
            "Referer": "https://www.auxsolcloud.com/",
            "Connection": "keep-alive"
        })

    def login(self):
        try:
            self.session.get(self.HOME_URL, timeout=10)
            url = f"{self.BASE_URL}/auth/login"
            payload = {"account": self.username, "password": self.password, "lang": "en-US"}

            response = self.session.post(url, json=payload, timeout=10)
            res_json = response.json()

            if res_json.get("code") == "AWX-0000":
                # DEBUG'da ko'ringan 'access_token' kalitini olamiz
                token = res_json.get("data", {}).get("access_token")

                if token:
                    self.session.headers.update({
                        "Authorization": f"Bearer {token}",
                        "token": token,  # Ba'zan kichik harfda ham so'raladi
                        "language": "2"
                    })
                    return True

            print(f"❌ Login xatosi: {res_json.get('msg')}")
            return False
        except Exception as e:
            print(f"🔥 Login Error: {e}")
            return False

    def get_solar_data(self, plant_id):
        url = f"{self.BASE_URL}/analysis/plantReport/queryPlantCurrentDataAll?plantId={plant_id}"
        try:
            # Login vaqtida o'rnatilgan headerlar va cookielar bilan so'rov yuboramiz
            response = self.session.get(url, timeout=15)
            return response.json()
        except Exception as e:
            print(f"🔥 Data Error: {e}")
            return None