from django.contrib import messages
from django.shortcuts import get_object_or_404, render, redirect
from django.core.exceptions import ValidationError

from .forms import OrderForm, OrderItemFormSet, OrderStatusForm, SearchForm
from .models import Order


def index(request):
    "Главная страница"

    template = 'ordering/index.html'
    context = {'orders': Order.objects.all()}
    return render(request, template, context)


def order_detail(request, order_pk):
    "Детали заказа"

    template = 'ordering/order_detail.html'
    order = get_object_or_404(Order, pk=order_pk)
    context = {'order': order}
    return render(request, template, context)


def create_order(request):
    "Создание заказа"

    template = 'ordering/create_order.html'
    if request.method == 'POST':
        form = OrderForm(request.POST)
        formset = OrderItemFormSet(request.POST)
        if form.is_valid() and formset.is_valid():
            try:
                order = form.save(commit=False)
                order.full_clean()
                order.save()
                instances = formset.save(commit=False)
                for instance in instances:
                    instance.order = order
                    instance.save()
                return redirect('index')
            except ValidationError as e:
                form.add_error('table_number', e.messages[0])
                messages.error(request, e.messages[0])
    else:
        form = OrderForm()
        formset = OrderItemFormSet()

    return render(request, template, {'form': form, 'formset': formset})


def delete_order(request, order_pk):
    "Удаление заказа"

    template = 'ordering/delete_order.html'
    instance = get_object_or_404(Order, pk=order_pk)
    form = OrderForm(instance=instance)
    context = {'form': form}
    if request.method == 'POST':
        instance.delete()
        return redirect('index')
    return render(request, template, context)


def order_change_status(request, order_pk):
    "Изменение статуса заказа"

    template = 'ordering/order_status.html'
    instance = get_object_or_404(Order, pk=order_pk)
    form = OrderStatusForm(request.POST or None,
                           instance=instance)
    context = {'form': form}
    if form.is_valid():
        order = form.save(commit=False)
        order.save()
        return redirect('ordering:order_detail', order_pk=order_pk)
    return render(request, template, context)


def total_price(request):
    "Расчёт выручки"

    template = 'ordering/total_price.html'
    orders = Order.objects.filter(status='paid')
    price_sum = 0
    for order in orders:
        price_sum += order.total_price
    context = {'price_sum': price_sum}
    return render(request, template, context)


def search(request):
    "Поиск по номеру стола или статусу заказа"

    template = 'ordering/search.html'
    form = SearchForm(data=request.GET if request.GET else None)
    results = Order.objects.all()
    query = ''

    status_mapping = {
        'оплачено': 'paid',
        'готово': 'ready',
        'в ожидании': 'waiting',
    }

    if form.is_valid():
        query = form.cleaned_data.get('query', '')
        if query:
            status_key = status_mapping.get(query)
            if status_key:
                results = results.filter(status=status_key)
            else:
                results = results.filter(table_number__icontains=query)

    context = {
        'form': form,
        'results': results,
        'query': query,
    }
    return render(request, template, context)
