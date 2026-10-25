
import uuid
from django.db import migrations, models


def remplir_references(apps, schema_editor):
    Reclamation = apps.get_model('reclamations', 'Reclamation')
    for reclamation in Reclamation.objects.filter(reference__isnull=True).iterator():
        reclamation.reference = uuid.uuid4()
        reclamation.save(update_fields=['reference'])


class Migration(migrations.Migration):

    dependencies = [
        ('reclamations', '0002_alter_reclamation_operateur'),
    ]

    operations = [
        migrations.AddField(
            model_name='reclamation',
            name='reference',
            field=models.UUIDField(null=True, editable=False),
        ),
        migrations.RunPython(
            remplir_references,
            migrations.RunPython.noop,
        ),
        migrations.AlterField(
            model_name='reclamation',
            name='reference',
            field=models.UUIDField(
                default=uuid.uuid4,
                editable=False,
                unique=True,
            ),
        ),
    ]
