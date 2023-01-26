# Generated by Django 2.1.15 on 2023-01-27 01:13

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='AlarmModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('time', models.DateTimeField(blank=True, null=True)),
                ('title', models.TextField(max_length=200)),
                ('content', models.TextField()),
                ('color', models.TextField()),
                ('icon_class', models.TextField()),
                ('more_info', models.BooleanField(default=False)),
                ('herf', models.TextField()),
                ('now', models.BooleanField(default=True)),
                ('user_id', models.ForeignKey(db_column='user_id', on_delete=django.db.models.deletion.CASCADE, related_name='user_alarm', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
