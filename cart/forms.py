from django import  forms

from .models import Payment



class PaymentForm(forms.ModelForm):

    class Meta:
        model = Payment
        fields = ('card_number', 'expire_date', 'security_number')


        def __init__(self, *args, **kwargs):
            super(PaymentForm, self).__init__(*args, **kwargs)
            self.fields['card_number'].required = True
            self.fields['security_number'].required = True