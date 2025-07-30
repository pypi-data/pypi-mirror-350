from cascade_filter.meta import Table

from typing import Type, Final
from json import loads

from django.forms.widgets import Widget


class CascadeFilterWidget(Widget):
	"""
	Cascade filter editor widget.

	Notes:
		Use only in conjunction with the JSON field and only if reliability is not needed.

	Examples:
		>>> class SomeForm(forms.Form):
		>>> 	some_field = forms.JSONField(
		>>> 		widget=CascadeFilterWidget(
		>>> 			attrs={'table_meta': YourTableMeta}
		>>> 		)
		>>> 	)
	"""
	ATTR_KEY_TABLE_META: Final[str] = "table_meta"
	template_name = "cascade_filter/widget.html"

	class Media:
		css = {
			"all": ("cascade_filter/cascade-filter.css", ),
		}

	def format_value(self, value):
		if isinstance(value, str) and value.startswith("\""):
			return str(loads(value))		# allows to use with django-annoying JSON field

		return value

	def extract_table_meta(self) -> Type[Table]:
		table_meta = self.attrs.get(self.ATTR_KEY_TABLE_META)

		if not isinstance(table_meta, type):
			raise TypeError("The table meta must be class")

		if not issubclass(table_meta, Table):
			raise TypeError(f"Table meta must be subclass of {Table.__name__}")

		return table_meta

	def build_attrs(self, base_attrs, extra_attrs=None):
		attrs = super().build_attrs(base_attrs, extra_attrs)

		if self.ATTR_KEY_TABLE_META in attrs:		# Removing table_meta because it's not serializable
			del attrs[self.ATTR_KEY_TABLE_META]

		return attrs

	def get_context(self, name, value, attrs):
		context = super().get_context(name, value, attrs)
		context[self.ATTR_KEY_TABLE_META] = self.extract_table_meta().serialize()
		return context
