# Generated by Django 3.2.9 on 2022-02-02 15:02

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('Paths', '0003_auto_20220202_1022'),
    ]

    operations = [
        migrations.CreateModel(
            name='PathwayPurchase',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('purchase_type', models.CharField(choices=[('author_free', 'author_invite'), ('author_paid', 'author_paid_invite'), ('organisation_free', 'organisation_invite'), ('organisation_paid', 'organisation_invite')], max_length=100)),
                ('purchase_owner', models.PositiveIntegerField()),
                ('status', models.CharField(choices=[('active', 'active'), ('pending', 'pending'), ('spent', 'spent')], max_length=100)),
                ('pathway', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='Paths.pathway')),
                ('spent_by_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='user_spends', to=settings.AUTH_USER_MODEL)),
                ('spent_on_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='pathway_purchases', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.DeleteModel(
            name='PathwayCompletitionRecord',
        ),
    ]
