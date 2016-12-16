from django.conf.urls import url
from . import views

urlpatterns = [
    # url(r'^$', views.hello_world, name='hello'),
    url(r'^obtener/$', views.generar_pdf),
    #r'^report/$'
]