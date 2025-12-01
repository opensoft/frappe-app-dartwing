# Copyright (c) 2025, Brett and contributors
# For license information, please see license.txt

"""Family Member child table with age calculation."""

import frappe
from frappe.model.document import Document
from frappe.utils import getdate, today, date_diff


# Age category definitions
AGE_CATEGORIES = {
    "Toddler": (0, 5),
    "Child": (6, 12),
    "Teen": (13, 17),
    "Adult": (18, 999),
}


class FamilyMember(Document):
    """Family Member document - child table of Family."""

    def validate(self):
        """Calculate age fields from date of birth."""
        self.calculate_age_fields()
        self.auto_split_name()

    def calculate_age_fields(self):
        """Calculate age, age_category, is_minor, and is_coppa_protected."""
        if not self.date_of_birth:
            # Clear age fields if no DOB
            self.age = None
            self.age_category = None
            self.is_minor = 0
            self.is_coppa_protected = 0
            return

        # Calculate age in years
        self.age = calculate_age(self.date_of_birth)

        # Determine age category
        self.age_category = get_age_category(self.age)

        # Set minor flags
        self.is_minor = 1 if self.age < 18 else 0
        self.is_coppa_protected = 1 if self.age < 13 else 0

    def auto_split_name(self):
        """Auto-populate first_name and last_name from full_name if empty."""
        if self.full_name and not (self.first_name or self.last_name):
            parts = self.full_name.strip().split(" ", 1)
            self.first_name = parts[0]
            if len(parts) > 1:
                self.last_name = parts[1]


def calculate_age(date_of_birth):
    """
    Calculate age in years from date of birth.

    Args:
        date_of_birth: Date string or date object

    Returns:
        int: Age in years
    """
    if not date_of_birth:
        return None

    dob = getdate(date_of_birth)
    today_date = getdate(today())

    # Calculate age
    age = today_date.year - dob.year

    # Adjust if birthday hasn't occurred this year
    if (today_date.month, today_date.day) < (dob.month, dob.day):
        age -= 1

    return max(0, age)


def get_age_category(age):
    """
    Determine age category from age.

    Args:
        age: Age in years

    Returns:
        str: Age category (Toddler, Child, Teen, Adult)
    """
    if age is None:
        return None

    for category, (min_age, max_age) in AGE_CATEGORIES.items():
        if min_age <= age <= max_age:
            return category

    return "Adult"  # Default for any edge cases


def is_coppa_protected(date_of_birth):
    """
    Check if a person is COPPA protected (under 13).

    Args:
        date_of_birth: Date string or date object

    Returns:
        bool: True if under 13
    """
    age = calculate_age(date_of_birth)
    return age is not None and age < 13


def is_minor(date_of_birth):
    """
    Check if a person is a minor (under 18).

    Args:
        date_of_birth: Date string or date object

    Returns:
        bool: True if under 18
    """
    age = calculate_age(date_of_birth)
    return age is not None and age < 18
