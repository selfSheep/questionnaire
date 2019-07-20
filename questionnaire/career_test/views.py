from django.shortcuts import render

from .models import QuestionBank, Choice


def cartel_test(request):
    context = dict()
    context['question_and_choice'] = QuestionBank.get_question('卡特尔')
    # 问题个数
    context['question_len'] = len(context['question_and_choice'])
    return render(request, 'career_test/cartel_test.html', context)

