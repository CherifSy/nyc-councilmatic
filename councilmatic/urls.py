"""councilmatic URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url
from django.contrib import admin
from haystack.query import SearchQuerySet
from councilmatic_core.views import CouncilmaticSearchForm, CouncilmaticFacetedSearchView
from councilmatic_core.feeds import CouncilmaticFacetedSearchFeed
# XXX TODO (so that we can infer bill status): from nyc.feeds import NYCCouncilmaticFacetedSearchFeed
from nyc.views import *
from nyc.feeds import *

sqs = SearchQuerySet().facet('bill_type')\
                      .facet('sponsorships', sort='index')\
                      .facet('controlling_body')\
                      .facet('inferred_status')

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^committees/$', NYCCommitteesView.as_view(), name='committees'),
    url(r'^search/rss/',
        NYCCouncilmaticFacetedSearchFeed(), name='councilmatic_search_feed'),
    url(r'^search/', CouncilmaticFacetedSearchView(searchqueryset=sqs, 
                                                   form_class=CouncilmaticSearchForm),
                     name='councilmatic_search'),
    url(r'^$', NYCIndexView.as_view(), name='index'),
    url(r'^about/$', NYCAboutView.as_view(), name='about'),
    url(r'^legislation/(?P<slug>[^/]+)/$', NYCBillDetailView.as_view(), name='bill_detail'),
    url(r'^legislation/(?P<slug>[^/]+)/widget/$', NYCBillWidgetView.as_view(), name='bill_widget'),
    url(r'^legislation/(?P<slug>[^/]+)/rss/$', NYCBillDetailActionFeed(), name='bill_detail_action_feed'),
    url(r'', include('councilmatic_core.urls')),
]
