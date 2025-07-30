import requests
from urllib.parse import quote
API_KEY = None

def checkStatus():
    try:
        response = requests.get('https://api.loopy5418.dev/health', timeout=3)
        if response.status_code == 200 and response.text.strip() == 'OK':
            return True
        else:
            return False
    except Exception:
        return False

def setApiKey(apiKey: str):
    global API_KEY
    if not apiKey or not isinstance(apiKey, str):
        raise ValueError("Expected string in setApiKey")
    API_KEY = apiKey

def getApiKey():
    global API_KEY
    if API_KEY is None:
        raise ValueError("API Key not set yet. Set it with setApiKey(key: str)")
    return API_KEY

class airesp:
    def __init__(self, data):
        self.success = data.get("success", False)
        self.response = data.get("response", "")
        self.model = data.get("model", "")
        self.prompt = data.get("prompt", "")

def ai(prompt: str, speed=1):
    global API_KEY
    smap = {0: "large", 1: "balanced", 2: "fast"}
    if not API_KEY:
        raise ValueError("API Key not set yet. Set it with setApiKey(key: str)")
    if not prompt or not isinstance(prompt, str):
        raise ValueError("Expected string at position 1 in ai(prompt, speed)")
    if speed not in smap:
        raise ValueError("Invalid speed option! Please pick 0 (large), 1 (balanced, default) or 2 (fast)")
    url = f"https://api.loopy5418.dev/openai/text?prompt={requests.utils.quote(prompt)}&speed={smap[speed]}&key={API_KEY}"
    try:
        r = requests.get(url, timeout=40)
        r.raise_for_status()
        data = r.json()
        return airesp(data)
    except requests.exceptions.RequestException as e:
        return airesp({
            "success": False,
            "response": f"Request failed: {e}",
            "model": "",
            "prompt": prompt
        })

def owoify(text):
    if not text or not isinstance(text, str):
        raise ValueError("Expected string/int in owoify!")
    try:
        response = requests.get(f"https://api.loopy5418.dev/owoify?text={quote(text, safe="")}")
        response.raise_for_status()
        return response.json().get("result")
    except requests.exceptions.RequestException as e:
        return f"Error in owoify: {e}"

def emojify(text: str):
    if not text or not isinstance(text, str):
        raise ValueError("Expected string/int in emojify!")
    try:
        response = requests.get(f"https://api.loopy5418.dev/emojify?text={quote(text, safe="")}")
        response.raise_for_status()
        return response.json().get("result")
    except requests.exceptions.RequestException as e:
        return f"Error in emojify: {e}"
    
def qr(data: str):
    if not API_KEY:
        raise ValueError("API Key not set yet. Set it with setApiKey(key: str)")
    if not data or not isinstance(data, str):
        raise ValueError("Expected data in qr(data) to be a string!")
    try:
        response = requests.get(f"https://api.loopy5418.dev/qr?data={quote(data, safe="")}&key={API_KEY}")
        response.raise_for_status()
        return response.content
    except requests.exceptions.RequestException or TypeError as e:
        return f"Error in qr: {e}"


class currencyinfo:
    def __init__(self, data):
        self.rate = data.get("rate", "")
        self.converted = data.get("converted", "")
        self.amount = data.get("amount", "")
        self.success = data.get("success", False)

def currency(base: str, target: str, amount: int):
    if not base or not isinstance(base, str):
        raise ValueError("Expected 'base' at the first position in currency to be a string.")
    if not target or not isinstance(target, str):
        raise ValueError("Expected 'target' at the second position in currency to be a string.")
    if not amount or not isinstance(amount, int):
        raise ValueError("Expected 'amount' at the first position in currency to be an integer.")
    if not API_KEY:
        raise ValueError("API Key not set yet. Set it with setApiKey(key: str)")
    url = f"https://api.loopy5418.dev/currency-converter?base={quote(base, safe="")}&target={quote(target, safe="")}&amount={quote(str(amount), safe="")}&key={API_KEY}"
    try:
        r = requests.get(url, timeout=5)
        r.raise_for_status()
        data = r.json()
        return currencyinfo(data)
    except requests.exceptions.RequestException as e:
        return currencyinfo({
            "rate": "",
            "converted": "",
            "amount": "",
            "error": {e},
            "success": False
        })

def seconds_to_time(seconds: int):
    if not seconds or not isinstance(seconds, int):
        raise ValueError("Expected 'seconds' to be integer at first position in seconds_to_time")
    try:
        response = requests.get(f"https://api.loopy5418.dev/seconds-to-time?seconds={quote(str(seconds), safe="")}")
        response.raise_for_status()
        return response.json().get("formatted_time")
    except requests.exceptions.RequestException or TypeError as e:
        return f"Error in seconds_to_time: {e}"

def pick(*args):
    if not args:
        raise ValueError("Expected 'args' at first position in pick")
    try:
        response = requests.get(f"https://api.loopy5418.dev/choose?options={quote(','.join(str(arg) for arg in args), safe="")}")
        response.raise_for_status()
        return response.json().get("result")
    except requests.exceptions.RequestException or TypeError as e:
        return f"Error in pick: {e}"

def ascii_art(text: str):
    if not text or not isinstance(text, str):
        raise ValueError("Expected 'text' as string at first position in ascii_art")
    try:
        response = requests.get(f"https://api.loopy5418.dev/ascii-art?text={quote(text, safe="")}")
        response.raise_for_status()
        return response.json().get("ascii_art")
    except requests.exceptions.RequestException or TypeError as e:
        return f"Error in ascii_art: {e}"