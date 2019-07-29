from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('', include('home.urls')),  # 引入主页urls
    path('PaperSheep/admin/', admin.site.urls),
    path('about/', include('about.urls')),  # 引入相关urls
    path('career_test/', include('career_test.urls')),  # 引入职规测试urls
]
