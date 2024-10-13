from .models import User

def exists_user(ip):
	try:
		user = User.objects.get(ip=ip)
		return True
	except:
		return False

def get_user(ip):
	if not exists_user(ip):
		return False

	return User.objects.get(ip=ip)

def create_user(ip):
	user = User.objects.create(ip=ip)