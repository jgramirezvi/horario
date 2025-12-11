def menu_colors_processor(request):
    """
    Procesador de contexto para añadir los colores del menú a todas las plantillas.
    """
    # Los mismos colores por defecto que en la vista 'settings_view'
    default_colors = {
        'bg_color': '#0000ff',
        'text_color': '#ffff00',
        'hover_bg_color': '#ff00ff',
        'hover_text_color': '#ffffff',
    }
    
    # Obtiene los colores de la sesión o usa los de por defecto
    menu_colors = request.session.get('menu_colors', default_colors)
    
    return {'menu_colors': menu_colors}