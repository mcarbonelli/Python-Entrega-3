from django.urls import path
from . import views

urlpatterns = [
    path('', views.LoginView.as_view(), name='login'), # Con esto hago que cuando no ingresa ninguna ruta vaya a la vista del login
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('dashboard/', views.DashboardView.as_view(), name='dashboard'),
    path('seleccionar-periodo/', views.SeleccionarPeriodoView.as_view(), name='seleccionar_periodo'),
    path('listar-rutas/', views.ListarRutasView.as_view(), name='listar_rutas'),
    path('tomar-lecturas/<str:ruta>/', views.TomarLecturasView.as_view(), name='tomar_lecturas'),
    path('guardar-lectura/<int:pk>/', views.GuardarLecturaView.as_view(), name='guardar_lectura'),
    path('eliminar-lectura/<int:pk>/', views.EliminarLecturaView.as_view(), name='eliminar_lectura'),
    path('agregar-novedad/<int:pk>/', views.AgregarNovedadView.as_view(), name='agregar_novedad'),
    path('cerrar-ruta/', views.CerrarRutaView.as_view(), name='cerrar_ruta'),
    path('abrir-ruta/', views.AbrirRutaView.as_view(), name='abrir_ruta'),

    path('listar-novedades/', views.ListarTiposNovedadesView.as_view(), name='listar_tipos_novedades'),    

]
