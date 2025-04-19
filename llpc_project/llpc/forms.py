from django import forms
from django.utils.translation import gettext_lazy as _
from .models import ParameterEvaluation, Laboratory
from captcha.fields import CaptchaField
from django_countries.widgets import CountrySelectWidget

class LaboratoryForm(forms.ModelForm):
    """Form for laboratory information."""
    captcha = CaptchaField(label=_('Sicherheitsüberprüfung'))
    
    class Meta:
        model = Laboratory
        fields = ['name', 'leader', 'lab_type', 'street', 'city', 'zip_code', 'country', 'referral_type']
        labels = {
            'name': _('Labor Name'),
            'leader': _('Laborleiter'),
            'lab_type': _('Labor Typ'),
            'street': _('Straße'),
            'city': _('Stadt'),
            'zip_code': _('PLZ'),
            'country': _('Land'),
            'referral_type': _('Einsender'),
        }
        widgets = {
            "country": CountrySelectWidget()
        }

class ParameterEvaluationForm(forms.ModelForm):
    """Form for parameter evaluation with LOINC search."""
    captcha = CaptchaField(label=_('Sicherheitsüberprüfung'))
    loinc_search = forms.CharField(
        label=_('LOINC Search'),
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': _('Search for LOINC code or parameter name...'),
            'autocomplete': 'off',
        })
    )
    
    class Meta:
        model = ParameterEvaluation
        fields = [
            'loinc_code', 'parameter_name', 'material',
            'preanalytical', 'analytical', 'expertise',
            'postanalytical', 'administrative', 'invasiveness',
            'time_required'
        ]
        labels = {
            'loinc_code': _('LOINC Code'),
            'parameter_name': _('Parameter Name'),
            'material': _('Material'),
            'preanalytical': _('Preanalytical Effort'),
            'analytical': _('Analytical Effort'),
            'expertise': _('Expertise Required'),
            'postanalytical': _('Postanalytical Effort'),
            'administrative': _('Administrative Effort'),
            'invasiveness': _('Invasiveness'),
            'time_required': _('Time Required'),
        }
        widgets = {
            'loinc_code': forms.TextInput(attrs={'readonly': 'readonly'}),
            'parameter_name': forms.TextInput(attrs={'readonly': 'readonly'}),
            'material': forms.Select(attrs={'class': 'form-select'}),
            'preanalytical': forms.Select(attrs={'class': 'form-select'}),
            'analytical': forms.Select(attrs={'class': 'form-select'}),
            'expertise': forms.Select(attrs={'class': 'form-select'}),
            'postanalytical': forms.Select(attrs={'class': 'form-select'}),
            'administrative': forms.Select(attrs={'class': 'form-select'}),
            'invasiveness': forms.Select(attrs={'class': 'form-select'}),
            'time_required': forms.Select(attrs={'class': 'form-select'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Add Bootstrap classes to all fields
        for field in self.fields:
            if not isinstance(self.fields[field].widget, forms.Select):
                self.fields[field].widget.attrs.update({'class': 'form-control'})
            else:
                self.fields[field].widget.attrs.update({'class': 'form-select'})
        
        # Add empty choice to all select fields
        for field_name in ['material', 'preanalytical', 'analytical', 'expertise', 
                          'postanalytical', 'administrative', 'invasiveness', 'time_required']:
            self.fields[field_name].empty_label = _('Please select') 