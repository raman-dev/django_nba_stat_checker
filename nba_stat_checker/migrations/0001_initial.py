# Generated by Django 2.2.3 on 2019-07-17 23:13

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Player',
            fields=[
                ('player_id', models.IntegerField(default=0, primary_key=True, serialize=False)),
                ('player_first_name', models.CharField(max_length=100)),
                ('player_last_name', models.CharField(max_length=100)),
                ('player_full_name', models.CharField(max_length=250)),
                ('player_num_stats', models.IntegerField(default=0)),
                ('player_is_active', models.BooleanField(default=False)),
            ],
        ),
    ]
