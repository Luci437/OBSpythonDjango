from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse, Http404, JsonResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.contrib import messages
from django.db.models import Q
from django.urls import reverse
from django.core import serializers
import random
import json

from .models import *
import copy

alldict = {}


def index(request):
    proobj = Product.objects.filter(is_active=True).order_by('-lcoin','-product_date')
    adsobj = Ads.objects.filter(endingdate__gte=datetime.now().today(),isactive=True)
    if request.session.has_key('user_id'):
        userid = request.session['user_id']
        logobj = LoginTable.objects.get(pk=userid)
        userobj = UserInformation.objects.get(login_id=logobj.id)
        chatobj = Community.objects.all()
        return render(request, 'home.html', {'user_info': userobj, 'products': proobj, 'ads': adsobj, 'comchats': chatobj})
    else:
        return render(request, 'home.html', {'products': proobj, 'ads': adsobj})


def login(request):
    if request.session.has_key('user_id'):
        return view_product(request)
    else:
        if request.method == 'POST':
            uname = request.POST.get('username')
            passwd = request.POST.get('password')

            if LoginTable.objects.filter(username=uname, password=passwd).exists():
                logobj = LoginTable.objects.get(username=uname, password=passwd)
                request.session['user_id'] = logobj.id
                messages.success(request, 'Welcome to Luci')
                return view_product(request)
            else:
                return render(request, 'login.html', context={'error_msg': 'Invalid Username/Password'})
        return render(request, 'login.html')


def signup(request):
    if request.method == 'POST':
        fname = request.POST.get('fname')
        uname = request.POST.get('username')
        passwd = request.POST.get('password')

        if LoginTable.objects.filter(username=uname).exists():
            return render(request, 'signup.html', context={'error_msg': 'Username taken'})
        else:
            logobj = LoginTable()
            logobj.username = uname
            logobj.password = passwd
            logobj.save()

            userobj = UserInformation()
            userobj.login_id = logobj
            userobj.f_name = fname
            userobj.save()

            messages.success(request, 'Successfully Account created.')
            return render(request, 'login.html')
    return render(request, 'signup.html')


def logout(request):
    if request.session.has_key('user_id'):
        del request.session['user_id']
        messages.success(request, 'Logout Successfully')
    return index(request)


def addproduct(request):
    if request.session.has_key('user_id'):
        userid = request.session['user_id']
        logobj = LoginTable.objects.get(pk=userid)
        userobj = UserInformation.objects.get(login_id=logobj.id)
        catobj = Category.objects.all()

        return render(request, 'addProduct.html', {'user_info': userobj, 'cats': catobj})
    return render(request, 'home.html')


def view_product(request):
    if request.session.has_key('user_id'):
        userid = request.session['user_id']
        logobj = LoginTable.objects.get(pk=userid)
        userobj = UserInformation.objects.get(login_id=logobj.id)
        proobj = Product.objects.filter(user_id=logobj, is_active=True)
        trobj = Product.objects.filter(user_id=logobj, is_active=False)

        return render(request, 'viewProduct.html', {'user_info': userobj, 'products': proobj, 'traded_product':trobj})
    return render(request, 'login.html')


def edit_profile(request):
    if request.session.has_key('user_id'):
        userid = request.session['user_id']
        logobj = LoginTable.objects.get(pk=userid)
        userobj = UserInformation.objects.get(login_id=logobj.id)

        if request.method == 'POST':
            oldpass = request.POST.get('oldpass')
            if logobj.password == oldpass:
                newpass = request.POST.get('newpass')
                newuname = request.POST.get('uname')
                newname = request.POST.get('name')
                about = request.POST.get('about')

                if about:
                    userobj.about_user = about

                if newname:
                    userobj.f_name = newname
                userobj.save()

                if newpass:
                    logobj.password = newpass
                if newuname:
                    if logobj.username == newuname:
                        pass
                    else:
                        if LoginTable.objects.filter(username=newuname).exists():
                            return render(request, 'editProfile.html', {'user_info': userobj, 'user_username': logobj,
                                                                        'error_msg': 'Username not available'})
                        else:
                            logobj.username = newuname
                            logobj.save()
                logobj.save()
            else:
                return render(request, 'editProfile.html', {'user_info': userobj, 'user_username': logobj, 'error_msg': 'Sorry, Wrong Password,Please try again'})
            return render(request, 'editProfile.html',
                          {'user_info': userobj, 'user_username': logobj, 'error_msg': 'Profile Updated Successfully'})
        return render(request, 'editProfile.html', {'user_info': userobj,'user_username': logobj})
    return render(request, 'home.html')


