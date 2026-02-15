# forms.py
from django import forms
from .models import Message

class MessageForm(forms.ModelForm):
    departement = forms.ChoiceField(
        choices=[('', 'Select your department')] + Message.DEPARTEMENT_CHOICES,
        widget=forms.Select()   
    )
    level = forms.ChoiceField(
        choices=[('', 'Choose your level')],  # Initial empty choice
        widget=forms.Select()
    )
    message_type = forms.ChoiceField(
        choices=[('', 'Message type')] + Message.MESSAGE_TYPE_CHOICES,
        widget=forms.Select()
    )

    class Meta:
        model = Message
        fields = ['departement', 'level', 'message_type', 'content']
        widgets = {
            'departement': forms.Select(attrs={'placeholder': 'Select your department'}),
            'level': forms.Select(attrs={'placeholder': 'Choose your level'}),
            'message_type': forms.Select(attrs={'placeholder': 'Message type'}),
            'content': forms.Textarea(attrs={'placeholder': 'Write your message here...'}),
        }


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Default: no filtering until department is chosen
        self.fields['level'].choices = []

        if 'departement' in self.data:
            dept = self.data.get('departement')

            if dept == 'BA':
                self.fields['level'].choices = [('L1','L1'),('L2','L2'),('L3','L3')]
            elif dept == 'G.CIVIL':
                self.fields['level'].choices = [('L1','L1'),('L2','L2'),('L3','L3'),('L4','L4'),('L5','L5')]
            elif dept == 'BTS':
                self.fields['level'].choices = [('L1','L1'),('L2','L2'),('L3','L3')]
            elif dept == 'SEG':
                self.fields['level'].choices = [('L1','L1'),('L2','L2'),('L3','L3')]
            elif dept == 'GLT':
                self.fields['level'].choices = [('L1','L1'),('L2','L2'),('L3','L3')]
            elif dept == 'D':
                self.fields['level'].choices = [('L1','L1'),('L2','L2'),('L3','L3')]
            elif dept == 'G.I': 
                self.fields['level'].choices = [('L1','L1'),('L2','L2'),('L3','L3'),('L4','L4'),('L5','L5')]
            elif dept == 'JC':
                self.fields['level'].choices = [('L1','L1'),('L2','L2'),('L3','L3')]
            else:
                # Default fallback
                self.fields['level'].choices = [('L1','L1'),('L2','L2'),('L3','L3')]