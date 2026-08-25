from django.contrib import admin
from django.contrib.staticfiles.views import serve as staticfiles_serve
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    # Serves /static/... via the staticfiles *finders* rather than a single
    # document root. Vercel's build has no collectstatic step, so this needs
    # to resolve files straight out of STATICFILES_DIRS (our css/img/app
    # assets) as well as out of installed apps like django.contrib.admin
    # (admin/css/base.css etc.) - a fixed document_root only covers one of
    # those and leaves the other 404ing.
    # `insecure=True` is required to allow this outside DEBUG; Django's docs
    # call the per-request disk read "grossly inefficient" for high-traffic
    # sites, which is an acceptable trade-off for this app's traffic level.
    path(
        'static/<path:path>',
        staticfiles_serve,
        {'insecure': True},
        name='static_file',
    ),
    path('', include('cars.urls')),
]
