from django.conf.urls import patterns, include, url
from django.contrib import admin


urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'nab.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^$', 'nab_iday.views.index', name='home'),
    url(r'^accounts/$', 'nab_iday.views.accounts', name='accounts'),
    url(r'^transactions/(?P<acc_token>[a-zA-Z0-9%\-]+==)/$', 'nab_iday.views.transactions', name='transactions'),

    url(r'^transactions/(?P<acc_token>[a-zA-Z0-9%\-]+==).json$', 'nab_iday.views.transactions_json'),
    url(r'^set-place-state$', 'nab_iday.views.set_place_state'),

    url(r'^admin/', include(admin.site.urls)),
)
