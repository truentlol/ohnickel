from django.contrib import admin

from models import *
#
#
#class UserAdmin(admin.ModelAdmin):
#    fieldsets = [
#        (None,               {'fields': ['name','email','password']}),
#    ]
#    list_display = ('name', 'email')
#
#
#
#class AdminAdmin(admin.ModelAdmin):
#    list_display = ('user',)

from ohnickel.admin_autoregister import autoregister
autoregister('ohnickel',)

#admin.site.register(Trade)
#admin.site.register(User)
#admin.site.register(Listing)
#admin.site.register(Purchase)
#admin.site.register(Item)
#admin.site.register(Tradeoffer)
#admin.site.register(Claim)
#admin.site.register(Wallet)
#admin.site.register(BotCredentials)




#admin.site.register(User,UserAdmin)
#admin.site.register(Admin,AdminAdmin)

#admin.site.register(Member)

