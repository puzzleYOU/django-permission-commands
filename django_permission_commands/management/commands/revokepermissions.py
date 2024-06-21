from django.contrib.auth.models import Group
from django.contrib.contenttypes.models import ContentType

from ._permissions import AbstractImpl, PermissionType


class Command(AbstractImpl):
    help = (
        "Revoke permissions for a certain model identified by its app label "
        "and model name."
    )

    def handle(
        self,
        content_type_descriptions: list[str],
        **opts,
    ):
        self._initialize(content_type_descriptions, opts)
        for content_type in self._content_types:
            self._revoke_permissions(
                self._group,
                content_type,
                self._permission_types,
            )

    def _revoke_permissions(
        self,
        group: Group,
        content_type: ContentType,
        permission_types: set[PermissionType],
    ):
        for permission_type in permission_types:
            permission = self._load_permission(content_type, permission_type)
            if permission not in group.permissions.all():
                self.stdout.write(
                    f"{permission} is already revoked from {group.name}"
                )
            else:
                group.permissions.remove(permission)
                self.stdout.write(
                    f"{permission} was successfully revoked from {group.name}"
                )
