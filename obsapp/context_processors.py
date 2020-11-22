from .models import *
from django.db.models import Q


def mainusercoin(request):
    if request.session.has_key('user_id'):
        # for showing l-coin
        logobj = LoginTable.objects.get(pk=request.session['user_id'])
        ucoin = logobj.lcoin

        # for showing favourite items
        favobj = FavouriteProduct.objects.filter(user_id=request.session['user_id'])
        prdobj = Product.objects.all()

        # for showing current user info
        userobj = UserInformation.objects.get(login_id=logobj)

        # notification count
        notcntobj = Notificationz.objects.filter(user_id=userobj, notificationseen=False).count()
        rqtcntobj = RequestExchange.objects.filter(towhom=userobj, is_responded=False).count()

        totalnoti = int(notcntobj) + int(rqtcntobj)

        #for showing chatlist
        chatlist = {}
        me = UserInformation.objects.get(login_id_id=request.session['user_id'])
        chatlist = ChatRoom.objects.filter(participant1=me)
        if chatlist:
            pass
        else:
            chatlist = ChatRoom.objects.filter(participant2=me)


        return {'mucoin': ucoin, 'favitem': favobj, 'fav': prdobj, 'current_user_info': userobj, 'noticount': totalnoti, 'chatlist': chatlist}
    else:
        return {'mucoin': 0}