def addads(request):
    if request.session.has_key('user_id'):
        userid = request.session['user_id']
        logobj = LoginTable.objects.get(pk=userid)
        userobj = UserInformation.objects.get(login_id=logobj.id)
        prdobj = Product.objects.filter(user_id=logobj, is_active=True)
        layoutobj = LayoutPrice.objects.get(pk=1)
        if prdobj:
            return render(request, 'advertise.html',{'user_info': userobj, 'products': prdobj, 'layouts': layoutobj})
        else:
            messages.success(request, 'Before that you need to Add a product to LUCI.')
            return view_product(request)
    return render(request, 'home.html')


def useraddproduct(request):
    if request.session.has_key('user_id'):
        if request.method == 'POST':
            pname = request.POST.get('product-name')
            info = request.POST.get('about')
            cats = request.POST.get('category')
            img = request.FILES['imageFile']
            ret1name = request.POST.get('returnitem1')
            ret1info = request.POST.get('aboutreturnitem1')
            ret2name = request.POST.get('returnitem2')
            ret2info = request.POST.get('aboutreturnitem2')
            ret3name = request.POST.get('returnitem3')
            ret3info = request.POST.get('aboutreturnitem3')
            userid = request.session['user_id']
            userobj = LoginTable.objects.get(pk=userid)

            catobj = Category.objects.get(categoryname=cats)

            productobj = Product()
            productobj.user_id = userobj
            productobj.productname = pname
            productobj.info = info
            productobj.productimage = img
            productobj.category = catobj
            productobj.save()

            retobj = Returns()
            retobj.product_id = productobj
            retobj.ret1name = ret1name
            retobj.ret1info = ret1info
            retobj.ret2name = ret2name
            retobj.ret2info = ret2info
            retobj.ret3name = ret3name
            retobj.ret3info = ret3info
            retobj.save()

            messages.success(request, 'Items Added Successfully.')
            return HttpResponseRedirect(reverse('viewproduct'))
        return addproduct(request)
    return HttpResponseRedirect(reverse('index'))


def userremoveproduct(request, pro_id):
    try:
        proobj = Product.objects.get(pk=pro_id)
    except:
        return view_product(request)
    else:
        proobj.delete()
        messages.success(request, 'Item removed Successfully')
        return view_product(request)


def saveads(request):
    if request.method == 'POST':
        userid = request.session['user_id']
        logobj = LoginTable.objects.get(pk=userid)
        prdid = request.POST.get('productname')
        prdobj = Product.objects.get(pk=prdid)
        startdate = request.POST.get('startingdate')
        endingdate = request.POST.get('endingdate')
        adsimage = request.FILES['imageFile']
        totalmoney = request.POST.get('real-money')
        layout = int(request.POST.get('layout'))
        layoutname = ''

        print(layout)

        if layout < 5000:
            layoutname = 'layout3'
        elif layout < 10000:
            layoutname = 'layout2'
        else:
            layoutname = 'layout1'

        adsobj = Ads()
        adsobj.logintable = logobj
        adsobj.product = prdobj
        adsobj.startingdate = startdate
        adsobj.endingdate = endingdate
        adsobj.adsimage = adsimage
        adsobj.layout = layoutname
        adsobj.totalamount = totalmoney
        adsobj.save()

        messages.success(request, 'Your Advertisement is Saved and Send for Validating.')
        return view_product(request)
    return addads(request)


