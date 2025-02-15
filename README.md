__Encrypted URL Notification System__

__Overview__

This project is a secure form submission system that generates a one-time encrypted URL upon user submission and sends it to the admin via SMS using Twilio. The encrypted URL leads to a web-based software platform for continuous communication between users and admins. This ensures secure and seamless interaction while maintaining data confidentiality.

__Features__

    i. Secure form submission

    ii. One-time encrypted URL generation

    iii. SMS notification to the admin using Twilio

    iv. Web-based communication platform for continuous interaction

    v. Scalable and globally accessible solution

    vi. Django-powered backend

__Technologies Used__

    i. Backend: Django (Python)

    ii. Frontend: HTML, TailwindCSS

    iii. SMS Service: Twilio API

    iv. Database: SQLite (for development)

    v. Security: URL encryption for secure link transmission


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
    
    5. Apply migrations & run the server

        python manage.py migrations

        python manage.py migrate

        python manage.py runserver

__Usage__

    i. Users fill out and submit the form.

    ii. The system generates a one-time encrypted URL.

    iii. The admin receives an SMS with the secure link via Twilio.

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