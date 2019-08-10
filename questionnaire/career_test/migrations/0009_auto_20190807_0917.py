# Generated by Django 2.1.4 on 2019-08-07 01:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('career_test', '0008_auto_20190729_1219'),
    ]

    operations = [
        migrations.CreateModel(
            name='NewHolland',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title_num', models.IntegerField(verbose_name='号码')),
                ('title', models.CharField(max_length=50, verbose_name='标题')),
            ],
        ),
        migrations.CreateModel(
            name='NewHollandTitleNumType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('score_condition', models.BooleanField(default=True, verbose_name='得分条件信息')),
                ('new_holland', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='career_test.NewHolland', verbose_name='题号信息')),
            ],
        ),
        migrations.CreateModel(
            name='NewHollandType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('item_type', models.CharField(choices=[('R', 'R'), ('I', 'I'), ('A', 'A'), ('S', 'S'), ('E', 'E'), ('C', 'C')], max_length=1, verbose_name='类型')),
                ('item_name', models.CharField(max_length=5, verbose_name='类型名称')),
                ('personality_tendency', models.CharField(max_length=200, verbose_name='人格倾向')),
                ('typical_occupation', models.CharField(max_length=100, verbose_name='典型职业')),
            ],
        ),
        migrations.AlterField(
            model_name='mbtianwsertype',
            name='choice',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='career_test.Choice'),
        ),
        migrations.AddField(
            model_name='newhollandtitlenumtype',
            name='new_holland_type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='career_test.NewHollandType', verbose_name='类型信息'),
        ),
    ]