def viewmainproduct(request, prd_id):
    prdobj = Product.objects.get(pk=prd_id)
    rtobj = Returns.objects.get(product_id=prd_id)
    thisuserid = prdobj.user_id_id
    logobj = LoginTable.objects.get(pk=thisuserid)
    if request.session.has_key("user_id"):
        ulogobj = LoginTable.objects.get(pk=request.session['user_id'])

    userobj = UserInformation.objects.get(login_id=logobj)
    if request.session.has_key('user_id'):
        if FavouriteProduct.objects.filter(user_id=request.session['user_id'], prd_id=prdobj).exists():
            return render(request, 'view_product.html', {'prd': prdobj, 'rt': rtobj, 'log': logobj, 'user': userobj, 'is_liked': 'yesi'})
        else:
            return render(request, 'view_product.html', {'prd': prdobj, 'rt': rtobj, 'log': logobj, 'user': userobj})
    else:
        return render(request, 'view_product.html', {'prd': prdobj, 'rt': rtobj, 'log': logobj, 'user': userobj})


def product_like(request, prd_liked):
    if request.session.has_key('user_id'):
        logobj = LoginTable.objects.get(pk=request.session['user_id'])
        prdobj = Product.objects.get(pk=prd_liked)
        if FavouriteProduct.objects.filter(prd_id=prdobj,user_id=logobj).exists():
            favobj = FavouriteProduct.objects.get(prd_id=prdobj,user_id=logobj)
            favobj.delete()
        else:
            favobj = FavouriteProduct()
            favobj.user_id = logobj
            favobj.prd_id = prdobj
            favobj.save()
            messages.success(request, 'Added to Favourites')

        return viewmainproduct(request, prd_liked)
    else:
        messages.success(request, 'You need to Login in order to add to Favourite')
        return login(request)


def changecoin(request, prd_id):
    if request.session.has_key('user_id'):
        logobj = LoginTable.objects.get(pk=request.session['user_id'])
        userobj = UserInformation.objects.get(login_id=logobj)
        prdobj = Product.objects.get(pk=prd_id)
        pcoin = prdobj.lcoin
        ucoin = logobj.lcoin

        if prdobj.is_editable:
            if request.method == 'POST':
                newval = request.POST.get('newval')
                if int(newval) > pcoin:
                    ab = int(newval) - pcoin
                    logobj.lcoin = int(ucoin) - int(ab)
                else:
                    ab = int(pcoin) - int(newval)
                    logobj.lcoin = int(ucoin) + int(ab)
                logobj.save()
                prdobj.lcoin = newval
                prdobj.save()
                messages.success(request, 'L-Coin Changed successfully')
                return view_product(request)
            else:
                return render(request, 'changeCoin.html', {'user_info': userobj, 'prd_coin': pcoin, 'ucoin': ucoin , 'prdid': prd_id, 'prd': prdobj})
        else:
            messages.success(request, 'You cannot edit Lcoin, because you have a request on that.')
            return HttpResponseRedirect(reverse('viewproduct'))
    else:
        return login(request)


def notificationz(request):
    if request.session.has_key('user_id'):
        logobj = LoginTable.objects.get(pk=request.session['user_id'])
        userobj = UserInformation.objects.get(login_id=logobj)
        notobj = Notificationz.objects.filter(user_id=userobj).order_by('-notificationtime')

        oldnotobj = copy.deepcopy(notobj)
        superold = copy.deepcopy(oldnotobj)

        for nt in notobj:
            if not nt.notificationseen:
                nt.notificationseen = True
                nt.save()

        rqstobj = RequestExchange.objects.filter(towhom=userobj, is_accepted=False, is_responded=False).order_by('-datetimeofrequest')

        return render(request, 'notifications.html', {'notificationz': superold, 'is_request_on': rqstobj})
    else:
        return login(request)


