from email.mime.text import MIMEText
import deform
import smtplib
from .config import CONTACT_FORM_ERROR
from .config import CONTACT_FORM_RECIPIENT
from .config import CONTACT_FORM_SUBJECT
from .config import SENDGRID_HOSTNAME
from .config import SENDGRID_PASSWORD
from .config import SENDGRID_USERNAME
from .forms import ContactFormSchema


def contact(request):
    """
    Create and render deform form containing colander schema
    """
    form = deform.Form(ContactFormSchema(), buttons=('Send', ))
    if 'Send' in request.POST:
        controls = request.POST.items()
        try:
            appstruct = form.validate(controls)
        except deform.ValidationFailure:
            return {
                'form': form.render(),
                'request': request,
            }
        sender = appstruct['email']
        body = appstruct['msg']
        body = body.encode('utf-8')
        body = str(body)
        msg = MIMEText(body)
        msg['Subject'] = CONTACT_FORM_SUBJECT
        msg['To'] = CONTACT_FORM_RECIPIENT
        msg['From'] = sender
        msg = msg.as_string()
        try:
            smtp_server = smtplib.SMTP(SENDGRID_HOSTNAME)
            smtp_server.starttls()
            smtp_server.login(SENDGRID_USERNAME, SENDGRID_PASSWORD)
            smtp_server.sendmail(sender, CONTACT_FORM_RECIPIENT, msg)
            smtp_server.quit()
        except:
            request.session.flash(CONTACT_FORM_ERROR)
        appstruct = []
        return {
            'form': form.render(),
            'request': request,
        }
    return {
        'form': form.render(),
        'request': request,
    }


def default(request):
    """
    This is the default view, to be used with most routes since we do not
    provide any content editing ability yet. Even then, maybe a default view
    would still be helpful.
    """
    return {}
