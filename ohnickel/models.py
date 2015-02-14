from django.db import models
from django import forms
import requests, json
#/manage.py schemamigration tweets --auto  or --initial
#/manage.py migrate tweets

#Grap any SQLite GUI tool (i.e. http://sqliteadmin.orbmu2k.de/)
#Change your model definition to match database definition (best approach is to comment new fields)
#Delete migrations folder in your model
#Delete rows in south_migrationhistory table where app_name match your application name (probably homework)
#Invoke: ./manage.py schemamigration <app_name> --initial
#Create tables by ./manage.py migrate <app_name> --fake (--fake will skip SQL execute because table already exists in your database)
#Make changes to your app's model
#Invoke ./manage.py schemamigration <app_name> --auto
#Then apply changes to database: ./manage.py migrate <app_name>

from django.db import models

from decimal import Decimal
import datetime

from django.utils import six, timezone
#import timezone



from django.db import models



class User(models.Model):

    username   = models.TextField(default='')




    last_login = models.DateTimeField(default=None, blank=True, null=True)
    is_active  = models.BooleanField(default=False)




    uid = models.TextField(default='')
    email = models.TextField(default='')


    is_admin = models.BooleanField(default=True)




    jointed_at = models.DateTimeField(auto_now_add=True, blank=True)



    def __unicode__(self):
        return "%s" % (self.username)




class Forum(models.Model):
    name = models.TextField(default='')

    description = models.TextField(default='')



    user = models.ForeignKey(User,related_name='forums')



    sticky = models.BooleanField(default=False)


    created_at = models.DateTimeField(auto_now_add=True, blank=True)


    def __unicode__(self):
        return "%s" % (self.name)



class Thread(models.Model):
    forum = models.ForeignKey(Forum,related_name='threads')

    name = models.TextField(default='')

    views = models.IntegerField(default=0)

    user = models.ForeignKey(User,related_name='threads')


    created_at = models.DateTimeField(auto_now_add=True, blank=True)


    def __unicode__(self):
        return "%s" % (self.name)



class Post(models.Model):
    thread = models.ForeignKey(Thread,related_name='posts')

    name = models.TextField(default='')


    text = models.TextField(default='')

    user = models.ForeignKey(User,related_name='posts')

    created_at = models.DateTimeField(auto_now_add=True, blank=True)


    def __unicode__(self):
        return "%s" % (self.name)


