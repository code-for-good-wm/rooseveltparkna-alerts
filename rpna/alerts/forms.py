from django import forms

from rpna.core.models import Profile

from .utils import format_number


class LoginForm(forms.Form):
    number = forms.CharField(
        required=True,
        label="Mobile Phone Number",
        widget=forms.TextInput(attrs={"type": "tel", "autofocus": True}),
    )

    def clean_number(self):
        value, error = format_number(self.cleaned_data["number"])
        if error:
            raise forms.ValidationError(error)
        return value


class LoginCodeForm(forms.Form):
    code = forms.CharField(
        required=True,
        label="Confirmation Code",
        widget=forms.TextInput(attrs={"autofocus": True}),
    )


class SetupForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = [
            "language",
            "neighborhood_updates",
            "volunteer_opportunities",
        ]
