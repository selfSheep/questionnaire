from django.shortcuts import render


# 主页
def home(request):
    context = dict()
    return render(request, 'home/home.html', context)