def requestdetails(request):
    if request.method == 'POST':
        productid = request.POST.get('productid')
        returnitem = request.POST.get('returnitem')

        logobj = LoginTable.objects.get(pk=request.session['user_id'])
        prodobj = Product.objects.get(pk=productid)

        towhobj = LoginTable.objects.get(pk=prodobj.user_id_id)
        touserobj = UserInformation.objects.get(login_id=towhobj)
        fromuserobj = UserInformation.objects.get(login_id=logobj)

        prodobj.is_editable = False
        prodobj.save()

        rqstobj = RequestExchange()
        rqstobj.towhom = touserobj
        rqstobj.fromwhom = fromuserobj
        rqstobj.whatproduct = prodobj
        rqstobj.withwhatproduct = returnitem
        rqstobj.is_request = True
        rqstobj.datetimeofrequest = datetime.now()
        rqstobj.save()

        notiobj = Notificationz()
        notiobj.user_id = fromuserobj
        userresponsetext = 'You send a request to '+ str(touserobj.f_name) + ' to trade ' + str(prodobj.productname) + ' with ' + str(returnitem) + '.'
        notiobj.notificationtext = userresponsetext
        notiobj.notificationtime = datetime.now()
        notiobj.save()

        notiobj2 = Notificationz()
        notiobj2.user_id = touserobj
        userresponsetext = str(fromuserobj.f_name) + ' send a request to trade ' + str(prodobj.productname) + ' with ' + str(returnitem) + '.'
        notiobj2.notificationtext = userresponsetext
        notiobj2.notificationtime = datetime.now()
        notiobj2.save()

        messages.success(request, 'Request send Successfully.')
        return HttpResponseRedirect(reverse('viewproduct'))

    else:
        return index(request)


def acceptrequest(request, reqt_id):
    if request.session['user_id']:
        rqobj = RequestExchange.objects.get(pk=reqt_id)
        currentobj = LoginTable.objects.get(pk=request.session['user_id'])
        userobj = UserInformation.objects.get(login_id=currentobj)

        productid = rqobj.whatproduct.pk
        prdobj = Product.objects.get(pk=productid)

        prdobj.is_active = False
        prdobj.save()

        rqobj.is_responded = True
        rqobj.is_accepted = True
        rqobj.save()

        fromid = rqobj.fromwhom.pk
        fromboj = UserInformation.objects.get(pk=fromid)

        notobj = Notificationz()
        notobj.user_id = fromboj
        notobj.notificationtext = "Congratulation "+ str(fromboj.f_name) +", "+ str(userobj.f_name) + " agreed to Trade with you"
        notobj.notificationtime = datetime.now()
        notobj.save()

        notobj = Notificationz()
        notobj.user_id = fromboj
        notobj.notificationtext = "You Exchanged "+ str(prdobj.productname) + " <=> "+ str(rqobj.withwhatproduct) + " from " + str(userobj.f_name) +"."
        notobj.notificationtime = datetime.now()
        notobj.save()

        notobj = Notificationz()
        notobj.user_id = fromboj
        notobj.notificationtext = str(prdobj.lcoin) + " L-coins added to your Account."
        notobj.notificationtime = datetime.now()
        notobj.save()

        #updating l-coins
        prdlcoin = prdobj.lcoin

        newcoin = 0

        newcoin = int(fromboj.login_id.lcoin) + int(prdlcoin)
        print("Lcoin after added: ",newcoin)
        newobj = LoginTable.objects.get(id=fromboj.login_id_id)
        newobj.lcoin = newcoin
        newobj.save()

        newcoin = int(userobj.login_id.lcoin) - int(prdlcoin)
        print("Lcoin after subtracted: ", newcoin)
        newobj2 = LoginTable.objects.get(id=userobj.login_id_id)
        newobj2.lcoin = newcoin
        newobj2.save()

        usernoti = Notificationz()
        usernoti.user_id = userobj
        usernoti.notificationtext = "You Exchanged "+ str(prdobj.productname) + " <=> "+ str(rqobj.withwhatproduct) + " from " + str(fromboj.f_name) +"."
        usernoti.notificationtime = datetime.now()
        usernoti.save()

        usernoti = Notificationz()
        usernoti.user_id = userobj
        usernoti.notificationtext = str(prdobj.lcoin) + " L-coins deducted from your Account."
        usernoti.notificationtime = datetime.now()
        usernoti.save()

        # sending notification and cancelling all request to this product
        allrqst = RequestExchange.objects.filter(whatproduct=prdobj)

        for nqst in allrqst:
            if nqst.fromwhom != fromboj:
                nuserid = nqst.fromwhom.pk
                uuserobj = UserInformation.objects.get(pk=nuserid)

                nqst.is_accepted = False
                nqst.is_responded = True
                nqst.save()

                nnoti = Notificationz()
                nnoti.user_id = uuserobj
                nnoti.notificationtext = "Sorry, "+ str(prdobj.productname) + " is Not Available, because its Traded with someone else."
                nnoti.notificationtime = datetime.now()
                nnoti.save()

        messages.success(request, "Your Trade Successfully completed.")
        return HttpResponseRedirect(reverse('notificationz'))
    else:
        return login(request)


