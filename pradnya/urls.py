"""pradnya URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""




from django.conf.urls import include, url
from django.contrib import admin
from mcq import views as myapp_views
#from site_config import views as site_views


urlpatterns = [

    url(r'^admin/', include(admin.site.urls)),
    url(r'^$',myapp_views.home,name='home'),
    url(r'^signup/',myapp_views.signup,name='index2'),
    url(r'^result/',myapp_views.index,name='index'),
    url(r'^question/$',myapp_views.new_user,name='new_user'),
    #url(r'^$', site_views.handler404,name='404'),
    url(r'^time/$',myapp_views.get_time,name='get_time'), #Calling function to get time dynamically
    # url(r'^select/$',myapp_views.select,name='select'),  #Returns the selection page after 20 mins
    # url(r'^skips/$',myapp_views.skips,name='skip'), #Skip selected and submit
    # url(r'^playmore/$',myapp_views.playmore,name='playmore'), #Play more for 5 mins
    url(r'^endgame/$',myapp_views.endgame,name='endgame'), #Ends the game after 5 mins 
    url(r'^powerbackup/$',myapp_views.powerbackup,name='powerbackup')
]
