# classes for secure work

class Role:
    ADMIN = "A"
    USER = "U"

ROLE_HIERARCHY = {
    Role.ADMIN: 2,
    Role.USER: 1,
}