def checkusernameexists(request):
    dataz = {}
    availability = False
    print("You are here.")
    if request.method == 'POST':
        username = request.POST.get('username')

        if LoginTable.objects.filter(username=username).exists():
            availability = False
        else:
            availability = True

        dataz = {
            'ans': availability
        }

    return JsonResponse(dataz)

"""
def pigeonshow(request, prd_id):
    if request.session.has_key('user_id'):
        prdobj = Product.objects.get(pk=prd_id)
        receverobj = UserInformation.objects.get(login_id=prdobj.user_id_id)
        rtobj = Returns.objects.get(product_id=prdobj)

        logobj = LoginTable.objects.get(pk=request.session['user_id'])
        fromwhomobj = UserInformation.objects.get(login_id=logobj)

        if RequestExchange.objects.filter(fromwhom=fromwhomobj, towhom=receverobj, whatproduct=prdobj).exists():
            retobj = RequestExchange.objects.get(fromwhom=fromwhomobj, towhom=receverobj, whatproduct=prdobj)
            if retobj.is_responded == True:
                return render(request, 'pigeon.html', {'prd': prdobj, 'receverinfo': receverobj, 'returns': rtobj, 'alreadyrequest': 'True', 'responded': 'True'})
            else:
                return render(request, 'pigeon.html', {'prd': prdobj, 'receverinfo': receverobj, 'returns': rtobj, 'alreadyrequest': 'True'})
        else:
            return render(request, 'pigeon.html', {'prd': prdobj, 'receverinfo': receverobj, 'returns': rtobj})
    else:
        messages.success(request, 'You need to Login in order to chat.')
        return login(request)


def pigeon(request):
    if request.method == 'POST':
        sender = request.session['user_id']
        messages = request.POST.get('messages')
        receiver = request.POST.get('receiverid')

        logsender = LoginTable.objects.get(pk=sender)
        senderobj = UserInformation.objects.get(login_id=logsender)
        logrecever = LoginTable.objects.get(pk=receiver)
        receiverobj = UserInformation.objects.get(login_id=logrecever)

        if Pigeons.objects.filter(sender_id=senderobj,receiver_id=receiverobj).exists():
            print("Chat room exists.")
        else:
            print("Need to create new Chat room.")

        return JsonResponse({'ans':'myanswer'})

    else:
        return "user"

"""


def pigeonshow(request, prd_id):
    if request.session.has_key('user_id'):

        prdobj = Product.objects.get(id=prd_id)

        sendobj = UserInformation.objects.get(login_id_id=request.session['user_id'])
        receiverobj = UserInformation.objects.get(login_id_id=prdobj.user_id_id)
        rtobj = Returns.objects.get(product_id=prdobj)

        if ChatRoom.objects.filter(product_id=prdobj, participant1=sendobj, participant2=receiverobj).exists():
            print('already chated')
            roomboj = ChatRoom.objects.get(product_id=prdobj, participant1=sendobj, participant2=receiverobj)
            chatobj = Chats.objects.filter(chatroomid=roomboj)
        elif ChatRoom.objects.filter(product_id=prdobj, participant2=sendobj, participant1=receiverobj).exists():
            print('already chated')
            roomboj = ChatRoom.objects.get(product_id=prdobj, participant2=sendobj, participant1=receiverobj)
            chatobj = Chats.objects.filter(chatroomid=roomboj)
        else:
            room = ChatRoom()
            room.product_id = prdobj
            room.participant1 = sendobj
            room.participant2 = receiverobj
            room.save()

            chatobj = Chats.objects.filter(chatroomid=room)

        requested = False
        responded = False
        if RequestExchange.objects.filter(whatproduct=Product.objects.get(id=prd_id),fromwhom=UserInformation.objects.get(login_id_id=request.session['user_id']),is_request=True).exists():
            requested = True
        else:
            requested = False

        return render(request, 'pigeon.html',{'chats':chatobj,'prd':prdobj,'returns': rtobj, 'alreadyrequest': requested})
    else:
        return login(request)


