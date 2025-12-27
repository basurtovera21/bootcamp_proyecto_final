from django.shortcuts import render, redirect
from django.db import models
from .models import (
    DatosPersonales, 
    ExperienciaLaboral, 
    Reconocimiento, 
    CursoRealizado, 
    ProductoAcademico, 
    ProductoLaboral, 
    VentaGarage
)

def get_perfil_activo():
    return DatosPersonales.objects.filter(perfil_activo=True).first()

def get_flags_secciones(perfil):
    if not perfil:
        return {}    
    return {
        'hay_experiencia': ExperienciaLaboral.objects.filter(perfil=perfil, activar_en_front=True).exists(),
        'hay_cursos': CursoRealizado.objects.filter(perfil=perfil, activar_en_front=True).exists(),
        'hay_reconocimientos': Reconocimiento.objects.filter(perfil=perfil, activar_en_front=True).exists(),
        'hay_ventas': VentaGarage.objects.filter(perfil=perfil, activar_en_front=True).exists(),
        'hay_productos': (
            ProductoAcademico.objects.filter(perfil=perfil, activar_en_front=True).exists() or 
            ProductoLaboral.objects.filter(perfil=perfil, activar_en_front=True).exists()
        )
    }

def home(request):
    perfil = get_perfil_activo()
    flags = get_flags_secciones(perfil)
    titulo_pestana = "Hoja de vida"
    labels = {}
    botones = {}
    datos_dinamicos = [] 
    
    if perfil:
        titulo_pestana = "Información personal"
        meta_datos = DatosPersonales._meta
        labels['info_personal'] = meta_datos.verbose_name
        labels['descripcion'] = meta_datos.get_field('descripcion_perfil').verbose_name
        botones['experiencia'] = ExperienciaLaboral._meta.verbose_name_plural
        botones['reconocimientos'] = Reconocimiento._meta.verbose_name_plural
        botones['cursos'] = CursoRealizado._meta.verbose_name_plural
        botones['ventas'] = VentaGarage._meta.verbose_name_plural
        botones['prod_academico'] = ProductoAcademico._meta.verbose_name_plural
        botones['prod_laboral'] = ProductoLaboral._meta.verbose_name_plural
        campos_ignorados = [
            'id', 'nombres', 'apellidos', 'descripcion_perfil', 'foto', 'perfil_activo'
        ]

        for field in meta_datos.fields:
            if field.name not in campos_ignorados:
                valor = getattr(perfil, field.name)
                
                if valor:
                    item = {
                        'label': field.verbose_name,
                        'valor': valor,
                        'es_link': isinstance(field, models.URLField) 
                    }
                    datos_dinamicos.append(item)

    context = {
        'perfil': perfil,
        'lbl': labels,
        'btn': botones,
        'datos_dinamicos': datos_dinamicos,
        'flags': flags,
        'titulo_pestana': titulo_pestana
    }
    
    return render(request, 'hoja_vida/home.html', context)

def experiencia(request):
    perfil = get_perfil_activo()
    if not perfil: return redirect('home')
    experiencias = ExperienciaLaboral.objects.filter(perfil = perfil, activar_en_front=True).order_by('-fecha_inicio')

    if not experiencias.exists(): return redirect('home')
    meta_exp = ExperienciaLaboral._meta
    meta_perfil = DatosPersonales._meta 
    
    labels = {
        'empresa': meta_exp.get_field('nombre_empresa').verbose_name,
        'descripcion': meta_exp.get_field('descripcion_funciones').verbose_name, 
        'direccion': meta_exp.get_field('lugar_empresa').verbose_name,
        'email': meta_exp.get_field('email_empresa').verbose_name,
        'url': meta_exp.get_field('sitio_web_empresa').verbose_name,
        'responsable': meta_exp.get_field('nombre_contacto').verbose_name,
        'telefono': meta_exp.get_field('telefono_contacto').verbose_name,
        'fecha_inicio': meta_exp.get_field('fecha_inicio').verbose_name,
        'fecha_fin': meta_exp.get_field('fecha_fin').verbose_name,
        'constancia': meta_exp.get_field('ruta_certificado').verbose_name, 
    }

    botones = {
        'home': meta_perfil.verbose_name, 
        'reconocimientos': Reconocimiento._meta.verbose_name_plural,
        'cursos': CursoRealizado._meta.verbose_name_plural,
        'prod_academico': ProductoAcademico._meta.verbose_name_plural,
        'prod_laboral': ProductoLaboral._meta.verbose_name_plural,
        'ventas': VentaGarage._meta.verbose_name_plural,
    }

    context = {
        'perfil': perfil,
        'experiencias': experiencias,
        'lbl': labels,
        'btn': botones,
        'flags': get_flags_secciones(perfil),
        'titulo_pestana': "Experiencia profesional"
    }
    
    return render(request, 'hoja_vida/experiencia.html', context)

