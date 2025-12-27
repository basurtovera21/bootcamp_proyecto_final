from django.db import models

class DatosPersonales(models.Model):
    SEXO_CHOICES = [('H', 'Hombre'), ('M', 'Mujer')]
    
    descripcion_perfil = models.CharField(max_length = 50, blank = True, verbose_name = "Descripción de perfil")
    perfil_activo = models.BooleanField(default = True, verbose_name = "Perfil activo/inactivo")
    apellidos = models.CharField(max_length = 60, verbose_name = "Apellido(s)")
    nombres = models.CharField(max_length = 60, verbose_name = "Nombre(s)")
    nacionalidad = models.CharField(max_length = 20, verbose_name = "Nacionalidad")
    lugar_nacimiento = models.CharField(max_length = 60, verbose_name = "Lugar de nacimiento")
    fecha_nacimiento = models.DateField(verbose_name = "Fecha de nacimiento")
    numero_cedula = models.CharField(max_length = 10, unique = True, verbose_name = "Cédula de identidad")
    sexo = models.CharField(max_length = 1, choices = SEXO_CHOICES, verbose_name = "Sexo")
    estado_civil = models.CharField(max_length = 50, verbose_name = "Estado civil")
    licencia_conducir = models.CharField(max_length = 6, blank = True, verbose_name = "Licencia de conducir vigente")
    telefono_celular = models.CharField(max_length = 15, verbose_name = "Número de teléfono celular")
    telefono_fijo = models.CharField(max_length = 15, blank = True, verbose_name = "Número de teléfono convencional")
    direccion_domiciliaria = models.CharField(max_length = 50, verbose_name = "Dirección de residencia")
    direccion_trabajo = models.CharField(max_length = 50, blank = True, verbose_name = "Dirección laboral")
    sitio_web = models.URLField(max_length = 60, blank = True, verbose_name = "URL personal")
    foto = models.ImageField(upload_to='perfil/', blank = True, null = True, verbose_name = "Fotografía")

    def __str__(self):
        return f"{self.nombres} {self.apellidos}"

    class Meta:
        verbose_name = "Información personal"
        verbose_name_plural = "Información personal"

class ExperienciaLaboral(models.Model):
    perfil = models.ForeignKey(DatosPersonales, on_delete = models.CASCADE, verbose_name = "Perfil registrado")
    cargo_desempenado = models.CharField(max_length = 100, verbose_name = "Cargo/puesto")
    nombre_empresa = models.CharField(max_length = 50, verbose_name = "Empresa empleadora")
    lugar_empresa = models.CharField(max_length = 50, verbose_name = "Dirección de la empresa")
    email_empresa = models.EmailField(max_length = 100, blank = True, verbose_name = "Correo electrónico empresarial")
    sitio_web_empresa = models.URLField(max_length = 100, blank = True, verbose_name = "URL de la empresa")
    nombre_contacto = models.CharField(max_length = 100, verbose_name = "Responsable de contacto")
    telefono_contacto = models.CharField(max_length = 60, verbose_name = "Número de contacto de empresa")
    fecha_inicio = models.DateField(verbose_name = "Fecha de incorporación")
    fecha_fin = models.DateField(verbose_name = "Fecha de finalización")
    descripcion_funciones = models.TextField(max_length = 500, verbose_name = "Descripción de responsabilidades")
    ruta_certificado = models.FileField(upload_to = 'certificados_laborales/', blank = True, null = True, verbose_name = "Constancia laboral")
    activar_en_front = models.BooleanField(default = True, verbose_name = "Visible/no visible")

    def __str__(self):
        return f"{self.cargo_desempenado} en {self.nombre_empresa}"

    class Meta:
        verbose_name = "Experiencia profesional"
        verbose_name_plural = "Experiencia profesional"

