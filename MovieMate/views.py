from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from django.utils import timezone
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives
from django.utils.html import strip_tags

from .models import (
    MovieCategory, Movie,
    Theatre, Show, Seat, Ticket
)

# ---------- Authentication Views ----------
def register_page(request):
    if request.method == "POST":
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')

        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already in use")
            return redirect('register')

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already taken")
            return redirect('register')

        user = User.objects.create_user(username=username, email=email)
        user.set_password(password)
        user.save()
        messages.success(request, "Account created successfully")
        return redirect('login')

    return render(request, 'register.html')


def login_page(request):
    next_url = request.GET.get('next')
    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')
        user_obj = User.objects.filter(email=email).first()

        if not user_obj:
            messages.error(request, "❌ Email not found.")
            return redirect('login')

        user = authenticate(username=user_obj.username, password=password)
        if user:
            login(request, user)
            return redirect(next_url or 'home')
        else:
            messages.error(request, "❌ Invalid password.")
            return redirect('login')

    if next_url:
        messages.warning(request, "⚠️ You must log in to complete this action.")
    return render(request, 'login.html')


def logout_page(request):
    logout(request)
    return redirect('login')


# ---------- Homepage ----------
def home(request):
    movies = Movie.objects.all().order_by('-created_at')
    context = {'movies': movies}
    return render(request, 'home.html', context)


# ---------- Booking Flow ----------
@login_required(login_url='login')
def select_theatre(request, movie_uid):
    movie = get_object_or_404(Movie, uid=movie_uid)
    theatres = Theatre.objects.filter(show__movie=movie).distinct()
    return render(request, 'booking/select_theatre.html', {'movie': movie, 'theatres': theatres})


@login_required(login_url='login')
def select_show(request, movie_uid, theatre_uid):
    movie = get_object_or_404(Movie, uid=movie_uid)
    theatre = get_object_or_404(Theatre, uid=theatre_uid)
    shows = Show.objects.filter(movie=movie, theatre=theatre).order_by('show_time')
    return render(request, 'booking/select_show.html', {'movie': movie, 'theatre': theatre, 'shows': shows})


@login_required(login_url='login')
def select_seats(request, show_uid):
    show = get_object_or_404(Show, uid=show_uid)
    available_seats = Seat.objects.filter(theatre=show.theatre, is_booked=False)

    if request.method == 'POST':
        selected_seats = request.POST.getlist('seats')
        seats = Seat.objects.filter(uid__in=selected_seats)
        total_price = show.movie.price * seats.count()

        ticket = Ticket.objects.create(user=request.user, show=show, total_price=total_price)
        ticket.seats.set(seats)
        for seat in seats:
            seat.is_booked = True
            seat.save()
        ticket.save()

        return redirect('pay_ticket', ticket_uid=ticket.uid)

    return render(request, 'booking/select_seats.html', {'show': show, 'available_seats': available_seats})


@login_required(login_url='login')
def pay_ticket(request, ticket_uid):
    ticket = get_object_or_404(Ticket, uid=ticket_uid, user=request.user)

    if request.method == 'POST':
        ticket.paid_at = timezone.now()  # ✅ Mark as paid
        ticket.save()

        # Send confirmation email
        html_content = render_to_string('emails/email_ticket.html', {
            'user': request.user,
            'ticket': ticket,
        })
        plain_text = strip_tags(html_content)

        email = EmailMultiAlternatives(
            subject='Your Movie Ticket Booking is Confirmed!',
            body=plain_text,
            from_email='seacode001@gmail.com',
            to=[request.user.email],
        )
        email.attach_alternative(html_content, "text/html")
        email.send()

        messages.success(request, "Ticket confirmed and emailed!")
        return redirect('booking_history')

    return render(request, 'booking/pay_ticket.html', {'ticket': ticket})
# ---------- Booking History ----------
@login_required(login_url='login')
def booking_history(request):
    bookings = Ticket.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'booking_history.html', {'bookings': bookings})



