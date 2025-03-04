
from fastapi import HTTPException
from .customfield import CustomField
import re

async def validate_custom_field(field: CustomField, value: str):
    """ Validates field value based on field type and constraints """

    if field.required and not value:
        raise HTTPException(status_code=400, detail=f"{field.name} is required.")

    if field.field_type in ["text", "textarea"]:
        if field.min_length and len(value) < field.min_length:
            raise HTTPException(status_code=400, detail=f"{field.name} must be at least {field.min_length} characters.")
        if field.max_length and len(value) > field.max_length:
            raise HTTPException(status_code=400, detail=f"{field.name} must be at most {field.max_length} characters.")
    
    if field.field_type == "number" or field.field_type == "amount":
        try:
            num_value = float(value)
            if field.min_value and num_value < field.min_value:
                raise HTTPException(status_code=400, detail=f"{field.name} must be at least {field.min_value}.")
            if field.max_value and num_value > field.max_value:
                raise HTTPException(status_code=400, detail=f"{field.name} must be at most {field.max_value}.")
        except ValueError:
            raise HTTPException(status_code=400, detail=f"{field.name} must be a valid number.")

    if field.field_type == "email":
        email_pattern = r"^[\w\.-]+@[\w\.-]+\.\w+$"
        if not re.match(email_pattern, value):
            raise HTTPException(status_code=400, detail="Invalid email format.")

    if field.field_type == "phone":
        phone_pattern = r"^\+?[1-9]\d{1,14}$"  # International phone format
        if not re.match(phone_pattern, value):
            raise HTTPException(status_code=400, detail="Invalid phone number format.")

    if field.regex:
        if not re.match(field.regex, value):
            raise HTTPException(status_code=400, detail=f"Invalid format for {field.name}.")

    return True