from django.shortcuts import render
from math import log, sqrt, log10

# Imports para la generación de PDF
from django.http import HttpResponse
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
import io

def calculator_view(request):
    context = {'title': 'Calculadora'}
    
    if request.method == 'POST':
        try:
            num1 = float(request.POST.get('number1'))
            operation = request.POST.get('operation')
            num2 = request.POST.get('number2') # Puede ser None

            result = None

            if operation == 'add':
                result = num1 + float(num2)
            elif operation == 'subtract':
                result = num1 - float(num2)
            elif operation == 'multiply':
                result = num1 * float(num2)
            elif operation == 'divide':
                if float(num2) == 0:
                    context['error'] = "Error: No se puede dividir por cero."
                else:
                    result = num1 / float(num2)
            elif operation == 'square':
                result = num1 ** 2
            elif operation == 'sqrt':
                if num1 < 0:
                    context['error'] = "Error: No se puede calcular la raíz cuadrada de un número negativo."
                else:
                    result = sqrt(num1)
            elif operation == 'log': # Logaritmo natural
                if num1 <= 0:
                    context['error'] = "Error: El logaritmo natural solo está definido para números positivos."
                else:
                    result = log(num1)
            elif operation == 'log10': # Logaritmo vulgar (base 10)
                if num1 <= 0:
                    context['error'] = "Error: El logaritmo vulgar solo está definido para números positivos."
                else:
                    result = log10(num1)
            context['result'] = result
        except (ValueError, TypeError):
            context['error'] = "Error: Por favor, introduce números válidos."

    return render(request, 'calculator/calculator.html', context)
    
def show_log_table(request):
    a = 10
    results = []
    for i in range(a + 1):
        # Evitamos el log(0) que causa un error matemático
        if i > 0:
            log_value = log(i)
        else:
            # El logaritmo de 0 es indefinido (tiende a -infinito)
            log_value = "-inf"
        
        results.append({'number': i, 'log': log_value})

    context = {
        'data': results,
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
    a = 10
    results = []
    for i in range(a + 1):
        if i > 0:
            log_value = f"{log(i):.4f}"
        else:
            log_value = "-inf"
        results.append({'number': i, 'log': log_value})

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
