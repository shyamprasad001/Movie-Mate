"""
URL configuration for TicketBooking project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from MovieMate.views import (
    home,
    login_page,
    register_page,
    logout_page,
    booking_history,
    
    # Booking flow
    select_theatre,
    select_show,
    select_seats,
    pay_ticket,
)

from django.conf import settings
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = [
    path('admin/', admin.site.urls),

    # Auth
    path('login/', login_page, name='login'),
    path('register/', register_page, name='register'),
    path('logout/', logout_page, name='logout'),

    # Movie home
    path('', home, name='home'),

    # Booking History
    path('history/', booking_history, name='booking_history'),

    # New Booking Flow (theatre -> show -> seats -> pay)
    path('book/theatre/<uuid:movie_uid>/', select_theatre, name='select_theatre'),
    path('book/show/<uuid:movie_uid>/<uuid:theatre_uid>/', select_show, name='select_show'),
    path('book/seats/<uuid:show_uid>/', select_seats, name='select_seats'),
    path('book/pay/<uuid:ticket_uid>/', pay_ticket, name='pay_ticket'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

urlpatterns += staticfiles_urlpatterns()


