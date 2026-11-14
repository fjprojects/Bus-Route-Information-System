from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True
    dependencies = []
    operations = [
        migrations.CreateModel(
            name="Route",
            fields=[
                ("id", models.SlugField(max_length=80, primary_key=True, serialize=False)),
                ("name", models.CharField(max_length=120)),
                ("origin", models.CharField(db_index=True, max_length=120)),
                ("destination", models.CharField(db_index=True, max_length=120)),
                ("stops", models.JSONField(default=list)),
                ("duration_min", models.PositiveSmallIntegerField()),
                ("frequency_min", models.PositiveSmallIntegerField()),
                ("service_label", models.CharField(default="Sample service", max_length=80)),
                ("updated_at", models.DateTimeField(auto_now=True)),
            ],
            options={"ordering": ("duration_min", "name")},
        ),
    ]
