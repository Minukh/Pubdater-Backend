from django.shortcuts import render
from django.http import JsonResponse
from django.http import HttpResponse
import json
from .pubdater import Pubdater
from .exceptions import ContentLengthException

def processUpdate(request):
    if request.method == "POST":
        try:
            try:
                payload = json.loads(request.body)
                pub = Pubdater(
                    payload.get("dependencies", ""), payload.get("version", "1.0")
                )
            except ContentLengthException as e:
                return JsonResponse(
                    {
                        "dependencies": payload.get("dependencies", ""),
                        "error": f"{e.message}",
                    },
                    status=400,
                )

            return JsonResponse(
                {
                    "dependencies": pub.pubspec_updated,
                    "message": f"{pub.message}",
                    "count": f"{pub.count}",
                }
            )
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON format"}, status=400)
    return JsonResponse({"error": "Invalid request method"}, status=400)


def index(request):
    return render(request, "index.html")
