from django.shortcuts import render, redirect, get_object_or_404
from django.core.mail import send_mail
from django.conf import settings
from django.http import HttpResponse
from django.urls import reverse
from django.contrib import messages
from twilio.rest import Client
from .models import Health, Reply
from .forms import HealthForm, AdminReplyForm, UserReplyForm

# Create your views here.

# Twilio Credentials
TWILIO_SID = settings.TWILIO_ACCOUNT_SID
TWILIO_AUTH_TOKEN = settings.TWILIO_AUTH_TOKEN
TWILIO_PHONE_NUMBER = settings.TWILIO_PHONE_NUMBER
ADMIN_PHONE_NUMBER = settings.ADMIN_PHONE_NUMBER

# Function to send SMS
def send_sms(to, message):
    client = Client(TWILIO_SID, TWILIO_AUTH_TOKEN)
    client.messages.create(body=message, from_=TWILIO_PHONE_NUMBER, to=to)

# Function to handle form submission and to send encrypted URL via SMS and Email
def health_form(request):
    form = HealthForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        health_instance = form.save()
        encrypted_url = health_instance.generate_encrypted_url()
        url = request.build_absolute_uri(reverse('dashboard', args=[encrypted_url]))

        # Send SMS to Admin
        sms_body = (
            "New Health Form Submitted\n\n"
            "A user has submitted a health inquiry. Please review and respond.\n\n"
            f"🔗 Dashboard: {url}\n\n"
            "Medix - Secure Medical Platform"
        )
        send_sms(ADMIN_PHONE_NUMBER, sms_body)

        # Send Email to Admin
        send_mail(
            subject = 'New Health Form Submitted',
            message=f"""Hello Dr,

            A new health form has been submitted by a user.

            To review the details and respond, please access the dashboard using the link below:

            {url}

            This notification is sent from Medix(I used the name 'Medix' just for testing), ensuring secure and efficient communication.

            Best regards,  
            Medix Team  
            """,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=settings.EMAIL_HOST_USER,
            fail_silently=False,
        )

        messages.success(request, 'Form submitted successfully. Our expert will reach out to you via email and SMS to continue the process. Thank you!')
        return redirect('success_url')  # Redirect to a success page

    context={
        'form': form,
        'title': 'Medix Consultation Request Form',
    }

    return render(request, 'pages/form.html', context)

# Function to handle access to the admin dashboard using the encrypted URL.
def dashboard(request, token):
    health_instance = get_object_or_404(Health, encrypted_url=token)

    if health_instance.access_attempts <= 0:
        return redirect('invalid_token_url') # Invalid token handling
    health_instance.access_attempts -= 1
    health_instance.save()

    form = AdminReplyForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        reply = form.save(commit=False)
        reply.health = health_instance
        reply.generate_encrypted_reply_url()
        reply.save()

        # Notify user via SMS and Email
        reply_url = request.build_absolute_uri(reverse('messages', args=[reply.encrypted_reply_url]))

        # Send SMS
        sms_body = (
            "Important Update on Your Medical Inquiry\n\n"
            "Our team has responded to your submission.\n"
            "Click the link below to securely view the response:\n\n"
            f"🔗 {reply_url}\n\n"
            "This message is securely sent from Medix."
        )
        send_sms(health_instance.phone, sms_body)

        # Send Email
        send_mail(
            subject='Important: Response to Your Medical Inquiry',
            message=f"""Hi Dear,

            We have reviewed your submitted health inquiry, and an official response has been provided.  

            For detailed information, kindly click the link below to view the response securely:  

            {reply_url}

            Please note that this message was sent from Medix, a secure platform for medical-related inquiries.  

            If you have further questions, you may respond via the provided portal.  

            Stay safe and take care!  

            Best regards,  
            Medix Team  
            """,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[health_instance.email],
        )

        messages.success(request, 'Reply sent successfully!')

    context = {
        'health': health_instance,
        'form': form,
        'title': 'Admin Panel | Medix System',
    }

    return render(request, 'pages/dashboard.html', context)


# This function allows user to view and reply admin messages via the encrypted URL.
def message_view(request, token):
    reply = get_object_or_404(Reply, encrypted_reply_url=token)

    if reply.reply_attempts <= 0:
        return redirect('invalid_token_url') # Invalid token handling
    reply.reply_attempts -= 1
    reply.save()

    form = UserReplyForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        user_reply = form.save(commit=False)
        user_reply.health = reply.health
        user_reply.parent_reply = reply
        user_reply.sender_type = 'user'
        user_reply.generate_encrypted_reply_url()
        user_reply.save()

        # Notify Admin via SMS and Email
        admin_reply_url = request.build_absolute_uri(reverse('dashboard', args=[reply.health.encrypted_url]))

        # Send SMS
        sms_body = (
            "Hello Dr\n\n"
            "User Replied to Your Message\n\n"
            "A user has responded to your health-related message.\n"
            "Click below to review:\n\n"
            f"🔗 {admin_reply_url}\n\n"
            "Medix - Secure Medical Platform"
        )
        send_sms(ADMIN_PHONE_NUMBER, sms_body)

        # Send Email
        send_mail(
            subject='User Responded to Your Message',
            message=f"""Hello Dr,

            A user has replied to your message regarding their health inquiry.

            To review the response and provide further assistance, please click the link below:  

            {admin_reply_url}

            This message is securely sent from Medix to ensure seamless communication.  

            Best regards,  
            Medix Team
            """,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=settings.EMAIL_HOST_USER,
        )

        messages.success(request, 'Reply sent successfully!')

    context={
        'reply': reply,
        'form': form,
        'title': 'Medix Direct Messaging: Connect with Our Experts'
    }

    return render(request, 'pages/message.html', context)

def success(request):
    context={
        'title': 'Submission Successful! Our Experts Will Reach Out Soon.',   
    }
    return render(request, 'pages/success.html', context)

def expired_view(request):
    context={
        'title': 'Your Access Link Has Expired',   
    }
    return render(request, 'pages/expired.html', context)
