from django.urls import path
from . import views


urlpatterns = [
    path('test_page/<str:test_type>', views.test_page, name='test_page'),  # 测试题页面
    path('handle_anwser/', views.handle_anwser, name='handle_anwser'),
]