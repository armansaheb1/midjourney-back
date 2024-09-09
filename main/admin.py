from django.contrib import admin
from .models import Link, ImagineOrder, Image, Transaction, Package, Pretrans, FaceSwaped, Plan, Coupon, Bonus, GPTMessages, GPTChatRoom, ImageDetail, AddDetail, Mimic, Parameter, Size, Permissions, Post, Training, File, Phone
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from django.contrib import admin
from django.db import models
from django import forms
from ckeditor.widgets import CKEditorWidget

from .models import Post

class PostAdminForm(forms.ModelForm):
    content = forms.CharField(widget=CKEditorWidget())
    class Meta:
        model = Post
        fields = '__all__'

class PostAdmin(admin.ModelAdmin):
    form = PostAdminForm

admin.site.register(Post, PostAdmin)

class PermissionsInline(admin.StackedInline):
    model = Permissions
    can_delete = False
    verbose_name_plural = "Permissions"

class UserAdmin(BaseUserAdmin):
    inlines = [PermissionsInline]




# Re-register UserAdmin
admin.site.unregister(User)
admin.site.register(User, UserAdmin)
# Register your models here.
#admin.site.register(Site)
#admin.site.register(Link)
admin.site.register(ImagineOrder)
admin.site.register(Transaction)
admin.site.register(Package)
admin.site.register(Pretrans)
admin.site.register(Image)
admin.site.register(FaceSwaped)
admin.site.register(Plan)
admin.site.register(Coupon)
admin.site.register(Bonus)
admin.site.register(GPTMessages)
admin.site.register(GPTChatRoom)
admin.site.register(ImageDetail)
admin.site.register(AddDetail)
admin.site.register(Mimic)
admin.site.register(Parameter)
admin.site.register(Size)
admin.site.register(Permissions)
admin.site.register(Training)
admin.site.register(File)
admin.site.register(Phone)