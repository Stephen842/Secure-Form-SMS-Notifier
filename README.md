__Secure Encrypted Messaging Platform__

This project is a secure and dynamic messaging system designed for confidential communication between users and administrators.

It ensures that messages are securely transmitted through one-time encrypted URLs, preventing unauthorized access while maintaining seamless interaction.

__Core Features:__

    i. User Form Submission: Users fill out and submit a health-related form containing personal and medical details.

    ii. Automated Notifications: Upon submission, the system generates a one-time encrypted URL and sends it to the admin via SMS and email for immediate access.

    iii. Admin Dashboard: The encrypted URL directs the admin to a secure dashboard where they can view and manage all user messages.

    iv. Reply System: The admin can reply to user messages from the dashboard. Once a reply is sent, the system generates another one-time encrypted URL and sends it to the user via SMS and email.

    v. User Response: Users can also reply to admin messages through their own secure messaging interface, ensuring a continuous and secure conversation.

    vi. Expiration Mechanism: Each encrypted URL expires after three access attempts, enhancing security and preventing unauthorized access.

    vii. Frontend & UI: The platform is styled with HTML and TailwindCSS for a modern, responsive, and user-friendly interface.

__Features__

    i. Secure form submission

    ii. One-time encrypted URL generation

    iii. SMS notification to the admin using Twilio

    iv. Email notification to the admin

    v. Web-based communication platform for continuous interaction

    vi. Scalable and globally accessible solution

    vii. Django-powered backend

__Technologies Used__

    i. Backend: Django (Python)

    ii. Frontend: HTML, TailwindCSS

    iii. SMS Service: Twilio API

    iv. Email Service: Django Email Backend (SMTP / Gmail)

    v. Database: SQLite (for development)

    vi. Security: URL encryption for secure link transmission


__Installation & Setup__

    1. Clone the repository

        git clone https://github.com/yourusername/Secure-Form-SMS-Notifier.git

        cd Secure-Form-SMS-Notifier

    2. Set up a virtual environment

        python -m venv venv

        source venv/bin/activate  # On Windows, use venv\Scripts\activate

    3. Install dependencies

        pip install -r requirements.txt

    4. Configure environment variables

        Create a .env file and add the following:

            TWILIO_ACCOUNT_SID=your_account_sid

            TWILIO_AUTH_TOKEN=your_auth_token

            TWILIO_PHONE_NUMBER=your_twilio_number

            ADMIN_PHONE_NUMBER=admin_phone_number

            SECRET_KEY=your_django_secret_key

            Email Configuration
            
            EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
            
            EMAIL_HOST=smtp.gmail.com
            
            EMAIL_PORT=587
            
            EMAIL_USE_TLS=True
            
            EMAIL_HOST_USER=your_email@example.com
            
            EMAIL_HOST_PASSWORD=your_email_password
            
            ADMIN_EMAIL=admin@example.com
    
    5. Apply migrations & run the server

        python manage.py migrations

        python manage.py migrate

        python manage.py runserver

__Usage__

    i. Users fill out and submit the form.

    ii. The system generates a one-time encrypted URL.

    iii.The admin receives:

        a. An SMS with the secure link via Twilio

        b. An Email with the encrypted URL

    iv. The link is valid for a single use and ensures confidentiality.

    v. The encrypted URL leads to a web-based software for continuous communication.
    
__License__

    This project is licensed under the MIT License. See the LICENSE file for more details.

__Contributing__

Contributions are welcome! To contribute:

__Fork the repository__

    i. Create a new branch (feature-branch)

    ii. Commit your changes (git commit -m "Added new feature")

    iii. Push to the branch (git push origin feature-branch)

    iv. Open a Pull Request