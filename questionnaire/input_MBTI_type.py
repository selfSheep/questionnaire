from career_test.models import QuestionBank, Choice, XXX


def input_anwser_type():
    for i in target:
        xxx = XXX()
        xxx.anwser = i.choice_set.get(choice_type='A')
        xxx.anwser_type = f.line()
        xxx.save
        xxx = XXX()
        xxx.anwser = i.choice_set.get(choice_type='B')
        xxx.anwser_type = f.line()
        xxx.save



