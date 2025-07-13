from django.contrib import admin
from .models import MovieCategory, Movie, Theatre, Show, Seat, Ticket

@admin.register(MovieCategory)
class MovieCategoryAdmin(admin.ModelAdmin):
    list_display = ['category_name']

@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    list_display = ['movie_name', 'category', 'price']

@admin.register(Theatre)
class TheatreAdmin(admin.ModelAdmin):
    list_display = ['name', 'location']

@admin.register(Show)
class ShowAdmin(admin.ModelAdmin):
    list_display = ['movie', 'theatre', 'show_time']

@admin.register(Seat)
class SeatAdmin(admin.ModelAdmin):
    list_display = ['theatre', 'seat_number', 'is_booked']
    list_filter = ['theatre', 'is_booked']
    search_fields = ['seat_number']

# Register your models here.
@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = ('user', 'show', 'total_price', 'paid_at', 'created_at')
    list_filter = ('paid_at', 'created_at')
    search_fields = ('user__username', 'show__movie__movie_name', 'show__theatre__name')