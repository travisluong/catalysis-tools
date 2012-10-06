from django.conf.urls import patterns, url

urlpatterns = patterns('sweet.views',
    url(r'^$', 'upload_file'),
    url(r'^upload_file$', 'upload_file'),
)