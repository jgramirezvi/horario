def menu_colors_processor(request):
    if 'menu_colors' not in request.session:
        request.session['menu_colors'] = {
            'bg_color': '#0000ff',
            'text_color': '#ffff00',
            'hover_bg_color': '#ff00ff',
            'hover_text_color': '#ffffff',
        }
    return {'menu_colors': request.session['menu_colors']}
