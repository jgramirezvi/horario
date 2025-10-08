from django.shortcuts import render
from math import log, sqrt, log10

# Imports para la generación de PDF
from django.http import HttpResponse
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
import io

def _get_log_data(limit=10):
    """Función auxiliar para generar los datos de la tabla de logaritmos."""
    results = []
    for i in range(limit + 1):
        if i > 0:
            log_value = log(i)
            results.append({'number': i, 'log': f"{log_value:.4f}"})
        else:
            # El logaritmo de 0 es indefinido (tiende a -infinito)
            results.append({'number': i, 'log': "-inf"})
    return results

def calculator_view(request):
    context = {'title': 'Calculadora'}
    
    if request.method == 'POST':
        try:
            num1 = float(request.POST.get('number1'))
            num2_str = request.POST.get('number2')
            operation = request.POST.get('operation')

            result = None
            
            # Definimos las operaciones en un diccionario para un código más limpio
            binary_operations = {
                'add': lambda a, b: a + b,
                'subtract': lambda a, b: a - b,
                'multiply': lambda a, b: a * b,
                'divide': lambda a, b: a / b if b != 0 else "Error: No se puede dividir por cero."
            }
            unary_operations = {
                'square': lambda a: a ** 2,
                'sqrt': lambda a: sqrt(a) if a >= 0 else "Error: No se puede calcular la raíz cuadrada de un número negativo.",
                'log': lambda a: log(a) if a > 0 else "Error: El logaritmo natural solo está definido para números positivos.",
                'log10': lambda a: log10(a) if a > 0 else "Error: El logaritmo vulgar solo está definido para números positivos."
            }

            if operation in binary_operations:
                num2 = float(num2_str)
                result = binary_operations[operation](num1, num2)
            elif operation in unary_operations:
                result = unary_operations[operation](num1)

            # Manejamos los errores que devuelven las funciones lambda
            if isinstance(result, str):
                context['error'] = result
                context['result'] = None
            else:
                context['result'] = result

        except (ValueError, TypeError):
            context['error'] = "Error: Por favor, introduce números válidos."

    return render(request, 'calculator/calculator.html', context)
    
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
