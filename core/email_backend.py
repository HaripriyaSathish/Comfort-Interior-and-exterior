from django.core.mail.backends.smtp import EmailBackend


class DatabaseEmailBackend(EmailBackend):
    """SMTP backend that reads its credentials from the admin-managed EmailSettings."""

    def __init__(self, fail_silently=False, **kwargs):
        from .models import EmailSettings

        cfg = EmailSettings.load()
        super().__init__(
            host=cfg.smtp_host,
            port=cfg.smtp_port,
            username=cfg.smtp_username,
            password=cfg.smtp_password,
            use_tls=cfg.use_tls,
            use_ssl=cfg.use_ssl,
            fail_silently=fail_silently,
            timeout=20,
            **kwargs,
        )
