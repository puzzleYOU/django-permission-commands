import re
from enum import Enum
from itertools import chain

from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.core.management import BaseCommand, CommandError


class PermissionType(Enum):
    ADD = "add"
    CHANGE = "change"
    VIEW = "view"
    DELETE = "delete"

    def __str__(self) -> str:
        return self.value

    @classmethod
    def values(cls) -> set[str]:
        return {instance.value for instance in cls}

    @classmethod
    def choices_as_comma_separated_str(cls) -> str:
        return ", ".join(cls.values())


class AbstractImpl(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument(
            "--group",
            help="The name of a django.contrib.auth.models.Group instance.",
            required=True,
            type=str,
        )
        parser.add_argument(
            "content_type_descriptions",
            metavar="app_label[.ModelName]",
            nargs="+",
            help="Adjusts permissions for the given app / model",
            type=str,
        )
        perms_group = parser.add_mutually_exclusive_group(required=True)
        perms_group.add_argument(
            "--permission",
            action="append",
            type=str,
            choices=PermissionType.values(),
        )
        perms_group.add_argument(
            "--all-permissions",
            help=(
                "takes all available permissions "
                f"({PermissionType.choices_as_comma_separated_str()})"
            ),
            action="store_true",
        )

    def _initialize(
        self,
        content_type_descriptions: list[str],
        opts: dict,
    ):
        self._permission_types = self._parse_permission_types(opts)
        try:
            self._group = Group.objects.get(name=opts["group"])
        except Group.DoesNotExist:
            raise CommandError(f"group '{opts['group']}' does not exist")
        self._content_type_description_expr = re.compile(
            r"^([a-zA-Z_][a-zA-Z0-9_]*)(\.([a-zA-Z_][a-zA-Z0-9_]*))?$"
        )
        self._content_types = chain.from_iterable(
            self._load_content_types(content_type_description)
            for content_type_description in content_type_descriptions
        )

    def _parse_permission_types(self, opts: dict) -> set[PermissionType]:
        return (
            {PermissionType(val) for val in opts["permission"]}
            if opts["permission"] is not None
            else set(PermissionType)
        )

    def _load_content_types(
        self, content_type_description: str
    ) -> list[ContentType]:
        match = self._content_type_description_expr.match(
            content_type_description
        )
        if match is None:
            raise CommandError(f"'{content_type_description}' is malformed")
        else:
            app_label = match.group(1)
            maybe_model_name = match.group(3)

        lookup = ContentType.objects.filter(app_label=app_label)
        if maybe_model_name is not None:
            lookup = lookup.filter(model=maybe_model_name.lower())
        result = list(lookup)
        if len(result) == 0:
            raise CommandError(f"'{content_type_description}' does not exist")
        return result

    def _load_permission(
        self,
        content_type: ContentType,
        permission_type: PermissionType,
    ):
        permission_codename = f"{permission_type}_{content_type.model}"
        try:
            return Permission.objects.get(
                content_type=content_type,
                codename=permission_codename,
            )
        except Permission.DoesNotExist:
            raise CommandError(f"permission not found: {permission_codename}")
