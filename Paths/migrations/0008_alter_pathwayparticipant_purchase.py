# Generated by Django 3.2.9 on 2022-02-04 11:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Paths', '0007_pathwayparticipant_purchase'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pathwayparticipant',
            name='purchase',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='Paths.pathwaypurchase'),
        ),
    ]
