from django import forms
from .models import Field

class DynamicForm(forms.Form):
    def __init__(self, form_instance, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in form_instance.fields.all():
            if field.field_type == 'text':
                self.fields[f'field_{field.id}'] = forms.CharField(label=field.label, required=True)
            elif field.field_type == 'dropdown':
                options = field.options.split(',')
                self.fields[f'field_{field.id}'] = forms.ChoiceField(label=field.label, choices=[(opt, opt) for opt in options])
            elif field.field_type == 'checkbox':
                options = field.options.split(',')
                self.fields[f'field_{field.id}'] = forms.MultipleChoiceField(
                    label=field.label,
                    choices=[(opt, opt) for opt in options],
                    widget=forms.CheckboxSelectMultiple,
                )
