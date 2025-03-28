# Generated by Django 4.2 on 2025-03-25 15:39

from django.db import migrations, models
import django.db.models.deletion
import ordering.validators


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Dish',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='Название блюда')),
                ('price', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Цена')),
            ],
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('table_number', models.IntegerField(validators=[ordering.validators.validate_table_available], verbose_name='Номер стола')),
                ('status', models.CharField(choices=[('waiting', 'В ожидании'), ('ready', 'Готово'), ('paid', 'Оплачено')], default='waiting', max_length=20, verbose_name='Статус')),
            ],
        ),
        migrations.CreateModel(
            name='OrderItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.PositiveIntegerField(default=1, verbose_name='Количество')),
                ('dish', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ordering.dish', verbose_name='Блюдо')),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ordering.order', verbose_name='Заказ')),
            ],
        ),
        migrations.AddField(
            model_name='order',
            name='dishes',
            field=models.ManyToManyField(through='ordering.OrderItem', to='ordering.dish', verbose_name='Блюда'),
        ),
    ]
