#!/usr/bin/env python3

import os
import sys
import platform
import time

ver = platform.python_version()

if (ver <= '3'):
        print("\033[91m This isn't compatible with python2 use python 3.x\033[00m")
        sys.exit(1)

import argparse
import concurrent.futures

parser = argparse.ArgumentParser(description="""\033[93m[~] Domain status code checker by khoabda
									https://matuhn.github.io\033[00m""")

group = parser.add_mutually_exclusive_group()
												#Taking arguments from CLI
parser.add_argument("-v","--verbose", help="verbose (status code + dig domain)",action="store_true")

parser.add_argument("-o","--output", help="write active domains in new file" ,metavar='out-file')

parser.add_argument("-t","--threads", help="number of concurrent threads" ,type=int,metavar="Threads")

group.add_argument("-f","--file", help="File which consist domains(sub.example.com)",metavar="Input file")

group.add_argument("-u","--url", help="single domain check",metavar="URL")

args = parser.parse_args()

verbose = args.verbose
file = args.file
url = args.url
output = args.output
threads = args.threads
os.popen("rm -f "+output)
										#Just A fancy banner!
print("""\033[91m
#    # #    #  ####    ##   #####  #####    ##   #####  ######  ####   ####  #    # 
#   #  #    # #    #  #  #  #    # #    #  #  #  #    # #      #    # #    # ##   # 
####   ###### #    # #    # #####  #    # #    # #    # #####  #      #    # # #  # 
#  #   #    # #    # ###### #    # #    # ###### #####  #      #      #    # #  # # 
#   #  #    # #    # #    # #    # #    # #    # #   #  #      #    # #    # #   ## 
#    # #    #  ####  #    # #####  #####  #    # #    # ######  ####   ####  #    # \033[00m

					\033[93m v1.0 By khoabda\033[00m
""")


if verbose:
	print("\033[93m[~] Verbosity is enabled..\033[00m")

if not threads:										#default number of threads
	threads = 20

t = time.time()

def recce(domain):
								#This function will make request to domain
	checkStatus = "curl -I " + domain + " -s -m 15 --write-out %{http_code} --output /dev/null"
	checkIp = "dig +short " + domain

	statusCode = os.popen(checkStatus).read().rstrip()
	ipDomain = os.popen(checkIp).read().rstrip()

	# Maybe can dig many ip, so use \n despite of " "
	result = ipDomain+"\n"+statusCode

	return result


