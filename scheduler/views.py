from django.views.static import serve

import os

def views_static_serve(request, path):
 	return serve(request, path, os.path.join(os.path.dirname(__file__),'../static/'), False)