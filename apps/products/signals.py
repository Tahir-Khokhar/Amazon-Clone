import os
import logging

from django.db.models.signals import post_delete, pre_save
from django.dispatch import receiver

from .models import Product, ProductImage

logger = logging.getLogger(__name__)


@receiver(post_delete, sender=ProductImage)
def auto_delete_product_image_on_delete(sender, instance, **kwargs):
    """
    Remove the image file from the filesystem when a ProductImage is deleted.
    """
    if instance.image and os.path.isfile(instance.image.path):
        try:
            os.remove(instance.image.path)
            logger.info(f"Deleted image file: {instance.image.path}")
        except (OSError, FileNotFoundError) as exc:
            logger.warning(
                f"Failed to delete image file {instance.image.path}: {exc}"
            )


@receiver(post_delete, sender=Product)
def auto_delete_product_thumbnail_on_delete(sender, instance, **kwargs):
    """
    Remove the thumbnail file from the filesystem when a Product is deleted.
    """
    if instance.thumbnail and os.path.isfile(instance.thumbnail.path):
        try:
            os.remove(instance.thumbnail.path)
            logger.info(f"Deleted thumbnail file: {instance.thumbnail.path}")
        except (OSError, FileNotFoundError) as exc:
            logger.warning(
                f"Failed to delete thumbnail file {instance.thumbnail.path}: {exc}"
            )


@receiver(pre_save, sender=ProductImage)
def auto_delete_old_image_on_change(sender, instance, **kwargs):
    """
    Delete the old image file from the filesystem when a ProductImage
    is updated with a new image.
    """
    if not instance.pk:
        return  # New instance, no old file to delete

    try:
        old_instance = ProductImage.objects.get(pk=instance.pk)
    except ProductImage.DoesNotExist:
        return

    old_image = old_instance.image
    new_image = instance.image

    if old_image and old_image != new_image and os.path.isfile(old_image.path):
        try:
            os.remove(old_image.path)
            logger.info(f"Deleted old image file: {old_image.path}")
        except (OSError, FileNotFoundError) as exc:
            logger.warning(
                f"Failed to delete old image file {old_image.path}: {exc}"
            )


@receiver(pre_save, sender=Product)
def auto_delete_old_thumbnail_on_change(sender, instance, **kwargs):
    """
    Delete the old thumbnail file from the filesystem when a Product
    is updated with a new thumbnail.
    """
    if not instance.pk:
        return  # New instance, no old file to delete

    try:
        old_instance = Product.objects.get(pk=instance.pk)
    except Product.DoesNotExist:
        return

    old_thumbnail = old_instance.thumbnail
    new_thumbnail = instance.thumbnail

    if old_thumbnail and old_thumbnail != new_thumbnail and os.path.isfile(old_thumbnail.path):
        try:
            os.remove(old_thumbnail.path)
            logger.info(f"Deleted old thumbnail file: {old_thumbnail.path}")
        except (OSError, FileNotFoundError) as exc:
            logger.warning(
                f"Failed to delete old thumbnail file {old_thumbnail.path}: {exc}"
            )

