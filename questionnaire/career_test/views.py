from django.db.models import Count
from django.http import JsonResponse
from django.shortcuts import render

from .models import (
    QuestionBank, Choice, MBTIAnwserType,
    MBTIResult, MBTIResultDetail, CareerResultType,
    HollandData, HollandDataItem, HollandTypeResult,
    NewHolland, NewHollandType, NewHollandTitleNumType
)


def test_page(request, test_type):
    context = dict()
    # get_question()根据题库名选出问题以及相应选项数据[
    #                                               ((题号, 题目), [(选项号, 选项内容), (选项号, 选项内容)]),
    #                                               ((题号, 题目), [(选项号, 选项内容), (选项号, 选项内容)]),
    #                                               ...]
    context['question_and_choice'] = QuestionBank.get_question(bank_name=test_type)
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
    # 分别处理MBTI以及职业锚
    if bank_name == 'MBTI':
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
        # 将选项类型转成对应分数
        anwser_choice = [int(x) for x in anwser_choice]
        for i in range(1, 7):
            score_count.append([i, 0, []])
        for choice, question_num in zip(anwser_choice, question_num):
            for score_data in score_count:
                if choice == score_data[0]:
                    score_data[1] += 1
                    score_data[2].append(question_num)
                    break
        # print(score_count)
        # 选出高分三个，同分则返回相应处理页面
        top_3 = 3
        for score_data in score_count[::-1]:
            if score_data[1] > top_3:
                # print(anwser_choice)
                # 根据题库名以及题号数选出题目数据
                # context['questions'] = QuestionBank.get_question(bank_name=bank_name, questions_num=score_data[2])
                questions = QuestionBank.get_question(bank_name=bank_name, questions_num=score_data[2])
                question_num_and_name = []
                for question in questions:
                    # question.question_num
                    # 每隔20个字就插入一个<br>的位置
                    question_name = question.question_name
                    len_question_name = len(question_name)
                    # [0:10][10:20][20:30][30:40]
                    for i in range(0, len_question_name // 20):
                        question_name = question_name[:20 + i * 20 + i * 4] + '<br>' + question_name[20 + i * 20 + i * 4:]
                    question_num_and_name.append((question.question_num, question_name))
                context['anwser_choice'] = anwser_choice
                context['test_type'] = bank_name
                context['question_num_and_name'] = question_num_and_name
                context['top_3'] = top_3
                return render(request, 'career_test/career_choice.html', context)
            elif score_data[1] == top_3:
                # 实现选项 +4 操作
                for i in score_data[2]:
                    anwser_choice[i - 1] += 4
                break
            elif score_data[1] > 0 and score_data[1] < top_3:
                # 实现选项 +4 操作
                for i in score_data[2]:
                    anwser_choice[i - 1] += 4
                top_3 -= score_data[1]

        get_max_list_and_career_result(anwser_choice, context)
        return render(request, 'career_test/career_result.html', context)

# 职业锚后半部分处理结果
def career_result(request):
    question_num = eval(request.POST.get('question_num', ''))
    question_num = [int(x) for x in question_num]
    anwser_choice = eval(request.POST.get('anwser_choice', ''))
    anwser_choice = [int(x) for x in anwser_choice]
    # anwser_choice用来存放各题分数
    # 执行相关题目分数加4
    for add_score in question_num:
        anwser_choice[add_score - 1] += 4

    context = dict()

    get_max_list_and_career_result(anwser_choice, context)
    return render(request, 'career_test/career_result.html', context)


def get_max_list_and_career_result(anwser_choice, context):
    # result_type_list用来存放各类型的分数总和
    result_type_list = [['TF', 0], ['GM', 0], ['AU', 0], ['SE', 0], ['EC', 0], ['SV', 0], ['CH', 0], ['LS', 0]]
    # 题目数递增8
    for q_num in range(0, 8):
        for add_num in range(0, 5):
            result_type_list[q_num][1] += anwser_choice[q_num + 8 * add_num]
    # print(result_type_list)
    # 选出最大值的列表
    max_list = [-1, []]
    for result_type in result_type_list:
        if max_list[0] < result_type[1]:
            max_list = [result_type[1], [result_type[0]]]
        elif max_list[0] == result_type[1]:
            max_list[1].append(result_type[0])
    # print(max_list)
    career_result = CareerResultType.get_career_result(type_names=max_list[1])
    # print(career_result)
    context['max_list'] = max_list
    context['career_result'] = career_result


def holland_test(request):
    context = dict()
    part_type = ['R', 'I', 'A', 'S', 'E', 'C']
    part_2_data = HollandData.get_holland_data(2)
    part_3_data = HollandData.get_holland_data(3)
    part_4_data = HollandData.get_holland_data(4)
    part_5_data = HollandData.get_holland_data(5)

    # [(type_str, HollandDataItem), ...]
    part_2_data_list = []
    for type_item in part_type:
        part_2_data_list.append((type_item, HollandDataItem.get_holland_data_item(part=part_2_data, part_type=type_item)))

    context['part_2_data'] = part_2_data
    context['part_2_data_list'] = part_2_data_list

    part_3_data_list = []
    for type_item in part_type:
        part_3_data_list.append((type_item, HollandDataItem.get_holland_data_item(part=part_3_data, part_type=type_item)))

    context['part_3_data'] = part_3_data
    context['part_3_data_list'] = part_3_data_list

    part_4_data_list = []
    for type_item in part_type:
        part_4_data_list.append((type_item, HollandDataItem.get_holland_data_item(part=part_4_data, part_type=type_item)))

    context['part_4_data'] = part_4_data
    context['part_4_data_list'] = part_4_data_list

    part_5_data_list = []
    for type_item in part_type:
        part_5_data_list.append((type_item, HollandDataItem.get_holland_data_item(part=part_5_data, part_type=type_item)))

    context['part_type'] = part_type
    context['part_5_data'] = part_5_data
    context['part_5_data_list'] = part_5_data_list

    return render(request, 'career_test/holland_test.html', context)


def holland_result(request):
    part_type = ['R', 'I', 'A', 'S', 'E', 'C']
    user_input_1 = eval(request.POST.get('user_input_1', ''))
    user_input_6 = eval(request.POST.get('user_input_6', ''))
    index_list = eval(request.POST.get('index_array', ''))
    result_type = []
    for i in index_list:
        result_type.append(part_type[i])
    result_content = HollandTypeResult.get_type_result(result_type=result_type)
    context = dict()
    context['user_input_1'] = user_input_1
    context['user_input_6'] = user_input_6
    context['result_content'] = result_content
    return render(request, 'career_test/holland_result.html', context)


def new_holland_test(request):
    context = dict()
    context['title_info_result'] = NewHolland.get_all_title()
    context['question_len'] = context['title_info_result'].count()
    return render(request, 'career_test/new_holland_test.html', context)


def new_holland_result(request):
    # 获取选中的题号
    tag_choice = eval(request.POST.get('tag_choice', ''))
    tag_choice = [int(x) for x in tag_choice]
    # choice_info_dic = NewHollandTitleNumType.get_new_holland_title_num_type(NewHolland.get_new_holland_list(tag_choice))
    choice_info_dic = NewHollandTitleNumType.get_new_holland_title_num_type(tag_choice)
    print(choice_info_dic)
    context = dict()
    return render(request, 'career_test/new_holland_result.html', context)
