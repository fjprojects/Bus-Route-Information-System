from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("api", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="ExerciseReference",
            fields=[
                ("id", models.SlugField(max_length=80, primary_key=True, serialize=False)),
                ("name", models.CharField(max_length=120)),
                ("category", models.CharField(db_index=True, max_length=80)),
                ("description", models.TextField()),
                ("professional_note", models.TextField()),
                ("sort_order", models.PositiveSmallIntegerField(default=0)),
            ],
            options={"ordering": ("sort_order", "name")},
        ),
        migrations.CreateModel(
            name="Measurement",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("date", models.CharField(max_length=80, unique=True)),
                ("left_step_time", models.DecimalField(decimal_places=3, max_digits=7)),
                ("right_step_time", models.DecimalField(decimal_places=3, max_digits=7)),
                ("walking_speed", models.DecimalField(decimal_places=3, max_digits=7)),
                ("balance_score", models.DecimalField(decimal_places=2, max_digits=7)),
                ("sort_order", models.PositiveSmallIntegerField(default=0)),
            ],
            options={"ordering": ("sort_order", "id")},
        ),
    ]
