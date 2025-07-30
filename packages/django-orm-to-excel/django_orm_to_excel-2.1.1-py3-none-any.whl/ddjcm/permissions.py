from abc import ABC, abstractmethod


class GranularPermission(ABC):
    @abstractmethod
    def can(self, role_name: str) -> bool:
        pass

    def __or__(self, other: "GranularPermission") -> "OrPermission":
        return OrPermission(self, other)

    def __and__(self, other: "GranularPermission") -> "AndPermission":
        return AndPermission(self, other)

    def __sub__(self, other: "GranularPermission") -> "SubtractPermission":
        return SubtractPermission(self, other)

    def __invert__(self) -> "InvertPermission":
        return InvertPermission(self)


class All(GranularPermission):
    def can(self, role_name: str) -> bool:
        return True

    def __repr__(self) -> str:
        return "All()"


class Me(GranularPermission):
    def can(self, role_name: str) -> bool:
        return role_name == "@me"

    def __repr__(self) -> str:
        return "Me()"


class Only(GranularPermission):
    def __init__(self, *roles: str):
        self.roles = set(roles)

    def can(self, role_name: str) -> bool:
        return role_name in self.roles

    def __repr__(self) -> str:
        return f"Only({', '.join(repr(r) for r in self.roles)})"


class Nobody(GranularPermission):
    def can(self, role_name):
        return False

    def __repr__(self) -> str:
        return "Nobody()"


class OrPermission(GranularPermission):
    def __init__(self, left: GranularPermission, right: GranularPermission):
        self.left = left
        self.right = right

    def can(self, role_name: str) -> bool:
        return self.left.can(role_name) or self.right.can(role_name)

    def __repr__(self) -> str:
        return f"({self.left} | {self.right})"


class AndPermission(GranularPermission):
    def __init__(self, left: GranularPermission, right: GranularPermission):
        self.left = left
        self.right = right

    def can(self, role_name: str) -> bool:
        return self.left.can(role_name) and self.right.can(role_name)

    def __repr__(self) -> str:
        return f"({self.left} & {self.right})"


class SubtractPermission(GranularPermission):
    def __init__(self, left: GranularPermission, right: GranularPermission):
        self.left = left
        self.right = right

    def can(self, role_name: str) -> bool:
        return self.left.can(role_name) and not self.right.can(role_name)

    def __repr__(self) -> str:
        return f"({self.left} - {self.right})"


class InvertPermission(GranularPermission):
    def __init__(self, permission: GranularPermission):
        self.permission = permission

    def can(self, role_name: str) -> bool:
        return not self.permission.can(role_name)

    def __repr__(self) -> str:
        return f"~{self.permission}"


class Permission:
    def __init__(self, view: GranularPermission = All(), edit: GranularPermission = All()):
        self.view_permission = view
        self.edit_permission = edit

    def can_view(self, role_name: str) -> bool:
        return self.view_permission.can(role_name)

    def can_edit(self, role_name: str) -> bool:
        return self.edit_permission.can(role_name)

    def __repr__(self) -> str:
        return f"Permission(view={self.view_permission}, edit={self.edit_permission})"
