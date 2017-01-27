import django
django.setup()

from django.contrib.auth.models import User, Permission
from django.contrib.contenttypes.models import ContentType

from getpass import getpass

usernames = ["eguser1", "eguser2"]


def get_permission():
    ct, _ = ContentType.objects.get_or_create(app_label="arcapp", model="permission")
    perm, _ = Permission.objects.get_or_create(name="ARC CE", codename="arc_ce", content_type=ct)
    return perm 


def create_users():

    perm = get_permission()

    for username in usernames:
        pw = getpass("Please provide password for user '%s': " % username).strip()
        user, _ = User.objects.get_or_create(username=username, password=pw, is_staff=False, is_active=True)
        user.user_permissions.add(perm) 
        user.save()
        print "Created user: %s" % username


if __name__ == "__main__":
 
    create_users()
