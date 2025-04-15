from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.utils.translation import gettext_lazy as _
from django.views.decorators.http import require_http_methods
from .forms import ParameterEvaluationForm, LaboratoryForm
from .models import ParameterEvaluation, Laboratory
from .utils import search_loinc, format_loinc_result

# Create your views here.

def index(request):
    """Home page view that provides options to input info or access the database."""
    return render(request, 'llpc/home.html')

@login_required
def parameter_evaluation(request):
    """View for parameter evaluation with LOINC search."""
    if request.method == 'POST':
        form = ParameterEvaluationForm(request.POST)
        if form.is_valid():
            evaluation = form.save(commit=False)
            evaluation.submitted_by = request.user
            evaluation.save()
            return redirect('evaluation_success')
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
    
    print(f"DEBUG: loinc_search view called with query: '{query}', language: '{language}'")
    
    if not query:
        print("DEBUG: Empty query, returning empty results")
        return JsonResponse({'results': []})
    
    print("DEBUG: Calling search_loinc function")
    results = search_loinc(query, language)
    print(f"DEBUG: search_loinc returned {len(results)} results")
    
    if not results:
        print("DEBUG: No results found, returning empty results")
        return JsonResponse({'results': []})
    
    print("DEBUG: Formatting results")
    formatted_results = [format_loinc_result(result) for result in results]
    print(f"DEBUG: Formatted {len(formatted_results)} results")
    
    print("DEBUG: Returning JSON response")
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
