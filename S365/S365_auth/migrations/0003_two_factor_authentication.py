# Generated by Django 3.2.14 on 2022-07-17 14:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('S365_auth', '0002_auto_20220717_1403'),
    ]

    operations = [
        migrations.CreateModel(
            name='two_factor_authentication',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('otp', models.CharField(max_length=6)),
                ('time', models.DateTimeField()),
                ('account', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='S365_auth.client_accounts')),
                ('client', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='S365_auth.clients')),
            ],
            options={
                'verbose_name': 'Two Factor Authentication',
                'verbose_name_plural': 'Two Factor Authentication',
            },
        ),
    ]
