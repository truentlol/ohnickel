import json
import time
import traceback

from celery import task
import requests

from models import *
from ohnickel.controllers.views import *


#Add to partners inventory
#/tradeoffer/new/partnerinventory/?sessionid=MTg0MjA0NTU1&partner=76561198085559367&appid=570&contextid=2

#START CELERY PROCESS
#./manage.py celeryd -l info


import celery

@task()
def track_listing_tradeoffer_status(listingid):
    try:
        listing = Listing.objects.get(id=listingid)
        user = listing.user

        if listing.tradeoffer == None:
            tradeoffer_json = new_steam_tradeoffer(user=user,trade_items=listing.items.all(),giver="them")

            print "TRADEOFFER JSON: " + json.dumps(tradeoffer_json)

            if tradeoffer_json != None:
                #if success == 'true', tradeofferid should be in the json
                #so create the tradeoffer object and save it to the claim
                if tradeoffer_json['success'] == 'true':

                    #create an expiration time 2 minutes from now
                    utc_time = get_current_utc()
                    expires_at = utc_time + datetime.timedelta(minutes=2)


                    tradeoffer = Tradeoffer(tradeofferid=tradeoffer_json['tradeofferid'],expires_at=expires_at,status='active')
                    tradeoffer.save()


                    listing.tradeoffer = tradeoffer
                    listing.save()
                else:
                    #The tradeoffer legit failed
                    print "Error creating tradeoffer, deleting listing " + str(listing.id)
                    print "Starting authenticate bot"
                    celery.current_app.send_task('ohnickel.tasks.authenticate_bot')

                    #if the bot isnt working atm, just delete this listing
                    #and tell the user to try again in a few minutes
                    listing.delete()
                    return

            else:
                print "Error creating tradeoffer, deleting listing " + str(listing.id)

                print "Starting authenticate bot"
                celery.current_app.send_task('ohnickel.tasks.authenticate_bot')
                #if the bot isnt working atm, just delete this listing
                #and tell the user to try again in a few minutes
                listing.delete()
                return



        #start tradeoffer time
        tradeofferid = listing.tradeoffer.tradeofferid


        trade_complete = False
        while trade_complete is False:
            #Check to see if this unverified listing has been cancled by the user
            try:
                listing = Listing.objects.get(id=listingid)
            except:
                #If there is an error getting the listing,
                #Shut down this task
                tradeoffer_cancel(tradeofferid)
                return


            status = tradeoffer_status(tradeofferid)


            if status == 'active':
                print "status is active"
            elif status == 'accepted':
                print "status is accepted"

                #for some reason deleting the tradeoffer deletes the
                #listing items???
                #listing.tradeoffer.delete()


                #Verify this listing and end this process
                listing.verified = True

                listing.save()
                return
            elif status == 'canceled':
                print "status is canceled"
                listing.tradeoffer.delete()
                print "Trade offer is over"
                listing.delete()
                print 'cancel steam trade request'
                tradeoffer_cancel(tradeofferid)
                return
            elif status == 'countered':
                print "status is countered"
                listing.tradeoffer.delete()
                print "Trade offer is over"
                print 'delete listing'
                listing.delete()
                print 'cancel steam trade request'
                tradeoffer_cancel(tradeofferid)
                return
            elif status == 'declined':
                print "status is declined"
                listing.tradeoffer.delete()
                print 'delete listing'
                listing.delete()
                print 'cancel steam trade request'
                tradeoffer_cancel(tradeofferid)
                return
            elif status == 'invaliditems':
                print "status is invalid"
                print "Trade offer is over"
                listing.tradeoffer.delete()
                print 'delete listing'
                listing.delete()
                print 'cancel steam trade request'
                tradeoffer_cancel(tradeofferid)

            try:
                #Check to see if

                curr_time = get_current_utc()
                if curr_time > listing.tradeoffer.expires_at:
                    #This tradeoffer has expired
                    print 'cancel steam trade request'
                    tradeoffer_cancel(tradeofferid)
                    listing.tradeoffer.delete()
                    listing.delete()

                    return
                else:
                    print "Tradeoffer<" + listing.tradeoffer.tradeofferid + "> expires at " + str(listing.tradeoffer.expires_at)

            except:
                print "tradeoffer doesnt exist"
                #code shouldnt get here but putting this here as safety net
                print "Trade offer is over"
                listing.delete()
                print 'cancel steam trade request'
                tradeoffer_cancel(tradeofferid)
                break

            time.sleep(10)
    except:
        print "TASK FAILED"
        print traceback.print_exc()
        return






#Creates a new tradeoffer and then starts tracking its status
#Until the countdown is over

