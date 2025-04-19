from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils.translation import gettext_lazy as _
from django_countries.fields import CountryField

class Laboratory(models.Model):
    """Model representing a laboratory."""
    LABORATORY_TYPES = [
        ('HOSPITAL', _('Kliniklabor')),
        ('PRIVATE', _('Privatlabor')),
        ('UNIVERSITY', _('Universitätslabor')),
        ('OTHER', _('Sonstiges')),
    ]

    REFERRAL_TYPES = [
        ('INTERNAL', _('Nur interne Aufträge')),
        ('EXT_INT', _('Interne und externe Aufträge')),
        ('EXTERNAL', _('Nur externe Aufträge')),
    ]

    name = models.CharField(max_length=200)
    leader = models.CharField(max_length=200)
    lab_type = models.CharField(max_length=20, choices=LABORATORY_TYPES)
    street = models.CharField(max_length=200, blank=True)
    city = models.CharField(max_length=200, blank=True)
    zip_code = models.CharField(max_length=10, blank=True)
    country = CountryField(blank_label='(Land auswählen)')
    referral_type = models.CharField(max_length=20, choices=REFERRAL_TYPES)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = _('Laboratorien')

    def __str__(self):
        return self.name

class ParameterEvaluation(models.Model):
    """Model for storing laboratory parameter evaluations."""
    # Material choices from index.html
    MATERIAL_CHOICES = [
        ('blood', _('Blut')),
        ('urine', _('Harn')),
        ('csf', _('Liquor')),
        ('punctate', _('Punktat')),
        ('swab', _('Abstrich')),
        ('stool', _('Stuhl')),
        ('tissue', _('Gewebe')),
        ('other', _('Sonstiges')),
    ]
    
    # Preanalytical choices from index.html
    PREANALYTICAL_CHOICES = [
        (0, _('Konzept nicht anwendbar')),
        (1, _('Vollautomatisierte Probenverarbeitung')),
        (4, _('Teilautomatisierte Probenverarbeitung')),
        (9, _('Manuelle Probenverarbeitung')),
    ]
    
    # Analytical choices from index.html
    ANALYTICAL_CHOICES = [
        (0, _('Vollautomatisiert (kein Aufwand)')),
        (1, _('Manueller Aufwand sehr gering (<15 min)')),
        (3, _('Manueller Aufwand gering (<1h)')),
        (5, _('Manueller Aufwand mittel (1-2h)')),
        (7, _('Manueller Aufwand hoch (2-4h)')),
        (9, _('Manueller Aufwand sehr hoch (>4h)')),
    ]
    
    # Expertise choices from index.html
    EXPERTISE_CHOICES = [
        (0, _('Konzept nicht anwendbar')),
        (1, _('Techniker mit Grundkenntnissen')),
        (4, _('Techniker mit erweiterten Laborkenntnissen')),
        (9, _('Techniker mit Spezialkenntnissen')),
    ]
    
    # Postanalytical choices from index.html
    POSTANALYTICAL_CHOICES = [
        (0, _('Konzept nicht anwendbar')),
        (1, _('Kein Aufwand')),
        (2, _('Technische Plausibilitätskontrolle notwendig')),
        (3, _('Potentieller Reflextest')),
        (5, _('Zusätzliche analytische Interpretation notwendig')),
        (6, _('Potentielle reflektive Testung')),
        (7, _('Potentielle reflektive Testung nach Rücksprache')),
        (8, _('Experteninterpretation notwendig')),
        (9, _('Experteninterpretation mit erweiterter Expertise notwendig')),
    ]
    
    # Administrative choices from index.html
    ADMINISTRATIVE_CHOICES = [
        (0, _('Konzept nicht anwendbar')),
        (1, _('Automatische Berechnung')),
        (2, _('Automatische schriftliche Interpretation')),
        (3, _('Zusätzliche Analyse nicht notwendig')),
        (5, _('Manuelle Übertragung/Berechnung in LIS/EHR')),
        (6, _('Individuelle schriftliche Interpretation')),
        (7, _('Direkter Kontakt zum Kliniker notwendig')),
    ]
    
    # Invasiveness choices from index.html
    INVASIVENESS_CHOICES = [
        (0, _('Konzept nicht anwendbar')),
        (1, _('Nicht invasiv')),
        (2, _('Minimal invasiv')),
        (3, _('Venenpunktion')),
        (4, _('Arterienpunktion')),
        (5, _('Punktion von Körperhöhlen oder Knochenmark')),
        (6, _('Punktion des ZNS')),
        (7, _('Endoskopische Probenentnahme (ohne Anästhesie)')),
        (8, _('Endoskopische Probenentnahme (mit Anästhesie)')),
        (9, _('Chirurgische Probenentnahme')),
    ]
    
    # Time required choices from index.html
    TIME_REQUIRED_CHOICES = [
        (0, _('Konzept nicht anwendbar')),
        (1, _('<1 Stunde')),
        (4, _('1-6 Stunden')),
        (6, _('6-12 Stunden')),
        (9, _('>12 Stunden')),
    ]
    
    loinc_code = models.CharField(max_length=20)
    parameter_name = models.CharField(max_length=200)
    material = models.CharField(max_length=50, choices=MATERIAL_CHOICES)
    
    # Evaluation criteria
    preanalytical = models.IntegerField(
        choices=PREANALYTICAL_CHOICES,
        validators=[MinValueValidator(0), MaxValueValidator(9)]
    )
    analytical = models.IntegerField(
        choices=ANALYTICAL_CHOICES,
        validators=[MinValueValidator(0), MaxValueValidator(9)]
    )
    expertise = models.IntegerField(
        choices=EXPERTISE_CHOICES,
        validators=[MinValueValidator(0), MaxValueValidator(9)]
    )
    postanalytical = models.IntegerField(
        choices=POSTANALYTICAL_CHOICES,
        validators=[MinValueValidator(0), MaxValueValidator(9)]
    )
    administrative = models.IntegerField(
        choices=ADMINISTRATIVE_CHOICES,
        validators=[MinValueValidator(0), MaxValueValidator(7)]
    )
    invasiveness = models.IntegerField(
        choices=INVASIVENESS_CHOICES,
        validators=[MinValueValidator(0), MaxValueValidator(9)]
    )
    time_required = models.IntegerField(
        choices=TIME_REQUIRED_CHOICES,
        validators=[MinValueValidator(0), MaxValueValidator(9)]
    )

    # Status and metadata
    is_approved = models.BooleanField(default=False)
    submitted_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    approved_at = models.DateTimeField(null=True, blank=True)
    approved_by = models.ForeignKey(
        User, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        related_name='approved_evaluations'
    )

    def __str__(self):
        return f"{self.parameter_name} ({self.loinc_code})"
    
    def get_llpc_sequence(self):
        return f"{self.loinc_code}-{self.preanalytical}-{self.analytical}-{self.expertise}-{self.postanalytical}-{self.administrative}-{self.invasiveness}-{self.time_required}"
    
    def calculate_total_score(self):
        return (
            self.preanalytical +
            self.analytical +
            self.expertise +
            self.postanalytical +
            self.administrative +
            self.invasiveness +
            self.time_required
        )

