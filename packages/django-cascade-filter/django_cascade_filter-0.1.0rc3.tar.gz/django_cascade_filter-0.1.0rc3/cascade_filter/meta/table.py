from cascade_filter.meta.field import Field

from typing import List


class Table:
	"""
	Contains info about table fields for filtering table data.

	Examples:
		>>> # your_table.py
		>>> class YourTable(Table):
		>>> 	field1 = TextField('Field 1 Name', nullable=False)
		>>>
		>>> # table_form_meta.py
		>>> class MyTableForm(forms.Form):
		>>> 	field = CascadeFilterField(table_meta=YourTableMeta)
	"""
	@classmethod
	def serialize(cls) -> List[dict]:
		data = []

		for attr_name, attr in cls.__dict__.items():
			if isinstance(attr, Field):
				field_data = attr.serialize()
				field_data["name"] = attr_name
				data.append(field_data)

		return data