def check(data,domain):
	data = data.split("\n")
	#1 domain can have different ip after dig 
	if verbose:
		if (data[len(data)-1] == "000"):
			print("\033[91m[~] ",data[len(data)-1] , "\n	[-] ", domain[:-1] , " is DOWN \033[00m")
		elif (data[len(data)-1] == "200"):
			if output:
				print("\033[92m[~] ",data[len(data)-1] , "\n 	[+]  DIG Domain: ",data[0:(len(data)-1)],"\n 	[+] ", domain[:-1] , " is ALIVE \033[00m")
				print("\033[92m[~] ",data[len(data)-1] , "\n 	[+]  DIG Domain: ",data[0:(len(data)-1)],"\n 	[+] ", domain[:-1] , " is ALIVE \033[00m", file =open(output, "a"))
			else:
				print("\033[92m[~] ",data[len(data)-1] , "\n 	[+]  DIG Domain: ",data[0:(len(data)-1)],"\n 	[+] ", domain[:-1] , " is ALIVE \033[00m")
		elif (data[len(data)-1] == "301"):
			if output:
				print("\033[34m[~] ",data[len(data)-1] , "\n 	[+]  DIG Domain: ",data[0:(len(data)-1)],"\n 	[+] ", domain[:-1] , " is MOVED PERMANENTLY \033[00m")
				print("\033[34m[~] ",data[len(data)-1] , "\n 	[+]  DIG Domain: ",data[0:(len(data)-1)],"\n 	[+] ", domain[:-1] , " is MOVED PERMANENTLY \033[00m", file =open(output, "a"))
			else:
				print("\033[34m[~] ",data[len(data)-1] , "\n 	[+]  DIG Domain: ",data[0:(len(data)-1)],"\n 	[+] ", domain[:-1] , " is MOVED PERMANENTLY \033[00m")
		elif (data[len(data)-1] == "302"):
			if output:
				print("\033[34m[~] ",data[len(data)-1] , "\n 	[+]  DIG Domain: ",data[0:(len(data)-1)],"\n 	[+] ", domain[:-1] , " is MOVED TEMPORARILY \033[00m")
				print("\033[34m[~] ",data[len(data)-1] , "\n 	[+]  DIG Domain: ",data[0:(len(data)-1)],"\n 	[+] ", domain[:-1] , " is MOVED TEMPORARILY \033[00m", file =open(output, "a"))
			else:
				print("\033[34m[~] ",data[len(data)-1] , "\n 	[+]  DIG Domain: ",data[0:(len(data)-1)],"\n 	[+] ", domain[:-1] , " is MOVED TEMPORARILY \033[00m")
		elif (data[len(data)-1] == "400"):
			if output:
				print("\033[33m[~] ",data[len(data)-1] , "\n 	[+]  DIG Domain: ",data[0:(len(data)-1)],"\n 	[+] ", domain[:-1] , " is BAD REQUEST \033[00m")
				print("\033[33m[~] ",data[len(data)-1] , "\n 	[+]  DIG Domain: ",data[0:(len(data)-1)],"\n 	[+] ", domain[:-1] , " is BAD REQUEST \033[00m", file =open(output, "a"))
			else:
				print("\033[33m[~] ",data[len(data)-1] , "\n 	[+]  DIG Domain: ",data[0:(len(data)-1)],"\n 	[+] ", domain[:-1] , " is BAD REQUEST \033[00m")
		elif (data[len(data)-1] == "403"):
			if output:
				print("\033[33m[~] ",data[len(data)-1] , "\n 	[+]  DIG Domain: ",data[0:(len(data)-1)],"\n 	[+] ", domain[:-1] , " is NEED AUTHORIZED \033[00m")
				print("\033[33m[~] ",data[len(data)-1] , "\n 	[+]  DIG Domain: ",data[0:(len(data)-1)],"\n 	[+] ", domain[:-1] , " is NEED AUTHORIZED \033[00m", file =open(output, "a"))
			else:
				print("\033[33m[~] ",data[len(data)-1] , "\n 	[+]  DIG Domain: ",data[0:(len(data)-1)],"\n 	[+] ", domain[:-1] , " is NEED AUTHORIZED \033[00m")
		elif (data[len(data)-1] == "404"):
			if output:
				print("\033[33m[~] ",data[len(data)-1] , "\n 	[+]  DIG Domain: ",data[0:(len(data)-1)],"\n 	[+] ", domain[:-1] , " is NOT FOUND \033[00m")
				print("\033[33m[~] ",data[len(data)-1] , "\n 	[+]  DIG Domain: ",data[0:(len(data)-1)],"\n 	[+] ", domain[:-1] , " is NOT FOUND \033[00m", file =open(output, "a"))
			else:
				print("\033[33m[~] ",data[len(data)-1] , "\n 	[+]  DIG Domain: ",data[0:(len(data)-1)],"\n 	[+] ", domain[:-1] , " is NOT FOUND \033[00m")
		elif (data[len(data)-1] == "405"):
			if output:
				print("\033[33m[~] ",data[len(data)-1] , "\n 	[+]  DIG Domain: ",data[0:(len(data)-1)],"\n 	[+] ", domain[:-1] , " is METHOD NOT ALLOWED \033[00m")
				print("\033[33m[~] ",data[len(data)-1] , "\n 	[+]  DIG Domain: ",data[0:(len(data)-1)],"\n 	[+] ", domain[:-1] , " is METHOD NOT ALLOWED \033[00m", file =open(output, "a"))
			else:
				print("\033[33m[~] ",data[len(data)-1] , "\n 	[+]  DIG Domain: ",data[0:(len(data)-1)],"\n 	[+] ", domain[:-1] , " is METHOD NOT ALLOWED \033[00m")
		elif (data[len(data)-1] == "500"):
			if output:
				print("\033[36m[~] ",data[len(data)-1] , "\n 	[+]  DIG Domain: ",data[0:(len(data)-1)],"\n 	[+] ", domain[:-1] , " is INTERNAL SERVER ERROR \033[00m")
				print("\033[36m[~] ",data[len(data)-1] , "\n 	[+]  DIG Domain: ",data[0:(len(data)-1)],"\n 	[+] ", domain[:-1] , " is INTERNAL SERVER ERROR \033[00m", file =open(output, "a"))
			else:
				print("\033[36m[~] ",data[len(data)-1] , "\n 	[+]  DIG Domain: ",data[0:(len(data)-1)],"\n 	[+] ", domain[:-1] , " is INTERNAL SERVER ERROR \033[00m")
		elif (data[len(data)-1] == "501"):
			if output:
				print("\033[36m[~] ",data[len(data)-1] , "\n 	[+]  DIG Domain: ",data[0:(len(data)-1)],"\n 	[+] ", domain[:-1] , " is NOT IMPLEMENTED \033[00m")
				print("\033[36m[~] ",data[len(data)-1] , "\n 	[+]  DIG Domain: ",data[0:(len(data)-1)],"\n 	[+] ", domain[:-1] , " is NOT IMPLEMENTED \033[00m", file =open(output, "a"))
			else:
				print("\033[36m[~] ",data[len(data)-1] , "\n 	[+]  DIG Domain: ",data[0:(len(data)-1)],"\n 	[+] ", domain[:-1] , " is NOT IMPLEMENTED \033[00m")
		elif (data[len(data)-1] == "502"):
			if output:
				print("\033[36m[~] ",data[len(data)-1] , "\n 	[+]  DIG Domain: ",data[0:(len(data)-1)],"\n 	[+] ", domain[:-1] , " is BAD GATEWAY \033[00m")
				print("\033[36m[~] ",data[len(data)-1] , "\n 	[+]  DIG Domain: ",data[0:(len(data)-1)],"\n 	[+] ", domain[:-1] , " is BAD GATEWAY \033[00m", file =open(output, "a"))
			else:
				print("\033[36m[~] ",data[len(data)-1] , "\n 	[+]  DIG Domain: ",data[0:(len(data)-1)],"\n 	[+] ", domain[:-1] , " is BAD GATEWAY \033[00m")
		elif (data[len(data)-1] == "503"):
			if output:
				print("\033[36m[~] ",data[len(data)-1] , "\n 	[+]  DIG Domain: ",data[0:(len(data)-1)],"\n 	[+] ", domain[:-1] , " is SERVICE UNAVAILABLE \033[00m")
				print("\033[36m[~] ",data[len(data)-1] , "\n 	[+]  DIG Domain: ",data[0:(len(data)-1)],"\n 	[+] ", domain[:-1] , " is SERVICE UNAVAILABLE \033[00m", file =open(output, "a"))
			else:
				print("\033[36m[~] ",data[len(data)-1] , "\n 	[+]  DIG Domain: ",data[0:(len(data)-1)],"\n 	[+] ", domain[:-1] , " is SERVICE UNAVAILABLE \033[00m")
		else:
			if output:
				print("\033[00m[~] ",data[len(data)-1] , "\n 	[+]  DIG Domain: ",data[0:(len(data)-1)],"\n 	[+] ", domain[:-1] , " is <NOT YET IMPLEMENTED THIS STATUS CODE> \033[00m")
				print("\033[00m[~] ",data[len(data)-1] , "\n 	[+]  DIG Domain: ",data[0:(len(data)-1)],"\n 	[+] ", domain[:-1] , " is <NOT YET IMPLEMENTED THIS STATUS CODE> \033[00m", file =open(output, "a"))
			else:
				print("\033[00m[~] ",data[len(data)-1] , "\n 	[+]  DIG Domain: ",data[0:(len(data)-1)],"\n 	[+] ", domain[:-1] , " is <NOT YET IMPLEMENTED THIS STATUS CODE> \033[00m")
	else:
		if (data[len(data)-1] == "000"):
			print("\033[91m[!] Domain " , domain[:-1] ," is DOWN \033[00m")
		else:
			print("\033[92m[~] Domain " , domain[:-1] , " is ALIVE \033[00m")
			if output:
				with open(output,"a") as output_file:						#Writing output to new file
					output_file.write(domain)

