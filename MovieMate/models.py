from django.db import models
from django.contrib.auth.models import User
import uuid

# 🔹 Base Model
class BaseModel(models.Model):
    uid = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True)
    created_at = models.DateTimeField(auto_now_add=True)  # Changed to DateTime for accurate booking logs
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

# 🔹 Movie & Category
class MovieCategory(BaseModel):
    category_name = models.CharField(max_length=100)

    def __str__(self):
        return self.category_name

class Movie(BaseModel):
    category = models.ForeignKey(MovieCategory, on_delete=models.CASCADE, related_name="movies")
    movie_name = models.CharField(max_length=100)
    price = models.IntegerField(default=100)
    images = models.CharField(max_length=500)

    def __str__(self):
        return self.movie_name

# 🔹 Theatre & Shows (New flow: Book > Theatre > Show > Seat)
class Theatre(BaseModel):
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.name} - {self.location}"

class Show(BaseModel):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    theatre = models.ForeignKey(Theatre, on_delete=models.CASCADE)
    show_time = models.DateTimeField()

    def __str__(self):
        if self.show_time:
            return f"{self.movie.movie_name} at {self.theatre.name} - {self.show_time.strftime('%d %b %Y, %I:%M %p')}"
        return f"{self.movie.movie_name} at {self.theatre.name} - No Time Set"


# 🔹 Seats & Tickets
class Seat(BaseModel):
    theatre = models.ForeignKey(Theatre, on_delete=models.CASCADE)
    seat_number = models.CharField(max_length=10)
    is_booked = models.BooleanField(default=False)

    def __str__(self):
        return f"Seat {self.seat_number} in {self.theatre.name}"

class Ticket(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    show = models.ForeignKey(Show, on_delete=models.CASCADE)
    seats = models.ManyToManyField(Seat)
    total_price = models.FloatField()
    booked_at = models.DateTimeField(auto_now_add=True)

    # ✅ Add this field
    paid_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"Ticket #{self.uid} for {self.user.username} - ₹{self.total_price}"
