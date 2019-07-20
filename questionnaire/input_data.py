from career_test.models import QuestionBank, Choice



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
