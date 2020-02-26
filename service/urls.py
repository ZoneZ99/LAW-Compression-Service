from django.urls import path

from service.views import CompressFileView

urlpatterns = [path("compress/", CompressFileView.as_view(), name="compress-file")]
