from datetime import datetime, time
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import user_passes_test
from .models import Booking, Service
from .forms import BookingForm


# Helper function: Check if the user is logged in AND marked as staff
def is_staff_user(user):
    return user.is_authenticated and user.is_staff


def book_appointment(request):
    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            booking = form.save()
            return redirect('booking_success', booking_id=booking.id)
    else:
        form = BookingForm()

    services = Service.objects.filter(is_active=True)
    return render(request, 'bookings/book_appointment.html', {
        'form': form,
        'services': services,
    })


def booking_success(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)
    whatsapp_url = booking.get_whatsapp_url()
    return render(request, 'bookings/booking_success.html', {
        'booking': booking,
        'whatsapp_url': whatsapp_url,
    })


@user_passes_test(is_staff_user, login_url='staff_login')
def staff_dashboard(request):
    selected_date = request.GET.get('date')
    bookings = Booking.objects.select_related('service').order_by('booking_date', 'start_time')

    if selected_date:
        bookings = bookings.filter(booking_date=selected_date)

    total_count = Booking.objects.count()
    confirmed_count = Booking.objects.filter(status='CONFIRMED').count()

    return render(request, 'bookings/dashboard.html', {
        'bookings': bookings,
        'total_count': total_count,
        'confirmed_count': confirmed_count,
        'selected_date': selected_date,
    })


def get_booked_slots(request):
    """Returns booked time strings ('HH:MM') for a given date."""
    date_str = request.GET.get('date')
    if not date_str:
        return JsonResponse({'booked_slots': []})

    try:
        selected_date = datetime.strptime(date_str, '%Y-%m-%d').date()
    except ValueError:
        return JsonResponse({'booked_slots': []})

    booked_times = Booking.objects.filter(
        booking_date=selected_date,
        status__in=['CONFIRMED', 'COMPLETED']
    ).values_list('start_time', flat=True)

    formatted = [t.strftime('%H:%M') for t in booked_times]
    return JsonResponse({'booked_slots': formatted})


@require_POST
@user_passes_test(is_staff_user, login_url='staff_login')
def update_booking_status(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)
    new_status = request.POST.get('status')
    if new_status in dict(Booking.STATUS_CHOICES):
        booking.status = new_status
        booking.save()
    return redirect('staff_dashboard')