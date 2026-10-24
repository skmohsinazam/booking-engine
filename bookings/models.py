import urllib.parse
from django.db import models


class Service(models.Model):
    name = models.CharField(max_length=150)
    description = models.TextField(blank=True)
    duration_minutes = models.PositiveIntegerField(default=30)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.name} ({self.duration_minutes} mins - ₹{self.price})"


class Booking(models.Model):
    STATUS_CHOICES = [
        ('CONFIRMED', 'Confirmed'),
        ('COMPLETED', 'Completed'),
        ('CANCELLED', 'Cancelled'),
    ]

    service = models.ForeignKey(Service, on_delete=models.PROTECT, related_name='bookings')
    customer_name = models.CharField(max_length=120)
    customer_phone = models.CharField(max_length=15)
    customer_email = models.EmailField(blank=True)
    booking_date = models.DateField()
    start_time = models.TimeField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='CONFIRMED')
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('booking_date', 'start_time')
        ordering = ['-booking_date', '-start_time']

    def __str__(self):
        return f"{self.customer_name} - {self.service.name} ({self.booking_date} at {self.start_time.strftime('%I:%M %p')})"

    def get_whatsapp_url(self):
        raw_phone = self.customer_phone.replace(' ', '').replace('-', '').replace('+', '')
        if len(raw_phone) == 10:
            formatted_phone = f"91{raw_phone}"
        else:
            formatted_phone = raw_phone

        formatted_time = self.start_time.strftime("%I:%M %p")
        message = (
            f"Hello {self.customer_name}, your appointment for *{self.service.name}* "
            f"has been confirmed for *{self.booking_date.strftime('%d-%b-%Y')}* at *{formatted_time}*. "
            f"Please reach out if you need to reschedule."
        )
        encoded_message = urllib.parse.quote(message)
        return f"https://wa.me/{formatted_phone}?text={encoded_message}"
    
    def get_whatsapp_cancel_url(self):
        raw_phone = self.customer_phone.replace(' ', '').replace('-', '').replace('+', '')
        formatted_phone = f"91{raw_phone}" if len(raw_phone) == 10 else raw_phone
        formatted_time = self.start_time.strftime("%I:%M %p")

        message = (
            f"Dear {self.customer_name}, your appointment for *{self.service.name}* "
            f"on *{self.booking_date.strftime('%d-%b-%Y')}* at *{formatted_time}* has been *Cancelled*. "
            f"Please reach out to us if you would like to reschedule."
        )
        return f"https://wa.me/{formatted_phone}?text={urllib.parse.quote(message)}"