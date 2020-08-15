import argparse
import requests as req
import threading
from queue import Queue
import sys

#---------------------------------------------------------------------------
#author:- Gagan_YK_Poojary aka SaffronShot
#ThanksTo:- TheCyberMentor, TryHackMe, TechWithTim and FreeCodeCamp
print("-"*70)
print('''
        author:- Gagan_YK_Poojary aka SaffronShot

ThanksTo:- TheCyberMentor, TryHackMe, TechWithTim and FreeCodeCamp ''')
print("-"*70)
#---------------------------------------------------------------------------

#Building commandline arguments and help menu using argparse.
parser=argparse.ArgumentParser(description="This program is a wordlist based directory bruteforcer (Non-Recursive).")
parser.add_argument("-u","--url",type=str,required=True,help="Specify the target in URL format, eg:- http://www.tryhackme.com/ .")
parser.add_argument("-w","--wordlist",type=str,required=True,help="Specify the wordlist file path,eg;- /usr/share/wordlists/dirb/common.txt.")
parser.add_argument("-t","--threads",type=int,required=True,help="Specify the number of threads.")
args=parser.parse_args()

#Checking if url and its format is correct
try:
	check=req.get(args.url)
	if 200<=check.status_code<400:
		print("The URL is valid.Undertaking further actions..")
		if args.url[-1]!="/":
			args.url=args.url+"/"
	else:
		print("Cannot reach the target;Check the URL and connection.")
		exit()
except:
	print("Cannot reach the target;Check the URL and connection.")
	exit()

#copying all the words from given wordlist to queue.
wordQue=Queue()
try:
	with open(args.wordlist,"r") as wd:
		for word in wd.readlines():
			wordQue.put(word.strip("\n"))
	print("Wordlist prepared..")
except:
	print(f"Wordlist {args.wordlist} does not exist")
	exit()

#Some not so important stuffs to decorate the output
print("-"*70)
count=1
total=wordQue.qsize()

#defining a checker function that pings a given directory to check if it is available.
alive=True
def checker():
	global alive
	while alive:
		if wordQue.not_empty:
			word=wordQue.get()
			try:
				response=req.get(str(args.url+word))
				status=response.status_code
				if 200<=status<400:
					output_data(word,status,"SUCCESS")
				else:
					output_data(word,status,"")
			except:
				break

#defining ouput_data function that controls output on the terminal
def output_data(word,status,call):
	global count,total
	print(f"{count}/{total}:- {word}--->{status}\t{call}")
	count+=1
	if count>total:
		alive=False
		exit()

#code to create and maintain threads
threadlist=[]

for thread in range(args.threads):
	threadlist.append(threading.Thread(target=checker))

for thread in threadlist:
	thread.start()

for thread in threadlist:	
	thread.join()

