import json
import sys
import requests


SAT = "192.168.213.98"
SAT_API = f"https://{SAT}/api/"
USERNAME = "admin"
PASSWORD = "qjsqulVPKyvDGRwVPLIaNQ"
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


def get_errata_count_all():
    url = SAT_API + 'hosts/'
    resultsjson = get_json(url)
    security_count = 0
    bugfix_count = 0
    enhancement_count = 0
    if resultsjson:
        data = resultsjson["results"]
        total = resultsjson["total"]
        for entry in data:
           if "content_facet_attributes" in entry:
              if entry["content_facet_attributes"]["errata_counts"]["security"] > 0:
                security_count += 1
                #print(entry["certname"],"Security",entry["content_facet_attributes"]["errata_counts"]["security"])
              if entry["content_facet_attributes"]["errata_counts"]["bugfix"] > 0:
                bugfix_count += 1
                #print(entry["certname"],"Bugfix",entry["content_facet_attributes"]["errata_counts"]["bugfix"])                
              if entry["content_facet_attributes"]["errata_counts"]["enhancement"] > 0:
                enhancement_count += 1
                #print(entry["certname"],"enhancement",entry["content_facet_attributes"]["errata_counts"]["enhancement"])

    return security_count,  bugfix_count,  enhancement_count, total
    #print (security_count, bugfix_count, enhancement_count)

def main():
    host = "oracle7"    
    #get_errata_count_by_host(SAT_API + 'hosts/' + host)
    #get_errata_count_all()

if __name__ == "__main__":
    main()
