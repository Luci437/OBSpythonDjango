from django.conf.urls import url
from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.login, name='login'),
    path('signup/', views.signup, name='signup'),
    path('signup/usernamecheck/', views.checkusernameexists, name='usernamecheck'),
    path('logout/', views.logout, name='logout'),
    path('addproduct/', views.addproduct, name='addproduct'),
    path('viewProduct/', views.view_product, name='viewproduct'),
    path('editProfile/', views.edit_profile, name='editprofile'),
    path('advertisement/', views.addads, name='advertise'),
    path('productadded/', views.useraddproduct, name='productadded'),
    path('<int:pro_id>/removeitem/', views.userremoveproduct, name='userremoveitem'),
    path('saveads/', views.saveads, name='saveads'),
    path('<int:prd_id>/products/', views.viewmainproduct, name='viewmainproduct'),
    path('<int:prd_liked>/liked/', views.product_like, name='productlike'),
    path('<int:prd_id>/changeCoin', views.changecoin, name='changecoin'),
    path('<int:prd_id>/pigeon', views.pigeonshow, name='pigeonshow'),
    path('pigeon/', views.pigeon, name='pigeon'),
    path('notificationz/', views.notificationz, name='notificationz'),
    path('requestedtotrade/', views.requestdetails, name='requested'),
    path('<int:reqt_id>/rejectrequest/', views.rejectrequest, name='rejectrequest'),
    path('<int:reqt_id>/acceptrequest/', views.acceptrequest, name='acceptrequest'),
    path('game1/', views.game1, name='game1'),
    path('2/startgame/game1run/', views.game1run, name='game1run'),
    url(r'^game2/$', views.game2, name='game2'),
    path('allgames/', views.allgames, name='allgames'),
    path('<int:gameid>/gamedetails/', views.detailsgame, name='detailsgame'),
    path('<int:gameid>/startgame/', views.startgame, name='startgame'),
    path('takeme/', views.takeme, name='takeme'),
    path('rategames/', views.rategames, name='rategames'),
    path('searchs/', views.searches, name='searchs'),
    path('finishgame/', views.gamefinish, name='finishgames'),
    path('ticketshow/', views.ticketshow, name='ticketshow'),
    path('report/', views.getReport, name='report'),
    path('showads/', views.showads, name='showads'),
    path('<int:ad_id>/adpaused/', views.pauseads, name='pauseadd'),
    path('<int:ad_id>/resumeads/', views.resumeads, name='resumeads'),
    path('getchat/', views.getcommmessage, name='getcommunity')
]
