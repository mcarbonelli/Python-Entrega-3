from django import forms
from django.core.exceptions import ValidationError
from .models import Lote, Novedad
from datetime import datetime


class LoginForm(forms.Form):
    """Formulario de login"""
    username = forms.CharField(
        label='Usuario',
        max_length=150,
        widget=forms.TextInput(attrs={
            'class': 'form-control form-control-lg',
            'placeholder': 'Ingrese su usuario'
        })
    )
    password = forms.CharField(
        label='Contraseña',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control form-control-lg',
            'placeholder': 'Ingrese su contraseña'
        })
    )


class PeriodoForm(forms.Form):
    """Formulario para seleccionar periodo de consumo"""    
    AÑOS_DISPONIBLES = [('2024', '2024'),
                         ('2025', '2025'),
                         ('2026', '2026')]
    MESES_DISPONIBLES = [(1, 'Enero'),
                         (2, 'Febrero'),
                         (3, 'Marzo'),
                         (4, 'Abril'),
                         (5, 'Mayo'),
                         (6, 'Junio'),
                         (7, 'Julio'),
                         (8, 'Agosto'),
                         (9, 'Septiembre'),
                         (10, 'Octubre'),
                         (11, 'Noviembre'),
                         (12, 'Diciembre'),
                         ]
    
    año = forms.ChoiceField(
        label='Año',
        choices=AÑOS_DISPONIBLES,
        initial=datetime.now().year,
        widget=forms.Select(attrs={'class': 'form-select form-select-lg'})
    )
    mes = forms.ChoiceField(
        label='Mes',
        choices=MESES_DISPONIBLES,
        initial=datetime.now().month,
        widget=forms.Select(attrs={'class': 'form-select form-select-lg'})
    )


class LecturaForm(forms.ModelForm):
    """Formulario para ingresar/editar lecturas"""
    class Meta:
        model = Lote
        fields = ['lectura_actual']
        widgets = {
            'lectura_actual': forms.NumberInput(attrs={
                'class': 'form-control form-control-lg',
                'placeholder': 'Ingrese lectura',
                'min': '0',
                'step': '1'
            })
        }
        labels = {
            'lectura_actual': 'Lectura Actual'
        }
    
    def __init__(self, *args, **kwargs):
        self.lectura_anterior = kwargs.pop('lectura_anterior', None)
        super().__init__(*args, **kwargs)
    
    def clean_lectura_actual(self):
        lectura_actual = self.cleaned_data.get('lectura_actual')
        
        # Validar que sea mayor a 0
        if lectura_actual is not None and lectura_actual <= 0:
            raise ValidationError('La lectura debe ser mayor a 0')
        
        # Validar que sea mayor o igual a lectura anterior
        if lectura_actual is not None and self.lectura_anterior is not None:
            if lectura_actual < self.lectura_anterior:
                raise ValidationError(
                    f'La lectura actual ({lectura_actual}) no puede ser menor a la lectura anterior ({self.lectura_anterior})'
                )
        
        return lectura_actual


class NovedadForm(forms.Form):
    """Formulario para agregar novedades a una lectura"""
    novedades_predefinidas = forms.MultipleChoiceField(
        label='Novedades',
        required=False,
        widget=forms.CheckboxSelectMultiple(attrs={'class': 'form-check-input'}),
        choices=[]
    )
    novedad_libre = forms.CharField(
        label='Observaciones adicionales',
        required=False,
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 3,
            'placeholder': 'Escriba aquí cualquier otra observación...'
        })
    )
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Cargar novedades predefinidas dinámicamente
        self.fields['novedades_predefinidas'].choices = [
            (nov.cod_novedad, nov.descripcion) for nov in Novedad.objects.all()
        ]
    
    def clean(self):
        cleaned_data = super().clean()
        novedades = cleaned_data.get('novedades_predefinidas')
        novedad_libre = cleaned_data.get('novedad_libre')
        
        # Validar que al menos haya una novedad o texto libre
        if not novedades and not novedad_libre:
            raise ValidationError('Debe seleccionar al menos una novedad o escribir una observación.')
        
        return cleaned_data


class NovedadModelForm(forms.ModelForm):
    """Formulario para crear/editar tipos de novedades"""
    class Meta:
        model = Novedad
        fields = ['descripcion']
        widgets = {
            'descripcion': forms.TextInput(attrs={
                'class': 'form-control form-control-lg',
                'placeholder': 'Ingrese la descripción de la novedad',
                'maxlength': '200'
            })
        }
        labels = {
            'descripcion': 'Descripción'
        }
    
    def clean_descripcion(self):
        descripcion = self.cleaned_data.get('descripcion')
        
        # Validar que no esté vacía
        if not descripcion or not descripcion.strip():
            raise ValidationError('La descripción no puede estar vacía')
        
        # Validar longitud mínima
        if len(descripcion.strip()) < 3:
            raise ValidationError('La descripción debe tener al menos 3 caracteres')
        
        return descripcion.strip()
