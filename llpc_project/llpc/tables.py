import django_tables2 as tables
from django.utils.translation import gettext_lazy as _
from .models import ParameterEvaluation, Laboratory

class ParameterEvaluationTable(tables.Table):
    llpc_code = tables.Column(accessor='get_llpc_sequence', verbose_name=_('LLPC-Code'))
    llpc_sum = tables.Column(accessor='calculate_total_score', verbose_name=_('LLPC-Summe'))

    class Meta:
        model = ParameterEvaluation
        template_name = "django_tables2/bootstrap5.html"
        fields = ('loinc_code', 'parameter_name', 'material', 'llpc_code', 'llpc_sum')
        attrs = {"class": "table table-striped table-bordered"}
        order_by = ('loinc_code',)

class LaboratoryTable(tables.Table):
    class Meta:
        model = Laboratory
        template_name = "django_tables2/bootstrap5.html"
        fields = ('name', 'leader', 'lab_type', 'country', 'city')
        attrs = {"class": "table table-striped table-bordered"}
        order_by = ('name',)

