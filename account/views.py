from django.shortcuts import render
from django.contrib.auth import logout
from django.shortcuts import redirect
from django.contrib.auth import authenticate
from django.contrib.auth import login
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from .forms import CustomLoginForm
from django.core.mail import EmailMultiAlternatives
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.urls import reverse
from django.conf import settings
from django.contrib.auth.decorators import login_required
User = get_user_model()

@login_required
def send_account_creation_email(request, user):
    # Generate password reset link
    token = default_token_generator.make_token(user)
    uid = urlsafe_base64_encode(force_bytes(user.pk))
    reset_url = request.build_absolute_uri(
      reverse('password_reset_confirm', kwargs={'uidb64': uid, 'token': token})
    )

    subject = "Welcome to Our Platform - Set Your Password"
    from_email = settings.DEFAULT_FROM_EMAIL
    to_email = [user.email]

    # HTML version
    html_content = f"""
    <html>
      <body style="font-family: Arial, sans-serif; color: #333;">
        <h2 style="color: #2c3e50;">Welcome, {user.first_name}!</h2>
        <p>Your account has been created successfully 🎉</p>
        <p>
          Please set your password by clicking the button below:
        </p>
        <p>
          <a href="{reset_url}" 
             style="background-color: #3498db; color: white; padding: 10px 20px; 
                    text-decoration: none; border-radius: 5px;">
             Set My Password
          </a>
        </p>
        <p>Once you’ve set your password, you can log in with your username: <b>{user.username}</b></p>
        <hr>
        <p style="font-size: 12px; color: #888;">
          If you didn’t request this account, please ignore this email.
        </p>
      </body>
    </html>
    """
    # Plain text version
    text_content = f"""
    Welcome, {user.first_name}!
    Your account has been created successfully. 
    Please set your password by visiting the following link:
    {reset_url}
    Once you’ve set your password, you can log in with your username: {user.username}
    If you didn’t request this account, please ignore this email. 
    """


    msg = EmailMultiAlternatives(subject, text_content, from_email, to_email)
    msg.attach_alternative(html_content, "text/html")
    msg.send()

@login_required
def trigger_account_email(request, user_id):
    user = get_object_or_404(User, pk=user_id)
    send_account_creation_email(request, user)
    return render(request, 'account/password-email-sent.html', {'user': user})

def login_view(request):
    if request.method == "POST":
        form = CustomLoginForm(request.POST)
        if form.is_valid():
            print("Form is valid!")  # debug
            user = form.cleaned_data["user"]
            login(request, user)
            return redirect("notification")  # Redirect to the notification page after login
        else:
            print("Form errors:", form.errors)  # debug
    else:
        form = CustomLoginForm()

    return render(request, "account/user-login.html", {"form": form})

@login_required
def logout_view(request): 
    logout(request)
    return redirect('login_view')  # Redirect to login page after logout
