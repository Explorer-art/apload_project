import os
import time
from .utils import *
from .db import *
from .config import *

def verify(ip, file_size):
	if file_size > MAX_FILE_SIZE:
		return False, get_messages("ru")["error_file_size"]

	_, _, free = disk_usage("/")

	if file_size > free - ADDED_FREE_BYTES:
		return False, get_message("ru")["error_not_disk_space"]

	if not exists_user(ip):
		create_user(ip)

	user = get_user(ip)
	
	expire = user.expire
	uploads = user.uploads
	uploaded = user.uploaded

	if time.time() > expire:
		user.expire = time.time() + EXPIRE_CLEAR
		user.uploads = 0
		user.uploaded = 0
		user.save()

	if uploads >= MAX_UPLOADS:
		return False, get_messages("ru")["error_max_uploads"]

	if uploaded + file_size > MAX_DISK_SPACE:
		return False, get_messages("ru")["error_max_uploaded"]

	user.uploads += 1
	user.uploaded += file_size
	user.save()

	return True, None