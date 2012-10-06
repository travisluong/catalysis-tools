from django.conf.urls import patterns, url

urlpatterns = patterns('sleep.views',
    url(r'^$', 'upload_file'),
    url(r'^upload_file$', 'upload_file'),
)