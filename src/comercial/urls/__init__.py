from django.urls import include, path
from . import auth, comercial

urlpatterns = [
    path('auth/', include((auth.urlpatterns, 'auth'), namespace='auth')),
    path('', include((comercial.urlpatterns, 'comercial'), namespace='comercial')),
]