if file:

	if os.path.isfile(file):
		num_domains = 0

		with open(file,"r") as f:
			for domain in f:
				num_domains += 1
		f.close()

		print("\033[92m[~] Total number of domains found in the file are: ", num_domains,"\033[00m")

		with open(file,"r") as f:

			pool = concurrent.futures.ThreadPoolExecutor(max_workers=threads)

		#Start the load operations and mark each future with its domain

			futures = {pool.submit(recce,domain[:-1]):domain for domain in f}

			for future in concurrent.futures.as_completed(futures):
				domain = futures[future]

				try:
					data = future.result()

					check(data,domain)

				except Exception as exc:

					print('%r generated an exception: %s' % (domain, exc))

	else:
		print("\033[91m[!] File not found..\033[00m")
		sys.exit(1)

if url:													#For single domain check
	check = "curl -I " + url + " -s -m 15 --write-out %{http_code} --output /dev/null/"

	answer = os.popen(check)

	if answer.read() == "000":
		print("\033[91m[!] Host ", url, " is down\033[00m")

	else:
		if verbose:
			print("\033[92m[~] Host ", url, "is live with status code: ",answer.read(),"\033[00m")
		else:
			print("\033[92m[~] Host ", url, "is live\033[00m")


print("\033[93m[~] Total time taken: " , time.time() -t , "\033[00m")