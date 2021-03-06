from django import forms


class RegistrationForm(forms.Form):
    name = forms.CharField(max_length=50)
    email = forms.EmailField()
    college = forms.CharField(max_length=50)
    mobile = forms.CharField(max_length=10)
    referral = forms.CharField(max_length=50, required=False)
    pack = forms.CharField(max_length=10)

    def clean_mobile(self):
        mobile = str(self.cleaned_data['mobile'])

        # accept empty
        if mobile == '':
            return mobile

        if not mobile.isdigit() or len(mobile) != 10:
            raise forms.ValidationError('Mobile must be 10 digits')

        return mobile

    def clean_pack(self):
        pack = self.cleaned_data['pack']

        if pack not in ('single', 'multiple'):
            raise forms.ValidationError('Pack should be either single/multiple')

        return pack


