from cascade_filter.django.widget import CascadeFilterWidget
from cascade_filter.django.validator import CascadeFilterValidator
from cascade_filter.meta import Table

from typing import Type

from django.forms.fields import JSONField


class CascadeFilterField(JSONField):
	"""
	Cascade filter field.
	Allows to represent and edit cascade filter.

	Examples:
		>>> class MyForm(forms.Form):
		>>> 	some_field = CascadeFilterField(table_meta=YourTableMeta)
	"""
	widget: Type[CascadeFilterWidget] = CascadeFilterWidget
	FilterValidator: Type[CascadeFilterValidator] = CascadeFilterValidator

	table_meta: Type[Table]

	def __init__(self, encoder=None, decoder=None, **kwargs):
		table_meta = kwargs.pop(self.widget.ATTR_KEY_TABLE_META)
		assert issubclass(table_meta, Table), f"Table meta must be of {Table.__name__} subclass"
		self.table_meta = table_meta
		kwargs["validators"] = [self.FilterValidator(self.table_meta), *kwargs.get("validators", [])]
		super().__init__(encoder, decoder, **kwargs)

	def widget_attrs(self, widget):
		attrs = super().widget_attrs(widget)
		attrs[self.widget.ATTR_KEY_TABLE_META] = self.table_meta
		return attrs
