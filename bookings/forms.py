from django import forms
from django.utils import timezone
from .models import Booking, Service


class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = [
            'service',
            'customer_name',
            'customer_phone',
            'customer_email',
            'booking_date',
            'start_time',
            'notes',
        ]
        widgets = {
            'service': forms.Select(attrs={'class': 'form-select'}),
            'customer_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Full Name'}),
            'customer_phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '10-digit Mobile Number'}),
            'customer_email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email Address (optional)'}),
            'booking_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'start_time': forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 2, 'placeholder': 'Notes or requirements...'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
      
        self.fields['service'].queryset = Service.objects.filter(is_active=True)

    def clean_booking_date(self):
        booking_date = self.cleaned_data.get('booking_date')
        if booking_date and booking_date < timezone.localdate():
            raise forms.ValidationError("You cannot book an appointment for a past date.")
        return booking_date

    def clean(self):
        cleaned_data = super().clean()
        booking_date = cleaned_data.get('booking_date')
        start_time = cleaned_data.get('start_time')

        if booking_date and start_time:
            conflict = Booking.objects.filter(
                booking_date=booking_date,
                start_time=start_time,
                status__in=['CONFIRMED', 'COMPLETED']
            ).exists()

            if conflict:
                formatted_date = booking_date.strftime('%d-%b-%Y')
                formatted_time = start_time.strftime('%I:%M %p')
                raise forms.ValidationError(
                    f"The time slot at {formatted_time} on {formatted_date} is already reserved. Please select another slot."
                )

        return cleaned_data