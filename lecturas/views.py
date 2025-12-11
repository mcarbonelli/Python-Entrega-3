from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, FormView, UpdateView
from django.contrib import messages
from django.db.models import Count, Q, Max
from django.utils import timezone

from django.views import View
from django.urls import reverse_lazy, reverse
from .models import Operador, Cliente, Lote, Novedad
from .forms import LoginForm, PeriodoForm, LecturaForm, NovedadForm

class LoginView(View):
    """Vista de login"""
    template_name = 'lecturas/login.html'
    
    def get(self, request):
        if request.user.is_authenticated:
            return redirect('dashboard')
        form = LoginForm()
        return render(request, self.template_name, {'form': form})
    
    def post(self, request):
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            
            if user is not None:
                login(request, user)
                messages.success(request, f'Bienvenido {user.get_full_name() or user.username}!')
                return redirect('dashboard')
            else:
                messages.error(request, 'Usuario o contraseña incorrectos')
        
        return render(request, self.template_name, {'form': form})


class LogoutView(LoginRequiredMixin, View):
    """Vista de logout"""
    def get(self, request):
        logout(request)
        messages.info(request, 'Sesión cerrada correctamente')
        return redirect('login')


class DashboardView(LoginRequiredMixin, View):
    """Dashboard principal"""
    template_name = 'lecturas/dashboard.html'
    
    def get(self, request):
        # Obtener estadísticas generales
        total_rutas = Lote.objects.values('ruta', 'ano_consumo', 'mes_consumo').distinct().count()
        rutas_abiertas = Lote.objects.filter(abierta=True).values('ruta', 'ano_consumo', 'mes_consumo').distinct().count()
        total_lecturas = Lote.objects.count()
        lecturas_tomadas = Lote.objects.filter(lectura_actual__isnull=False).count()
        
        # Obtener operador actual
        try:
            operador = request.user.operador
            mis_lecturas = Lote.objects.filter(operador=operador).count()
        except:
            operador = None
            mis_lecturas = 0
        
        context = {
            'total_rutas': total_rutas,
            'rutas_abiertas': rutas_abiertas,
            'total_lecturas': total_lecturas,
            'lecturas_tomadas': lecturas_tomadas,
            'lecturas_pendientes': total_lecturas - lecturas_tomadas,
            'mis_lecturas': mis_lecturas,
        }
        
        return render(request, self.template_name, context)


class SeleccionarPeriodoView(LoginRequiredMixin, FormView):
    """Vista para seleccionar periodo de consumo"""
    template_name = 'lecturas/seleccionar_periodo.html'
    form_class = PeriodoForm
    
    def form_valid(self, form):
        año = form.cleaned_data['año']
        mes = form.cleaned_data['mes']
        # Guardar en sesión
        self.request.session['periodo_año'] = año
        self.request.session['periodo_mes'] = mes
        messages.success(self.request, f'Periodo seleccionado: {dict(form.fields["mes"].choices)[int(mes)]} {año}')
        return redirect('listar_rutas')


class ListarRutasView(LoginRequiredMixin, ListView):
    """Vista para listar rutas del periodo seleccionado"""
    template_name = 'lecturas/listar_rutas.html'
    context_object_name = 'rutas'
    
    def get_queryset(self):
        ano = self.request.session.get('periodo_año')
        mes = self.request.session.get('periodo_mes')
        
        if not ano or not mes:
            return []
        
        # Obtener rutas únicas con estadísticas
        rutas = Lote.objects.filter(
            ano_consumo=ano,
            mes_consumo=mes
        ).values('ruta', 'area', 'abierta').annotate(
            total_medidores=Count('cod_lectura'),
            leidos=Count('cod_lectura', filter=Q(lectura_actual__isnull=False)),
            operador_nombre=Max('operador__user__first_name')
        ).order_by('ruta')
        
        # Calcular faltantes
        for ruta in rutas:
            ruta['faltantes'] = ruta['total_medidores'] - ruta['leidos']
        
        return rutas
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        ano = self.request.session.get('periodo_año')
        mes = self.request.session.get('periodo_mes')
        
        if ano and mes:
            meses = ['', 'Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio',
                    'Julio', 'Agosto', 'Septiembre', 'Octubre', 'Noviembre', 'Diciembre']
            context['periodo'] = f"{meses[int(mes)]} {ano}"
            context['ano'] = ano
            context['mes'] = mes
        else:
            context['periodo'] = 'No seleccionado'
        
        return context


class TomarLecturasView(LoginRequiredMixin, ListView):
    """Vista para tomar lecturas de una ruta"""
    template_name = 'lecturas/tomar_lecturas.html'
    context_object_name = 'lecturas'
    paginate_by = 20
    
    def get_queryset(self):
        ruta = self.kwargs.get('ruta')
        ano = self.request.session.get('periodo_año')
        mes = self.request.session.get('periodo_mes')
        
        if not ano or not mes or not ruta:
            return Lote.objects.none()
        
        return Lote.objects.filter(
            ano_consumo=ano,
            mes_consumo=mes,
            ruta=ruta
        ).select_related('cliente', 'operador').prefetch_related('novedades').order_by('orden')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        ruta = self.kwargs.get('ruta')
        ano = self.request.session.get('periodo_año')
        mes = self.request.session.get('periodo_mes')
        
        if ano and mes and ruta:
            meses = ['', 'Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio',
                    'Julio', 'Agosto', 'Septiembre', 'Octubre', 'Noviembre', 'Diciembre']
            context['periodo'] = f"{meses[int(mes)]} {ano}"
            context['ruta'] = ruta
            
            # Verificar si la ruta está abierta
            lectura_ejemplo = self.get_queryset().first()
            context['ruta_abierta'] = lectura_ejemplo.abierta if lectura_ejemplo else False
        
        return context


