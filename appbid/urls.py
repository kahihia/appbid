from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^i18n/', include('django.conf.urls.i18n')),
    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    url(r'^', include('home.urls', namespace='home')),
    url(r'^comments/', include('django.contrib.comments.urls')),
    url(r'^seller/', include('seller.urls', namespace='seller')),
    url(r'^usersetting/', include('usersetting.urls', namespace='usersetting')),
    url(r'^query/', include('query.urls', namespace='query')),
    url(r'^bid/', include('bid.urls', namespace='bid')),
    url(r'^dashboard/', include('dashboard.urls', namespace='dashboard')),
    url(r'^order/', include('order.urls', namespace='order')),
    url(r'^payment/', include('payment.urls', namespace='payment')),
    url(r'^transaction/', include('transaction.urls', namespace='transaction')),
    url(r'^social-auth/', include('social_auth.urls')),
    url(r'^auth/', include('auth.urls', namespace='auth')),
    url(r'^help/', include('help.urls', namespace='help')),
    url(r'^developer/', include('developer.urls', namespace='developer')),
    url(r'^joblistings/', include('offer.urls', namespace='offer')),

    url(r'^', include('favicon.urls')),
)

#urlpatterns += (url(r'^admin/django-ses/', include('django_ses.urls')),)
# urlpatterns += patterns('django.contrib.flatpages.views',
#     url(r'^about-us/$', 'flatpage', {'url': '/about-us/'}, name='about'),
#     url(r'^license/$', 'flatpage', {'url': '/license/'}, name='license'),
# )


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
