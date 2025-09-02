from django.contrib.auth.models import User
from django.db import models
from django.dispatch import receiver


class Pass(models.Model):
    """Модель заявки на пропуск."""

    client_name = models.CharField(
        verbose_name="ФИО гостя",
        max_length=150,
    )
    worker = models.ForeignKey(
        User,
        verbose_name="Сотрудник",
        on_delete=models.CASCADE,
    )
    is_approved = models.BooleanField(
        verbose_name="Заявка одобрена сотрудником",
        null=True,
        blank=True,
    )
    is_validated = models.BooleanField(
        verbose_name="Пропуск выдан охраной",
        null=True,
        blank=True,
    )




@receiver(models.signals.post_save, sender=Pass)
def notify_worker(sender, instance, created, *args, **kwargs):
    if created:
        # send telegram message
        ...
