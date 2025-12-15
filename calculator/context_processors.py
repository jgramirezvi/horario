def menu_colors_processor(request):
    """
    Procesador de contexto para añadir los colores del menú a todas las plantillas.
    """
    # Los mismos colores por defecto que en la vista 'settings_view'
    default_colors = {
        'bg_color': '#f8f9fa',
        'text_color': '#343a40',
        'hover_bg_color': '#e9ecef',
        'hover_text_color': '#0056b3',
    }
    
    # Obtiene los colores de la sesión o usa los de por defecto
    menu_colors = request.session.get('menu_colors', default_colors)
    
    return {'menu_colors': menu_colors}