from django.contrib import admin
from django.urls import path
from django.contrib.auth import views as auth_views
from bookings.views import (
    book_appointment,
    booking_success,
    staff_dashboard,
    get_booked_slots,
    update_booking_status,
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', book_appointment, name='book_appointment'),
    path('booking/<int:booking_id>/success/', booking_success, name='booking_success'),
    path('dashboard/', staff_dashboard, name='staff_dashboard'),
    path('api/booked-slots/', get_booked_slots, name='get_booked_slots'),
    path('booking/<int:booking_id>/status/', update_booking_status, name='update_booking_status'),

    # Staff Auth Routes
    path(
        'staff/login/',
        auth_views.LoginView.as_view(template_name='bookings/staff_login.html'),
        name='staff_login'
    ),
    path(
        'staff/logout/',
        auth_views.LogoutView.as_view(next_page='book_appointment'),
        name='staff_logout'
    ),
]