def reconocimientos(request):
    perfil = get_perfil_activo()
    if not perfil: return redirect('home')
    
    lista_reconocimientos = Reconocimiento.objects.filter(
        perfil = perfil, activar_en_front=True
    ).order_by('-fecha_reconocimiento')
    
    if not lista_reconocimientos.exists(): return redirect('home')
    meta_rec = Reconocimiento._meta
    meta_perfil = DatosPersonales._meta
    
    labels = {
        'nombre_premio': meta_rec.get_field('descripcion').verbose_name,
        'tipo': meta_rec.get_field('tipo_reconocimiento').verbose_name,
        'fecha': meta_rec.get_field('fecha_reconocimiento').verbose_name,
        'institucion': meta_rec.get_field('entidad_patrocinadora').verbose_name,
        'contacto': meta_rec.get_field('nombre_contacto').verbose_name,
        'telefono': meta_rec.get_field('telefono_contacto').verbose_name,
        'certificado': meta_rec.get_field('ruta_certificado').verbose_name,
    }

    botones = {
        'titulo_vista': meta_rec.verbose_name_plural,
        'home': meta_perfil.verbose_name,
        'experiencia': ExperienciaLaboral._meta.verbose_name_plural,
        'cursos': CursoRealizado._meta.verbose_name_plural,
        'prod_academico': ProductoAcademico._meta.verbose_name_plural,
        'prod_laboral': ProductoLaboral._meta.verbose_name_plural,
        'ventas': VentaGarage._meta.verbose_name_plural,
    }
        
    context = {
        'perfil': perfil, 
        'reconocimientos': lista_reconocimientos,
        'lbl': labels, 
        'btn': botones,
        'flags': get_flags_secciones(perfil),
        'titulo_pestana': "Acreditaciones"
    }
    return render(request, 'hoja_vida/reconocimientos.html', context)

def cursos(request):
    perfil = get_perfil_activo()
    if not perfil: return redirect('home')
    
    lista_cursos = CursoRealizado.objects.filter(
        perfil = perfil, activar_en_front = True
    ).order_by('-fecha_inicio')

    if not lista_cursos.exists(): return redirect('home')
    
    meta_curso = CursoRealizado._meta
    meta_perfil = DatosPersonales._meta
    
    labels = {
        'titulo': meta_curso.get_field('nombre_curso').verbose_name,
        'institucion': meta_curso.get_field('entidad_patrocinadora').verbose_name,
        'descripcion': meta_curso.get_field('descripcion').verbose_name,
        'horas': meta_curso.get_field('total_horas').verbose_name,
        'contacto': meta_curso.get_field('nombre_contacto').verbose_name,
        'telefono': meta_curso.get_field('telefono_contacto').verbose_name,
        'email': meta_curso.get_field('email_patrocinadora').verbose_name,
        'inicio': meta_curso.get_field('fecha_inicio').verbose_name,
        'fin': meta_curso.get_field('fecha_fin').verbose_name,
        'certificado': meta_curso.get_field('ruta_certificado').verbose_name,
    }

    botones = {
        'titulo_vista': meta_curso.verbose_name_plural,
        'home': meta_perfil.verbose_name,
        'experiencia': ExperienciaLaboral._meta.verbose_name_plural,
        'reconocimientos': Reconocimiento._meta.verbose_name_plural,
        'prod_academico': ProductoAcademico._meta.verbose_name_plural,
        'prod_laboral': ProductoLaboral._meta.verbose_name_plural,
        'ventas': VentaGarage._meta.verbose_name_plural,
    }
        
    context = {
        'perfil': perfil, 
        'cursos': lista_cursos,
        'lbl': labels,
        'btn': botones,
        'flags': get_flags_secciones(perfil),
        'titulo_pestana': "Formación realizada"
    }
    
    return render(request, 'hoja_vida/cursos.html', context)

