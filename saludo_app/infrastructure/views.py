import json
from django.http import JsonResponse
from django.views import View
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

from saludo_app.application.use_cases import SaludarUseCase

@method_decorator(csrf_exempt, name='dispatch')
class SaludoHttpAdapter(View):
    use_case = SaludarUseCase()

    def post(self, request, *args, **kwargs):
        try:
            body = json.loads(request.body)
            nombre = body.get("nombre", "")
            
            mensaje = self.use_case.ejecutar(nombre=nombre)
            
            return JsonResponse({"mensaje": mensaje}, status=200)
            
        except ValueError as e:
            return JsonResponse({"error": str(e)}, status=400)
        except json.JSONDecodeError:
            return JsonResponse({"error": "El cuerpo de la petición debe ser un JSON válido."}, status=400)