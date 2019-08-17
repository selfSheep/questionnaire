from django.contrib import admin
from .models import (
    QuestionBank, Choice, MBTIAnwserType,
    MBTIResult, MBTIResultDetail, CareerResultType,
    HollandData, HollandDataItem, HollandTypeResult,
    NewHolland, NewHollandType, NewHollandTitleNumType,
    NewHollandResult
)

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


@admin.register(HollandData)
class HollandDataAdmin(admin.ModelAdmin):
    list_display = ('id', 'part_num', 'part_title')


@admin.register(HollandDataItem)
class HollandDataItemAdmin(admin.ModelAdmin):
    list_display = ('id', 'item_num', 'part_type', 'content', 'part')


@admin.register(HollandTypeResult)
class HollandTypeResultAdmin(admin.ModelAdmin):
    list_display = ('id', 'result_type', 'result_title', 'result_detail')


@admin.register(NewHolland)
class NewHollandAdmin(admin.ModelAdmin):
    list_display = ('id', 'title_num', 'title')


@admin.register(NewHollandType)
class NewHollandTypeAdmin(admin.ModelAdmin):
    list_display = ('id', 'item_type', 'item_name', 'personality_tendency', 'typical_occupation')


@admin.register(NewHollandTitleNumType)
class NewHollandTitleNumTypeAdmin(admin.ModelAdmin):
    list_display = ('id', 'new_holland', 'new_holland_type', 'score_condition')


@admin.register(NewHollandResult)
class NewHollandResultAdmin(admin.ModelAdmin):
    list_display = ('id', 'result_type', 'result_content')
