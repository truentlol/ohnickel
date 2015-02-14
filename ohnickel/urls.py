from django.conf.urls import patterns, include, url
from django.contrib import admin
from ohnickel.controllers import views, forum, thread

admin.autodiscover()



urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'ohnickel.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^$', views.index, name='index'),

    url(r'^test/$', views.test, name='test'),


    url(r'^thread/create/$', thread.create, name='thread_create'),


    url(r'^forum/create/$', forum.create, name='forum_create'),


    url(r'^forums/$', forum.forums, name='forums'),



    url(r'^forum/(?P<forum_id>.+)/threads/$',  forum.threads, name='forum_threads'),
    url(r'^forum/(?P<forum_id>.+)/$',  forum.view, name='forum_view'),


    url(r'^thread/(?P<thread_id>.+)/$',  thread.view, name='thread_view'),



    url(r'', include('social_auth.urls')),








    url(r'^admin/', include(admin.site.urls)),
    #
    #url(r'', include('social_auth.urls')),
    #url(r'^test/$',  views.test, name='test'),
    #url(r'^myprofile/$',  views.myprofile, name='myprofile'),
    #url(r'^updateitemdb/$',  views.update_item_db, name='update_item_db'),
    ##url(r'^log/', csrf_exempt(views.log), name='log'),
    ##url(r'^steambotlogin/$',  csrf_exempt(views.steambotlogin), name='steambotlogin'),
    ##url(r'^user/register',  views.register, name='register'),
    #url(r'^user/wallet/balance/$',  views.get_user_wallet_balance, name='get_user_wallet_balance'),
    #url(r'^user/steam_trade_url/update/$',  views.update_steam_trade_url, name='update_steam_trade_url'),
    #url(r'^user/steam_trade_url/$',  views.get_steam_trade_url, name='get_steam_trade_url'),
    #url(r'^user/inventory/$',  csrf_exempt(views.user_inventory), name='user_inventory'),
    #url(r'^user/withdraw/$',  views.withdraw_bitcoin, name='withdraw_bitcoin'),
    ##url(r'^user/login',  views.login, name='login'),
    ##url(r'^user/logout',  views.logout, name='logout'),
    ##url(r'^user/(?P<user_name>.+)/$',  views.user, name='user'),
    #
    #url(r'^listing/search/',  views.listing_search, name='listing_search'),
    ##url(r'^api/user',  views.api_user, name='api_user'),
    #url(r'^listings/$',  views.listings, name='listings'),
    #
    #
    #
    #url(r'^listing/new',  views.listing_new, name='listing_new'),
    #url(r'^listing/(?P<listingid>.+)/verified/cancel',  views.verified_listing_cancel, name='verified_listing_cancel'),
    #url(r'^listing/(?P<listingid>.+)/unverified/cancel',  views.unverified_listing_cancel, name='unverified_listing_cancel'),
    #url(r'^listing/(?P<listingid>.+)/tradeoffer/status', csrf_exempt( views.listing_tradeoffer_status), name='listing_tradeoffer_status'),
    #url(r'^listing/(?P<listingid>.+)/json',  views.listing_json, name='listing_json'),
    #url(r'^listing/(?P<listingid>.+)/buy/$',  views.listing_buy, name='listing_buy'),
    #url(r'^listing/(?P<listingid>.+)/$',  views.listing, name='listing'),
    #
    #
    #url(r'^claim/(?P<claimid>.+)/tradeoffer/status',  csrf_exempt(views.claim_tradeoffer_status), name='claim_tradeoffer_status'),
    #url(r'^claim/(?P<claimid>.+)/$',  views.claim_items, name='claim_items'),
    #
    #url(r'^botstatus',  csrf_exempt(views.bot_status), name='bot_status'),
    #
    #url(r'^getunverifiedlistings',  csrf_exempt(views.getunverifiedlistings), name='getunverifiedlistings'),
    #url(r'^getactivelistings',  csrf_exempt(views.getactivelistings), name='getactivelistings'),
    #
    #url(r'^getclaims',  views.getclaims, name='getclaims'),
    #
    #url(r'^tradeoffer/(?P<tradeofferid>.+)/status',  csrf_exempt(views.tradeoffer_status), name='tradeoffer_status'),
    #url(r'^tradeoffer/(?P<tradeofferid>.+)/countdown',  csrf_exempt(views.tradeoffer_countdown), name='tradeoffer_countdown'),
    ##url(r'^tradeoffer/(?P<tradeofferid>.+)/status',  csrf_exempt(views.tradeoffer_status), name='tradeoffer_status')
    ##url(r'^tradeoffer/(?P<tradeofferid>.+)/cancel',  views.tradeoffer_cancel, name='tradeoffer_cancel'),
)
