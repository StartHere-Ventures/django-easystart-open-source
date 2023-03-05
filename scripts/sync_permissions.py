import os
import sys
import traceback

import yaml
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType

from apps.core.models import GlobalSettings


def run():
    pid = str(os.getpid())
    pidfile = "/tmp/sync_permissions.pid"

    if os.path.isfile(pidfile):
        print("sync_permissions.py script is already running...")
        sys.exit()

    open(pidfile, "w").write(pid)

    # initialise
    try:
        management_group = Group.objects.get(name="management")
        with open("permissions.yml", "r") as file:
            content_type = ContentType.objects.get_for_model(GlobalSettings)
            permissions = yaml.safe_load(file)
            for p in permissions["permissions"]:
                permission, created = Permission.objects.update_or_create(
                    codename=p["codename"],
                    content_type=content_type,
                    defaults={"name": p["name"]},
                )
                management_group.permissions.add(permission)

    except Exception:
        traceback.print_exc()
    finally:
        traceback.print_exc()
        os.unlink(pidfile)
