from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from .models import Laboratory, ParameterEvaluation, LaboratoryUpload, ParameterVolume, BenchmarkingResult

@admin.register(Laboratory)
class LaboratoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'leader', 'lab_type', 'referral_type', 'user', 'created_at')
    list_filter = ('lab_type', 'referral_type', 'created_at')
    search_fields = ('name', 'leader', 'address')
    readonly_fields = ('created_at', 'updated_at')
    fieldsets = (
        (None, {
            'fields': ('name', 'leader', 'lab_type', 'address', 'referral_type', 'user')
        }),
        (_('Timestamps'), {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

@admin.register(ParameterEvaluation)
class ParameterEvaluationAdmin(admin.ModelAdmin):
    list_display = ('loinc_code', 'parameter_name', 'material', 'is_approved', 'submitted_by', 'created_at')
    list_filter = ('is_approved', 'material', 'created_at')
    search_fields = ('loinc_code', 'parameter_name')
    readonly_fields = ('created_at', 'updated_at', 'approved_at')
    fieldsets = (
        (None, {
            'fields': ('loinc_code', 'parameter_name', 'material')
        }),
        (_('Evaluation Criteria'), {
            'fields': (
                'preanalytical', 'analytical', 'expertise',
                'postanalytical', 'administrative', 'invasiveness',
                'time_required'
            )
        }),
        (_('Status'), {
            'fields': ('is_approved', 'submitted_by', 'approved_by')
        }),
        (_('Timestamps'), {
            'fields': ('created_at', 'updated_at', 'approved_at'),
            'classes': ('collapse',)
        }),
    )
    
    def save_model(self, request, obj, form, change):
        if 'is_approved' in form.changed_data and obj.is_approved:
            from django.utils import timezone
            obj.approved_at = timezone.now()
            obj.approved_by = request.user
        super().save_model(request, obj, form, change)

@admin.register(LaboratoryUpload)
class LaboratoryUploadAdmin(admin.ModelAdmin):
    list_display = ('laboratory', 'year', 'upload_date', 'processed')
    list_filter = ('processed', 'year', 'upload_date')
    search_fields = ('laboratory__name',)
    readonly_fields = ('upload_date',)

@admin.register(ParameterVolume)
class ParameterVolumeAdmin(admin.ModelAdmin):
    list_display = ('laboratory', 'loinc_code', 'year', 'volume')
    list_filter = ('year',)
    search_fields = ('laboratory__name', 'loinc_code')

@admin.register(BenchmarkingResult)
class BenchmarkingResultAdmin(admin.ModelAdmin):
    list_display = ('laboratory', 'evaluation', 'total_score', 'percentile_rank', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('laboratory__name', 'evaluation__parameter_name')
    readonly_fields = ('created_at',)
