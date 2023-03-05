from django.core.exceptions import ValidationError


class AtLeastOneDigitValidator(object):
    def __init__(self):
        pass

    def validate(self, password, user=None):
        if not any(char.isdigit() for char in password):
            raise ValidationError("Password must contain at least 1 digit.")

    def get_help_text(self):
        return "Your password must contain at least one digit."


class AtLeastOneUpperLetterValidator(object):
    def __init__(self):
        pass

    def validate(self, password, user=None):
        uppercase = 0
        for value in password:
            if value.isupper():
                uppercase += 1

        if not uppercase:
            raise ValidationError(
                "Your password must contain at least one uppercase letter."
            )

    def get_help_text(self):
        return "Your password must container at least one uppercase letter."


class AtLeastOneLowerLetterValidator(object):
    def __init__(self):
        pass

    def validate(self, password, user=None):
        lowercase = 0
        for value in password:
            if value.islower():
                lowercase += 1

        if not lowercase:
            raise ValidationError(
                "Your password must contain at least one lowercase letter."
            )

    def get_help_text(self):
        return "Your password must container at least one lowercase letter."


class AtLeastOneSpecialCharacterValidator(object):
    def __init__(self):
        pass

    def validate(self, password, user=None):
        special_character = 0

        for value in password:
            if value.isupper():
                pass
            elif value.islower():
                pass
            elif value.isdigit():
                pass
            elif not value.isspace():
                special_character += 1
            elif value.isspace():
                raise ValidationError("Your password must not contain spaces.")

        if not special_character:
            raise ValidationError(
                "Your password must contain at least special character like: ?!+-."
            )

    def get_help_text(self):
        return "Your password must contain at least special " "character like: ?!+-."