def pigeon(request):
    print('came here')
    if request.session.has_key('user_id'):
        if request.method == 'POST':
            chatmessage = request.POST.get('message')
            prd_id = request.POST.get('productid')

            prdobj = Product.objects.get(id=prd_id)
            rtobj = Returns.objects.get(product_id=prdobj)

            sobj = LoginTable.objects.get(id=request.session['user_id'])
            sendobj = UserInformation.objects.get(login_id=sobj)
            receiverobj = UserInformation.objects.get(login_id_id=prdobj.user_id_id)

            if ChatRoom.objects.filter(product_id=prdobj, participant1=sendobj, participant2=receiverobj).exists():
                print('already chated1')
                roomboj = ChatRoom.objects.get(product_id=prdobj, participant1=sendobj, participant2=receiverobj)
                chatz = Chats()
                chatz.chatroomid = roomboj
                chatz.user_id = sendobj
                chatz.messagetime = datetime.now()
                chatz.chatmessage = chatmessage
                chatz.save()

                chatobj = Chats.objects.filter(chatroomid=roomboj)
                return render(request, 'pigeon.html', {'chats': chatobj,'prd': prdobj,'returns': rtobj})

            else:
                print('already chated2')
                roomboj = ChatRoom.objects.get(product_id=prdobj, participant2=sendobj, participant1=receiverobj)
                chatz = Chats()
                chatz.chatroomid = roomboj
                chatz.user_id = sendobj
                chatz.messagetime = datetime.now()
                chatz.chatmessage = chatmessage
                chatz.save()
                chatobj = Chats.objects.filter(chatroomid=roomboj)

                return render(request, 'pigeon.html', {'chats':chatobj,'prd':prdobj,'returns': rtobj})
        return login(request)



def game1(request):
    allqstobj = Questions.objects.all()[:15]
    totaleasy = 0
    totalhard = 0
    totalmedium = 0
    ranhard = 0
    raneasy = 0
    ranmedium = 0
    alleasyqst = []
    allhardqst = []
    allmediumqst = []
    newobj = []
    easyqstobj = Questions.objects.filter(typeofqst='EASY')
    print(len(easyqstobj))
    hardqstobj = Questions.objects.filter(typeofqst='HARD')
    print(len(hardqstobj))
    mediumqstobj = Questions.objects.filter(typeofqst='MEDIUM')
    print(len(mediumqstobj))

    for i in range(len(easyqstobj)):
        if totaleasy < 5:
            raneasy = random.randint(0,len(easyqstobj))
            if raneasy in alleasyqst:
                pass
            else:
                newobj.append(easyqstobj[raneasy])
                alleasyqst.append(raneasy)
                totaleasy += 1

    for i in range(len(mediumqstobj)):
        if totalmedium < 5:
            ranmedium = random.randint(0,len(mediumqstobj))
            if ranmedium in allmediumqst:
                pass
            else:
                newobj.append(mediumqstobj[ranmedium])
                allmediumqst.append(mediumqstobj[ranmedium])
                totalmedium += 1

    for i in range(len(hardqstobj)):
        if totalhard < 5:
            ranhard = random.randint(0,len(hardqstobj))
            if ranhard in allhardqst:
                pass
            else:
                newobj.append(hardqstobj[ranhard])
                allmediumqst.append(hardqstobj[ranhard])
                totalhard += 1
    logobj = LoginTable.objects.get(pk=request.session['user_id'])
    gameobj = Games.objects.get(pk=1)
    if GamePlayed.objects.filter(userid=logobj, gameid=gameobj).exists():
        return render(request, 'YCBB.html', {'qst': newobj, 'notnoob':'not a noob'})
    else:
        return render(request, 'YCBB.html', {'qst': newobj})


def game1run(request):
    data = {}
    if request.method == 'POST':
        qstid = request.POST.get('qstid')
        myanswer = request.POST.get('ans')

        qstobj = Questions.objects.get(pk=qstid)
        orgianswer = qstobj.answer
        print(orgianswer)
        print(myanswer)

        if myanswer == orgianswer:
            data = {
                'ans': True
            }
        else:
            data = {
                'ans': False
            }
    return JsonResponse(data)


