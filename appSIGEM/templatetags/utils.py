from django import template
register = template.Library()
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.contrib.auth import get_user_model

@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)


User = get_user_model()

def enviar_correo_admin(solicitud):
    subject = f"📝 Nueva solicitud ingresada - {solicitud.numero_solicitud}"
    to = [admin.email for admin in User.objects.filter(is_superuser=True, is_active=True)]
    context = {'solicitud': solicitud}
    html_content = render_to_string('emails/nueva_solicitud_admin.html', context)
    text_content = render_to_string('emails/nueva_solicitud_admin.txt', context)

    msg = EmailMultiAlternatives(subject, text_content, 'noreply@sigem.com', to)
    msg.attach_alternative(html_content, "text/html")
    msg.send()

def enviar_correo_usuario_respuesta(solicitud):
    subject = f"📬 Respuesta a tu solicitud #{solicitud.numero_solicitud}"
    to = [solicitud.usuario.email]
    context = {'solicitud': solicitud}
    html_content = render_to_string('emails/respuesta_solicitud_usuario.html', context)
    text_content = render_to_string('emails/respuesta_solicitud_usuario.txt', context)

    msg = EmailMultiAlternatives(subject, text_content, 'noreply@sigem.com', to)
    msg.attach_alternative(html_content, "text/html")
    msg.send()