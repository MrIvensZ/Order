from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


def validate_table_available(table_number):
    from .models import Order

    if Order.objects.filter(table_number=table_number).exists():
        raise ValidationError(
            _('Стол %(table_number)s уже занят'),
            params={'table_number': table_number},
        )
