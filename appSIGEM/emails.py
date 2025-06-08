from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string

def enviar_email_html(destinatario, context):
    subject = 'Restablecer Contraseña - SIGEM'
    from_email = 'noreply@sigem.com'
    to = [destinatario]

    html_content = render_to_string('paginas/auth/password_reset_email.html', context)
    text_content = f"Hola {context['user'].get_full_name()}, para restablecer tu contraseña, haz clic en el siguiente enlace: {context['reset_link']}"

    msg = EmailMultiAlternatives(subject, text_content, from_email, to)
    msg.attach_alternative(html_content, "text/html")
    msg.send()
