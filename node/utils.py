import os
import time
import datetime
import random
import json
from .config import *

def generate_random_string(length):
	chars = "qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM1234567890"
	random_string = "".join(random.choices(chars, k=length))
	return random_string

def generate_code(length=LINK_LENGTH):
	code = generate_random_string(length)

	if os.path.exists("media/" + code):
		code = generate_code(length)

	return code

def disk_usage(path):
	st = os.statvfs(path)
	total = st.f_blocks * st.f_frsize
	used = (st.f_blocks - st.f_bfree) * st.f_frsize
	free = st.f_bavail * st.f_frsize

	return total, used, free

def get_messages(language):
	with open("messages/" + language + ".json") as file:
		data = json.load(file)

	return data

def add_data(file_code, expiries):
	data = {
		"created_time": int(time.time()),
		"created_date": str(datetime.datetime.now().date()),
		"expiries": int(time.time()) + expiries,
	}

	os.mkdir("media/" + file_code + "/info")

	with open("media/" + file_code + "/info/info.json", "w") as file:
		json.dump(data, file, indent=4)

def get_data(file_code):
	with open("media/" + file_code + "/info/info.json", "r") as file:
		data = json.load(file)

	return data

def get_client_ip(request):
	x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")

	if x_forwarded_for:
		ip = x_forwarded_for.split(",")[0]
	else:
		ip = request.META.get("REMOTE_ADDR")

	return ip