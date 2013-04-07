from django import forms

__all__ = ['EditProfileForm',]

class EditProfileForm(forms.Form):
    """
    Form for editing the user profile information.
    """
    email = forms.EmailField(required=False, label="E-Mail Address")
    password = forms.CharField(required=False, widget=forms.PasswordInput, label="Current Password")
    password1 = forms.CharField(required=False, widget=forms.PasswordInput, label="New Password")
    password2 = forms.CharField(required=False, widget=forms.PasswordInput, label="Repeat New Password")

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')

        if not password2 and password1:
            raise forms.ValidationError("You must confirm your password")
        if password1 != password2:
            raise forms.ValidationError("Your passwords do not match")
        return password2
