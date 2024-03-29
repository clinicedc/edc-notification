from django.conf import settings
from django.contrib.auth.models import User
from django.test.testcases import TestCase
from django.test.utils import override_settings

from edc_notification.decorators import register
from edc_notification.models import Notification as NotificationModel
from edc_notification.notification import GradedEventNotification
from edc_notification.site_notifications import site_notifications

from ..models import AE


class TwilioTestClient:
    # noinspection PyUnusedLocal
    def __init__(self, **kwargs):
        self.messages = TwillioTestClientMessages()


class TwillioTestClientMessages:
    created: list = []

    sid = "test-sid"

    def create(self, to, from_, body):
        self.created.append({"to": to, "from_": from_, "body": body})
        return self


class TestTwilio(TestCase):
    @override_settings(
        TWILIO_ENABLED=True,
        TWILIO_SENDER="5555555555",
        EDC_PROTOCOL_PROJECT_NAME="My Project",
    )
    def test_(self):
        self.maxDiff = None
        user = User.objects.create(username="erikvw", is_active=True, is_staff=True)

        site_notifications._registry = {}
        site_notifications.update_notification_list()

        @register()
        class G3EventNotification(GradedEventNotification):
            name = "g3_event"
            display_name = "Test Grade3 Event"
            grade = 3
            model = "edc_notification.ae"
            sms_client = TwilioTestClient

        site_notifications.update_notification_list()
        notification = NotificationModel.objects.get(name=G3EventNotification.name)
        user.userprofile.sms_notifications.add(notification)
        user.userprofile.mobile = settings.TWILIO_TEST_RECIPIENT
        user.userprofile.save()

        self.assertIn(settings.TWILIO_TEST_RECIPIENT, G3EventNotification().sms_recipients)

        AE.objects.create(subject_identifier="1", ae_grade=3)

        self.assertEqual(
            TwillioTestClientMessages.created[0].get("body"),
            (
                "TEST MESSAGE. NO ACTION REQUIRED - My Project: "
                "Report 'Test Grade3 Event' "
                "for patient 1 at site 'What A Site' may require your attention. "
                "Login to review. (See your user profile to unsubscribe.)"
            ),
        )
