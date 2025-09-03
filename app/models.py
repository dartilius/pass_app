from django.contrib.auth.models import User
from django.db import models
from django.dispatch import receiver

from app.telegram import telegram_message


class Worker(models.Model):
    """Модель сотрудника."""

    name = models.CharField(
        verbose_name="ФИО сотрудника",
        max_length=150,
    )
    chat_id = models.IntegerField(
        verbose_name="ID чата в тг"
    )

    def __str__(self):
        return self.name


class Pass(models.Model):
    """Модель заявки на пропуск."""

    name = models.CharField(
        verbose_name="ФИО гостя",
        max_length=150,
    )
    worker = models.ForeignKey(
        Worker,
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
        telegram_message.send_worker_message(
            instance.name,
            instance.id,
            instance.worker.chat_id
        )
