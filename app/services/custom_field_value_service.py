from app import db
from app.models.custom_field_value import CustomFieldValue


class CustomFieldService:

    def __init__(self):
        self.session = db.session()

    def insert(self, custom_fields, task_id):
        for key, value in custom_fields.iteritems():
            custom_field_id = "cf".split("_")
            custom_field_value = CustomFieldValue(
                custom_fiueld_id=custom_field_id,
                task_id=task_id,
                value=value
            )
            self.session.add(custom_field_value)
        self.session.commit()


"""
TODO something that returns the following:

SELECT
     cf.value as key
    ,cfv.value as value
FROM Custom_Field_Value cfv
INNER JOIN Task t ON
    t.id = cfv.task_id
INNER JOIN custom_field cf ON
    cf.id = cfv.custom_field_id
WHERE
    t.id = <<task_id>>
"""
