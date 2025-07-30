import requests
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
    if apiKey is None:
        raise ValueError("maybe try inputting a key???? the function name is literally setApiKey")
    API_KEY = apiKey

def getApiKey():
    global API_KEY
    if API_KEY is None:
        raise ValueError("fucking dumbass you didnt set apikey yet")
    return API_KEY

class airesp:
    def __init__(self, data):
        self.success = data.get("success", False)
        self.response = data.get("response", "")
        self.model = data.get("model", "")
        self.prompt = data.get("prompt", "")

def ai(prompt, speed=1):
    global API_KEY
    smap = {0: "large", 1: "balanced", 2: "fast"}
    if not API_KEY:
        raise ValueError("you didnt set a key dumbass")
    if speed not in smap:
        raise ValueError("invalid speed brbrbrbrbr")
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
