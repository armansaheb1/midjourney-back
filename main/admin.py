from django.contrib import admin
from .models import Site, Link, ImagineOrder, Image, Transaction

# Register your models here.
admin.site.register(Site)
admin.site.register(Link)
admin.site.register(ImagineOrder)
admin.site.register(Transaction)
#admin.site.register(Image)