#item dict holds {defindex:item_count,}
@task()
def track_claim_tradeoffer_status(claimid):


    claim = Claim.objects.get(id=claimid)
    user = claim.user


    #claim.tradeoffer wont be null because it is
    #assigned a tradeoffer right before this is called
    if claim.tradeoffer.status == 'pending':

        tradeoffer_json = new_steam_tradeoffer(user=user,trade_items=claim.items.all(),giver="me")
        print "TRADEOFFER JSON: " + json.dumps(tradeoffer_json)

        #if success == 'true', tradeofferid should be in the json
            #so create the tradeoffer object and save it to the claim
        if tradeoffer_json['success'] == 'true':

            #create an expiration time 2 minutes from now
            utc_time = get_current_utc()
            expires_at = utc_time + datetime.timedelta(minutes=2)
            #tradeoffer = Tradeoffer(tradeofferid=tradeoffer_json['tradeofferid'],expires_at=expires_at,active=True)
            #tradeoffer.save()
            #claim.tradeoffer = tradeoffer
            #claim.save()

            #edit the tradeoffer that should already exist
            claim.tradeoffer.expires_at = expires_at
            claim.tradeoffer.tradeofferid = tradeoffer_json['tradeofferid']
            claim.tradeoffer.status = 'active'
            claim.tradeoffer.save()

            claim.save()
        else:
            print "Error creating tradeoffer, deleting listing " + str(claim.id)
            print "Starting authenticate bot"
            celery.current_app.send_task('ohnickel.tasks.authenticate_bot')

            #if the bot isnt working atm, just delete this listing
            #and tell the user to try again in a few minutes
            #claim.tradeoffer = None

            #Dont delete the tradeoffer, just set it to inactive
            claim.tradeoffer.status = 'inactive'
            claim.tradeoffer.save()

            return

    #if success == 'true', tradeofferid should be in the json
    #so create the tradeoffer object and save it to the claim
    else:
        print 'tradeoffer is not pending, exiting task'
        print 'tradeoffer.status: ' + claim.tradeoffer.status
        #If there is already a current tradeoffer, exit this
        return





    tradeofferid = claim.tradeoffer.tradeofferid

    trade_complete = False
    while trade_complete is False:
        #Check to see if this unverified listing has been cancled by the user
        try:
            claim = Claim.objects.get(id=claimid)
        except:
            #If there is an error getting the listing,
            #Shut down this task
            print "user canceled this claim"
            tradeoffer_cancel(tradeofferid)
            return


        status = tradeoffer_status(tradeofferid)


        if status == 'active':
            print "status is active"
        elif status == 'accepted':
            print "status is accepted"
            #Delete the claim
            #claim.tradeoffer = None
            claim.tradeoffer.status = 'complete'
            #claim.delete()
            claim.tradeoffer.save()

            return
        elif status == 'canceled':
            print "status is canceled"

            #Set tradeoffer to none
            #so the user can request another
            #claim.tradeoffer = None
            claim.tradeoffer.status = 'inactive'
            claim.tradeoffer.save()

            return
        elif status == 'countered':
            print "status is countered"

            print 'cancel steam trade request'
            tradeoffer_cancel(tradeofferid)

            #claim.tradeoffer = None
            claim.tradeoffer.status = 'inactive'
            claim.save()



            return
        elif status == 'declined':
            print "status is declined"
            print 'cancel steam trade request'
            tradeoffer_cancel(tradeofferid)

            claim.tradeoffer.status = 'inactive'
            claim.tradeoffer.save()



            return
        elif status == 'invaliditems':
            print "status is invalid"

            print 'cancel steam trade request'
            tradeoffer_cancel(tradeofferid)

            claim.tradeoffer.status = 'inactive'
            claim.tradeoffer.save()


            return


        try:
            curr_time = get_current_utc()
            if curr_time > claim.tradeoffer.expires_at:
                print 'claim has expired'
                print 'cancel steam trade request'
                tradeoffer_cancel(tradeofferid)
                #This tradeoffer has expired
                claim.tradeoffer.status = 'inactive'
                claim.tradeoffer.save()
                return

            else:
                print "Tradeoffer<" + claim.tradeoffer.tradeofferid + "> expires at " + str(claim.tradeoffer.expires_at)

        except:
            print "Trade offer is over"
            claim.tradeoffer.status = 'inactive'
            claim.tradeoffer.save()
            print 'cancel steam trade request'
            tradeoffer_cancel(tradeofferid)
            break

        time.sleep(10)




