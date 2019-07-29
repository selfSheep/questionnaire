import os

from career_test.models import QuestionBank, Choice, MBTIAnwserType, HollandData, HollandDataItem



def input_questions():
    for i in range(1, 13):
        new_item = QuestionBank()
        new_item.bank_name = '卡特尔'
        new_item.question_num = i
        new_item.question_name = '这是第{}题的题目'.format(i)
        new_item.save()
    print('录入了测试题目')


def input_anwsers():
    questions = QuestionBank.objects.all().order_by('question_num')
    for question in questions:
        for i in ['a', 'b', 'c']:
            new_item = Choice()
            new_item.choice_type = i
            new_item.choice_content = '这是第{q_num}题的{c_type}选项'.format(c_type=i, q_num=question.question_num)
            new_item.question = question
            new_item.save()
    print('录入了测试答案')


def input_MBTI_questions():
    with open('预处理数据/MBTI题目与选项.txt', 'r', encoding='UTF-8') as f:
        question_object = None
        split_tag = 'B'
        question_num = 1
        for i, line in enumerate(f.readlines()):
            if i % 2 == 0:
                new_item = QuestionBank()
                new_item.bank_name = 'MBTI'
                new_item.question_num = question_num
                new_item.question_name = line.replace('\n', '')
                new_item.save()
                question_object = new_item
                question_num += 1
            else:
                choices = line.replace('\n', '').split(split_tag)
                a_item = Choice()
                a_item.choice_type = choices[0][0]
                a_item.choice_content = choices[0][1:]
                a_item.question = question_object
                a_item.save()
                b_item = Choice()
                b_item.choice_type = split_tag
                b_item.choice_content = choices[1]
                b_item.question = question_object
                b_item.save()
    print('录入成功')


def input_career_anchor_questions():
    with open('预处理数据/职业锚题目与选项.txt', 'r', encoding='UTF-8') as f:
        question_num = 1
        for line in f.readlines():
            new_item = QuestionBank()
            new_item.bank_name = 'career_anchor'
            new_item.question_num = question_num
            new_item.question_name = line.replace('\n', '')
            new_item.save()
            question_num += 1
            for i, value in enumerate(['从不', '偶尔', '有时', '经常', '频繁', '总是']):
                choice_item = Choice()
                choice_item.choice_type = '{}'.format(i + 1)
                choice_item.choice_content = value
                choice_item.question = new_item
                choice_item.save()
    print('录入成功')


def input_anwser_type():
    with open('预处理数据/MBTI答案类型.txt', 'r', encoding='UTF-8') as f:
        count_num = 1
        for index, line in enumerate(f.readlines()):
            questions = QuestionBank.objects.get(bank_name='MBTI', question_num=count_num)
            if index % 2 == 0:
                new_item = MBTIAnwserType()
                new_item.choice = questions.choice_set.get(choice_type='A')
                new_item.anwser_type = line.replace('\n', '')
                new_item.save()
                # print('{}{}'.format(questions.choice_set.get(choice_type='A'), line.replace('\n', '')))
            else:
                new_item = MBTIAnwserType()
                new_item.choice = questions.choice_set.get(choice_type='B')
                new_item.anwser_type = line.replace('\n', '')
                new_item.save()
                count_num += 1
                # print('{}{}'.format(questions.choice_set.get(choice_type='B'), line.replace('\n', '')))
    print('录入成功')



def input_holland_data():
    is_part = False
    is_title = False
    is_type = False
    # is_item = False
    item_type = None
    # part_num = None
    with open('预处理数据/霍兰德题目.txt', 'r', encoding='UTF-8') as f:
        holland_data = None
        item_num = 0
        for line in f.readlines():
            line_content = line.replace('\n', '')
            if line_content == 'part':
                is_part = True
                holland_data = HollandData()
                continue
            if is_part:
                holland_data.part_num = line_content
                is_part = False
                continue
            if line_content == 'title':
                is_title = True
                continue
            if is_title:
                holland_data.part_title = line_content
                is_title = False
                holland_data.save()
                continue
            if line_content == 'type':
                is_type = True
                continue
            if is_type:
                item_type = line_content
                is_type = False
                # is_item = True
                continue
            item_num += 1
            holland_data_item = HollandDataItem()
            holland_data_item.item_num = item_num
            holland_data_item.part_type = item_type
            holland_data_item.content = line_content
            holland_data_item.part = holland_data
            holland_data_item.save()
    print('录入成功')

