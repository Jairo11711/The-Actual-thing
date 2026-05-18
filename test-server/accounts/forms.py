from django import forms
from django.contrib.auth.forms import UserCreationForm
from dashboard.models import Customer

class CustomerRegistrationForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # This applies your specific CSS class to every field in the form
        for field in self.fields.values():
            field.widget.attrs.update({
                'class': 'login-input',
            })

class CustomerProfileForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ("email", "phone_number")

        widgets = {
            'email' : forms.EmailInput(attrs={
                'class' : 'login-input',
                'placeholder' : 'Enter Your Email'
            }),
            'phone_number' : forms.TextInput(attrs={
                'class' : 'login-input',
                'placeholder' : '09876543210'
            }),
            
            
        }