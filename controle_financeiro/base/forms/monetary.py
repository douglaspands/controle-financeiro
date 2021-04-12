import locale
import re
from decimal import Decimal
from typing import Optional

from django import forms
from django.conf import settings
from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _

locale.setlocale(locale.LC_MONETARY, settings.DEFAULT_LOCALE)

[THOUSAND_POINT, DECIMAL_POINT] = list(
    re.findall(r"[.,]", locale.currency(1234.56, grouping=True, symbol=False))
)

ECMA_ONKEYUP = (r'(e=>{const s=e.value.match(/[0-9]/g).join("");if(s){const[t,i]=(parseInt(s)/100).toFixed(2).split("."),u=t.split("").reverse().reduce((e,s,t)=>(t<=1?e.push(s):(t+1)%3==1?e.push(`${s}THOUSAND_POINT`):e.push(s),e),[]).reverse().join("");e.value=`${u}DECIMAL_POINT${i}`}else e.value=""})(this);'
                .replace("THOUSAND_POINT", THOUSAND_POINT)
                .replace("DECIMAL_POINT", DECIMAL_POINT))


class MonetaryField(forms.Field):
    def __init__(self, *args, **kwargs):
        kwargs["widget"] = forms.TextInput(attrs={"onkeyup": ECMA_ONKEYUP})
        super().__init__(*args, **kwargs)

    def prepare_value(self, value: Optional[Decimal]) -> str:
        if isinstance(value, Decimal):
            return locale.currency(value, grouping=True, symbol=False)
        else:
            return ""

    def to_python(self, value: Optional[str]) -> Optional[Decimal]:
        try:
            _value = Decimal(
                value.replace(THOUSAND_POINT, "").replace(DECIMAL_POINT, ".")
            )
        except BaseException:
            _value = None
        return _value

    def validate(self, value: Optional[Decimal]):
        super().validate(value)
        if not isinstance(value, Decimal):
            raise ValidationError(_("Invalid value"), code="invalid")
