from rest_framework.decorators import api_view
from rest_framework.response import Response
from .services import match_resume_to_job

@api_view(["POST"])
def resume_matcher(request):
    resume_text = request.data.get("resume_text")
    job_description = request.data.get("job_description")

    if not resume_text or not job_description:
        return Response(
            {"error": "resume_text and job_description are required"},
            status=400
        )

    score = match_resume_to_job(resume_text, job_description)

    return Response({
        "similarity_score": score
    })
