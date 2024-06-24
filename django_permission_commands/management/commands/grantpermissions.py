from django.contrib.auth.models import Group
from django.contrib.contenttypes.models import ContentType

from ._permissions import AbstractImpl, PermissionType


class Command(AbstractImpl):
    help = (
        "Grant permissions for a certain model identified by its app label "
        "and model name."
    )

    def handle(
        self,
        content_type_descriptions: list[str],
        **opts,
    ):
        self._initialize(content_type_descriptions, opts)
        for content_type in self._content_types:
            self._grant_permissions(
                self._group,
                content_type,
                self._permission_types,
            )

    def _grant_permissions(
        self,
        group: Group,
        content_type: ContentType,
        permission_types: set[PermissionType],
    ):
        for permission_type in permission_types:
            permission = self._load_permission(content_type, permission_type)
            if permission in group.permissions.all():
                self.stdout.write(
                    f"{permission} is already granted to {group.name}"
                )
            else:
                group.permissions.add(permission)
                self.stdout.write(
                    f"{permission} was successfully granted to {group.name}"
                )
