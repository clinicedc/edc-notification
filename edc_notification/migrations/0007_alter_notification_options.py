# Generated by Django 4.2.1 on 2023-07-05 02:16

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("edc_notification", "0006_auto_20200513_0023"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="notification",
            options={
                "default_manager_name": "objects",
                "default_permissions": (
                    "add",
                    "change",
                    "delete",
                    "view",
                    "export",
                    "import",
                ),
                "get_latest_by": "modified",
                "ordering": ("display_name",),
            },
        ),
    ]
