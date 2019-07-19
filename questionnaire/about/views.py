from django.shortcuts import render


# 关于我们页面
def about(request):
    context = dict()
    return render(request, 'about/about.html', context)
