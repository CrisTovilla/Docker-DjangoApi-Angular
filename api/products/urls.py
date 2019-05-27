from django.urls import path,re_path
from products.views import ProductView,SingleProductView

urlpatterns = [
    path('<int:pk>', SingleProductView.as_view()),
    re_path(r'^',ProductView.as_view()),  
]