
from django.conf.urls import patterns, url
from seller import views

urlpatterns = patterns('',
    url(r'^app-store-link/(?P<pk>\d*)$', views.registerApp,
        {'flag': 1.1,
         'backPage': 'seller/register_content.html',
         'nextPage': 'seller:appStore_info',
         'saveMethod': views.saveAppStoreLink,
         }, name='appStore_link'),
    url(r'^app-store-info/(?P<pk>\d+)$', views.registerApp,
        {'flag': 1.2,
         'backPage': 'seller/register_content.html',
         'nextPage': 'seller:marketing',
         'saveMethod': views.saveAppStoreInfo,
         }, name='appStore_info'),
    url(r'^marketing/(?P<pk>\d+)$', views.registerApp,
        {'flag': 2,
         'backPage': 'seller/register_content.html',
         'nextPage': 'seller:additional_info',
         'saveMethod': views.saveMarketing,
         }, name='marketing'),
    url(r'^additional-info/(?P<pk>\d+)$', views.registerApp,
        {'flag': 3,
         'backPage': 'seller/register_content.html',
         'nextPage': 'seller:sale',
         'saveMethod': views.saveAdditionalInfo,
         }, name='additional_info'),
    url(r'^sale/(?P<pk>\d+)$', views.registerApp,
        {'flag': 4,
         'backPage': 'seller/register_content.html',
         'nextPage': 'seller:delivery',
         'saveMethod': views.saveSale,
         }, name='sale'),
    url(r'^delivery/(?P<pk>\d+)$', views.registerApp,
        {'flag': 5,
         'backPage': 'seller/register_content.html',
         'nextPage': '/seller/payment',
         'saveMethod': views.saveDelivery,
         }, name='delivery'),
    #[a-z] for 'new' key word - create the new payment
    url(r'^payment/(?P<pk>\d+)/(?P<sn>[0-9a-z]*)$', views.registerApp,
        {'flag': 6,
         'backPage': 'seller/register_content.html',
         'nextPage': 'order:checkout',
         'saveMethod': views.saveService,
         }, name='payment'),
    url(r'^verification/(?P<pk>\d+)$', views.registerApp,
        {'flag': 7,
         'backPage': 'seller/register_content.html',
         'nextPage': 'seller:verification',
         'saveMethod': views.saveVerification,
         }, name='verification'),
    url(r'^delete-attachment/(?P<pk>\d*)$', views.deleteAttachment, name='deleteAttachment'),
)
