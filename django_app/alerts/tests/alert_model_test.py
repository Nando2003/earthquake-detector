from faker import Faker
from django.test import TestCase
from alerts.models import Alert as AlertModel

faker = Faker('pt-BR')


class AlertModelTest(TestCase):
    def setUp(self):
        self.level = [AlertModel.LevelOfSeverity.LOW, AlertModel.LevelOfSeverity.HIGH]
        self.level_choice = faker.random_element(elements=self.level)
        self.detected_at = faker.date_time_this_year()

        self.alert = AlertModel.objects.create(
            level_of_severity=self.level_choice,
            detected_at=self.detected_at
        )
        return super().setUp()
    
    def test_alert_model_str_method(self):
        expected_str = f"Alert=<detected_at='{self.alert.detected_at}', level_of_severity='{self.alert.level_of_severity}'>"
        self.assertEqual(str(self.alert), expected_str)

    def test_alert_model_detected_at_field(self):
        self.assertEqual(self.alert.detected_at, self.detected_at)

