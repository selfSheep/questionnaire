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
        # print(context)
        return render(request, 'career_test/mbti_result.html', context)
    else:
        # 统计前三个最高分的选项，若出现同分，则询问用户更加喜爱哪个题目
        # print(request.POST)
        # 统计个得分的个数及题号
        score_count = []  # [[score, count, [question_num, ...]], ...]
        for i in range(1, 7):
            score_count.append([i, 0, []])
        for choice, question_num in zip(anwser_choice, question_num):
            choice = int(choice)
            for score_data in score_count:
                if choice == score_data[0]:
                    score_data[1] += 1
                    score_data[2].append(question_num)
                    break
        print(score_count)
        # 选出高分三个，同分则返回相应处理页面
        pass
        # 题目数递增8
        # 计算1、9、17、25、33的总分
        pass
        # 计算2、10、18、26、34的总分
        pass
        # 计算3、11、19、27、35的总分
        pass
        # 计算4、12、20、28、36的总分
        pass
        # 计算5、13、21、29、37的总分
        pass
        # 计算6、14、22、30、38的总分
        pass
        # 计算7、15、23、31、39的总分
        pass
        # 计算8、16、24、32、40的总分
        pass
        # 将数据传到结果界面
        return render(request, 'career_test/career_result.html', context)
