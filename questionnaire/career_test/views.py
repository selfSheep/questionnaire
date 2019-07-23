from django.db.models import Count
from django.http import JsonResponse
from django.shortcuts import render

from .models import QuestionBank, Choice, MBTIAnwserType, MBTIResult, MBTIResultDetail


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
        # question_target = QuestionBank.objects.filter(bank_name=bank_name, question_num__in=question_num)
        # choice_target = Choice.objects.filter(question__in=question_target, choice_type__in=anwser_choice)
        anwser_targets = []
        for a_choice, q_num in zip(anwser_choice, question_num):
            anwser_targets.append(Choice.objects.get(choice_type=a_choice, question__question_num=q_num))
        group_by_type = MBTIAnwserType.objects.values('anwser_type').annotate(anwser_type_num=Count('anwser_type')).filter(choice__in=anwser_targets)
        # print(group_by_type)
        # print(group_by_type.get(anwser_type='E')['anwser_type_num'])
        result_str = ''
        result_str += 'I' if group_by_type.get(anwser_type='E')['anwser_type_num'] <= group_by_type.get(anwser_type='I')['anwser_type_num'] else 'E'
        result_str += 'N' if group_by_type.get(anwser_type='S')['anwser_type_num'] <= group_by_type.get(anwser_type='N')['anwser_type_num'] else 'S'
        result_str += 'F' if group_by_type.get(anwser_type='T')['anwser_type_num'] <= group_by_type.get(anwser_type='F')['anwser_type_num'] else 'T'
        result_str += 'P' if group_by_type.get(anwser_type='J')['anwser_type_num'] <= group_by_type.get(anwser_type='P')['anwser_type_num'] else 'J'
        final_results = MBTIResult.objects.get(result_type=result_str).mbtiresultdetail_set.all().order_by('result_num')
        context['result_str'] = result_str
        context['final_results'] = final_results
        print(context)
    else:
        pass
    return render(request, 'career_test/test_result.html', context)
