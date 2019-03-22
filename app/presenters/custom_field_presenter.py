from app.models.custom_field import FieldTypes


class CustomFieldPresenter:
    def convert(self, custom_field):
        return {
            "id": custom_field.id,
            "type": "custom-field",
            "title": custom_field.title,
            "field_type": FieldTypes(custom_field.field_type).name,
        }

    def convert_list(self, custom_fields):
        return map(self.convert, custom_fields)
