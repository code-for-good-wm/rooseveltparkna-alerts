from django import forms

import phonenumbers


class LoginForm(forms.Form):
    number = forms.CharField(
        required=True,
        label="Mobile Phone Number",
        widget=forms.TextInput(attrs={"type": "tel", "autofocus": True}),
    )

    def clean_number(self):
        try:
            parsed = phonenumbers.parse(self.cleaned_data["number"], "US")
        except phonenumbers.NumberParseException as e:
            raise forms.ValidationError(e.args[0])
        return phonenumbers.format_number(parsed, phonenumbers.PhoneNumberFormat.E164)


class LoginCodeForm(forms.Form):
    code = forms.CharField(
        required=True,
        label="Confirmation Code",
        widget=forms.TextInput(attrs={"autofocus": True}),
    )
