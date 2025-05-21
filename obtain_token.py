import file_abbr as myfile
import json
import keyring
import re
import requests

from base64 import b64encode
from getpass import getpass

# Constants of the first month of TOTDs
NANDO_TOKEN = "https://prod.trackmania.core.nadeo.online/v2/authentication/token/"
UBI_TOKEN = "https://public-ubiservices.ubi.com/v3/profiles/sessions"

# Constants of keyring access data
AUTH_SERVICEID = "MY AUTHORIZATION!"
AUTH_USER = "USER MASK"

# Constants of file names
ACCESS_FILE = "access_token.txt"
REFRESH_FILE = "refresh_token.txt"

# GLOBAL VARIABLES FOR ACCESS TOKENS
access_token = ""
refresh_token = ""



# AuthorizationError - The login info was not entered or you're account is banned
class AuthorizationError(Exception):
	"Authorization failed when getting Ubisoft Ticket"
	pass
# RateLimitError - You have been rate limited by Ubisoft's API. Please write an
class RateLimitError(Exception):
	"Ubisoft's API rate limit exceeded. Please send a report on Github, ."
	pass
# AccessTokenError - The ACCESS token is not valid because it has expired
class AccessTokenError(Exception):
	"The access token has expired"
	pass
# RefreshTokenError - The REFRESH token is not valid because it has expired
class RefreshTokenError(Exception):
	"The refresh token has expired"
	pass


# Creates authorization parameters to access NadeoLiveServices
def ubisoft_login():
	print("Logging into Ubisoft Servers...")
	print("Please enter your UbisoftConnect account details below:")

	regex = re.compile(
		r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+'
	)
	while True:
		# enter login credentials
		email = input("\tEmail address: ")
		if not re.fullmatch(regex, email):
			print("\tThe provided email is invalid! Please re-enter!\n")
			continue
		password = getpass("\tPasword: ")

		# encode the file
		print("Checking credentials...")
		auth = str(b64encode(bytes(f"{email}:{password}", 'utf-8')))[2:-1]
		try:
			ubisoft_getticket(auth)
			break
		except AuthorizationError:
			print("\tERROR: Login information is incorrect! Please re-enter!\n")
	
	# create keyring
	print("\tEncrypting login data...")
	keyring.set_password(AUTH_SERVICEID, AUTH_USER, auth)


# Access Ubisoft servers
#	auth -> encrypted login info for Ubisoft servers
def ubisoft_getticket(auth: str):
	ubi_header = {
		"Content-Type": "application/json",
		"Ubi-AppId": "86263886-327a-4328-ac69-527f0d20a237",
		"Authorization": "Basic " + str(auth or ""),
		"User-Agent": "TOTDistribution v0.6.0 by TomatoServal"
	}

	ubi_response = requests.post(UBI_TOKEN, headers=ubi_header)

	# If the request is invalid
	if ubi_response.status_code == 401:
		raise AuthorizationError("You must log into your Ubisoft account!")
	elif ubi_response.status_code == 429:
		raise RateLimitError("Ubisoft's API rate limit exceeded. Please send a report on Github (README.md).")

	print(f"\tWelcome, {ubi_response.json()['nameOnPlatform']}!")
	return ubi_response.json()['ticket']


# Obtains an access and refresh token for NANDO's live servers. For technical 
# info on this process, visit "https://webservices.openplanet.dev/auth"
def nadeo_newtoken():
	global access_token, refresh_token
	# get Ubisoft ticket
	auth = keyring.get_password(AUTH_SERVICEID, AUTH_USER)
	ubi_token = ubisoft_getticket(auth)

	# accessing NANDO servers
	nando_url = NANDO_TOKEN + "ubiservices"
	nando_header = {
		"Content-Type": "application/json",
		"Authorization": "ubi_v1 t=" + ubi_token,
		"User-Agent": "TOTDistribution v0.6.0 by TomatoServal"
	}
	nando_body = {
		"audience": "NadeoLiveServices"
	}
	nando_response = requests.post(nando_url,            \
								   headers=nando_header, \
								   json=nando_body)

	nando_tokens = nando_response.json()
	access_token = nando_tokens['accessToken']
	refresh_token = nando_tokens['refreshToken']
	
	tokens_to_file()


# Obtains the data from 
def nadeo_refreshtoken():
	global access_token, refresh_token

	nando_url = NANDO_TOKEN + "refresh"
	nando_header = {
		"Authorization": "nadeo_v1 t=" + refresh_token
	}
	nando_response = requests.post(nando_url, headers=nando_header)

	if nando_response.status_code == 401:
		raise RefreshTokenError("The refresh token has expired!")

	nando_tokens = nando_response.json()
	access_token = nando_tokens['accessToken']
	refresh_token = nando_tokens['refreshToken']

	tokens_to_file()


# Prints both the access token and refresh token (obtained by the server token
# functions)
def tokens_to_file():
	global access_token, refresh_token
	# access token
	at_file = myfile.write_file(ACCESS_FILE)
	at_file.write(access_token)
	at_file.close()

	# refresh token
	rt_file = myfile.write_file(REFRESH_FILE)
	rt_file.write(refresh_token)
	rt_file.close()


# Checks request with nadeo servers. Throws an error
#   url ----> The link of the request
#	header -> Header of the API request
def check_request(url: str, header: json):
	global access_token

	header['Authorization'] = "nadeo_v1 t=" + access_token
	response = requests.get(url, headers=header)

	if response.status_code == 401:
		raise AccessTokenError("The access token has expired!")

	return response


# Creates a get request from the 
#   url ----> The link of the request
#	header -> Header of the API request
def make_request(url: str, header: json):
	global access_token, refresh_token

	# Check for files
	try:
		if access_token == "":
			access_token = myfile.read_file(ACCESS_FILE).read()
		if refresh_token == "":
			refresh_token = myfile.read_file(REFRESH_FILE).read()
	except FileNotFoundError:
		print("\tAccess token file not found! Creating necessary files...")
		myfile.write_file(ACCESS_FILE)
		myfile.write_file(REFRESH_FILE)

	# Make the request
	try:
		response = check_request(url, header)
	except AccessTokenError:
		try:
			print("\tAccess token has expired! Refreshing token...")
			nadeo_refreshtoken()
		except RefreshTokenError:
			try:
				print("\tRefresh token has expired! Getting new token...")
				nadeo_newtoken()
			except AuthorizationError:
				print("\tUbisoft authorization failed! Please enter your UbisoftConnect account details below...")
				ubisoft_login()
		finally:
			print("\n")
			response = check_request(url, header)

	return response

def remove_keyring():
	keyring.delete_password(AUTH_SERVICEID, AUTH_USER)

# If the user runs the script, they will obtain tokens with no prerequisites
if __name__ == "__main__":
	#remove_keyring()
	
	try:
		nadeo_newtoken()
	except AuthorizationError:
		ubisoft_login()