class LaboratoryUpload(models.Model):
    """Model for storing laboratory parameter uploads."""
    laboratory = models.ForeignKey(Laboratory, on_delete=models.CASCADE)
    upload_date = models.DateTimeField(auto_now_add=True)
    file = models.FileField(upload_to='lab_uploads/')
    processed = models.BooleanField(default=False)
    year = models.IntegerField()

    def __str__(self):
        return f"{self.laboratory.name} - Upload {self.upload_date}"

class ParameterVolume(models.Model):
    """Model for storing the volume of parameters per laboratory."""
    laboratory = models.ForeignKey(Laboratory, on_delete=models.CASCADE)
    loinc_code = models.CharField(max_length=20)
    month = models.IntegerField()
    year = models.IntegerField()
    volume = models.IntegerField(validators=[MinValueValidator(0)])
    upload = models.ForeignKey(LaboratoryUpload, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('laboratory', 'loinc_code', 'year')

    def __str__(self):
        return f"{self.laboratory.name} - {self.loinc_code} ({self.year})"

class BenchmarkingResult(models.Model):
    """Model for storing benchmarking results."""
    laboratory = models.ForeignKey(Laboratory, on_delete=models.CASCADE)
    evaluation = models.ForeignKey(ParameterEvaluation, on_delete=models.CASCADE)
    volume = models.ForeignKey(ParameterVolume, on_delete=models.CASCADE)
    total_score = models.FloatField()
    percentile_rank = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.laboratory.name} - {self.evaluation.parameter_name} Benchmark"
