# forms.py
from django import forms
from .models import Message

class MessageForm(forms.ModelForm):
    departement = forms.ChoiceField(
        label='Département',
        choices=[('', 'Sélectionnez votre département')] + Message.DEPARTEMENT_CHOICES,
        widget=forms.Select(),
    )
    level = forms.ChoiceField(
        label='Niveau',
        choices=[('', 'Choisissez votre niveau')],
        widget=forms.Select(),
    )
    message_type = forms.ChoiceField(
        label='Type de message',
        choices=[('', 'Type de message')] + Message.MESSAGE_TYPE_CHOICES,
        widget=forms.Select(),
    )

    class Meta:
        model = Message
        fields = ['departement', 'level', 'message_type', 'content']
        labels = {
            'content': 'Message',
        }
        widgets = {
            'content': forms.Textarea(attrs={
                'placeholder': 'Rédigez votre message ici…',
                'rows': 6,
            }),
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
                self.fields['level'].choices = [('L1','ANNEE: 1'),('L2','ANNEE: 2'),('L3','ANNEE: 3'),('L4','ANNEE: 4'),('L5','ANNEE: 5')]
            elif dept == 'BTS':
                self.fields['level'].choices = [('L1','L1'),('L2','L2'),('L3','L3')]
            elif dept == 'SEG':
                self.fields['level'].choices = [('L1','L1'),('L2','L2'),('L3','L3')]
            elif dept == 'GLT':
                self.fields['level'].choices = [('L1','L1'),('L2','L2'),('L3','L3')]
            elif dept == 'D':
                self.fields['level'].choices = [('L1','L1'),('L2','L2'),('L3','L3')]
            elif dept == 'G.I': 
                self.fields['level'].choices = [('L1','ANNEE: 1'),('L2','ANNEE: 2'),('L3','ANNEE: 3'),('L4','ANNEE: 4'),('L5','ANNEE: 5')]
            elif dept == 'JC':
                self.fields['level'].choices = [('L1','L1'),('L2','L2'),('L3','L3')]
            else:
                # Default fallback
                self.fields['level'].choices = [('L1','L1'),('L2','L2'),('L3','L3')]