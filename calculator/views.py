from django.shortcuts import render, redirect
from math import log, sqrt, log10, factorial
from asteval import Interpreter

# Imports para la generación de PDF
from django.http import HttpResponse
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
import io

def portal_view(request):
    """Vista para la página del portal principal."""
    return render(request, 'calculator/portal.html')

def home_view(request):
    """Vista para la página de inicio del proyecto."""
    return render(request, 'calculator/home.html')

def _get_log_data(limit=10):
    """Función auxiliar para generar los datos de la tabla de logaritmos."""
    results = []
    for number in range(limit + 1):
        if number > 0:
            log_value = log(number)
            results.append({'number': number, 'log': f"{log_value:.4f}"})
        else:
            # El logaritmo de 0 es indefinido (tiende a -infinito)
            results.append({'number': number, 'log': "-inf"})
    return results

def calculator_view(request):
    context = {'title': 'Calculadora'}
    
    # El historial se mantiene entre peticiones usando la sesión de Django
    if 'history' not in request.session:
        request.session['history'] = []

    if request.method == 'POST':
        expression = request.POST.get('expression', '')
        try:
            # Usamos asteval para una evaluación segura de la expresión matemática.
            # Es mucho más seguro que eval().
            aeval = Interpreter()

            # Eliminamos las funciones por defecto que no queremos (por seguridad)
            # y añadimos las nuestras.
            aeval.symtable = {
                'sqrt': sqrt, 'log': log, 'log10': log10, 'factorial': factorial
            }

            result = aeval.eval(expression)
            context['result'] = result

            # Añadir al historial
            request.session['history'].append(f"{expression} = {result}")
            request.session.modified = True

        except Exception as e:
            context['error'] = f"Error: {e}"

    return render(request, 'calculator/calculator.html', context)

def clear_history(request):
    """Limpia el historial de la sesión."""
    if 'history' in request.session:
        request.session['history'] = []
    return redirect('calculator')
    
def show_log_table(request):
    context = {
        'data': _get_log_data(),
        'title': 'Tabla de Logaritmos'
    }
    return render(request, 'calculator/log_table.html', context)

def generate_log_pdf(request):
    # Crea un buffer de bytes en memoria para el archivo PDF
    buf = io.BytesIO()

    # Crea el objeto PDF, usando el buffer como su "archivo"
    c = canvas.Canvas(buf, pagesize=letter, bottomup=0)

    # Crea un objeto de texto para escribir en el PDF
    textob = c.beginText()
    textob.setTextOrigin(inch, inch)
    textob.setFont("Helvetica", 14)

    # Lógica para obtener los datos (similar a show_log_table)
    results = _get_log_data()
    # Añade el contenido al PDF
    textob.textLine("Tabla de Logaritmos")
    textob.setFont("Helvetica", 12)
    textob.textLine("-" * 20)
    for item in results:
        textob.textLine(f"Número: {item['number']}, Logaritmo: {item['log']}")

    # Finaliza la escritura y guarda el PDF
    c.drawText(textob)
    c.showPage()
    c.save()
    buf.seek(0)

    # Devuelve el PDF como una respuesta HTTP
    return HttpResponse(buf, content_type='application/pdf')

def settings_view(request):
    """Vista para la página de configuración."""
    if request.method == 'POST':
        colors = {
            'bg_color': request.POST.get('bg_color', '#0000ff'),
            'text_color': request.POST.get('text_color', '#ffff00'),
            'hover_bg_color': request.POST.get('hover_bg_color', '#ff00ff'),
            'hover_text_color': request.POST.get('hover_text_color', '#ffffff'),
        }
        request.session['menu_colors'] = colors
        return redirect('settings')

    return render(request, 'calculator/settings.html')

