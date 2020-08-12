import argparse
import requests as req

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
parser.add_argument("-w","--wordlist",type=str,required=True,help="Specify the wordlist file path,eg;- /usr/share/wordlists/dirb/common.txt")
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

#copying all words from wordlist file to a list
with open(args.wordlist,"r") as wd:
	words=[x.strip("\n") for x in wd.readlines()]

print("Wordlist prepared..")

#Some not so important stuffs to decorate the output
print("-"*70)
count=1
total=len(words)

#Checking response for each word and outputting it on screen.
for word in words:
	print("{}/{}".format(count,total),end=":- ")
	print(word,end="--->")
	response=req.get(str(args.url+word))
	print(response.status_code,end="\t")
	if 200<=response.status_code<400:
		print("[SUCCESS]")
	else:
		print("")
	count+=1

