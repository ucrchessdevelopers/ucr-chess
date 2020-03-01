from django.urls import path, include

from django.contrib import admin

admin.autodiscover()

from django.conf.urls import url
from django.contrib.staticfiles.urls import static, settings, staticfiles_urlpatterns
import hello.views

# To add a new path, first import the app:
# import blog
#
# Then add the new path:
# path('blog/', blog.urls, name="blog")
#
# Learn more here: https://docs.djangoproject.com/en/2.1/topics/http/urls/

urlpatterns = [
    path("", hello.views.index, name="index"),
    path("db/", hello.views.db, name="db"),
    path("rankings/", hello.views.rankings, name="rankings"),
    path("admin/", admin.site.urls),
    path("about/", hello.views.about, name="about"),
    url(r'^files/', include('db_file_storage.urls')),
]
urlpatterns += staticfiles_urlpatterns()
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