def game2(request):
    logobj = LoginTable.objects.get(pk=request.session['user_id'])
    gameobj= Games.objects.get(pk=2)

    if GamePlayed.objects.filter(userid=logobj, gameid=gameobj).exists():
        return render(request, 'OddorEven.html', {'game': gameobj})
    else:
        return render(request, 'OddorEven.html', {'game': gameobj, 'noob':'yes i am new'})


def allgames(request):
    gamesobj = Games.objects.all()
    return render(request, 'games.html', {'games':gamesobj})


def detailsgame(request, gameid):
    gamesobj = Games.objects.get(pk=gameid)
    reviewobj = GameRating.objects.filter(gameid=gamesobj).order_by('-reviewtime')
    return render(request, 'gamedetails.html',{'reviewz': reviewobj,'games':gamesobj})


def startgame(request, gameid):
    if request.session.has_key('user_id'):
        logobj = LoginTable.objects.get(pk=request.session['user_id'])
        if GamePlayed.objects.filter(gameid=gameid, userid=logobj).exists():
            pass
        else:
            gpobj = GamePlayed()
            gpobj.userid = logobj
            gpobj.gameid = Games.objects.get(pk=gameid)
            gpobj.startedgame = datetime.now()
            gpobj.save()

            gobj = Games.objects.get(id=gameid)
            gobj.totalplays += 1
            gobj.save()

        if gameid == 1:
            return game2(request)
        elif gameid == 2:
            return game1(request)
    else:
        messages.success(request, 'You need to login in order to play games.')
        return HttpResponseRedirect(reverse('login'))


def takeme(request):
    import xlrd

    alldata = xlrd.open_workbook("final questions.xlsx")
    sheets = alldata.sheet_by_index(0)

    datas = []

    for i in range(1, 1331):
        for y in range(7):
            datas.append(sheets.cell_value(i, y))
        qstobj = Questions()
        qstobj.typeofqst = datas[0]
        qstobj.question = datas[1]
        qstobj.option1 = datas[2]
        qstobj.option2 = datas[3]
        qstobj.option3 = datas[4]
        qstobj.option4 = datas[5]
        qstobj.answer = datas[6]
        qstobj.save()
        datas.clear()
    print("All data added to Database successfully.")
    return index(request)


def rategames(request):
    if request.session.has_key('user_id'):
        if request.method == 'POST':
            gameid = request.POST.get('gameid')
            gamereview = request.POST.get('review')
            logid = LoginTable.objects.get(pk=request.session['user_id'])
            userid = UserInformation.objects.get(login_id=logid)
            gameobj = Games.objects.get(pk=gameid)

            rateobj = GameRating()
            rateobj.gameid = gameobj
            rateobj.review = gamereview
            rateobj.userid = userid
            rateobj.save()

            messages.success(request, 'Thank you for your Review, it helps a lot')
        return detailsgame(request, gameid)
    else:
        return login(request)


def rejectrequest(request,reqt_id):
    if request.session.has_key('user_id'):

        rqstobj = RequestExchange.objects.get(id=reqt_id)
        rqstobj.is_accepted = False
        rqstobj.is_responded = True
        rqstobj.is_request = False
        rqstobj.save()

        if RequestExchange.objects.filter(whatproduct=rqstobj.whatproduct,is_responded=False).exists():
            print('ddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddd')
            print(rqstobj.whatproduct.productname)
            print('ddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddd')
        else:
            print('sssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssss')
            print(rqstobj.whatproduct.productname)
            print('sssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssss')
            newobj = Product.objects.get(id=rqstobj.whatproduct.id)
            newobj.is_editable = True
            newobj.save()

        notobj = Notificationz()
        notobj.user_id = rqstobj.fromwhom
        notobj.notificationtext = "Your request to exchange "+ str(rqstobj.whatproduct.productname) +" was REJECTED by trader"
        notobj.notificationtime = datetime.now()
        notobj.save()

        notobj2 = Notificationz()
        notobj2.user_id = rqstobj.towhom
        notobj2.notificationtext = "You REJECTED the request from "+ str(rqstobj.fromwhom.f_name) + "."
        notobj2.notificationtime = datetime.now()
        notobj2.save()
        messages.success(request, 'Opps that was a rejection.')

        return HttpResponseRedirect(reverse('notificationz'))
    else:
        return HttpResponseRedirect(reverse('login'))


