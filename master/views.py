import os
import requests
from django.shortcuts import render
from django.http import HttpResponse, HttpResponsePermanentRedirect, JsonResponse
from django.core.cache import cache
from django.conf import settings
from .utils import *
from . import config

def home(request):
	context = {}

	context["file_expire"] = config.FILE_EXPIRE

	return render(request, "index.html", context)

def images(request, filename):
	if not filename:
		return JsonResponse({"success": False, "message": get_messages("ru")["error_file_not_found"]}, status=403)

	path = "master/static/images"

	if not os.path.exists(path + "/" + filename):
		return JsonResponse({"success": False, "message": get_messages("ru")["error_file_not_found"]}, status=404)

	download_path = os.path.join(settings.MEDIA_ROOT, path + filename)

	with open(path + "/" + filename, "rb") as f:
		data = f.read()

		response = HttpResponse(data, content_type="application/octet-stream")
		response["Content-Disposition"] = "inline; filename=" + filename

		return response

def search_node(request, file_code):
	if file_code in cache:
		url = cache.get(file_code)
		return HttpResponsePermanentRedirect(url)

	for server in config.SERVERS:
		print(server)
		payload = {"password": config.STATUS_PASSWORD, "file_code": file_code}

		try:
			response = requests.post("http://" + server + "/search", json=payload, timeout=2)
		except:
			continue

		if response.status_code == 200:
			url = "http://" + server + "/" + file_code

			cache.set(file_code, url, CACHE_TTL)

			return HttpResponsePermanentRedirect(url)
		
	return JsonResponse({"success": False, "message": get_messages("ru")["error_file_not_found"]}, status=404)

def load_balancer(request):
	if request.method == "GET":
		best_server = {}

		for server in config.SERVERS:
			rate = 0

			payload = {"password": config.STATUS_PASSWORD}

			try:
				response = requests.post("http://" + server + "/status", json=payload, timeout=2)
			except:
				continue

			free = response.json()["free"]
			rate += free

			if best_server != {}:
				if best_server["rate"] < rate:
					best_server["host"] = server
					best_server["rate"] = rate
			else:
				best_server = {
					"host": server,
					"rate": rate
				}

			return JsonResponse({"success": True, "best_server": best_server["host"]})

		return JsonResponse({"success": False, "message": get_messages("ru")["eror_not_connection"]}, status=500)
	else:
		return JsonResponse({"success": False, "message": get_messages("ru")["error_get_only"]}, status=403)