# Generated by Django 2.2.3 on 2019-08-05 21:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('nba_stat_checker', '0010_team'),
    ]

    operations = [
        migrations.AddField(
            model_name='team',
            name='name',
            field=models.CharField(default='N/A', max_length=75),
        ),
        migrations.AddField(
            model_name='team',
            name='players',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='nba_stat_checker.Player'),
        ),
    ]
