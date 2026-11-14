from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("api", "0002_shared_demo_catalogues"),
    ]

    operations = [
        migrations.DeleteModel(name="ExerciseReference"),
        migrations.DeleteModel(name="Measurement"),
    ]
