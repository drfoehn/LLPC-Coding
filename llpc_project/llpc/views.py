from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.utils.translation import gettext_lazy as _
from django.views.decorators.http import require_http_methods
from django_tables2 import SingleTableView, RequestConfig
from django_tables2.views import SingleTableMixin
from django.views.generic import ListView
from django.db.models import Q
from .forms import ParameterEvaluationForm, LaboratoryForm
from .models import ParameterEvaluation, Laboratory
from .utils import search_loinc, format_loinc_result
from .tables import ParameterEvaluationTable, LaboratoryTable

# Create your views here.

def index(request):
    """Home page view that provides options to input info or access the database."""
    return render(request, 'llpc/home.html')

@login_required
def parameter_evaluation(request):
    """View for parameter evaluation with LOINC search."""
    if request.method == 'POST':
        print("DEBUG: POST request received")
        form = ParameterEvaluationForm(request.POST)
        print(f"DEBUG: Form data: {request.POST}")
        if form.is_valid():
            print("DEBUG: Form is valid")
            evaluation = form.save(commit=False)
            evaluation.submitted_by = request.user
            evaluation.save()
            print("DEBUG: Evaluation saved successfully")
            return redirect('llpc:evaluation_success')
        else:
            print(f"DEBUG: Form errors: {form.errors}")
    else:
        form = ParameterEvaluationForm()
    
    return render(request, 'llpc/parameter_evaluation.html', {
        'form': form,
    })

@require_http_methods(['GET'])
def loinc_search(request):
    """API endpoint for LOINC search with autocomplete."""
    query = request.GET.get('q', '')
    language = request.GET.get('lang', 'de')
    
    if not query:
        return JsonResponse({'results': []})
    
    results = search_loinc(query, language)
    
    if not results:
        return JsonResponse({'results': []})
    
    formatted_results = [format_loinc_result(result) for result in results]
    
    return JsonResponse({'results': formatted_results})

@login_required
def evaluation_success(request):
    """View shown after successful parameter evaluation submission."""
    return render(request, 'llpc/evaluation_success.html')

@login_required
def laboratory_form(request):
    """View for creating a new laboratory."""
    if request.method == 'POST':
        form = LaboratoryForm(request.POST)
        if form.is_valid():
            laboratory = form.save(commit=False)
            laboratory.user = request.user
            laboratory.save()
            return redirect('llpc:index')
    else:
        form = LaboratoryForm()
    
    return render(request, 'llpc/laboratory_form.html', {
        'form': form,
        'title': _('Create Laboratory'),
    })

class ParameterEvaluationListView(SingleTableMixin, ListView):
    model = ParameterEvaluation
    table_class = ParameterEvaluationTable
    template_name = 'llpc/parameter_evaluation_list.html'
    
    def get_queryset(self):
        queryset = super().get_queryset()
        search_query = self.request.GET.get('search', '')
        if search_query:
            queryset = queryset.filter(
                Q(loinc_code__icontains=search_query) |
                Q(parameter_name__icontains=search_query) |
                Q(material__icontains=search_query)
            )
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_query'] = self.request.GET.get('search', '')
        return context

class LaboratoryListView(SingleTableMixin, ListView):
    model = Laboratory
    table_class = LaboratoryTable
    template_name = 'llpc/laboratory_list.html'
    
    def get_queryset(self):
        queryset = super().get_queryset()
        search_query = self.request.GET.get('search', '')
        if search_query:
            queryset = queryset.filter(
                Q(name__icontains=search_query) |
                Q(leader__icontains=search_query) |
                Q(city__icontains=search_query) |
                Q(country__icontains=search_query)
            )
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_query'] = self.request.GET.get('search', '')
        return context

