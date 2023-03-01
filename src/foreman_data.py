import requests
import logging
import os
import sys
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

FOREMAN = os.environ.get('FOREMAN_HOST')
FOREMAN_API = f"https://{FOREMAN}/api/v2/"
USERNAME = os.environ.get('FOREMAN_USER')
PASSWORD = os.environ.get('FOREMAN_TOKEN')
SSL_VERIFY = False
ORG_ID = os.environ.get('FOREMAN_ORGID')

root = logging.getLogger()
root.setLevel(logging.DEBUG)
handler = logging.StreamHandler(sys.stdout)
handler.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
root.addHandler(handler)

def main_erratum():
  
   try:

      totalpages = get_totalhosts()

      if totalpages:
        url = FOREMAN_API + f"hosts?search=hypervisor%20%3D%20false%20and%20organization_id={ORG_ID}&per_page={totalpages}"
        logging.info(f"getting info: {url}")
        r = requests.get(url, auth=(USERNAME, PASSWORD), verify=SSL_VERIFY)
        r.raise_for_status()
        errata_count  = get_errata_count_all(r.json())
        errata_byhost = get_errata_count_by_host(r.json())
      else:
        logging.error(f"Cannot connect to {url}")

   except requests.exceptions.HTTPError as err:
      logging.error(f"Cannot access the endpoint: {url}") 
   except requests.exceptions.Timeout as errt:
      logging.error(f"Timeout accessing: {url}")  
     
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
             
             lifecycle = entry["content_facet_attributes"]["lifecycle_environment_name"]  
             osname    = str(entry["operatingsystem_name"])

             security_count = entry["content_facet_attributes"]["errata_counts"]["security"]
             erratum.update({f"sec{count}" : {"host": hostname, "errata_type": "security", "errata_count": security_count, "lifecycle": lifecycle, "osname": osname }})              
             
             bugfix_count = entry["content_facet_attributes"]["errata_counts"]["bugfix"]               
             erratum.update({f"bug{count}": {"host": hostname, "errata_type": "bugfix", "errata_count": bugfix_count, "lifecycle": lifecycle, "osname": osname }})   
             
             enhancement_count = entry["content_facet_attributes"]["errata_counts"]["enhancement"]                
             erratum.update({f"enha{count}": {"host": hostname, "errata_type": "enhancement", "errata_count": enhancement_count, "lifecycle": lifecycle, "osname": osname }})      

             packages_count = entry["content_facet_attributes"]["upgradable_package_count"]               
             erratum.update({f"pack{count}": {"host": hostname, "errata_type": "totalpackages", "errata_count": packages_count, "lifecycle": lifecycle, "osname": osname }})          
                                     
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

    return security_count, bugfix_count, enhancement_count, total

def get_totalhosts ():
 
 try:

   url = FOREMAN_API + f"hosts?search=hypervisor%20%3D%20false%20and%20organization_id={ORG_ID}"
   logging.info(f"get total hosts:{url}")
   r = requests.get(url, auth=(USERNAME, PASSWORD), verify=SSL_VERIFY)
   totalhosts = r.json()   
   return totalhosts["subtotal"]
 except:
   logging.error(f"Cannot access the endpoint: {url}")