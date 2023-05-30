# Generated by Django 4.1.7 on 2023-05-29 16:54

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='user',
            old_name='thumbnail',
            new_name='profile_piq',
        ),
        migrations.AlterField(
            model_name='administrator',
            name='user_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='administrators', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='airlinecompany',
            name='country_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='airline_companies', to='base.country'),
        ),
        migrations.AlterField(
            model_name='airlinecompany',
            name='user_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='airline_companies', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='customer',
            name='user_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='customers', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='flight',
            name='airline_company_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='flights', to='base.airlinecompany'),
        ),
        migrations.AlterField(
            model_name='ticket',
            name='customer_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tickets', to='base.customer'),
        ),
        migrations.AlterField(
            model_name='ticket',
            name='flight_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tickets', to='base.flight'),
        ),
    ]
