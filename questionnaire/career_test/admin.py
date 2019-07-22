from django.contrib import admin
from .models import QuestionBank, Choice, MBTIAnwserType


@admin.register(QuestionBank)
class QuestionBankAdmin(admin.ModelAdmin):
    list_display = ('id', 'question_num', 'bank_name', 'question_name')


@admin.register(Choice)
class ChoiceAdmin(admin.ModelAdmin):
    list_display = ('id', 'choice_type', 'choice_content', 'question')


@admin.register(MBTIAnwserType)
class MBTIAnwserTypeAdmin(admin.ModelAdmin):
    list_display = ('id', 'choice', 'anwser_type')
