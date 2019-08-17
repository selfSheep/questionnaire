import itertools  # 排列组合的库

from django.db.models import Count
from django.http import JsonResponse
from django.shortcuts import render

from .models import (
    QuestionBank, Choice, MBTIAnwserType,
    MBTIResult, MBTIResultDetail, CareerResultType,
    HollandData, HollandDataItem, HollandTypeResult,
    NewHolland, NewHollandType, NewHollandTitleNumType,
    NewHollandResult
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
                    for i in range(0, len_question_name // 12):
                        question_name = question_name[:12 + i * 12 + i * 5] + ' <br>' + question_name[12 + i * 12 + i * 5:]
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
    title_info_result = []
    for title_info in context['title_info_result']:
        title_num = title_info.title_num
        title_info_title = title_info.title
        len_title_info_title = len(title_info_title)
        for i in range(0, len_title_info_title // 12):
            title_info_title = title_info_title[:12 + i * 12 + i * 4] + '<br>' + title_info_title[12 + i * 12 + i * 4:]
        title_info_result.append({'title_num': title_num, 'title': title_info_title})
    context['title_info_result'] = title_info_result
    return render(request, 'career_test/new_holland_test.html', context)


def new_holland_result(request):
    context = dict()
    # 获取选中的题号
    tag_choice = eval(request.POST.get('tag_choice', ''))
    tag_choice = [int(x) for x in tag_choice]
    # choice_info_dic = NewHollandTitleNumType.get_new_holland_title_num_type(NewHolland.get_new_holland_list(tag_choice))
    choice_info_dic = NewHollandTitleNumType.get_new_holland_title_num_type(tag_choice)
    # print(choice_info_dic['select_num'])
    # 初始化记录分数的字典
    # {('R', '现实型'): 0, ('I', '研究型'): 0, ..}
    result_dic = dict()
    for type_content in NewHollandType.objects.all():
        result_dic[(type_content.item_type, type_content.item_name)] = 0
    # print(result_dic)
    # 把相应类型的题合计总分
    for select_num_item in choice_info_dic['select_num']:
        if select_num_item.score_condition:
            result_dic[(select_num_item.new_holland_type.item_type, select_num_item.new_holland_type.item_name)] += 1
    for not_select_num_item in choice_info_dic['not_select_num']:
        if not not_select_num_item.score_condition:
            result_dic[(not_select_num_item.new_holland_type.item_type, not_select_num_item.new_holland_type.item_name)] += 1
    # print(result_dic)
    # [[name(type), ...], [score, ...]]
    context['result_data'] = [[], []]
    for key, value in result_dic.items():
        context['result_data'][0].append('{}（{}）'.format(key[1], key[0]))
        context['result_data'][1].append(value)
    context['result_dic'] = zip(context['result_data'][0], context['result_data'][1])
    # 第一种是筛选方式
    # score_dic = {new_ranking: [score, [key_1, key_2, ...]], ...}
    # score_dic = dict()
    # 记录各个分数的排名
    # new_ranking = 0
    # 初始化分数排名字典
    # score_dic[new_ranking] = [[key], score]
    # for key, value in result_dic.items():
    #     if not score_dic:
    #         score_dic[new_ranking] = [[key], value]
    #         new_ranking += 1
    #         continue
    #     for i in range(0, new_ranking):
    #         if value > score_dic[i][1]:
    #             for ranking in range(new_ranking, i, -1):
    #                 score_dic[ranking] = score_dic[ranking - 1]
    #             score_dic[i] = [[key], value]
    #             new_ranking += 1
    #             break
    #         elif value == score_dic[i][1]:
    #             # print(score_dic[i][0])
    #             score_dic[i][0].append(key)
    #             # print(score_dic[i][0])
    #             break
    #         elif value < score_dic[i][1]:
    #             # 小于最后一个最小值
    #             if i == new_ranking - 1:
    #                 score_dic[new_ranking] = [[key], value]
    #                 new_ranking += 1
    #                 break
    # print(score_dic)
    # 第二种是筛选方式
    # [[value, len, [key, ...]], ...]
    result_score_list = [[-1, 0, []], [-1, 0, []], [-1, 0, []]]
    for key, value in result_dic.items():
        for i, result_list in enumerate(result_score_list):
            if value > result_list[0]:
                # print(result_score_list)
                result_score_list = result_score_list[: i] + [[value, 1, [key,]]] + result_score_list[i: -1]
                break
            elif value == result_list[0]:
                result_list[1] += 1
                result_list[2].append(key)
                break
            elif value < result_list[0]:
                continue
    # print(result_score_list)
    # 筛选出最高分的信息
    result_score_content = []
    for result_score in result_score_list[0][2]:
        result_score_content.append(result_score[0])
    context['top_score_list'] = NewHollandType.objects.filter(item_type__in=result_score_content)
    # 筛选类型
    end_tag = 3
    index_tag = 1
    for result_score in result_score_list:
        if result_score[1] >= end_tag:
            break
        else:
            end_tag -= result_score[1]
            index_tag += 1
    # print(result_score_list[:index_tag])

    result_str_list = []
    end_tag = 3
    for result_info in result_score_list[:index_tag]:
        result_str = []
        for item in result_info[2]:
            result_str.append(item[0])
        result_str_list.append(result_str)
        if result_info[1] >= end_tag:
            break
        else:
            end_tag -= result_info[1]
    # print(result_str_list)
    result_list = []
    if len(result_str_list) == 3:
        for str_item in result_str_list[2]:
            result_list.append(result_str_list[0][0] + result_str_list[1][0] + str_item)
    elif len(result_str_list) == 2:
        if len(result_str_list[0]) == 2:
            for str_item in result_str_list[1]:
                result_list.append(result_str_list[0][0] + result_str_list[0][1] + str_item)
                result_list.append(result_str_list[0][1] + result_str_list[0][0] + str_item)
        else:
            for str_item in itertools.permutations(result_str_list[1], 2):
                result_list.append(result_str_list[0][0] + str_item[0] + str_item[1])
    else:
        for str_item in itertools.permutations(result_str_list[0], 3):
            result_list.append(str_item[0] + str_item[1] + str_item[2])
    # print(result_list)
    context['result_list'] = result_list
    context['result_list_content'] = NewHollandResult.objects.filter(result_type__in=result_list)
    # 没有相关记录
    if context['result_list_content'].count() == 0:
        context['result_error'] = '该代码无详细说明，请参照以下得分较高的人格类型所提供的典型职业'
        context['result_list_content'] = NewHollandResult.objects.filter(result_type__startswith=result_score_content[0])
    # context['test_SQL'] = NewHollandResult.objects.filter(result_type__icontains='A')
    return render(request, 'career_test/new_holland_result.html', context)

