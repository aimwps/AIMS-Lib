# Generated by Django 3.2.6 on 2021-08-26 16:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Development', '0004_auto_20210823_1533'),
    ]

    operations = [
        migrations.AddField(
            model_name='aim',
            name='in_order',
            field=models.PositiveIntegerField(default=1),
            preserve_default=False,
        ),
        migrations.AddConstraint(
            model_name='aim',
            constraint=models.UniqueConstraint(fields=('user', 'in_order'), name='unique_aims_orderby'),
        ),
    ]