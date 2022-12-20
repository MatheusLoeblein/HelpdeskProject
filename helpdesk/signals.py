import os

from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import send_mail
from django.db.models.signals import post_save, pre_delete, pre_save
from django.dispatch import receiver

from helpdesk.models import Comment, Tarefa


def delete_cover(instance):
    try:
        os.remove(instance.cover.path)
    except (ValueError, FileNotFoundError):
        ...


@receiver(pre_delete, sender=Tarefa)
def tarefa_cover_delete(sender, instance, *args, **kwargs):
    old_instance = Tarefa.objects.filter(pk=instance.pk).first()

    if not old_instance:
        return
    if old_instance:
        delete_cover(old_instance)


@receiver(pre_save, sender=Tarefa)
def tarefa_cover_update(sender, instance, *args, **kwargs):
    old_instance = Tarefa.objects.filter(pk=instance.pk).first()

    if not old_instance:
        return
    is_new_cover = old_instance.cover != instance.cover

    if is_new_cover:
        delete_cover(old_instance)


@receiver(pre_delete, sender=Comment)
def comment_cover_delete(sender, instance, *args, **kwargs):
    old_instance = Comment.objects.filter(pk=instance.pk).first()

    if old_instance:
        delete_cover(old_instance)


@receiver(pre_save, sender=Comment)
def comment_cover_update(sender, instance, *args, **kwargs):
    old_instance = Comment.objects.filter(pk=instance.pk).first()

    if not old_instance:
        return
    is_new_cover = old_instance.cover != instance.cover

    if is_new_cover:
        delete_cover(old_instance)


@receiver(post_save, sender=Tarefa)
def send_email_on_model_change(sender, instance, **kwargs):

    if kwargs['created']:
        subject = f'Help Desk Formédica - {str(instance.tipe)}'
        message = f'A Tarefa com o assunto "{str(instance.tipe)}" e com o id #{instance.id}, foi Criada você pode verificar agora, pode ser importante..'
        recipient_list = ['informatica@formedica.com.br']
    else:
        subject = f'Help Desk Formédica - {str(instance.tipe)}'
        message = f'A Tarefa com o assunto "{str(instance.tipe)}" e com o id #{instance.id}, acaba de ser atualizada'
        recipient_list = [instance.author.email]

    from_email = 'formedica@formedica.com.br'
    # Obtém o URL do post
    post_url = f'http://34.68.42.61/tarefa/{instance.id}'

    # Adiciona o URL do post à mensagem do email
    message += '\n\nVeja a solicitaçõa clicando aqui: {}'.format(post_url)

    send_mail(subject, message, from_email, recipient_list)
