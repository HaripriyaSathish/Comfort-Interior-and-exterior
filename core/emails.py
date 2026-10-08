import logging

from django.core.mail import EmailMessage, get_connection

from .models import EmailSettings, SiteSettings

logger = logging.getLogger(__name__)


def _summary(enquiry):
    return (
        f'Name:     {enquiry.name}\n'
        f'Phone:    {enquiry.phone}\n'
        f'Email:    {enquiry.email}\n'
        f'Service:  {enquiry.service}\n'
        f'Received: {enquiry.created_at:%d %b %Y, %I:%M %p}\n\n'
        f'Message:\n{enquiry.message}\n'
    )


def send_enquiry_emails(enquiry):
    """Email the business about a new enquiry and send the customer a confirmation.

    Returns True when the business notification was sent. Never raises: the enquiry is
    already saved, so a mail failure must not break the form for the visitor.
    """
    cfg = EmailSettings.load()
    if not cfg.is_configured or not cfg.notify_email:
        logger.warning('Enquiry %s saved but SMTP is not configured in admin.', enquiry.pk)
        return False

    sender = cfg.from_email or cfg.smtp_username
    site_name = SiteSettings.load().site_name

    notified = False
    try:
        with get_connection() as connection:
            EmailMessage(
                subject=f'New enquiry: {enquiry.name} — {enquiry.service}',
                body=f'You have a new enquiry from the {site_name} website.\n\n{_summary(enquiry)}',
                from_email=sender,
                to=[cfg.notify_email],
                reply_to=[enquiry.email],
                connection=connection,
            ).send()
            notified = True

            if cfg.send_auto_reply:
                EmailMessage(
                    subject=cfg.auto_reply_subject,
                    body=f'Hi {enquiry.name},\n\n{cfg.auto_reply_message}\n\n'
                         f'--- Your enquiry ---\n{_summary(enquiry)}',
                    from_email=sender,
                    to=[enquiry.email],
                    reply_to=[cfg.notify_email],
                    connection=connection,
                ).send()
    except Exception:
        logger.exception('Failed to send emails for enquiry %s', enquiry.pk)
    return notified
