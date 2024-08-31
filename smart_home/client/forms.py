from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import RoomObjectIdentifiers, DataSensorObjects,User,OperatorID, Task

class OperatorAccountForm(UserCreationForm):
    # email=forms.EmailField(max_length=100)
    class Meta:
        model = User
        fields = ["username", "password1", "password2"]
        exclude = ['id']

class OperatorForm(forms.ModelForm):
    class Meta:
        model = OperatorID
        fields = ['id', 'theme']

class RoomObjectForm(forms.ModelForm):
    class Meta:
        model = RoomObjectIdentifiers
        fields = ['service_room', 'roomObject_name', 'switch_type', 'interaction_key','config_id']
        exclude = ['room_operator']


from django import forms
from .models import Task

class TaskCreateForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'description', 'image', 'amount']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
        }

class TaskCompleteForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['url', 'proof_of_work_url']
