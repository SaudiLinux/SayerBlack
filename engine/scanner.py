from concurrent.futures import ThreadPoolExecutor
from engine.crawler import crawl
from engine.waf import detect_waf
from engine.subdomain import find_subdomains
from engine.nmap_scan import nmap_scan

def run_full_scan(target, progress_callback, log_callback):

    results = {"vulns": {}, "network": {}}
    log_callback("INFO", f"Scanning {target}")

    with ThreadPoolExecutor(max_workers=4) as executor:
        future_crawl = executor.submit(crawl, target)
        future_waf = executor.submit(detect_waf, target)
        future_sub = executor.submit(find_subdomains, target)
        future_nmap = executor.submit(nmap_scan, target)

        progress_callback(40)
        results["vulns"]["Crawled URLs"] = future_crawl.result()

        progress_callback(60)
        results["vulns"]["WAF"] = future_waf.result()

        progress_callback(75)
        results["vulns"]["Subdomains"] = future_sub.result()

        progress_callback(90)
        results["network"] = future_nmap.result()

    return results
