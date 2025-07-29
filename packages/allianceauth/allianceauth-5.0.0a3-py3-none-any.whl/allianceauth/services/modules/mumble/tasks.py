import logging

from celery import shared_task

from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist

from allianceauth.services.tasks import QueueOnce

from .models import MumbleUser

logger = logging.getLogger(__name__)


class MumbleTasks:
    def __init__(self):
        pass

    @staticmethod
    def has_account(user):
        try:
            return user.mumble.username != ''
        except ObjectDoesNotExist:
            return False

    @staticmethod
    def disable_mumble():
        logger.info("Deleting all MumbleUser models")
        MumbleUser.objects.all().delete()

    @staticmethod
    @shared_task(bind=True, name="mumble.update_groups", base=QueueOnce)
    def update_groups(self, pk):
        user = User.objects.get(pk=pk)
        logger.debug(f"Updating mumble groups for user {user}")
        if MumbleTasks.has_account(user):
            try:
                if not user.mumble.update_groups():
                    raise Exception("Group sync failed")
                logger.debug(f"Updated user {user} mumble groups.")
                return True
            except MumbleUser.DoesNotExist:
                logger.info(f"Mumble group sync failed for {user}, user does not have a mumble account")
            except Exception as e:
                logger.exception(f"Mumble group sync failed for {user}, retrying in 10 mins")
                raise self.retry(exc=e, countdown=60 * 10) from e
        else:
            logger.debug(f"User {user} does not have a mumble account, skipping")
        return False

    @staticmethod
    @shared_task(bind=True, name="mumble.update_display_name", base=QueueOnce)
    def update_display_name(self, pk):
        user = User.objects.get(pk=pk)
        logger.debug(f"Updating mumble groups for user {user}")
        if MumbleTasks.has_account(user):
            try:
                if not user.mumble.update_display_name():
                    raise Exception("Display Name Sync failed")
                logger.debug(f"Updated user {user} mumble display name.")
                return True
            except MumbleUser.DoesNotExist:
                logger.info(f"Mumble display name sync failed for {user}, user does not have a mumble account")
            except Exception as e:
                logger.exception(f"Mumble display name sync failed for {user}, retrying in 10 mins")
                raise self.retry(exc=e, countdown=60 * 10) from e
        else:
            logger.debug(f"User {user} does not have a mumble account, skipping")
        return False

    @staticmethod
    @shared_task(name="mumble.update_all_groups")
    def update_all_groups():
        logger.debug("Updating ALL mumble groups")
        for mumble_user in MumbleUser.objects.exclude(username__exact=''):
            MumbleTasks.update_groups.delay(mumble_user.user.pk)

    @staticmethod
    @shared_task(name="mumble.update_all_display_names")
    def update_all_display_names():
        logger.debug("Updating ALL mumble display names")
        for mumble_user in MumbleUser.objects.exclude(username__exact=''):
            MumbleTasks.update_display_name.delay(mumble_user.user.pk)
