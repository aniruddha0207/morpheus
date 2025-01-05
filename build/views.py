from django.shortcuts import render, get_object_or_404, redirect
from .models import Form, Submission, SubmissionData
from .forms import DynamicForm
from django.shortcuts import render

def home(request):
    return render(request, 'builder/home.html')  # Ensure the template exists
def form_view(request, form_id):
    form_instance = get_object_or_404(Form, id=form_id)
    if request.method == 'POST':
        form = DynamicForm(form_instance, request.POST)
        if form.is_valid():
            submission = Submission.objects.create(form=form_instance)
            for field_id, value in form.cleaned_data.items():
                field = form_instance.fields.get(id=field_id.split('_')[1])
                if isinstance(value, list):
                    value = ', '.join(value)
                SubmissionData.objects.create(submission=submission, field=field, value=value)
            return render(request, 'builder/success.html', {'form_instance': form_instance})
    else:
        form = DynamicForm(form_instance)
    return render(request, 'builder/form.html', {'form': form, 'form_instance': form_instance})

def analytics_view(request, form_id):
    form_instance = get_object_or_404(Form, id=form_id)
    analytics_data = {}
    for field in form_instance.fields.all():
        field_data = field.submissiondata_set.values_list('value', flat=True)
        if field.field_type == 'text':
            word_count = {}
            for data in field_data:
                for word in data.split():
                    if len(word) >= 5:
                        word_count[word] = word_count.get(word, 0) + 1
            analytics_data[field.label] = sorted(word_count.items(), key=lambda x: x[1], reverse=True)[:5]
        elif field.field_type in ['dropdown', 'checkbox']:
            option_count = {}
            for data in field_data:
                options = data.split(', ')
                for option in options:
                    option_count[option] = option_count.get(option, 0) + 1
            analytics_data[field.label] = sorted(option_count.items(), key=lambda x: x[1], reverse=True)[:5]
    return render(request, 'builder/analytics.html', {'form_instance': form_instance, 'analytics_data': analytics_data})
