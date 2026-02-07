from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from .services import compute_match_score

@csrf_exempt
def match_resume(request):
    if request.method != "POST":
        return JsonResponse(
            {"error": "POST request required"},
            status=400
        )

    resume_text = request.POST.get("resume", "")
    job_text = request.POST.get("job", "")

    score = compute_match_score(resume_text, job_text)

    return JsonResponse({
        "score": score,
        "status": "success",
        "note": "Dummy scoring logic (no ML model yet)"
    })
