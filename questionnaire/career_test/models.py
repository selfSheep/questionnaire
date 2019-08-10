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

    @staticmethod
    def get_holland_data(part_num):
        return HollandData.objects.get(part_num=part_num)

    def __str__(self):
        return '<id:{} HollandData: {}>'.format(self.id, self.part_title)


class HollandDataItem(models.Model):
    item_num = models.IntegerField(verbose_name='号码')
    part_type = models.CharField(max_length=2, verbose_name='类型')
    content = models.CharField(max_length=100, verbose_name='内容')
    part = models.ForeignKey(HollandData, on_delete=models.CASCADE)

    @staticmethod
    def get_holland_data_item(part, part_type):
        return HollandDataItem.objects.filter(part=part, part_type=part_type).order_by('item_num')

    def __str__(self):
        return '< id:{} item_num: {} part_type: {} >'.format(self.id, self.item_num, self.part_type)


class HollandTypeResult(models.Model):
    result_type = models.CharField(max_length=2, verbose_name='类型')
    result_title = models.CharField(max_length=30, verbose_name='标题')
    result_detail = models.CharField(max_length=300, verbose_name='内容')

    @staticmethod
    def get_type_result(result_type):
        return HollandTypeResult.objects.filter(result_type__in=result_type)


class NewHolland(models.Model):
    title_num = models.IntegerField(verbose_name='号码')
    title = models.CharField(max_length=50, verbose_name='标题')

    @classmethod
    def get_all_title(cls):
         return cls.objects.all()

    # @staticmethod
    # def get_new_holland_list(num_list):
    #     return NewHolland.objects.filter(title_num__in=num_list)

    class Meta():
        ordering = ['title_num']

    def __str__(self):
        return '< id:{} title_num: {} title: {} >'.format(self.id, self.title_num, self.title)


class NewHollandType(models.Model):
    TYPE_ITEMS = (
        ('R', 'R'),
        ('I', 'I'),
        ('A', 'A'),
        ('S', 'S'),
        ('E', 'E'),
        ('C', 'C'),
    )

    item_type = models.CharField(max_length=1, choices=TYPE_ITEMS, verbose_name='类型')
    item_name = models.CharField(max_length=5, verbose_name='类型名称')
    personality_tendency = models.CharField(max_length=200, verbose_name='人格倾向')
    typical_occupation = models.CharField(max_length=100, verbose_name='典型职业')

    class Meta():
        ordering = ['id']

    def __str__(self):
        return '< id:{} item_type: {} item_name: {} >'.format(self.id, self.item_type, self.item_name)


class NewHollandTitleNumType(models.Model):
    new_holland = models.ForeignKey(NewHolland, on_delete=models.CASCADE, verbose_name='题号信息')
    new_holland_type = models.ForeignKey(NewHollandType, on_delete=models.CASCADE, verbose_name='类型信息')
    score_condition = models.BooleanField(default=True, verbose_name='得分条件信息')

    @staticmethod
    def get_new_holland_title_num_type(num_list):
        context = dict()
        context['select_num'] = NewHollandTitleNumType.objects.filter(new_holland__title_num__in=num_list)  
        context['not_select_num'] = NewHollandTitleNumType.objects.exclude(new_holland__title_num__in=num_list)  
        return context
