from django import forms

class LoginForm(forms.Form):
    email = forms.CharField(label='email', 
                            max_length=100, 
                            widget=forms.EmailInput(attrs={'class': 'form-control'}), 
                            help_text='We`ll never share your email with anyone else.'
                            )
    password = forms.CharField(label='password', 
                               max_length=100, 
                               widget=forms.PasswordInput(attrs={'class': 'form-control'}))