#
#
#
#
#
#
#
#
#class Wallet(models.Model):
#    address = models.TextField(default='')
#
#    #check if wallet has enough coin before calling
#    #this method or else it will return an error
#    def send_to_address(self, amount, address):
#        print 'Sending ' + str(amount) + " BTC to " + address
#        #Convert to satoshi form
#        amount *= Decimal(100000000)
#        print "SATOSHI AMOUNT: " + str(amount)
#        payload = {
#            'password': wallet_password,
#            'to': address,
#            'amount': str(amount).replace('.0000',''),   #multiping decimals adds four zeros after decimal point
#            'from': self.address,
#            'note': 'Test payment from steamcoins.com'
#        }
#        r = requests.get(base_blockchain_url + '/payment', params=payload)
#
#        json_data = json.loads(r.text)
#        #All bitcoin values are in Satoshi i.e. divide by 100000000 to get the amount in BTC.
#        print json_data
#        return json_data
#        #If there is an error, return false
#
#
#    def get_balance(self):
#        payload = {
#            'password': wallet_password,
#            'address': self.address,
#            'confirmations': '1' #'1'
#        }
#        r = requests.get(base_blockchain_url + '/address_balance', params=payload)
#
#        json_data = json.loads(r.text)
#        #All bitcoin values are in Satoshi i.e. divide by 100000000 to get the amount in BTC.
#        return json_data['balance'] / 100000000.0
#
#
#    def get_balance_usd(self,bitcoin_balance):
#        payload = {
#            'qty':bitcoin_balance
#        }
#
#        r = requests.get('https://coinbase.com/api/v1/prices/buy', params=payload)
#
#        json_data = json.loads(r.text)
#        usd_price = json_data['subtotal']['amount']
#
#        #All bitcoin values are in Satoshi i.e. divide by 100000000 to get the amount in BTC.
#        return usd_price
#
#
#
#class User(models.Model):
#    name = models.TextField()
#
#    steamid = models.TextField()
#    steam_trade_url = models.TextField(default='')
#    img_url = models.TextField(default='')
#    wallet = models.ForeignKey(Wallet,null=True,default=None)
#
#    #wallet_address = models.TextField(default='')
#
#
#
#class Trade(models.Model):
#
#    steamid = models.TextField()
#
#class Item(models.Model):
#    name = models.TextField()
#    defindex = models.TextField()
#    rarity = models.TextField()
#    image_url = models.TextField()
#
#    def __unicode__(self):
#        return "%s" % (self.defindex)
#
#from django.contrib.contenttypes import generic
#
#
#
##class TradeItems(models.Model):
##    #listing = models.ForeignKey(Listing,related_name='items')
##    article = generic.GenericForeignKey('content_type', 'object_id')
##    #tradeoffer = models.ForeignKey(Tradeoffer,related_name='items') #generic.GenericForeignKey()
##    item = models.ForeignKey(Item)
##    quantity = models.IntegerField()
#
#
#
#
#class Listing(models.Model):
#    #Essentially the user
#    user = models.ForeignKey(User,related_name='listings')
#    #items = models.ManyToManyField(Item,blank=True)
#    items_json = models.TextField(default='')
#    #Max price is 999,999.99
#    usd_price = models.DecimalField(max_digits=8, decimal_places=2)
#    verified = models.BooleanField(default=False)
#    sold = models.BooleanField(default=False)
#    tradeoffer = models.ForeignKey(Tradeoffer,related_name='listings',null=True,default=None)
#    #appid - holds id of steam game that items are from
#
#    #items = generic.GenericRelation(TradeItems)
#
#    created_at = models.DateTimeField()
#
#    def save(self, *args, **kwargs):
#        if not self.id:
#            self.created_at = datetime.datetime.today()
#
#        return super(Listing, self).save(*args, **kwargs)
#
#    def formatted_price(self):
#        return "%01.2f" % self.usd_price
#
#
#    def __unicode__(self):
#        return "%s" % (self.id)
#
##/listing/id/cancel
##delete the listing
##create a new claim obj with
##items field
##have user be able to click
#
#class Claim(models.Model):
#    user = models.ForeignKey(User,null=True,default=None)
#    tradeoffer = models.ForeignKey(Tradeoffer,null=True,default=None,related_name="claims")
#    #items = models.ManyToManyField(Item,blank=True)
#    #items = generic.GenericRelation(TradeItems)
#
#
#    #def __unicode__(self):
#    #    return "%s - %s - %s" % (self.id,self.user.name,self.tradeoffer.id)
#
#    def __unicode__(self):
#        return "%s" % (self.id)
#
#class ListingItems(models.Model):
#    listing = models.ForeignKey(Listing,related_name='items')
#    #article = generic.GenericForeignKey('content_type', 'object_id')
#    #tradeoffer = models.ForeignKey(Tradeoffer,related_name='items') #generic.GenericForeignKey()
#    item = models.ForeignKey(Item)
#    count = models.IntegerField(default=1)
#
#
#class ClaimItems(models.Model):
#    claim = models.ForeignKey(Claim,related_name='items')
#    #article = generic.GenericForeignKey('content_type', 'object_id')
#    #tradeoffer = models.ForeignKey(Tradeoffer,related_name='items') #generic.GenericForeignKey()
#    item = models.ForeignKey(Item)
#    count = models.IntegerField(default=1)
#
#class Purchase(models.Model):
#    listing = models.ForeignKey(Listing,null=True,default=None,related_name='purchases')
#    #'user' for now
#    user = models.ForeignKey(User,related_name='purchases')
#    #final_bitcoin_price = models.DecimalField(max_digits=8, decimal_places=6)
#    #Bitcoin verification code
#    #code = models.TextField()
#    #finalized = models.BooleanField(default=False)
#    #items_claimed = models.BooleanField(default=False)
#    #tradeoffer = models.ForeignKey(Tradeoffer,related_name='purchases', null=True,default=None)
#
#class BotCredentials(models.Model):
#    name = models.TextField(default='')
#    password = models.TextField(default='')
#    steamid = models.TextField(default='')
#    api_key = models.TextField(default='')
#
#    working = models.BooleanField(default=False)
#    #This holds the authenticated cookies
#    #with sessionid
#    cookies_json = models.TextField(default='{}')
#
#    #this contains the machine auth code/s cookies
#    #and no session id
#    #used strictly for re-logging in
#    #copy cookies from steam /dologin/
#    login_cookies_json = models.TextField(default='')
#
#    #These are the cookies sent to //login/transfer
#    #alot of overlap amongst these cookie fields but its not that
#    #much work to just put them in here once
#    #and not have to deal with it again
#    transfer_cookies_json = models.TextField(default='')
#    #converts cookies_json string to dict
#    def cookies_dict(self):
#        cookies = json.loads(self.cookies_json)
#        return cookies
#
#    def login_cookies_dict(self):
#        cookies = json.loads(self.login_cookies_json)
#        return cookies
#
#    def transfer_cookies_dict(self):
#        cookies = json.loads(self.transfer_cookies_json)
#        return cookies
#
#    def __unicode__(self):
#        return "%s" % (self.name)
#
#



#class CustomMemberManager(UserManager):
#    def create_user(self):
#        return self.model._default_manager.create()
#
#class Member(models.Model):
#    username   = models.CharField(max_length=20)
#    last_login = models.DateTimeField(blank=True)
#    is_active  = models.BooleanField(default=False)
#    steam_id = models.CharField(max_length=20)
#    reputation = models.IntegerField(default=0)
#    objects = CustomMemberManager()

#class User(models.Model):
#    username = models.CharField(max_length=20)
#    email = models.CharField(max_length=30)
#    password = models.CharField(max_length=20)
#
#    def __unicode__(self):
#        return "%s" % (self.name)

#class Admin(models.Model):
#    user = models.ForeignKey(User,related_name='admins')
#
#
#class UserForm(forms.ModelForm):
#    password = forms.CharField(widget=forms.PasswordInput())
#    class Meta:
#        model = User