#DONT LET THIS METHOD BE CALLED IF THE BOT IS NOT WORKING
#giver = "me" or "them"
#use .all() on items before passing into this function
def new_steam_tradeoffer(user,trade_items,giver):
    print "ATTEMPTING NEW STEAM TRADEOFFER"
    current_bot = get_current_bot()

    #This is just an extra safety precaution to make sure authenticate_bot is not called twice
    #current_bot.working should already be checked at the view level so there is no chance
    #of auth task being called twice
    if current_bot.working:
        headers = {
            'Content-Type':'application/x-www-form-urlencoded; charset=UTF-8',
            'Connection':'keep-alive',
            'Accept':'text/javascript, text/html, application/xml, text/xml, */*',
            'X-Requested-With':'XMLHttpRequest',
            'User-Agent':"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/31.0.1650.57 Safari/537.36",
            'Referer':user.steam_trade_url,
            'Accept-Encoding': 'gzip,deflate,sdch',
            'Accept-Language': 'en-US,en;q=0.8',
            'Timeout':'50000'
        }

        tradeoffer_dict = {
            'newversion':True,
            'version':2,
            'me':{
                'assets':[],
                'currency':[],
                'ready':False
            },
            'them':{
                'assets':[],
                'currency':[],
                'ready':False
            }
        }

        #ASSET
        #{"appid":570,"contextid":2,"amount":1,"assetid":"4076476180"}
        #convert defindex to asset id's

        #Holds defindex:count
        #defindex_dict = {}
        #for item in items:
        #    if item.defindex in defindex_dict:
        #        defindex_dict[item.defindex] += 1
        #    else:
        #        defindex_dict[item.defindex] = 1
        #for trade_item in trade_items:
        #    defindex_dict[trade_item.item.defindex] = trade_item.count

        defindex_list = []
        for trade_item in trade_items:
            defindex_list.append(trade_item.item.defindex)

        #if giver == "me":
        #    #use the bots steam id
        #    id_dict = defindex_to_id(get_current_bot().steamid,defindex_dict)
        #else:
        #    id_dict = defindex_to_id(user.steamid,defindex_dict)
        #id_list = []

        if giver == "me":
            #use the bots steam id
            id_list = defindex_to_id(get_current_bot().steamid,defindex_list)
        else:
            id_list = defindex_to_id(user.steamid,defindex_list)


        print "TRADE OFFER ID LIST"
        print id_list
        # asset = {'appid':570,'contextid':2,'amount':1,'assetid':}
        #for itemid, amount in id_dict.iteritems():
        #    asset = {'appid':570,'contextid':2,'amount':amount,'assetid':str(itemid)}
        #    tradeoffer_dict[giver]['assets'].append(asset)
        for assetid in id_list:
            asset = {'appid':570,'contextid':2,'amount':1,'assetid':str(assetid)}
            tradeoffer_dict[giver]['assets'].append(asset)

        json_tradeoffer_string = json.dumps(tradeoffer_dict)
        trade_url = user.steam_trade_url
        trade_token = extract_token(trade_url)

        print "JSON TRADEOFFER STRING"
        print json_tradeoffer_string


        #Add extra stuff to the cookies so it works with /tradeoffer/new/send
        authenticated_cookies = current_bot.cookies_dict()
        authenticated_cookies.update(current_bot.login_cookies_dict())


        authenticated_cookies['strTradeLastInventoryContext'] = '570_2'
        authenticated_cookies['bCompletedTradeOfferTutorial'] = 'true'
        #authenticated_cookies['webTradeEligibility'] = '%7B%22allowed%22%3A0%2C%22reason%22%3A32%2C%22allowed_at_time%22%3A1410478630%2C%22steamguard_required_days%22%3A15%2C%22sales_this_year%22%3A0%2C%22max_sales_per_year%22%3A200%2C%22forms_requested%22%3A0%2C%22new_device_cooldown_days%22%3A7%7D'

        #TO GET THE WEB TRADE ELIGIBILITY COOKIE,
        #s = requests.Session()
        #trade_url_response = s.get(trade_url,headers=headers,cookies=authenticated_cookies)
        #
        #print s.cookies
        #
        #authenticated_cookies['webTradeEligibility'] = dict(s.cookies)['webTradeEligibility']

        data = {
            #The session cookie MUST be decoded before being passed as a data param
            #because steam does not do it on their end
            'sessionid': urllib.unquote(authenticated_cookies['sessionid']).decode('utf8'),  #Get current sessionid from authenticated cookies
            'partner':user.steamid,
            'tradeoffermessage':'',
            'json_tradeoffer':json_tradeoffer_string,
            "trade_offer_create_params":'{"trade_offer_access_token":"' + trade_token + '"}'
        }
        #r = requests.post('https://steamcommunity.com/tradeoffer/new/send', headers=headers,cookies=cookies,data=data)
        print "SENDING TRADEOFFER POST REQUEST"
        r = requests.post('https://steamcommunity.com/tradeoffer/new/send', headers=headers,cookies=authenticated_cookies,data=data)

        print "TRADEOFFER RESPONSE: " + str(r.text)
        print r.text
        print r.headers
        print r.cookies

        try:
            tradeoffer_response_json = json.loads(r.text)
        except:
            tradeoffer_response_json = None






        if tradeoffer_response_json != None:

            if 'tradeofferid' in tradeoffer_response_json:
                if tradeoffer_response_json['tradeofferid'] != '':
                    print "Tradeoffer was successful!"
                    tradeoffer_response_json['success'] = 'true'
                    return tradeoffer_response_json
                else:
                    check_tradeoffer_data = check_tradeoffer(tradeoffer_dict,user.steamid)
                    if check_tradeoffer_data['success']:
                        #Tradeoffer returned unsuccessfully but was actually created
                        print "Tradeoffer was successful!"
                        tradeoffer_response_json['success'] = 'true'
                        tradeoffer_response_json['tradeofferid'] = check_tradeoffer_data['tradeofferid']
                        return tradeoffer_response_json
                    else:
                        response_json = {}
                        print "Tradeoffer was unsuccessful"
                        #This is the only place authenticate_bot should be called
                        #Since we are setting current_bot.working to False,
                        #No one else should be able to call this task.

                        #Since we are returning false, the caller should delete the listing
                        response_json['success'] = 'false'

                        current_bot.working = False
                        current_bot.save()
                        return response_json
            else:
                check_tradeoffer_data = check_tradeoffer(tradeoffer_dict,user.steamid)
                if check_tradeoffer_data['success']:
                    #Tradeoffer returned unsuccessfully but was actually created
                    print "Tradeoffer was successful!"
                    tradeoffer_response_json['success'] = 'true'
                    tradeoffer_response_json['tradeofferid'] = check_tradeoffer_data['tradeofferid']
                    return tradeoffer_response_json
                else:

                    print "Tradeoffer was unsuccessful"
                    #This is the only place authenticate_bot should be called
                    #Since we are setting current_bot.working to False,
                    #No one else should be able to call this task.

                    #Since we are returning false, the caller should delete the listing
                    current_bot.working = False
                    current_bot.save()
                    return {'success':'false'}


            #Python throws 'keyerror' if tradeoffer doenst exist
            #try:
            #
            #except:
            #    response_json = {}
            #    print "Tradeoffer was unsuccessful"
            #    #This is the only place authenticate_bot should be called
            #    #Since we are setting current_bot.working to False,
            #    #No one else should be able to call this task.
            #
            #    #Since we are returning false, the caller should delete the listing
            #    response_json['success'] = 'false'
            #
            #    current_bot.working = False
            #    current_bot.save()
            #    return response_json

        else:
            check_tradeoffer_data = check_tradeoffer(tradeoffer_dict,user.steamid)
            if check_tradeoffer_data['success']:
                #Tradeoffer returned unsuccessfully but was actually created
                print "Tradeoffer was successful!"
                tradeoffer_response_json['success'] = 'true'
                tradeoffer_response_json['tradeofferid'] = check_tradeoffer_data['tradeofferid']
                return tradeoffer_response_json
            else:

                print "Tradeoffer was unsuccessful"
                #This is the only place authenticate_bot should be called
                #Since we are setting current_bot.working to False,
                #No one else should be able to call this task.

                current_bot.working = False
                current_bot.save()
                return {'success':'false'}


            #call function again so it authenticates,
            #then after call the function again and hopefully work
            #new_steam_tradeoffer(user,items,giver)
            #If the tradeoffer was unsuccessful, try to reauthenticate once\
    else:
        return {'success':'false'}







