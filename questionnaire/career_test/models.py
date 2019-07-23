from django.db import models


class QuestionBank(models.Model):
    bank_name = models.CharField(max_length=20, verbose_name='题库名')
    question_num = models.IntegerField(verbose_name='题号')
    question_name = models.CharField(max_length=300, verbose_name='题目')
    
    @staticmethod
    def get_question(bank_name):
        questions = QuestionBank.objects.filter(bank_name=bank_name).order_by('question_num')
        question_and_choice = []
        for question in questions:
            choices = question.choice_set.all().order_by('choice_type')
            choice_detail = []
            for choice in choices:
                choice_detail.append((choice.choice_type, choice.choice_content))
            question_and_choice.append(((question.question_num, question.question_name), choice_detail))
        # question_and_choice = [((题号, 题目), [(选项号, 选项内容), (选项号, 选项内容)]), ((题号, 题目), [(选项号, 选项内容), (选项号, 选项内容)]), ...]
        return question_and_choice

    def __str__(self):
        return '<QuestionBank: {}题目{} 题库名{}>'.format(self.question_num, self.question_name, self.bank_name)

class Choice(models.Model):
    choice_type = models.CharField(max_length=5, verbose_name='选项类型')
    choice_content = models.CharField(max_length=100, verbose_name='选项内容')
    question = models.ForeignKey(QuestionBank, on_delete=models.CASCADE)

    def __str__(self):
        return '<id:{} Choice: {}{}>'.format(self.id, self.choice_type, self.choice_content)


class MBTIAnwserType(models.Model):
    ANWSER_TYPE_ITEMS = (
        ('E', 'E'),
        ('I', 'I'),
        ('S', 'S'),
        ('N', 'N'),
        ('T', 'T'),
        ('F', 'F'),
        ('J', 'J'),
        ('P', 'P'),
    )
    choice = models.ForeignKey(Choice, on_delete=models.CASCADE)
    anwser_type = models.CharField(max_length=5, choices=ANWSER_TYPE_ITEMS, verbose_name='答案类型')