def productos(request):
    perfil = get_perfil_activo()
    if not perfil: return redirect('home')
    
    prod_academicos = ProductoAcademico.objects.filter(
        perfil = perfil, activar_en_front=True
    ).order_by('nombre_recurso')
    
    prod_laborales = ProductoLaboral.objects.filter(
        perfil = perfil, activar_en_front=True
    ).order_by('-fecha_producto')

    if not prod_academicos.exists() and not prod_laborales.exists():
        return redirect('home')

    meta_acad = ProductoAcademico._meta
    meta_lab = ProductoLaboral._meta
    meta_perfil = DatosPersonales._meta

    labels = {
        'acad_titulo': meta_acad.get_field('nombre_recurso').verbose_name,
        'acad_tipo': meta_acad.get_field('clasificador').verbose_name,
        'acad_desc': meta_acad.get_field('descripcion').verbose_name,
        'lab_titulo': meta_lab.get_field('nombre_producto').verbose_name,
        'lab_fecha': meta_lab.get_field('fecha_producto').verbose_name,
        'lab_desc': meta_lab.get_field('descripcion').verbose_name,
    }

    titulos_secciones = {
        'academico': meta_acad.verbose_name_plural,
        'laboral': meta_lab.verbose_name_plural,
    }

    botones = {
        'home': meta_perfil.verbose_name,
        'experiencia': ExperienciaLaboral._meta.verbose_name_plural,
        'reconocimientos': Reconocimiento._meta.verbose_name_plural,
        'cursos': CursoRealizado._meta.verbose_name_plural,
        'ventas': VentaGarage._meta.verbose_name_plural,
    }

    context = {
        'perfil': perfil,
        'prod_academicos': prod_academicos,
        'prod_laborales': prod_laborales,
        'lbl': labels,
        'titulos': titulos_secciones,
        'btn': botones,
        'flags': get_flags_secciones(perfil),
        'titulo_pestana': "Producción académica/laboral"
    }
    
    return render(request, 'hoja_vida/productos.html', context)

def venta_garage(request):
    perfil = get_perfil_activo()
    if not perfil: return redirect('home')
    
    ventas = VentaGarage.objects.filter(
        perfil = perfil, activar_en_front=True
    ).order_by('nombre_producto')
 
    if not ventas.exists(): return redirect('home')
    meta_venta = VentaGarage._meta
    meta_perfil = DatosPersonales._meta
    
    labels = {
        'producto': meta_venta.get_field('nombre_producto').verbose_name,
        'estado': meta_venta.get_field('estado_producto').verbose_name,
        'descripcion': meta_venta.get_field('descripcion').verbose_name,
        'precio': meta_venta.get_field('valor_bien').verbose_name,
        'foto': 'Foto del producto', 
    }

    botones = {
        'titulo_vista': meta_venta.verbose_name_plural,
        'home': meta_perfil.verbose_name,
        'experiencia': ExperienciaLaboral._meta.verbose_name_plural,
        'reconocimientos': Reconocimiento._meta.verbose_name_plural,
        'cursos': CursoRealizado._meta.verbose_name_plural,
        'prod_academico': ProductoAcademico._meta.verbose_name_plural,
        'prod_laboral': ProductoLaboral._meta.verbose_name_plural,
    }
        
    context = {
        'perfil': perfil, 
        'ventas': ventas,
        'lbl': labels,
        'btn': botones,
        'flags': get_flags_secciones(perfil),
        'titulo_pestana': "Listado de productos en venta"
    }
    
    return render(request, 'hoja_vida/venta_garage.html', context)