class Reconocimiento(models.Model):
    TIPO_CHOICES = [('Académica', 'Académica'), ('Pública', 'Pública'), ('Privada', 'Privada')]

    perfil = models.ForeignKey(DatosPersonales, on_delete = models.CASCADE, verbose_name = "Perfil registrado")
    tipo_reconocimiento = models.CharField(max_length = 50, choices = TIPO_CHOICES, verbose_name = "Naturaleza de acreditación")
    descripcion = models.CharField(max_length = 100, verbose_name = "Descripción de la acreditación")
    fecha_reconocimiento = models.DateField(verbose_name = "Fecha de acreditación")
    entidad_patrocinadora = models.CharField(max_length = 100, verbose_name = "Institución patrocinadora")
    nombre_contacto = models.CharField(max_length=100, blank=True, verbose_name = "Responsable de contacto")
    telefono_contacto = models.CharField(max_length=60, blank=True, verbose_name = "Número de contacto institucional")
    ruta_certificado = models.FileField(upload_to='reconocimientos/', blank=True, null=True, verbose_name = "Acreditación")
    activar_en_front = models.BooleanField(default = True, verbose_name = "Visible/no visible")
    
    class Meta:
        verbose_name = "Acreditación"
        verbose_name_plural = "Acreditaciones"

class CursoRealizado(models.Model):
    perfil = models.ForeignKey(DatosPersonales, on_delete = models.CASCADE, verbose_name = "Perfil registrado")
    nombre_curso = models.CharField(max_length = 100, verbose_name = "Formación realizada")
    fecha_inicio = models.DateField(verbose_name = "Fecha de incorporación")
    fecha_fin = models.DateField(verbose_name ="Fecha de finalización")
    total_horas = models.IntegerField(verbose_name = "Horas de formación")
    descripcion = models.CharField(max_length = 100, verbose_name = "Descripción de la formación")
    entidad_patrocinadora = models.CharField(max_length = 100, verbose_name = "Institución patrocinadora")
    nombre_contacto = models.CharField(max_length = 100, blank = True, verbose_name = "Responsable de contacto")
    telefono_contacto = models.CharField(max_length = 60, blank = True, verbose_name = "Número de contacto institucional")
    email_patrocinadora = models.EmailField(max_length = 60, blank = True, verbose_name = "Correo electrónico institucional")
    ruta_certificado = models.FileField(upload_to = 'cursos/', blank = True, null = True, verbose_name = "Certificado")
    activar_en_front = models.BooleanField(default = True, verbose_name = "Visible/no visible")

    class Meta:
        verbose_name = "Formación realizada"
        verbose_name_plural = "Formación realizada"

class ProductoAcademico(models.Model):
    perfil = models.ForeignKey(DatosPersonales, on_delete = models.CASCADE, verbose_name = "Perfil registrado")
    nombre_recurso = models.CharField(max_length = 100, verbose_name = "Nombre del producto")
    clasificador = models.CharField(max_length = 100, verbose_name = "Tipo de producto")
    descripcion = models.CharField(max_length = 100, verbose_name = "Descripción del producto")
    activar_en_front = models.BooleanField(default = True, verbose_name = "Visible/no visible")

    class Meta:
        verbose_name = "Producción académica"
        verbose_name_plural = "Producción académica"

class ProductoLaboral(models.Model):
    perfil = models.ForeignKey(DatosPersonales, on_delete = models.CASCADE, verbose_name = "Perfil registrado")
    nombre_producto = models.CharField(max_length = 100, verbose_name = "Nombre del producto")
    fecha_producto = models.DateField(verbose_name = "Fecha de realización")
    descripcion = models.CharField(max_length=100, verbose_name = "Descripción del producto")
    activar_en_front = models.BooleanField(default=True, verbose_name = "Visible/no visible")

    class Meta:
        verbose_name = "Producción laboral"
        verbose_name_plural = "Producción laboral"

class VentaGarage(models.Model):
    ESTADO_CHOICES = [('En buen estado', 'En buen estado'), ('Estado aceptable', 'Estado aceptable')]

    perfil = models.ForeignKey(DatosPersonales, on_delete = models.CASCADE, verbose_name = "Perfil registrado")
    nombre_producto = models.CharField(max_length = 100, verbose_name = "Nombre del producto")
    estado_producto = models.CharField(max_length = 40, choices=ESTADO_CHOICES, verbose_name = "Condición del producto")
    descripcion = models.CharField(max_length = 100, verbose_name = "Descripción del producto")
    foto = models.ImageField(upload_to = 'venta_garage/', blank = True, null = True, verbose_name = "Fotografía")
    valor_bien = models.DecimalField(max_digits = 5, decimal_places = 2, verbose_name = "Precio de venta")
    activar_en_front = models.BooleanField(default = True, verbose_name = "Visible/no visible")

    class Meta:
        verbose_name = "Producto en venta"
        verbose_name_plural = "Listado de productos en venta"