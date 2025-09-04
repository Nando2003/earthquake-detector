from faker import Faker
from datetime import date
from django.test import TestCase
from subscribers.models import Subscriber as SubscriberModel

faker = Faker('pt-BR')


class SubscriberModelTest(TestCase):
    def setUp(self) -> None:
        self.subscriber = SubscriberModel.objects.create(
            contact=faker.phone_number(),
            contact_type=SubscriberModel.ContactTypes.SMS,
            show_alerts=True
        )
        return super().setUp()
    
    def test_subscriber_model_str_method(self):
        expected_str = f"Subscriber<contact='{self.subscriber.contact}', contact_type='{self.subscriber.contact_type}'>"
        self.assertEqual(str(self.subscriber), expected_str)

    def test_subscriber_model_created_at_field(self):
        today = date.today()
        self.assertEqual(self.subscriber.created_at.date(), today)

    def test_subscriber_model_updated_at_field(self):
        today = date.today()
        self.assertEqual(self.subscriber.updated_at.date(), today)
        