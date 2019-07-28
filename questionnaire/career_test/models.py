from django.db import models


class QuestionBank(models.Model):
    bank_name = models.CharField(max_length=20, verbose_name='题库名')
    question_num = models.IntegerField(verbose_name='题号')
    question_name = models.CharField(max_length=300, verbose_name='题目')
    
    @staticmethod
    def get_question(bank_name, questions_num=None):
        if not questions_num:
            questions = QuestionBank.objects.filter(bank_name=bank_name).order_by('question_num')
        else:
            questions = QuestionBank.objects.filter(bank_name=bank_name, question_num__in=questions_num).order_by('question_num')
            return questions
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


class MBTIResult(models.Model):
    RESULT_TYPE_ITEMS = (
        ('ISTJ', 'ISTJ'),
        ('ISFJ', 'ISFJ'),
        ('INFJ', 'INFJ'),
        ('INTJ', 'INTJ'),
        ('ISTP', 'ISTP'),
        ('ISFP', 'ISFP'),
        ('INFP', 'INFP'),
        ('INTP', 'INTP'),
        ('ESTP', 'ESTP'),
        ('ESFP', 'ESFP'),
        ('ENFP', 'ENFP'),
        ('ENTP', 'ENTP'),
        ('ESTJ', 'ESTJ'),
        ('ESFJ', 'ESFJ'),
        ('ENFJ', 'ENFJ'),
        ('ENTJ', 'ENTJ'),
    )
    result_type = models.CharField(max_length=5, choices=RESULT_TYPE_ITEMS, verbose_name='报告类型')

    def __str__(self):
        return '<id:{} result_type: {}>'.format(self.id, self.result_type)

class MBTIResultDetail(models.Model):
    result_type = models.ForeignKey(MBTIResult, on_delete=models.CASCADE)
    result_num = models.IntegerField(verbose_name='结果号')
    result_content = models.CharField(max_length=100, verbose_name='结果内容')


class CareerResultType(models.Model):
    type_name = models.CharField(max_length=2, verbose_name='结果类型')
    type_title = models.CharField(max_length=100, verbose_name='结果标题')
    type_content = models.CharField(max_length=500, verbose_name='结果内容')

    @staticmethod
    def get_career_result(type_names):
        return CareerResultType.objects.filter(type_name__in=type_names)


class HollandData(models.Model):
    part_num = models.IntegerField(verbose_name='号码')
    part_title = models.CharField(max_length=30, verbose_name='标题')

    def __str__(self):
        return '<id:{} HollandData: {}>'.format(self.id, self.part_title)


class HollandDataItem(models.Model):
    item_num = models.IntegerField(verbose_name='号码')
    part_type = models.CharField(max_length=2, verbose_name='类型')
    content = models.CharField(max_length=100, verbose_name='内容')
    part = models.ForeignKey(HollandData, on_delete=models.CASCADE)
