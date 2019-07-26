from django.contrib import admin
from .models import QuestionBank, Choice, MBTIAnwserType, MBTIResult, MBTIResultDetail, CareerResultType


@admin.register(QuestionBank)
class QuestionBankAdmin(admin.ModelAdmin):
    list_display = ('id', 'question_num', 'bank_name', 'question_name')


@admin.register(Choice)
class ChoiceAdmin(admin.ModelAdmin):
    list_display = ('id', 'choice_type', 'choice_content', 'question')


@admin.register(MBTIAnwserType)
class MBTIAnwserTypeAdmin(admin.ModelAdmin):
    list_display = ('id', 'choice', 'anwser_type')


@admin.register(MBTIResult)
class MBTIResultAdmin(admin.ModelAdmin):
    list_display = ('id', 'result_type')


@admin.register(MBTIResultDetail)
class MBTIResultDetailAdmin(admin.ModelAdmin):
    list_display = ('id', 'result_type', 'result_num', 'result_content')


@admin.register(CareerResultType)
class CareerResultTypeAdmin(admin.ModelAdmin):
    list_display = ('id', 'type_name', 'type_title', 'type_content')