#TRUENTLOL WORKING COOKIES /dologin/
#POST https://steamcommunity.com/login/dologin/ HTTP/1.1
#Host: steamcommunity.com
#Connection: keep-alive
#Content-Length: 565
#Accept: text/javascript, text/html, application/xml, text/xml, */*
#X-Prototype-Version: 1.7
#Origin: https://steamcommunity.com
#X-Requested-With: XMLHttpRequest
#User-Agent: Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1985.125 Safari/537.36
#Content-type: application/x-www-form-urlencoded; charset=UTF-8
#Referer: https://steamcommunity.com/login/home/?goto=0
#Accept-Encoding: gzip,deflate,sdch
#Accept-Language: en-US,en;q=0.8
#Cookie: steamMachineAuth76561198043771344=C01DB008566B2C5B6E67CD292B77303198F7E513; steamMachineAuth76561198096335208=FF1ECA04C53C55575856790A1D468412AF688FE1; steamMachineAuth76561198147109455=DF403666921CD63503C51E7E46D5E366ED568658; recentlyVisitedAppHubs=247730%2C440%2C22370; Steam_Language=english; sessionid=MzIxNTk1OTk0; steamCC_72_193_38_64=US; tsTradeOffersLastRead=1407212320; timezoneOffset=-25200,0; __utma=268881843.509654730.1401732126.1407722148.1407826325.78; __utmb=268881843.0.10.1407826325; __utmc=268881843; __utmz=268881843.1407397830.74.30.utmcsr=google|utmccn=(organic)|utmcmd=organic|utmctr=(not%20provided)
#
#password=Fcrw88woK2g3S8NO0hzOIJrXT%2FqdYjJ2aHmd%2F9rbGfZ5abo56gHOVEH01Ys2UVWaJmdaBSsQm2n8PS%2FhlR44wCLGjQuomz7ztQWBOjA%2BIKIStzdutRMuYS30c6tBekZcDNnufTi91V1jhm0ubZ8hz1eP%2F997MTigKPF56gNK8jiIzd0%2Bn4gUwvm5oe%2BzhUbjHrEF70IKAG6Qbd%2FdU8KL6724RR%2FDpc8E80N%2B%2BXyU4unMn0cdNnZKpjG%2FDKK%2BTNR9H1ukQjY0afSnNDs8YkyZ7EgUvcopt7e7EH%2F0FzQgJI6JCVI094ug%2B4wvGGTTZoeGz85K5IxGtVazW1%2FojVIwCg%3D%3D&username=truentlol&twofactorcode=&emailauth=&loginfriendlyname=&captchagid=-1&captcha_text=&emailsteamid=&rsatimestamp=39626150000&remember_login=true&donotcache=1407826597170



