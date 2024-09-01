from django.db import migrations


def create_moderators_group(apps, schema_editor):
    Group = apps.get_model('auth', 'Group')
    Permission = apps.get_model('auth', 'Permission')

    moderators_group, created = Group.objects.get_or_create(name='Moderators')

    permissions = Permission.objects.filter(
        codename__in=[
            'view_course',
            'change_course',
            'view_lesson',
            'change_lesson',
        ]
    )

    for permission in permissions:
        moderators_group.permissions.add(permission)


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(create_moderators_group),
    ]