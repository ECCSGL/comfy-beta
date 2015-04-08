from django.conf.urls import patterns, include, url
from django.contrib import admin
import comfy.views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'eccsgl.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^all_matches',comfy.views.all_match_details),
    url(r'^$',comfy.views.all_match_details),
    url(r'^match/(?P<match>[0-9]+)',comfy.views.one_match_details),
    url(r'^account/(?P<hash>[0-9a-zA-Z]+)',comfy.views.account_incl_hash),
    url(r'^account/',comfy.views.account_excl_hash),
    url(r'^placebet/',comfy.views.place_bet),
    url(r'^faq/',comfy.views.faq),
    url(r'^decookie/',comfy.views.decookie),
    url(r'^switchbet/',comfy.views.switch_bet)) + static(settings.STATIC_URL,document_root=settings.STATIC_ROOT)
