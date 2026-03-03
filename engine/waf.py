import requests

def detect_waf(target):
    try:
        r = requests.get(target)
        headers = str(r.headers).lower()
        if "cloudflare" in headers:
            return "Cloudflare Detected"
        if "akamai" in headers:
            return "Akamai Detected"
    except:
        pass
    return "No WAF Detected"
