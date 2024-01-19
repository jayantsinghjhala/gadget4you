from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',include('app.urls')),
]


admin.site.site_header = "Gadget4You Admin"
admin.site.site_title = "Gadget4You Admin Portal"
admin.site.index_title = "Welcome to Gadget4You Portal"