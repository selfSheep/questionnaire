from django.db.models import Count
from django.http import JsonResponse
from django.shortcuts import render

from .models import QuestionBank, Choice, MBTIAnwserType


def test_page(request, test_type):
    context = dict()
    context['question_and_choice'] = QuestionBank.get_question(test_type)
    # 问题个数
    context['question_len'] = len(context['question_and_choice'])
    context['test_type'] = test_type
    # print(context)
    return render(request, 'career_test/test_page.html', context)


# def handle_anwser(request):
#     context = dict()
#     context['datas'] = request.POST.get('datas', '')
#     context['test_type'] = request.POST.get('test_type', '')
#     print(context)
#     # return JsonResponse(context)
#     return render(request, 'career_test/test_result.html', context)


def handle_anwser(request):
    context = dict()
    # datas, test_type
    bank_name = request.POST.get('test_type', '')
    # datas = request.POST.get('datas', '')
    question_num = eval(request.POST.get('question_num', ''))
    # 字符串列表转数字列表
    question_num = [int(x) for x in question_num]
    anwser_choice = eval(request.POST.get('anwser_choice', ''))
    if bank_name == 'MBTI':
        # print(request.POST)
        # group_by_type = QuestionBank.objects.filter(bank_name=bank_name, question_num__in=question_num).choice_set.filter(choice_type__in=anwser_choice).mbtianwsertype_set.values('anwser_type').annotate(anwser_type_num=Count('anwser_type'))
        question_target= QuestionBank.objects.filter(bank_name=bank_name, question_num__in=question_num)
        choice_target = Choice.objects.filter(question__in=question_target, choice_type__in=anwser_choice)
        group_by_type = MBTIAnwserType.objects.filter(choice__in=choice_target).values('anwser_type').annotate(anwser_type_num=Count('anwser_type'))
        print(group_by_type)
        # result_str = ''
        # result_str += 'I' if group_by_type['E'] <= group_by_type['I'] else 'E'
        # result_str += 'N' if group_by_type['S'] <= group_by_type['N'] else 'S'
        # result_str += 'F' if group_by_type['T'] <= group_by_type['F'] else 'T'
        # result_str += 'P' if group_by_type['J'] <= group_by_type['P'] else 'J'
        # final_results = MBTIResult.objects.get(result_type=result_str).MBTIResultDetail_set.all().order_by('result_num')
        # context['result_str'] = result_str
        # context['final_results'] = final_results
    else:
        pass
    return render(request, 'career_test/test_result.html', context)
