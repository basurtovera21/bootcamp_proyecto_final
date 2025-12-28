from .models import (
    DatosPersonales, 
    ExperienciaLaboral, 
    Reconocimiento, 
    CursoRealizado, 
    ProductoAcademico, 
    ProductoLaboral, 
    VentaGarage
)

def visibilidad_menu(request):
    perfil = DatosPersonales.objects.filter(perfil_activo=True).first()
    if not perfil:
        return {}

    return {
        'menu_hay_experiencia': ExperienciaLaboral.objects.filter(perfil=perfil, activar_en_front=True).exists(),
        'menu_hay_reconocimientos': Reconocimiento.objects.filter(perfil=perfil, activar_en_front=True).exists(),
        'menu_hay_cursos': CursoRealizado.objects.filter(perfil=perfil, activar_en_front=True).exists(),
        'menu_hay_ventas': VentaGarage.objects.filter(perfil=perfil, activar_en_front=True).exists(),
        'menu_hay_proyectos': (
            ProductoAcademico.objects.filter(perfil=perfil, activar_en_front=True).exists() or 
            ProductoLaboral.objects.filter(perfil=perfil, activar_en_front=True).exists()
        ),
    }