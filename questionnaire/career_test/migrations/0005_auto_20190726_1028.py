# Generated by Django 2.1.4 on 2019-07-26 02:28

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('career_test', '0004_auto_20190726_1022'),
    ]

    operations = [
        migrations.CreateModel(
            name='CareerResultType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type_name', models.CharField(max_length=2, verbose_name='结果类型')),
                ('type_title', models.CharField(max_length=100, verbose_name='结果标题')),
                ('type_content', models.CharField(max_length=500, verbose_name='结果内容')),
            ],
        ),
        migrations.DeleteModel(
            name='CareerType',
        ),
        migrations.AlterField(
            model_name='mbtianwsertype',
            name='choice',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='career_test.Choice'),
        ),
    ]
