from tqdm import tqdm
import requests,time,sys,os,colorama
from bs4 import BeautifulSoup
from urllib.parse import urlparse
from icecream import ic


ic.disable()
colorama.init()
OUTPUT_FILE='new_discovered_domains'
processed_domains=[]
if os.path.isfile('processed_domains.txt'):processed_domains=open('processed_domains.txt','r').read().splitlines()

def save_processed_domains(domain):
	ic()
	with open('processed_domains.txt','a+')as file:file.write(f"{domain}\n")
	
def log_new_domain(domain,filename=OUTPUT_FILE):
	ic()
	try:
		with open(filename,'a+')as f:f.write(domain+'\n')
	except Exception as e:print(f"\nError writing new domain {domain} to log file: {e}")
	
def extract_domains_from_page(html_content):
	ic()
	try:
		domains=[];soup=BeautifulSoup(html_content,'html.parser')
		for a_tag in soup.find_all('a',href=True):url=a_tag['href'];domain=urlparse(url).netloc;domains.append(domain);unique_domains=list(set(domain for domain in domains if domain.strip()))
		for d in unique_domains:print(f"New domain discovered: {colorama.Fore.GREEN}{d}{colorama.Style.RESET_ALL}");log_new_domain(d)
	except Exception as e:print(f"\nError while extracting domains: {e}")
	
def log_failed_domain(domain,filename='failed_domains.txt'):
	ic()
	try:
		with open(filename,'a+')as f:f.write(domain+'\n')
	except Exception as e:print(f"Error writing failed domain {domain} to log file: {e}")
	
def process_domains(domain,max_retries=3,retry_delay=10,failed_log_file='failed_domains.txt'):
	domain=domain.strip();retries=0;print('\n')
	with tqdm(total=max_retries,desc=domain,leave=False,ncols=100)as pbar:
		while retries<max_retries:
			try:
				response=requests.get(f"http://{domain}",timeout=5,headers={'User-Agent':'Mozilla/5.0 (Linux; Android 13; SM-S911U Build/TP1A.220624.014; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/111.0.5563.116 Mobile Safari/537.36 [FB_IAB/FB4A;FBAV/404.0.0.26.70;]'});response.raise_for_status()
				if response.status_code==200:
					if response.headers.get('Server')=='GitHub.com':pbar.set_postfix({'Status':'Valid (GitHub.com)'});print('\n');f=open(OUTPUT_FILE+'.github','a+');f.write(domain+'\n');f.close()
					extract_domains_from_page(response.text);break
			except requests.exceptions.ConnectionError:retries+=1;pbar.update(1)
			except requests.exceptions.Timeout:retries+=1;pbar.update(1)
			except requests.exceptions.HTTPError as e:pbar.set_postfix({'Status':'Domain Issue'});log_failed_domain(domain,failed_log_file);break
			except requests.exceptions.RequestException as e:retries+=1;pbar.update(1)
			if retries>=max_retries:pbar.set_postfix({'Status':'Failed'});os.system('clear');print(f"{colorama.Fore.RED}{domain}{colorama.Style.RESET_ALL}");log_failed_domain(domain,failed_log_file)
			time.sleep(retry_delay)
	save_processed_domains(domain)

try:
	filename=sys.argv[1]
	with open(filename,'r')as file:
		all_domains=file.read().splitlines()
		for domain in all_domains:
			if domain in processed_domains:continue
			process_domains(domain)
	print('All domains have been processed')
except Exception as err:print(f"Usage: python main.py <filename>\n{err}")
