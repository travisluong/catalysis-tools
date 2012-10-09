from django.conf.urls import patterns, include, url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf import settings
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('django.views.generic.simple',
    (r'^$', 'direct_to_template', {'template': 'base_home.html'}),
    (r'^rem/$', 'direct_to_template', {'template': 'rem.html'}),
)

urlpatterns += patterns('',
    url(r'^sleep/', include('sleep.urls')),
    url(r'^polls/', include('polls.urls')),
    url(r'^sweet/', include('sweet.urls')),
    url(r'^admin/', include(admin.site.urls)),
)




# urlpatterns += patterns('django.contrib.staticfiles.views',
    # url(r'^static/img/(?P<path>.*)$', 'serve'),
    # url(r'^static/js/(?P<path>.*)$', 'serve'),
    # url(r'^static/css/(?P<path>.*)$', 'serve'),
    # url(r'^static/(?P<path>.*)$', 'serve'),
# )

# urlpatterns += staticfiles_urlpatterns()

if settings.DEBUG:
    urlpatterns += patterns('',
            (r'^static/(.*)$', 'django.views.static.serve', {'document_root': settings.STATIC_ROOT}),
    )
