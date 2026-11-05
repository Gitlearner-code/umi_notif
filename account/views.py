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

  subject = "UMI NOTIF — Définissez votre mot de passe"
  from_email = settings.DEFAULT_FROM_EMAIL
  to_email = [user.email]

  # HTML version
  html_content = f"""
  <html>
    <body style="font-family: Arial, sans-serif; color: #333;">
      <h2 style="color: #2c3e50;">Bienvenue, {user.first_name} !</h2>
      <p>Votre compte a été créé avec succès.</p>
      <p>
        Veuillez définir votre mot de passe en cliquant sur le bouton ci-dessous :
      </p>
      <p>
        <a href="{reset_url}" 
            style="background-color: #3498db; color: white; padding: 10px 20px; 
                  text-decoration: none; border-radius: 5px;">
            Définir mon mot de passe
        </a>
      </p>
      <p>Une fois votre mot de passe défini, connectez-vous avec l'identifiant : <b>{user.username}</b></p>
      <hr>
      <p style="font-size: 12px; color: #888;">
        Si vous n'êtes pas à l'origine de cette demande, ignorez cet e-mail.
      </p>
    </body>
  </html>
  """
  # Plain text version
  text_content = f"""
  Bienvenue, {user.first_name} !
  Votre compte a été créé avec succès.
  Définissez votre mot de passe en visitant le lien suivant :
  {reset_url}
  Une fois votre mot de passe défini, connectez-vous avec l'identifiant : {user.username}
  Si vous n'êtes pas à l'origine de cette demande, ignorez cet e-mail.
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
    return redirect('login_view')  
