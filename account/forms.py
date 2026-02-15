from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth import get_user_model

User = get_user_model()

class CustomLoginForm(forms.Form):
    username = forms.CharField(
        max_length=150,
        label="Nom d'utilisateur",
        required=True
    )
    password = forms.CharField(
        widget=forms.PasswordInput,
        label="Mot de passe",
        required=True
    )
    user_type = forms.ChoiceField(
        choices=User.USER_TYPE_CHOICES,
        label="Type d'utilisateur",
        required=True
    )

    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get("username")
        password = cleaned_data.get("password")
        user_type = cleaned_data.get("user_type")

        # Authenticate user
        user = authenticate(username=username, password=password)
        if user is None:
            raise forms.ValidationError("Nom d'utilisateur ou mot de passe invalide.")

        # Extra checks
       
        if user.user_type != user_type:
            raise forms.ValidationError("Type d'utilisateur invalide pour ce compte.")

        cleaned_data["user"] = user
        return cleaned_data