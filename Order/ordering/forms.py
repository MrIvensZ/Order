from django import forms
from django.forms import inlineformset_factory

from .models import Order, OrderItem


class OrderForm(forms.ModelForm):
    "Форма для добавления заказа"

    class Meta:
        model = Order
        fields = ('table_number',)


class OrderItemForm(forms.ModelForm):
    "Форма для добавления блюда в заказ"

    class Meta:
        model = OrderItem
        fields = ['dish', 'quantity']


class OrderStatusForm(forms.ModelForm):
    "Форма для изменения статуса заказа"

    class Meta:
        model = Order
        fields = ('status',)


OrderItemFormSet = inlineformset_factory(
    Order,
    OrderItem,
    form=OrderItemForm,
    extra=5,
    can_delete=False
)


class SearchForm(forms.Form):
    "Форма для поиска заказа"

    query = forms.CharField(
        label='Поиск',
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={'placeholder': 'Номер стола или статус'})
    )