def searches(request):
    if request.method == 'POST':
        searchtext = request.POST.get('search')

        prdobj = Product.objects.filter(productname__contains=searchtext, is_active=True).order_by('-lcoin')
        return render(request, 'search.html', {'products': prdobj})
    return index(request)


def gamefinish(request):
    if request.method == 'POST':
        yourscore = request.POST.get('score')
        gameid = request.POST.get('gameid')
        usercoin = request.POST.get('wincoin')

        print("Your score: ", yourscore)

        gameobj = Games.objects.get(pk=gameid)
        logobj = LoginTable.objects.get(pk=request.session['user_id'])

        if gameobj.highestscore < int(yourscore):
            userobj = UserInformation.objects.get(login_id=logobj)

            gameobj.kingofgame = userobj.f_name
            gameobj.highestscore = yourscore
            gameobj.save()
            messages.success(request, 'Congratulations your are a King now')

        logobj.lcoin = logobj.lcoin + int(usercoin)
        logobj.save()
        messages.success(request, 'Thank you for playing LUCI games')

    return HttpResponseRedirect(reverse('allgames'))


def ticketshow(request):
    if request.method == 'POST':
        ticketid = request.POST.get('tiid')
        print('So Ajax worked good',ticketid)

        if Lticket.objects.filter(pk=ticketid, is_available=True).exists():
            tiobj = Lticket.objects.get(pk=ticketid)
            tiobj.is_available = False
            tiobj.save()
            print("ticket buyed")
        else:
            print("Not available")
            return HttpResponse("Sorry ticket Sold out")
    ticketobj = Lticket.objects.filter(is_available=True)
    return render(request, 'Tickets.html', {'tickets': ticketobj})


def getReport(request):
    if request.session.has_key('user_id'):
        if request.method == 'POST':
            reson = request.POST.get('report')
            prdid = request.POST.get('prdid')

            prdobj = Product.objects.get(id=prdid)
            userobj = UserInformation.objects.get(login_id_id=request.session['user_id'])

            reobj = Report()
            reobj.user_id = userobj
            reobj.prd_id = prdobj
            reobj.reson = reson
            reobj.resondate = datetime.now()
            reobj.save()
            messages.success(request, 'Thank you, Review make us stronger')

            notobj = Notificationz()
            notobj.user_id = userobj
            notobj.notificationtime = datetime.now()
            notobj.notificationtext = 'You said that/"'+ reson + '/" ,about '+ prdobj.productname +',[REPORT]'
            notobj.notificationseen = False
            notobj.save()

            return viewmainproduct(request,prdid)
    messages.success(request, 'You need to login before reporting.')
    return login(request)


def showads(request):
    if request.session.has_key('user_id'):
        logobj = LoginTable.objects.get(id=request.session['user_id'])
        adsobj = Ads.objects.filter(logintable=logobj).order_by('-endingdate')

        return render(request, 'viewadvertismentdetails.html', {'ads':adsobj})
    return login(request)


def pauseads(request,ad_id):
    if request.session.has_key('user_id'):
        adobj = Ads.objects.get(id=ad_id)
        adobj.isactive = False
        adobj.save()

        return showads(request)
    return login(request)


def resumeads(request,ad_id):
    if request.session.has_key('user_id'):
        adobj = Ads.objects.get(id=ad_id)

        if adobj.endingdate >= datetime.now().date():
            adobj.isactive = True
            adobj.save()
        else:
            messages.success(request, 'Sorry that ad expired')
        return showads(request)
    return login(request)


def getcommmessage(request):
    if request.method == 'POST':
        data={}
        mesg = request.POST.get('message')

        logobj = LoginTable.objects.get(id=request.session['user_id'])
        userobj = UserInformation.objects.get(login_id=logobj)

        comobj = Community()
        comobj.user_id = userobj
        comobj.actual_message = mesg
        comobj.message_time = datetime.now()
        comobj.save()

        objz = Community.objects.all()
        data = {
            'chats': list(objz.values_list()),
            'totalchat': objz.count(),
            'users': list(UserInformation.objects.all().values_list()),
            'totaluser': UserInformation.objects.all().count()
        }

        return JsonResponse(data)
    return login(request)