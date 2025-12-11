from django.db import models                    #Esta libreria nos permite heredar los metodos para trabajr con el ORM.
from django.contrib.auth.models import User     #Esta libreria nos permite heredar los metodos para trabajr con el ORM.
from django.utils import timezone               #Esta libreria la uso para insertar un timestamp en el campo fecha_hora_registro.


class Operador(models.Model):
    """Esta clase modela los operadores del sistema"""
    cod_ope = models.AutoField(primary_key=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='operador')
    
    # Redefino algunas propiedades de la clase Meta heredadas de models para que sean ms representativas
    class Meta:
        verbose_name = 'Operador'
        verbose_name_plural = 'Operadores'
    
    def __str__(self):
        return f"{self.user.get_full_name() or self.user.username}"


class Cliente(models.Model):
    """Esta clase modela los clientes"""
    cod_cli = models.AutoField(primary_key=True)
    denominacion = models.CharField(max_length=200, verbose_name='Nombre y Apellido')
    domicilio = models.CharField(max_length=300, verbose_name='Domicilio')
    
    # Redefino algunas propiedades de la clase Meta heredadas de models para que sean ms representativas
    class Meta:
        verbose_name = 'Cliente'
        verbose_name_plural = 'Clientes'
    
    def __str__(self):
        return self.denominacion


class Novedad(models.Model):
    """Esta clase modela las novedades"""
    cod_novedad = models.AutoField(primary_key=True)
    descripcion = models.CharField(max_length=200, verbose_name='Descripción')
    
    # Redefino algunas propiedades de la clase Meta heredadas de models para que sean ms representativas
    class Meta:
        verbose_name = 'Novedad'
        verbose_name_plural = 'Novedades'
    
    def __str__(self):
        return self.descripcion


class Lote(models.Model):
    """Esta clase modela las lecturas de medidores y sus posibles novedades"""
    cod_lectura = models.AutoField(primary_key=True)
    
    # Periodo de consumo
    ano_consumo = models.IntegerField(verbose_name='Año de Consumo')
    mes_consumo = models.IntegerField(verbose_name='Mes de Consumo')
    
    # Datos del cliente y suministro
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, related_name='lecturas')
    suministro_numero = models.CharField(max_length=50, verbose_name='Nº Suministro')
    
    # Datos de la ruta
    area = models.CharField(max_length=50, verbose_name='Área')
    ruta = models.CharField(max_length=50, verbose_name='Ruta')
    orden = models.IntegerField(verbose_name='Orden')
    
    # Datos del medidor
    tipo_medidor = models.CharField(max_length=50, verbose_name='Tipo de Medidor')
    numero_medidor = models.CharField(max_length=50, verbose_name='Nº Medidor')
    
    # Lecturas y consumo
    lectura_anterior = models.IntegerField(verbose_name='Lectura Anterior')
    lectura_actual = models.IntegerField(null=True, blank=True, verbose_name='Lectura Actual')
    consumo_kwh = models.IntegerField(null=True, blank=True, verbose_name='Consumo (kWh)')
    
    # Novedades
    novedades = models.ManyToManyField(Novedad, blank=True, through='NovedadLectura')
    novedad_libre = models.TextField(null=True, blank=True, verbose_name='Novedad Libre')
    
    # Estados
    enviado_comercial = models.BooleanField(default=False, verbose_name='Enviado a Comercial')
    abierta = models.BooleanField(default=True, verbose_name='Ruta Abierta')
    
    # Auditoría
    fecha_hora_registro = models.DateTimeField(null=True, blank=True, verbose_name='Fecha/Hora Registro')
    ubi_gps = models.CharField(max_length=100, null=True, blank=True, verbose_name='Ubicación GPS')
    operador = models.ForeignKey(Operador, on_delete=models.SET_NULL, null=True, blank=True, related_name='lecturas')
    
    # Redefino algunas propiedades de la clase Meta heredadas de models para que sean ms representativas
    class Meta:
        verbose_name = 'Lectura'
        verbose_name_plural = 'Lecturas'
        ordering = ['ano_consumo', 'mes_consumo', 'ruta', 'orden']
        indexes = [
            models.Index(fields=['ano_consumo', 'mes_consumo']),
            models.Index(fields=['ruta']),
        ]
    
    def __str__(self):
        return f"Lectura {self.cod_lectura} - {self.cliente.denominacion} ({self.ano_consumo}/{self.mes_consumo})"
    
    def save(self, *args, **kwargs):
        # Calculo el consumo si hay lectura actual
        if self.lectura_actual is not None and self.lectura_anterior is not None:
            self.consumo_kwh = self.lectura_actual - self.lectura_anterior
        super().save(*args, **kwargs)
    
    @property
    def tiene_lectura(self):
        """Devuelve True si ya se registró la lectura"""
        return self.lectura_actual is not None
    
    @property
    def periodo_str(self):
        """Devuelve el periodo en formato legible"""
        meses = ['Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio',
                'Julio', 'Agosto', 'Septiembre', 'Octubre', 'Noviembre', 'Diciembre']
        return f"{meses[self.mes_consumo]} {self.ano_consumo}"


class NovedadLectura(models.Model):
    """Tabla intermedia para relacion muchos a muchos entre Lote y Novedad"""
    lectura = models.ForeignKey(Lote, on_delete=models.CASCADE)
    novedad = models.ForeignKey(Novedad, on_delete=models.CASCADE)
    fecha_registro = models.DateTimeField(auto_now_add=True)
    
    # Redefino algunas propiedades de la clase Meta heredadas de models para que sean ms representativas
    class Meta:
        verbose_name = 'Novedad de Lectura'
        verbose_name_plural = 'Novedades de Lecturas'
        unique_together = ['lectura', 'novedad']
    
    def __str__(self):
        return f"{self.lectura.cod_lectura} - {self.novedad.descripcion}"
