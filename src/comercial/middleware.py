from django.shortcuts import redirect
from django.urls import reverse

class AuthRequiredMiddleware:
    """
    Middleware que redireciona usuários não autenticados para a página de login
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # URLs que não requerem autenticação
        public_urls = [
            reverse('auth:login'),
            reverse('auth:register'),
            '/admin/login/',
        ]
        
        # Se o usuário não está autenticado e não está em uma URL pública
        if not request.user.is_authenticated and request.path not in public_urls:
            # Se não é uma requisição AJAX, redireciona para login
            if not request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return redirect('auth:login')
        
        response = self.get_response(request)
        return response
