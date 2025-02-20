from django.shortcuts import render, redirect, get_object_or_404
from django.core.mail import send_mail, EmailMessage
from django.conf import settings
from django.http import HttpResponse
from django.urls import reverse
from django.contrib import messages
from datetime import datetime
from twilio.rest import Client
from .models import Health, Reply
from .forms import HealthForm, AdminReplyForm, UserReplyForm

# Create your views here.

# Twilio Credentials
TWILIO_SID = settings.TWILIO_ACCOUNT_SID
TWILIO_AUTH_TOKEN = settings.TWILIO_AUTH_TOKEN
TWILIO_PHONE_NUMBER = settings.TWILIO_PHONE_NUMBER
MESSAGING_SERVICE_SID = settings.MESSAGING_SERVICE_SID
ADMIN_PHONE_NUMBER = settings.ADMIN_PHONE_NUMBER

# Function to send SMS
def send_sms(to, message):
    client = Client(TWILIO_SID, TWILIO_AUTH_TOKEN)
    client.messages.create(
        messaging_service_sid=MESSAGING_SERVICE_SID,
        body=message,
        from_=TWILIO_PHONE_NUMBER,
        to=to,
    )

# Function to handle form submission and to send encrypted URL via SMS and Email
def health_form(request):
    form = HealthForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        health_instance = form.save()
        encrypted_url = health_instance.generate_encrypted_url()
        url = request.build_absolute_uri(reverse('dashboard', args=[encrypted_url]))

        # Send SMS to Admin
        #sms_body = (
        #    "New Health Form Submitted\n\n"
        #    "A user has submitted a health inquiry. Please review and respond.\n\n"
        #    f"🔗 Dashboard: {url}\n\n"
        #    "Medix - Secure Medical Platform"
        #)
        #send_sms(ADMIN_PHONE_NUMBER, sms_body)

        # Send Email to Admin
        email = EmailMessage(
            subject = 'New Health Form Submitted',
            body=f"""
            <p>Hello Dr,</p>

            <p>A new health form has been submitted by a user.</p>

            <p>To review the details and respond, please click the link below:</p>

            <p><a href="{url}" style="color: blue;">Click here to view</a></p>

            <p>This notification is sent from <strong>Medix</strong>, ensuring secure and efficient communication.</p>

            <p>Best regards, <br> Medix Team</p>
            """,
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[settings.EMAIL_HOST_USER],
        )
        email.content_subtype = "html"  # Important for HTML formatting
        email.send()

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

    # To fetch forms and messages submitted
    health_forms = Health.objects.order_by('-submitted_at')[:5]
    messages_list = Reply.objects.order_by('-created_at')[:10]

    # Greeetings 
    current_hour = datetime.now().hour
    if current_hour < 12:
        greeting = "Good morning"
    elif current_hour < 16:
        greeting = "Good afternoon"
    else:
        greeting = "Good evening"

    context = {
        'health_forms': health_forms,
        'messages_list': messages_list,
        'token': token,
        'greeting': greeting,
        'title': 'Admin Panel | Medix System',
    }

    return render(request, 'pages/dashboard.html', context)

# This function allows the admin to view a form and also to send reply.
def form_details(request, form_id):
    health_instance = get_object_or_404(Health, id=form_id)
    form = AdminReplyForm(request.POST or None, request.FILES or None)  # Handle file uploads)

    if request.method == 'POST' and form.is_valid():
        reply = form.save(commit=False)
        reply.health = health_instance
        reply.generate_encrypted_reply_url()
        reply.save()

        # Notify user via SMS and Email
        reply_url = request.build_absolute_uri(reverse('messages', args=[reply.encrypted_reply_url]))

        # Send SMS
        #sms_body = (
        #    "Important Update on Your Medical Inquiry\n\n"
        #    "Our team has responded to your submission.\n"
        #    "Click the link below to securely view the response:\n\n"
        #    f"🔗 {reply_url}\n\n"
        #    "This message is securely sent from Medix."
        #)
        #send_sms(health_instance.phone, sms_body)

        # Send Email
        email = EmailMessage(
            subject='Important: Response to Your Medical Inquiry',
            body=f"""
            <p>Hi {health_instance.name},</p>

            <p>We have reviewed your submitted health inquiry, and an official response has been provided.</p>

            <p>For detailed information, kindly click the link below to view the response securely:</p>

            <p><a href="{reply_url}" style="color: blue;">Click here to view</a></p>

            <p>Please note that this message was sent from Medix, a secure platform for medical-related inquiries.</p> 

            <p>If you have further questions, you may respond via the provided portal.</p>

            <p>Stay safe and take care!</p>

            <p>Best regards,</p>
            <p><strong> Medix Team </strong></p>
            """,
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[health_instance.email],
        )
        email.content_subtype = "html"  # Important for HTML formatting
        email.send()

        messages.success(request, 'Reply sent successfully!')

    context = {
        'health': health_instance,
        'form': form,
        'title': 'Health Form Details',
    }

    return render(request, 'pages/admin_form_details.html', context)

