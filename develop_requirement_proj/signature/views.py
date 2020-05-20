from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http.response import HttpResponse
from django.views.generic import TemplateView, View

from .models import Document


class IndexView(TemplateView):
    template_name = "drs.html"


class DownloadView(View):
    # login_url = '/cas/login'

    def get(self, request, relative_filename, *args, **kwargs):
        """
        Provide web server redirect download file feature.

        relative_filename : the name of the file which store in filesystem.

        filename : the the name of the file which user named it.
        """
        instance = Document.objects.filter(path=relative_filename).first()
        # Check document exist and file exist filesystem or not
        if instance is None:
            message = '<h1>There is no file which you want to find.</h1>'
            return HttpResponse(message, status=404)
        elif not instance.path.storage.exists(instance.path.name):
            message = '<h1>There is no file which you want to find.</h1>'
            return HttpResponse(message, status=404)
        # Get user's deafult filename and filesize
        filename, size = instance.path.name, instance.size
        # Add filename and size in HTTP header
        if settings.DEBUG:
            response = HttpResponse(open(instance.path.path, 'rb'))
        else:
            response = HttpResponse()
        response['Content-Type'] = 'application/octet-stream; charset=utf-8'
        response['Content-Disposition'] = f'attachment; filename="{filename}"'
        response['Content-Length'] = size
        if settings.DEBUG:
            return response
        # Assign web server (nginx) to serve file for downloading
        redirect_path = f'/protected_file/{instance.path.name}'
        response['X-Accel-Redirect'] = redirect_path
        return response
