from django.conf.urls import patterns, include, url
from django.contrib import admin
import comfy.views

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'eccsgl.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^all_matches',comfy.views.all_match_details)
)
