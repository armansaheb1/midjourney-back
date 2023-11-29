from django.contrib import admin
from .models import Site, Link, ImagineOrder, Image, Transaction, Package, Pretrans, FaceSwaped, Plan, Coupon, Bonus

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