from auth.session import current_user


ROLE_PERMISSIONS = {

    "Administrator": [
        "manage_users",
        "manage_payments",
        "manage_farmers",
        "upload_receipts",
        "view_reports"
    ],

    "Manager": [
        "manage_payments",
        "manage_farmers",
        "upload_receipts",
        "view_reports"
    ],

    "Cashier": [
        "manage_payments",
        "upload_receipts"
    ],

    "Data Entry": [
        "manage_farmers"
    ],

    "Viewer": [
        "view_reports"
    ]
}


def has_permission(permission):

    user = current_user()

    if not user:
        return False

    role = user["role"]

    return permission in ROLE_PERMISSIONS.get(role, [])