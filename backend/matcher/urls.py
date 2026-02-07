from django.urls import path
from .views import resume_matcher

urlpatterns = [
    path("match/", resume_matcher),
]
