# Generated Code

from pydantic import BaseModel, EmailStr
from typing import List


class Email(BaseModel):
    """Data model for an email."""

    address: EmailStr
    category: str

    @property
    def type(self):
        return "Internal" if self.address.endswith("@askaiden.com") else "External"


class EmailCategory(BaseModel):
    """Data model for an email category."""

    name: str
    emails: List[Email]


class EmailContent(BaseModel):
    """Data model for an email content."""

    subject: str
    body: str


# has to be a pure python list only with strings as elements
email_categories = [
    "Personal",
    "Work",
    "Promotions",
    "Social",
    "Updates",
]


# Prompt Template String
prompt_template_str = "Please generate a list named 'email_categories' with exactly 5 categories. Also classify the email as Internal or external based on if the email address ends with @askaiden.com"
