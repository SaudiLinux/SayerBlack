import requests

def find_subdomains(domain):
    subs = ["admin", "dev", "api", "test"]
    found = []

    domain = domain.replace("http://","").replace("https://","")

    for sub in subs:
        url = f"http://{sub}.{domain}"
        try:
            if requests.get(url, timeout=3).status_code < 400:
                found.append(url)
        except:
            pass

    return found
