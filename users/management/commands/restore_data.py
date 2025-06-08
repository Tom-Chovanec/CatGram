# users/management/commands/restore_data.py

from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from cats.models import CatImage


class Command(BaseCommand):
    help = 'Restores users and posts from an old database file.'

    def handle(self, *args, **kwargs):
        self.stdout.write("Starting data restoration...")

        # --- STEP 1: Restore Users (Uncommented) ---
        # This ensures all users from the old DB exist before we try to link images to them.
        # self.stdout.write("Syncing users...")
        # old_users = User.objects.using('old').all()
        # restored_users = 0
        # for old_user in old_users:
        #     if not User.objects.filter(username=old_user.username).exists():
        #         new_user = User(
        #             id=old_user.id,
        #             username=old_user.username,
        #             email=old_user.email,
        #             password=old_user.password,
        #             is_staff=old_user.is_staff,
        #             is_superuser=old_user.is_superuser,
        #             is_active=old_user.is_active,
        #             date_joined=old_user.date_joined,
        #             last_login=old_user.last_login,
        #         )
        #         new_user.save()
        #         restored_users += 1
        # self.stdout.write(self.style.SUCCESS(f"Restored {restored_users} new users."))

        # --- STEP 2: Restore Cat Images with a Safety Check ---
        self.stdout.write("Restoring Cat Images...")
        old_images = CatImage.objects.using('old').all()
        restored_images = 0
        skipped_images = 0
        for old_image in old_images:
            print(old_image.__str__())
            if not CatImage.objects.filter(id=old_image.id).exists():
                if User.objects.filter(id=old_image.uploaded_by_id).exists():
                    new_image = CatImage(
                        id=old_image.id,
                        uploaded_by_id=old_image.uploaded_by_id,
                        uploaded_at=old_image.uploaded_at,
                        image=old_image.image,
                        title=old_image.title,
                    )
                    new_image.save()
                    liking_user_ids = old_image.likes.values_list(
                        'pk', flat=True)
                    favorite_user_ids = old_image.favorites.values_list(
                        'pk', flat=True)

                    if liking_user_ids:
                        new_image.likes.set(liking_user_ids)
                    if favorite_user_ids:
                        new_image.favorites.set(favorite_user_ids)
                    restored_images += 1
                else:
                    # This tells you which images are being skipped and why
                    self.stdout.write(self.style.WARNING(
                        f"Skipping image ID {old_image.id}: User ID {
                            old_image.uploaded_by_id} not found in new DB."
                    ))
                    skipped_images += 1

        self.stdout.write(self.style.SUCCESS(
            f"Restored {restored_images} Cat Images."))
        if skipped_images > 0:
            self.stdout.write(self.style.WARNING(
                f"Skipped {skipped_images} images due to missing users."))

        self.stdout.write(self.style.SUCCESS("Data restoration complete."))
