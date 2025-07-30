from pydantic import BaseModel
from wtforms import StringField, BooleanField, Field, IntegerField, SelectField, TextAreaField
from wtforms.form import BaseForm


class Former:
    """Base class for form generation from Pydantic models."""

    def __init__(self, model: BaseModel):
        self.model = model

    def gen_form(self) -> BaseForm:
        """Generate a WTForms form based on the Pydantic model."""
        return BaseForm(self.gen_form_schema())

    def gen_form_schema(self) -> dict[str, Field]:
        base_schema = self.model.model_json_schema()
        form_schema = {}

        for key, value in base_schema["properties"].items():
            if "$ref" in value:
                definition = base_schema["$defs"][value["$ref"].split("/")[-1]]
                attr = Former.__process_field_attr(value)
                if "enum" in definition:
                    form_schema[key] = SelectField(
                        choices=[(item, item) for item in definition["enum"]],
                        **attr,
                    )
                else:
                    form_schema[key] = TextAreaField(**attr)
                continue

            form_schema[key] = self.__process_field(value, key)

        return form_schema

    @staticmethod
    def __process_field(field: dict, key: str) -> Field:
        """Process a field definition to create a WTForms field."""
        field_type = field.get("type", "string")
        attr = Former.__process_field_attr(field)

        if field_type == "string":
            return StringField(**attr)
        elif field_type == "integer":
            return IntegerField(**attr)
        elif field_type == "boolean":
            return BooleanField(**attr)
        elif field_type in ["object", "array"]:
            return TextAreaField(**attr)
        else:
            raise ValueError(f"Unsupported field type: {field_type}")

    @staticmethod
    def __process_field_attr(field: dict) -> dict:
        attr = {}
        if "title" in field:
            attr["label"] = field["title"]
        if "default" in field:
            attr["default"] = field["default"]
        if "description" in field:
            attr["description"] = field["description"]

        return attr
