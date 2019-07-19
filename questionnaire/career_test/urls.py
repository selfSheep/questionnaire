from django.urls import path
from . import views


urlpatterns = [
    path('cartel_test/', views.cartel_test, name='cartel_test'),  # 卡塔尔测试题
]