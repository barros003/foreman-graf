import json
import sys
import requests


SAT = "192.168.213.98"
SAT_API = f"https://{SAT}/api/"
USERNAME = "admin"
PASSWORD = "deltas"
SSL_VERIFY = False

def get_json(url):
    r = requests.get(url, auth=(USERNAME, PASSWORD), verify=SSL_VERIFY)
    return r.json()

def get_errata_count_by_host(url):
    resultsjson = get_json(url)
    if resultsjson:
         data = resultsjson["content_facet_attributes"]["errata_counts"]
         for key, value in data.items():
            print(key, value)  
         
         #securitypatch = resultsjson["content_facet_attributes"]["errata_counts"]["security"]
         #bugfixpatch = resultsjson["content_facet_attributes"]["errata_counts"]["bugfix"]
         #enhancementpatch = resultsjson["content_facet_attributes"]["errata_counts"]["enhancement"]
         #total = resultsjson["content_facet_attributes"]["errata_counts"]["total"]
         #print("totalpatch: " + str(total))

def get_errata_count_all(url):
    resultsjson = get_json(url)
    if resultsjson:
        data = resultsjson["results"]["content_facet_attributes"]
        for host in data.items():
            print(str(host["cert_name"]))
            print(str(host["errata_counts"]))


def main():
    host = "oracle7"    
    #get_errata_count_by_host(SAT_API + 'hosts/' + host)
    get_errata_count_all(SAT_API + 'hosts/')

if __name__ == "__main__":
    main()