@task()
def authenticate_bot():
    print "authenticating bot..."
    current_bot = get_current_bot()
    username = current_bot.name
    password = current_bot.password
    #username = 'truentlol'
    #password = 'shahexlol1'
    s = requests.Session()
    #https://steamcommunity.com/login/home/?goto=0

    #This line adds "sessionid" cookie to the session
    home_request = s.get("https://steamcommunity.com/login/home/?goto=0")

    #flags
    logged_in = False
    captcha_needed = False
    emailauth_needed = False

    #json returned from steam
    login_json = None


    print 'encrypting password with javascript from python'
    rsa_json = get_rsa_json(username)
    encoded_password = js_encrypt(rsa_json,password)
    print "ENCODED PASSWORD"
    print encoded_password



    while not logged_in:

        headers = {
            'Content-Type':'application/x-www-form-urlencoded; charset=UTF-8',
            #'method':'post',
            'Connection':'keep-alive',
            'Accept':'text/javascript, text/html, application/xml, text/xml, */*',
            'X-Requested-With':'XMLHttpRequest',
            'User-Agent':"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/31.0.1650.57 Safari/537.36",
            'Referer':'"https://steamcommunity.com/login/home/?goto=0"',
            'Accept-Encoding': 'gzip,deflate,sdch',
            'Accept-Language': 'en-US,en;q=0.8',
            'Timeout':'50000'
        }

        data = {
            'username': username,
            'password': encoded_password,
            'emailauth': '',
            'loginfriendlyname': '',
            'captchagid': -1,
            'captcha_text': '',
            'emailsteamid': '',
            'rsatimestamp': rsa_json['timestamp'],
            'remember_login':'true',
            'donotcache': current_milli_time(),

        }

        captchagid = -1
        captcha_text = ''
        if captcha_needed:
            print "Captcha is required"
            #MMS this image to my cell phone
            #https://steamcommunity.com/public/captcha.php?gid=" + login_json['captcha_gid']
            #then loop here and wait for my response

            #My email response should be In the format of
            #create a new email, NOT a reply
            #Subject: generated_id
            #Body: Captcha
            subject_id = id_generator()
            send_email(subject='Captcha: ' + subject_id,message='https://steamcommunity.com/public/captcha.php?gid=' + login_json['captcha_gid'],to_address='adroitcode@gmail.com')
            #Loops here forever until I enter the captcha code
            while captcha_needed:
                email_msg = check_inbox(subject_id)
                print email_msg
                if email_msg != None:
                    captcha_text = email_msg
                    captcha_needed = False
                    break
                #Check every 30 seconds if I have sent a captcha code
                time.sleep(30)

        data['captchagid'] = captchagid
        data['captcha_text'] = captcha_text



        emailauth = ''
        emailsteamid = ''
        if emailauth_needed:
            print "Email auth is required"
            #text me or email then wait for response
            subject_id = id_generator()
            send_email(subject='EmailAuthCode: ' + subject_id,message='Send email auth code',to_address='adroitcode@gmail.com')
            #Loops here forever until I enter the captcha code
            while emailauth_needed:
                email_msg = check_inbox(subject_id)
                if email_msg != None:
                    email_auth = email_msg
                    emailauth_needed = False
                    break
                #Check every 30 seconds if I have sent a captcha code
                time.sleep(30)


        data['emailauth'] = emailauth
        data['emailsteamid'] = emailsteamid


        login_response = s.post('https://steamcommunity.com/login/dologin/', data=data,cookies=current_bot.login_cookies_dict(),headers=headers)
        print login_response.content
        print login_response.headers
        #Convert steam server response to json
        login_json = json.loads(login_response.text)
        print login_json

        #Set captcha flag for the next loop so we can input it
        try:
            if login_json['captcha_needed']:
                captcha_needed = True
        except:
            print "No captcha needed"
            captcha_needed = False

        #Set steamguard flag for the next loop so we can input it
        try:
            if login_json['emailauth_needed']:
                emailauth_needed = True
        except:
            print "No captcha needed"
            emailauth_needed = False

        #If we are successfully logged in, set the flag so
        #the while loop breaks
        if login_json['success']:
            logged_in = True
            print "SUCCESSFULLY LOGGED IN!"

            #Dont need the session headers
            #print "SESSION HEADERS"
            #print s.headers
            print "SESSION COOKIES"

            print dict(s.cookies) #convert 'cookiejar' to dict

            #After login, steam requires you to submit token/securetoken/auth
            transfer_params = login_json['transfer_parameters']
            xfer_headers = {
                'Connection': 'keep-alive',
                'Content-Length': '184',
                'Cache-Control': 'max-age=0',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1985.125 Safari/537.36',
                'Content-Type': 'application/x-www-form-urlencoded',
                'Referer': 'https://steamcommunity.com/login/home/?goto=0',
                'Accept-Encoding': 'gzip,deflate,sdch',
                'Accept-Language': 'en-US,en;q=0.8'
            }

            xfer_data = {
                'steamid': transfer_params['steamid'],
                'remember_login':'true',
                'token':transfer_params['token'],
                'token_secure':transfer_params['token_secure'],
                'auth':transfer_params['auth']
            }

            #Dont use the session object for this request because it pollutes the cookies (causes duplicates)
            xfer_response = requests.post('https://store.steampowered.com//login/transfer', data=xfer_headers,cookies=current_bot.transfer_cookies_dict(),headers=xfer_data)


            #Convert authenticated cookies with working "sessionid"
            #into string and store with bot
            current_bot.cookies_json = json.dumps(dict(s.cookies))
            current_bot.working = True
            current_bot.save()


