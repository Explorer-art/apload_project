import os
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.core.files.storage import FileSystemStorage
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from .utils import *
from .verifier import verify
from . import config

@csrf_exempt
def upload(request):
	if request.method == "POST":
		client_ip = get_client_ip(request)
		file = request.FILES["file"]
		file_expire = int(request.POST.get("file_expire"))

		if not file_expire in config.AVAILABLES_FILE_EXPIRE:
			return JsonResponse({"success": False, "message": get_messages("ru")["error_file_expire_not_available"]}, status=403)

		status, err = verify(client_ip, file.size)

		if not status:
			return JsonResponse({"success": False, "message": err}, status=401)

		file_code = generate_code()
		os.mkdir("media/" + file_code)

		fs = FileSystemStorage()
		name = fs.save(file_code + "/" + file.name.replace(" ", "_"), file)

		add_info(file_code, file_expire)
	else:
		return JsonResponse({"success": False, "message": get_messages("ru")["error_post_only"]}, status=403)

	return JsonResponse({"success": True, "file_code": file_code, "message": get_messages("ru")["succesfully_upload"]})

def download(request, file_code):
	if not file_code:
		return JsonResponse({"success": False, "message": get_messages("ru")["error_file_not_found"]}, status=403)

	path = "media/" + file_code

	if not os.path.exists(path):
		return JsonResponse({"success": False, "message": get_messages("ru")["error_file_not_found"]}, status=404)

	filename = request.GET.get("filename")

	if not filename:
		context = {}

		files = os.listdir(path)
		files_data = []

		for file in files:
			if os.path.isfile(path + "/" + file):
				ext = os.path.splitext(file)[-1].lower()

				thumbnail_path = ""

				if ext == ".zip" or ext == ".rar" or ext == ".7z" or ext == ".tar" or ext == ".gz":
					thumbnail_path = "images/archive.png"
				elif ext == ".txt":
					thumbnail_path = "images/txt.png"
				elif ext == ".png" or ext == ".jpg":
					thumbnail_path = file_code + "?filename=" + file
				else:
					thumbnail_path = "images/unknown.png"

				table = {
					"name": file,
					"thumbnail_url": thumbnail_path,
					"download_url": file_code + "?filename=" + file
				}

				files_data.append(table)

		context["created_date"] = get_info(file_code)["created"]
		context["files"] = files_data

		return render(request, "download.html", context)
	else:
		if filename.lower() == "info/info.json":
			return JsonResponse({"success": False, "message": get_messages("ru")["error_not_permissions"]}, status=401)

		with open(path + "/" + filename, "rb") as f:
			data = f.read()

			response = HttpResponse(data, content_type="application/octet-stream")
			response["Content-Disposition"] = "inline; filename=" + os.path.basename(path + "/" + filename)

			return response

@csrf_exempt
def search(request):
	if request.method == "POST":
		client_ip = get_client_ip(request)

		if client_ip == config.MASTER_SERVER and json.loads(request.body)["password"] == config.STATUS_PASSWORD:
			file_code = json.loads(request.body)["file_code"]

			if os.path.exists("media/" + file_code):
				return JsonResponse({"success": True})
			else:
				return JsonResponse({"success": False}, status=404)
		else:
			return JsonResponse({"success": False, "message":get_messages("ru")["error_not_permissions"]}, status=401)
	else:
		return JsonResponse({"success": False, "message": get_messages("ru")["error_post_only"]})

@csrf_exempt
def status(request):
	if request.method == "POST":
		client_ip = get_client_ip(request)

		if client_ip == config.MASTER_SERVER and json.loads(request.body)["password"] == config.STATUS_PASSWORD:
			_, _, free = disk_usage("/")

			return JsonResponse({"success": True, "free": free})
		else:
			return JsonResponse({"success": False, "message":get_messages("ru")["error_not_permissions"]}, status=401)
	else:
		return JsonResponse({"success": False, "message": get_messages("ru")["error_post_only"]})