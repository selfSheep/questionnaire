from django.urls import path
from . import views


urlpatterns = [
    path('test_page/<str:test_type>', views.test_page, name='test_page'),  # 测试题页面
    path('handle_anwser/', views.handle_anwser, name='handle_anwser'),  # 处理MBTI以及职业锚的部分逻辑
    path('career_result/', views.career_result, name='career_result'),  # 处理职业锚的后续逻辑
    path('holland_test/', views.holland_test, name='holland_test'),  # 处理霍兰德的题
    path('new_holland_test/', views.new_holland_test, name='new_holland_test'),  # 处理新霍兰德的题
    path('holland_result/', views.holland_result, name='holland_result'),  # 处理霍兰德的结果页
    path('new_holland_result/', views.new_holland_result, name='new_holland_result'),  # 处理霍兰德的结果页
]