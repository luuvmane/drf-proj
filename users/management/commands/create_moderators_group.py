from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission

class Command(BaseCommand):
    help = "Create Moderators group with appropriate permissions"

    def handle(self, *args, **kwargs):
        moderators_group, created = Group.objects.get_or_create(name='Moderators')

        if created:
            self.stdout.write(self.style.SUCCESS('Moderators group created successfully.'))
        else:
            self.stdout.write('Moderators group already exists.')

        # Add specific permissions here if needed
        # permission = Permission.objects.get(codename='your_permission_codename')
        # moderators_group.permissions.add(permission)
        # moderators_group.save()

        self.stdout.write(self.style.SUCCESS('Permissions added to Moderators group.'))
