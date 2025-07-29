# Standard Library
from io import StringIO

# Django
from django.test import TestCase, override_settings

# Alliance Auth (External Libs)
from app_utils.testing import create_fake_user


class ManagementCommandAnonymizeEmailsTests(TestCase):
    def call_command(self, *args, **kwargs):
        # Django
        from django.core.management import call_command

        call_command(
            "tnnt_anonymize_emails",
            *args,
            stdout=StringIO(),
            stderr=StringIO(),
            **kwargs,
        )

    def setUp(self):
        """
        Setup tests
        """

        self.user = create_fake_user(character_id=2001, character_name="Wesley Crusher")

        self.user.email = "wesley.crusher@enterprise.space"
        self.user.save()

    @override_settings(SITE_URL="https://auth.testserver.net")
    def test_command_anonymize_emails(self):
        """
        Test command
        """

        self.call_command("--no-input")

        self.user.refresh_from_db()

        self.assertEqual(
            first=self.user.email, second=f"{self.user.pk}@auth.testserver.net"
        )