# This function is to view all messages between admin and users
def all_submisions(request):
    submission_list = Health.objects.order_by('-submitted_at')

    # Greeetings 
    current_hour = datetime.now().hour
    if current_hour < 12:
        greeting = "Good morning"
    elif current_hour < 16:
        greeting = "Good afternoon"
    else:
        greeting = "Good evening"

    context = {
        'submission_list': submission_list,
        'greeting': greeting,
        'title': 'Submissions',
    }

    return render(request, 'pages/all_submission.html', context)

# This function is to view all messages between admin and users
def all_messages(request):
    messages_list = Reply.objects.order_by('-created_at')

    # Greeetings 
    current_hour = datetime.now().hour
    if current_hour < 12:
        greeting = "Good morning"
    elif current_hour < 16:
        greeting = "Good afternoon"
    else:
        greeting = "Good evening"

    context = {
        'messages_list': messages_list,
        'greeting': greeting,
        'title': 'Messages',
    }

    return render(request, 'pages/all_messages.html', context)

# This function allows admin to view and reply users messages via the encrypted URL
def Admin_message_view(request, thread_id):
    reply_instance = get_object_or_404(Reply, id=thread_id) 

    form = AdminReplyForm(request.POST or None, request.FILES or None)  # Handle file uploads

    if request.method == 'POST' and form.is_valid():
        admin_reply = form.save(commit=False)
        admin_reply.health = reply_instance.health
        admin_reply.parent_reply = reply_instance
        admin_reply.sender_type = 'admin'
        admin_reply.generate_encrypted_reply_url()
        admin_reply.save()

        # Notify User via SMS and Email
        reply_url = request.build_absolute_uri(reverse('messages', args=[admin_reply.encrypted_reply_url]))

        # Send SMS
        #sms_body = (
        #    "Important: New reply from Medix.\n\n"
        #    "Our team has responded to your message.\n"
        #    "Click the link below to securely view the response:\n\n"
        #    f"🔗 {reply_url}\n\n"
        #    "This message is securely sent from Medix."
        #)
        #send_sms(reply_instance.health.phone, sms_body)

        # Send Email
        email = EmailMessage(
            subject='Important: New reply from Medix.',
            body=f"""
            <p> Hi {reply_instance.health.name}, </p>

            <p> Our team has responded to your message. </p>

            <p> Click below to view securely: </p>

            <p><a href="{reply_url}" style="color: blue;">Click here to view</a></p>

            <p> Please note that this message was sent from Medix, a secure platform for medical-related inquiries. </p>

            <p> If you have further questions, you may respond via the provided portal. </p>

            <p> Stay safe and take care! </p> 

            <p> Best regards, </p> 
            <p><strong> Medix Team </strong></p>
            """,
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[reply_instance.health.email],
        )
        email.content_subtype = "html"  # Important for HTML formatting
        email.send()
        
        messages.success(request, 'Reply sent successfully!')

    # Ensure chat history is ordered correctly
    chat_history = Reply.objects.filter(health=reply_instance.health).order_by('created_at')

    context = {
        'reply': reply_instance,
        'form': form,
        'chat_history': chat_history,
        'title': 'Medix Direct Messaging: Connect with Our Experts'
    }

    return render(request, 'pages/message.html', context)


# This function allows user to view and reply admin messages via the encrypted URL.
def user_message_view(request, token):
    reply = get_object_or_404(Reply, encrypted_reply_url=token)
    health_instance = reply.health # To get the related health form


    if reply.reply_attempts <= 0:
        return redirect('invalid_token_url') # Invalid token handling
    reply.reply_attempts -= 1
    reply.save()

    form = UserReplyForm(request.POST or None, request.FILES or None)  # Handle file uploads
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
        #sms_body = (
        #    "Hello Dr\n\n"
        #    "User Replied to Your Message\n\n"
        #    "Click below to review:\n\n"
        #    f"🔗 {admin_reply_url}\n\n"
        #    "Medix - Secure Medical Platform"
        #)
        #send_sms(ADMIN_PHONE_NUMBER, sms_body)

        # Send Email
        email = EmailMessage(
            subject='User Responded to Your Message',
            body=f"""
            <p>Hello Dr,</p>

            <p>A user has replied to your message.</p>

            <p>To review the response and provide further assistance, please click the link below:</p>

            <p><a href="{admin_reply_url}" style="color: blue;">Click here to view</a></p>

            <p>This message is securely sent from Medix to ensure seamless communication.</p>  

            <p>Best regards,</p> 
            <p><strong>Medix Team</strong></p>
            """,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[settings.EMAIL_HOST_USER],
        )
        email.content_subtype = "html"  # Important for HTML formatting
        email.send()

        messages.success(request, 'Reply sent successfully!')

    # Ensure messages are retrieved **only once** and in correct order
    chat_history = Reply.objects.filter(health=reply.health).order_by('created_at')

    context={
        'reply': reply,
        'form': form,
        'chat_history': chat_history,
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

