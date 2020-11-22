from datetime import datetime

from django.db import models

# Create your models here.


class LoginTable(models.Model):
    username = models.CharField(max_length=100, unique=True)
    password = models.CharField(max_length=100)
    lcoin = models.IntegerField(default=100)

    def __str__(self):
        return self.username


class UserInformation(models.Model):
    login_id = models.ForeignKey(LoginTable, on_delete=models.CASCADE)
    f_name = models.CharField(max_length=100)
    about_user = models.CharField(max_length=1000, default="")


class Category(models.Model):
    categoryname = models.CharField(max_length=100)


class Product(models.Model):
    user_id = models.ForeignKey(LoginTable, on_delete=models.CASCADE,default=True)
    productname = models.CharField(max_length=500)
    info = models.CharField(max_length=2000)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    product_date = models.DateTimeField(default=datetime.now, blank=True)
    lcoin = models.IntegerField(default=0)
    productimage = models.ImageField()
    is_active = models.BooleanField(default=True)
    is_editable = models.BooleanField(default=True)

    def __str__(self):
        return self.productname


class Returns(models.Model):
    product_id = models.ForeignKey(Product, on_delete=models.CASCADE)
    ret1name = models.CharField(max_length=200)
    ret1info = models.CharField(max_length=1000, default='Nothing much')
    ret2name = models.CharField(max_length=200, default='No Product')
    ret2info = models.CharField(max_length=1000, default='Nothing much')
    ret3name = models.CharField(max_length=200, default='No Product')
    ret3info = models.CharField(max_length=1000, default='Nothing much')


class LayoutPrice(models.Model):
    layout1price = models.IntegerField(default=0)
    layout2price = models.IntegerField(default=0)
    layout3price = models.IntegerField(default=0)


class Ads(models.Model):
    logintable = models.ForeignKey(LoginTable, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    layout = models.CharField(max_length=20)
    totalamount = models.IntegerField(default=0)
    startingdate = models.DateField()
    endingdate = models.DateField()
    adsimage = models.ImageField()
    isactive = models.BooleanField(default=True)


class FavouriteProduct(models.Model):
    user_id = models.ForeignKey(LoginTable, on_delete=models.CASCADE)
    prd_id = models.ForeignKey(Product, on_delete=models.CASCADE)
    like_status = models.BooleanField(default=False)


class ChatRoom(models.Model):
    product_id = models.ForeignKey(Product, on_delete=models.CASCADE)
    participant1 = models.ForeignKey(UserInformation, on_delete=models.CASCADE, related_name='part1')
    participant2 = models.ForeignKey(UserInformation, on_delete=models.CASCADE, related_name='part2')


class Chats(models.Model):
    chatroomid = models.ForeignKey(ChatRoom, on_delete=models.CASCADE)
    user_id = models.ForeignKey(UserInformation, on_delete=models.CASCADE)
    chatmessage = models.CharField(max_length=2000)
    messagetime = models.DateField(default=datetime.now())


class Pigeons(models.Model):
    sender_id = models.ForeignKey(UserInformation, on_delete=models.CASCADE)
    receiver_id = models.ForeignKey(UserInformation, on_delete=models.CASCADE, related_name='receiver')
    product_id = models.ForeignKey(Product, on_delete=models.CASCADE, blank=True)
    actualmessage = models.CharField(max_length=2000)
    messagetime = models.DateTimeField(default=datetime.now,blank=True)
    messageseen = models.BooleanField(default=False)


class RequestExchange(models.Model):
    towhom = models.ForeignKey(UserInformation, on_delete=models.CASCADE)
    fromwhom = models.ForeignKey(UserInformation, on_delete=models.CASCADE, related_name='fromwhom')
    whatproduct = models.ForeignKey(Product, on_delete=models.CASCADE)
    withwhatproduct = models.CharField(max_length=50)
    is_request = models.BooleanField(default=False)
    is_accepted = models.BooleanField(default=False)
    is_responded = models.BooleanField(default=False)
    datetimeofrequest = models.DateTimeField(default=datetime.now())

    def __str__(self):
        return self.whatproduct.productname


class Notificationz(models.Model):
    user_id = models.ForeignKey(UserInformation, on_delete=models.CASCADE)
    notificationtext = models.CharField(max_length=1000)
    notificationtime = models.DateTimeField(default=datetime.now())
    notificationseen = models.BooleanField(default=False)


class Questions(models.Model):
    question = models.CharField(max_length=2000)
    typeofqst = models.CharField(max_length=50)
    option1 = models.CharField(max_length=500)
    option2 = models.CharField(max_length=500)
    option3 = models.CharField(max_length=500)
    option4 = models.CharField(max_length=500)
    answer = models.CharField(max_length=500)

    def __str__(self):
        return self.question


class Games(models.Model):
    game_category = (
        ("action","action"),
        ("puzzle","puzzle"),
        ("fun games","fun games"),
    )
    gamename = models.CharField(max_length=200)
    category = models.CharField(max_length=50, choices=game_category,default='puzzle')
    aboutgame = models.CharField(max_length=2000)
    gameiconimg = models.ImageField()
    gamewallpaperimg = models.ImageField()
    kingofgame = models.CharField(max_length=100, default='Still Waiting')
    totalplays = models.IntegerField(default=0)
    htmlname = models.CharField(default='', max_length=100)
    highestscore = models.IntegerField(default=0)


class GameRating(models.Model):
    userid = models.ForeignKey(UserInformation, on_delete=models.CASCADE)
    review = models.CharField(max_length=2000)
    gameid = models.ForeignKey(Games, on_delete=models.CASCADE)
    reviewtime = models.DateField(default=datetime.now())


class GamePlayed(models.Model):
    userid = models.ForeignKey(LoginTable, on_delete=models.CASCADE)
    gameid = models.ForeignKey(Games, on_delete=models.CASCADE)
    startedgame = models.DateField(default=datetime.now())


class TicketType(models.Model):
    ticketprize = models.IntegerField(default=0)
    ticketcoin = models.IntegerField(default=0)
    ticketname = models.CharField(max_length=200)

    def __str__(self):
        return self.ticketname


class Lticket(models.Model):
    ticketname = models.ForeignKey(TicketType, on_delete=models.CASCADE)
    ticketnumber = models.CharField(max_length=100)
    is_available = models.BooleanField(default=True)

    def __str__(self):
        return self.ticketnumber


class Report(models.Model):
    user_id = models.ForeignKey(UserInformation, on_delete=models.CASCADE)
    prd_id = models.ForeignKey(Product, on_delete=models.CASCADE)
    reson = models.CharField(max_length=2000)
    resondate = models.DateField(default=datetime.now())


class Community(models.Model):
    user_id = models.ForeignKey(UserInformation, on_delete=models.CASCADE)
    actual_message = models.CharField(max_length=2000)
    message_time = models.DateTimeField(default=datetime.now())
