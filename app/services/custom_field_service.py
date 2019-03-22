from app import db
from app.models.custom_field import CustomField, FieldTypes


class CustomFieldService:

    def __init__(self):
        self.session = db.session()

    # TODO: need to think about this one
    # def get(self):
    #     return Status.query.filter_by(is_deleted=False).all()

    def get_by_id(self, id):
        return self.session.query(CustomField).filter_by(
            id=id,
            is_deleted=False
        ).first()

    def post(self, title, field_type):
        field_type_id = FieldTypes[field_type.upper()].value
        #
        # TODO What if FieldType not valid???
        #
        custom_field = CustomField(title=title, field_type=field_type_id)
        self.session.add(custom_field)
        self.session.commit()
        return custom_field

    def delete(self, id):
        custom_field = CustomField.query.filter_by(id=id).first()
        custom_field.is_deleted = True
        self.session.commit()
        return {"success": True}

    def put(self, id, title):
        custom_field = CustomField.query.filter_by(id=id).first()
        custom_field.title = title
        self.session.add(custom_field)
        self.session.commit()
        return custom_field
