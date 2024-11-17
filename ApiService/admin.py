from django.contrib import admin
from .models import Organization, OrganizationAPIKey, OrganizationAPI, GPTChatRoom, GPTMessages
# Register your models here.


admin.site.register(Organization)
admin.site.register(OrganizationAPI)


admin.site.register(GPTChatRoom)
admin.site.register(GPTMessages)