class GuardarLecturaView(LoginRequiredMixin, View):
    """Vista para guardar/actualizar una lectura"""
    def post(self, request, pk):
        lectura = get_object_or_404(Lote, pk=pk)
        
        # Verificar que la ruta esté abierta
        if not lectura.abierta:
            messages.error(request, 'No se puede modificar una ruta cerrada')
            return redirect('tomar_lecturas', ruta=lectura.ruta)
        
        form = LecturaForm(request.POST, instance=lectura, lectura_anterior=lectura.lectura_anterior)
        
        if form.is_valid():
            lectura = form.save(commit=False)
            lectura.fecha_hora_registro = timezone.now()
            
            # Asignar operador
            try:
                lectura.operador = request.user.operador
            except:
                pass
            
            lectura.save()
            messages.success(request, f'Lectura guardada correctamente para {lectura.cliente.denominacion}')
        else:
            for error in form.errors.values():
                messages.error(request, error)
        
        return redirect('tomar_lecturas', ruta=lectura.ruta)


class EliminarLecturaView(LoginRequiredMixin, View):
    """Vista para eliminar una lectura"""
    def post(self, request, pk):
        lectura = get_object_or_404(Lote, pk=pk)
        
        # Verificar que la ruta esté abierta
        if not lectura.abierta:
            messages.error(request, 'No se puede modificar una ruta cerrada')
            return redirect('tomar_lecturas', ruta=lectura.ruta)
        
        ruta = lectura.ruta
        lectura.lectura_actual = None
        lectura.consumo_kwh = None
        lectura.save()
        
        messages.success(request, 'Lectura eliminada correctamente')
        return redirect('tomar_lecturas', ruta=ruta)


class AgregarNovedadView(LoginRequiredMixin, View):
    """Vista para agregar novedades a una lectura"""
    template_name = 'lecturas/agregar_novedad.html'
    
    def get(self, request, pk):
        lectura = get_object_or_404(Lote, pk=pk)
        form = NovedadForm(initial={'novedad_libre': lectura.novedad_libre})
        return render(request, self.template_name, {'form': form, 'lectura': lectura})
    
    def post(self, request, pk):
        lectura = get_object_or_404(Lote, pk=pk)
        
        # Verificar que la ruta esté abierta
        if not lectura.abierta:
            messages.error(request, 'No se puede modificar una ruta cerrada')
            return redirect('tomar_lecturas', ruta=lectura.ruta)
        
        form = NovedadForm(request.POST)
        
        if form.is_valid():
            # Limpiar novedades anteriores
            lectura.novedades.clear()
            
            # Agregar novedades seleccionadas
            novedades_ids = form.cleaned_data.get('novedades_predefinidas', [])
            for nov_id in novedades_ids:
                novedad = Novedad.objects.get(cod_novedad=nov_id)
                lectura.novedades.add(novedad)
            
            # Guardar novedad libre
            lectura.novedad_libre = form.cleaned_data.get('novedad_libre', '')
            lectura.save()
            
            messages.success(request, 'Novedades guardadas correctamente')
            return redirect('tomar_lecturas', ruta=lectura.ruta)
        
        return render(request, self.template_name, {'form': form, 'lectura': lectura})


class CerrarRutaView(LoginRequiredMixin, View):
    """Vista para cerrar una ruta"""
    def post(self, request):
        ruta = request.POST.get('ruta')
        ano = request.session.get('periodo_año')
        mes = request.session.get('periodo_mes')
        
        if ruta and ano and mes:
            Lote.objects.filter(
                ruta=ruta,
                ano_consumo=ano,
                mes_consumo=mes
            ).update(abierta=False)
            
            messages.success(request, f'Ruta {ruta} cerrada correctamente')
        else:
            messages.error(request, 'Error al cerrar la ruta')
        
        return redirect('listar_rutas')


class AbrirRutaView(LoginRequiredMixin, View):
    """Vista para abrir una ruta cerrada"""
    def post(self, request):
        ruta = request.POST.get('ruta')
        ano = request.session.get('periodo_año')
        mes = request.session.get('periodo_mes')
        
        if ruta and ano and mes:
            Lote.objects.filter(
                ruta=ruta,
                ano_consumo=ano,
                mes_consumo=mes
            ).update(abierta=True)
            
            messages.success(request, f'Ruta {ruta} abierta correctamente')
        else:
            messages.error(request, 'Error al abrir la ruta')
        
        return redirect('listar_rutas')



class ListarTiposNovedadesView(LoginRequiredMixin, ListView):
    """Vista para listar tipos de novedades"""
    model = Novedad
    template_name = 'lecturas/listar_tipos_novedades.html'
    context_object_name = 'novedades'   
    ordering = ['descripcion']


