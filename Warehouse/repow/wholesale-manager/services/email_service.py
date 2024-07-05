from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags


class EmailSender:
    @staticmethod
    def send(
        subject,
        body=None,
        to_emails=(),
        from_email=None,
        template=None,
        context=None,
        cc_emails=(),
        bcc_emails=(),
        reply_to=[],
        headers=None,
        strip_tag=False,
        attach_file=False,
    ):
        """Send email to passed email using the passed subject, body and html.

        The type of email is text/html by default

        Args:
            subject:
            body:
            html_content:
            to_email:
            mimetype (str, optional): Defaults to "text/html".
        """
        try:
            if not from_email:
                from_email = settings.DEFAULT_FROM_EMAIL

            if template:
                if context:
                    body = render_to_string(template, context)
                else:
                    return {"error": "Provide context."}

            # If body isn't provided then it shows error
            if not body:
                return {"error": "Provide body."}

            if strip_tag:
                body = strip_tags(body)

            msg = EmailMultiAlternatives(
                subject=subject,
                body=body,
                from_email=from_email,
                to=to_emails,
                reply_to=reply_to,
                cc=cc_emails,
                bcc=bcc_emails,
                headers=headers,
            )

            msg.content_subtype = "html"
            if attach_file:
                for file in attach_file:
                    msg.attach_file(file)
            msg.send()
        except Exception as e:
            import traceback

            traceback.format_exc()
            print(e)