import string
import random
def id_generator(size=6, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


from settings import BOT_EMAIL,BOT_EMAIL_PASSWORD
#Checks inbox for email with specific subject
#returns the email body if email is found, None otherwise
def check_inbox(subject):
    ##if not mb.email_box_port: mb.email_box_port = 143
    #server = imaplib.IMAP4(mb.email_box_host, int(143))
    #server.login(mb.email_box_user, mb.email_box_pass)
    #server.select(mb.email_box_imap_folder)
    #status, data = server.search(None, 'ALL')
    try:
        import imaplib
        mail = imaplib.IMAP4_SSL('imap.gmail.com')
        email_address = BOT_EMAIL
        password = BOT_EMAIL_PASSWORD
        mail.login(email_address, password)
        mail.list()
        # Out: list of "folders" aka labels in gmail.
        mail.select("inbox") # connect to inbox.
        #result, data = mail.search(None, "ALL")
        #
        #ids = data[0] # data is a list.
        #id_list = ids.split() # ids is a space separated string
        #latest_email_id = id_list[-1] # get the latest


        result, data = mail.uid('search', None, '(HEADER Subject "' + subject +'")')
        latest_email_uid = data[0].split()[-1]
        result, data = mail.uid('fetch', latest_email_uid, '(RFC822)')
        raw_email = data[0][1]
        print raw_email
        #result, data = mail.fetch(latest_email_id, "(RFC822)") # fetch the email body (RFC822) for the given ID
        #
        #raw_email = data[0][1] # here's the body, which is raw text of the whole email
        #print raw_email

        import email

        email_message = email.message_from_string(raw_email)
        print "DIR"
        print dir(email_message)
        print email_message['To']

        print email.utils.parseaddr(email_message['From']) # for parsing "Yuji Tomita" <yuji@grovemade.com>

        print 'PAYLOAD'
        email_body = str(email_message.get_payload()[0].get_payload()).strip()
        return email_body
    except:
        return None




from django.core.mail import EmailMultiAlternatives


def send_email(subject,message,to_address):
    email_address = BOT_EMAIL #getattr(settings, "BOT_EMAIL", None)
    msg = EmailMultiAlternatives(subject, message, email_address, [to_address])
    #msg.attach_alternative("<a href='" + accept_link +"'>Click here to accept</a>", "text/html")
    msg.send()









def tradeoffer_cancel(tradeofferid):
    #86106882
    current_bot_api_key = get_current_bot().api_key
    try:
        print "Canceling trade offer (" + tradeofferid + ")"
        data = {
            'tradeofferid':tradeofferid,
            'key': current_bot_api_key,
            'language':'english'
        }
        r = requests.post('http://api.steampowered.com/IEconService/CancelTradeOffer/v1/?key=' + current_bot_api_key + '&tradeofferid=' + tradeofferid ,data=data)
        print r.text
    except:
        print "Error canceling listing"
        print traceback.print_exc()


















tradeoffer_status_data = {
    1:'invalid',
    2:'active',
    3:'accepted',
    4:'countered', #recipient made a counter  offer
    5:'expired',
    6:'canceled', #sender canceled
    7:'declined', #recipient declined
    8:'invaliditems' #some of the items are no longer available or missing
}

def tradeoffer_status(tradeofferid):

    try:
        r = requests.get('http://api.steampowered.com/IEconService/GetTradeOffer/v1/?key=1E41E17182126BECB331504414C93700&tradeofferid=' + tradeofferid + '&language=english')
        print r.text
        status_json = json.loads(r.text)
        trade_offer_state = status_json['response']['offer']['trade_offer_state'] #integer
        return tradeoffer_status_data[trade_offer_state]
    except:
        return 'error'

#DJANGO LAMP
#http://carlosgabaldon.com/2010/05/12/django-lamp/



#SCHEMA URL
# http://api.steampowered.com/IEconItems_570/GetSchema/v0001/?key=1E41E17182126BECB331504414C93700

#Item rarity schema.. returns as VDF
# http://cdn.dota2.com/apps/570/scripts/items/items_game.92d7eee66f789a3a7ce613f0103c021887d1b192.txt
@task()
def update_item_db():
    #Iterate through all items in steam schema and
    #see if we already have it in our DB. If not,
    #create it ;)
    item_schema = json.loads(requests.get('http://api.steampowered.com/IEconItems_570/GetSchema/v0001/?key=1E41E17182126BECB331504414C93700').text)
    items_list = item_schema['result']['items']


    #item_rarity_schema = json.loads(open(os.path.join(PROJECT_ROOT,'files/item_rarities.txt')).read())
    #Uses php script on my server to parse VDF format to JSON
    r = requests.post('http://23.226.139.144/static/php/vdf_to_json.php',data={'vdf_url':'http://cdn.dota2.com/apps/570/scripts/items/items_game.92d7eee66f789a3a7ce613f0103c021887d1b192.txt','key':'A1B2C3'})
    item_rarity_schema_json = json.loads(r.text)
    #print json_obj['items_game']['items']['0']['name']

    #item_rarity_dict = item_rarity_schema['items_game']['items']
    item_rarity_dict = item_rarity_schema_json['items_game']['items']


    for steam_item in items_list:
        defindex = str(steam_item['defindex'])
        try:
            item = Item.objects.get(defindex=defindex)
        except:
            #Item doesnt exist
            rarity_info = item_rarity_dict[str(defindex)]
            rarity = 'common'
            try:
                #If the item has a item_rarity attribute,
                #it is uncommon+
                rarity = rarity_info['item_rarity']
            except:
                print ""

            #Capitalize first letter
            rarity = rarity.capitalize()
            item = Item(name=steam_item['name'],defindex=defindex,image_url=steam_item['image_url'],rarity=rarity)
            item.save()






#passin trade url
#and extract token
def extract_token(tradeurl):
    token_index = tradeurl.index("token=")
    token = tradeurl[token_index + 6:]
    return token






#Sometimes steam "fails" creating a tradeoffer, but actually does create it
#and doesnt return the tradeofferid
#This function takes in
def check_tradeoffer(tradeoffer_dict,other_steam_id):
    current_bot = get_current_bot()

    #This is just an extra safety precaution to make sure authenticate_bot is not called twice
    #current_bot.working should already be checked at the view level so there is no chance
    #of auth task being called twice
    if current_bot.working:

        headers = {
                'Content-Type':'application/x-www-form-urlencoded; charset=UTF-8',
                #'method':'post',
                'Connection':'keep-alive',
                'Accept':'text/javascript, text/html, application/xml, text/xml, */*',
                'X-Requested-With':'XMLHttpRequest',
                'User-Agent':"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/31.0.1650.57 Safari/537.36",
                'Referer':'steamcommunity.com',
                'Accept-Encoding': 'gzip,deflate,sdch',
                'Accept-Language': 'en-US,en;q=0.8',
                'Timeout':'50000'
            }
        #http://steamcommunity.com/id/Truentlol/tradeoffers/
        r = requests.get('http://steamcommunity.com/id/Truentlol/tradeoffers/sent',headers=headers,cookies=current_bot.cookies_dict())

        from bs4 import BeautifulSoup

        soup = BeautifulSoup(r.text)
        #print soup
        tradeoffers = soup.findAll("div", { "class" : "tradeoffer" })

        if(len(tradeoffers) > 0):


            #for x in xrange(0,1):
            for tradeoffer in tradeoffers:
                #tradeoffer = tradeoffers[0]

                tradeofferid = tradeoffer['id'].replace('tradeofferid_','')

                item_ctn = tradeoffer.find('div',{'class':'tradeoffer_items_ctn'})

                #my_items_list = item_ctn.findAll('div',{'class':'tradeoffer_items primary'})[0]
                my_items_list = item_ctn.find('div',{'class':'tradeoffer_items primary'})

                #their_items_list = item_ctn.findChildren()[10].findChildren()[4]  #.find("div",{"class":"tradeoffer_item_list"})
                their_items_list = item_ctn.find('div',{'class':'tradeoffer_items secondary'})


                my_items = my_items_list.findAll("div", { "class" : "trade_item" })
                print "my items"
                print my_items
                my_item_ids = []
                for item in my_items:
                    item_data = item.attrs['data-economy-item']
                    print "ITEM DATA"
                    print item_data

                    item_data = item_data.split('/')
                    steam_id = item_data[3]
                    item_id = item_data[2]
                    my_item_ids.append(item_id)




                their_items = their_items_list.findAll("div", { "class" : "trade_item" })
                print "their items"
                print their_items


                their_item_ids = []

                for item in their_items:
                    item_data = item.attrs['data-economy-item']

                    print "ITEM DATA"
                    print item_data

                    item_data = item_data.split('/')
                    steam_id = item_data[3]

                    #Check if this trade is with the person
                    #it's supposed to be
                    if steam_id != other_steam_id:
                        return {'success':False}

                    item_id = item_data[2]
                    their_item_ids.append(item_id)



                same = True
                #Loop through items in my_item_ids and their item_ids
                #and check if id is in the tradeoffer.
                my_asset_id_list = assets_to_id_list(tradeoffer_dict['me']['assets'])
                for item_id in my_item_ids:
                    if item_id not in my_asset_id_list:
                        same = False
                        break

                #only check if same is still true, otherwise waste computation
                their_asset_id_list = assets_to_id_list(tradeoffer_dict['them']['assets'])
                if same is True:
                    for item_id in their_item_ids:
                        if item_id not in their_asset_id_list:
                            same = False
                            break


                #If the tradeoffer is exactly the same,
                #this tradeoffer actually was created even though
                #steam returned an error
                #return tradeofferid
                if same:
                    print 'True'
                    #return HttpResponse(json.dumps({'success': 'true'}), 'application/json')
                    return {'success':True,'tradeofferid':tradeofferid}
                else:
                    return {'success':False}

            #If the code gets here, it has gone through a few recent tradeoffers and has not
            #found one matching the tradeoffer that failed so we can assume that the tradeoffer was not created
            #return {'success':'false'}
            #print 'False'

        else:
            print "tradeoffer actually did fail"
            return {'success':False}
    else:
        print 'Bot is not working atm'
        return {'success':False}


#converts tradeoffer assets to a list of assetid's
def assets_to_id_list(assets):
    asset_id_list = []
    for asset in assets:
        asset_id_list.append(asset['assetid'])
    return asset_id_list




def parse_html():

        headers = {
                'Content-Type':'application/x-www-form-urlencoded; charset=UTF-8',
                #'method':'post',
                'Connection':'keep-alive',
                'Accept':'text/javascript, text/html, application/xml, text/xml, */*',
                'X-Requested-With':'XMLHttpRequest',
                'User-Agent':"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/31.0.1650.57 Safari/537.36",
                'Referer':'steamcommunity.com',
                'Accept-Encoding': 'gzip,deflate,sdch',
                'Accept-Language': 'en-US,en;q=0.8',
                'Timeout':'50000'
            }
        #http://steamcommunity.com/id/Truentlol/tradeoffers/

        r = requests.get('http://steamcommunity.com/id/' + get_current_bot().name.capitalize() + '/tradeoffers/sent')


        from bs4 import BeautifulSoup

        soup = BeautifulSoup(r.text)

        tradeoffers = soup.findAll("div", { "class" : "tradeoffer" })

        if(len(tradeoffers) > 0):
            print "Check the first few tradeoffers to see if one matches the tradeoffer we just sent"

            for x in xrange(0,3):
                tradeoffer = tradeoffers[0]
                print tradeoffer

                #get the item container

                # .findChildren()
                item_ctn = tradeoffer.children[1]

                my_items_list = item_ctn.children[0][2]
                their_items_list = item_ctn.children[2][2]