from rest_framework.serializers import ModelSerializer, ValidationError
from accounts.models import User
import datetime


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = [
            "username",
            "password",
            "can_be_contacted",
            "can_data_be_shared",
            "date_of_birth",
        ]

    def validate_date_of_birth(self, value: datetime.date):
        """User must be at least 15 years old.
        """
        test_d = datetime.date(year=value.year + 15, month=value.month, day=value.day)
        if test_d > datetime.date.today():
            raise ValidationError("Minimal age of 15 is required to consent and subscribe.")
        return value
