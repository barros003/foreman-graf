import json
import sys
import requests
import logging



SAT = "192.168.213.98"
#SAT = ""
SAT_API = f"https://{SAT}/api/"
USERNAME = "admin"
PASSWORD = "qjsqulVPKyvDGRwVPLIaNQ"
#USERNAME = ""
#PASSWORD = ""
SSL_VERIFY = False
ORG_ID = 3


def main_erratum():
   logging.basicConfig(level=logging.INFO, filename="main.log", format="%(asctime)s - %(levelname)s - %(message)s")
   try:
      
      url = SAT_API + f"v2/hosts?search=name%20!~%20virt-who*%20and%20organization_id={ORG_ID}&per_page=550"
      logging.info(f"Calling endpoint:{url}")
      r = requests.get(url, auth=(USERNAME, PASSWORD), verify=SSL_VERIFY)
      r.raise_for_status()
      errata_count  = get_errata_count_all(r.json())
      errata_byhost = get_errata_count_by_host(r.json())  
   except requests.exceptions.HTTPError as err:
      logging.error("Cannot access the endpoint:" + url + err) 
   except requests.exceptions.Timeout as errt:
      logging.error("Timeout accessing:" + url + errt)
       
  
   logging.info(f"Endpoint ok")
   return errata_count, errata_byhost

def get_errata_count_by_host(json_return):
    
    resultsjson = json_return
  
    if resultsjson:
         data = resultsjson["results"]
         erratum = dict()
         count = 1
         for entry in data:
           if "content_facet_attributes" in entry:             
             hostname = str(entry["certname"])

             security_count = entry["content_facet_attributes"]["errata_counts"]["security"]
             erratum.update({f"sec{count}" : {"host": hostname, "errata_type": "security", "errata_count": security_count }})              
             
             bugfix_count = entry["content_facet_attributes"]["errata_counts"]["bugfix"]               
             erratum.update({f"bug{count}": {"host": hostname, "errata_type": "bugfix", "errata_count": bugfix_count }})   
             
             enhancement_count = entry["content_facet_attributes"]["errata_counts"]["enhancement"]                
             erratum.update({f"enha{count}": {"host": hostname, "errata_type": "enhancement", "errata_count": enhancement_count }})
              
             count += 1

    return erratum  


def get_errata_count_all(json_return):
 
    resultsjson = json_return
    security_count = 0
    bugfix_count = 0
    enhancement_count = 0
    if resultsjson:
        data = resultsjson["results"]
        total = resultsjson["subtotal"]
        for entry in data:
           if "content_facet_attributes" in entry:
              if entry["content_facet_attributes"]["errata_counts"]["security"] > 0:
                security_count += 1
                
              if entry["content_facet_attributes"]["errata_counts"]["bugfix"] > 0:
                bugfix_count += 1
                            
              if entry["content_facet_attributes"]["errata_counts"]["enhancement"] > 0:
                enhancement_count += 1            

    return security_count,  bugfix_count,  enhancement_count, total
 

#def main():
    
    #get_errata_count_by_host("security")
    #testedict()
    

#if __name__ == "__main__":
#    main()