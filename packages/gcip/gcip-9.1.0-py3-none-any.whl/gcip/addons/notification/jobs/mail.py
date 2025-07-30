from dataclasses import InitVar, dataclass
from typing import Any, Dict

from gcip.addons.container.images import PredefinedImages
from gcip.core.job import Job


@dataclass(kw_only=True)
class SendMail(Job):
    """
    Send an email over an SMTP server.

    The configuration can be done by environment variables and parameters.

    The default environment variables are following:

    - SMTP_SERVER
    - SMTP_PORT (Defauls to 587)
    - SMTP_USER
    - SMTP_PASSWORD
    - FROM_EMAIL (Defaults to SMTP_USER)
    - TO_EMAILS (can be multiple recipients separated by comma)
    - SUBJECT
    - EMAIL_BODY_PATH - path to the file containing the email body

    You can change the name of the environment variables, if they already present to
    the pipeline but you have no means to change them itself. This can be accomplished
    with the follwing parameters (camleCase) or environment  variables (UPPER_CASE):

    - smtpServerVar / SMTP_SERVER_VAR
    - smtpPortVar / SMTP_PORT_VAR
    - smtpUserVar / SMTP_USER_VAR
    - smtpPasswordVar / SMTP_PASSWORD_VAR
    - fromEmailVar / FROM_EMAIL_VAR
    - toEmailsVar / TO_EMAILS_VAR
    - subjectVar / SUBJECT_VAR
    - emailBodyPathVar / EMAIL_BODY_PATH_VAR

    Finally you can configure all values, except the password, by parameters directly:

    Args:
      smtpServer (str): Same as SMTP_SERVER env.
      smtpPort (int): Same as SMTP_PORT env.
      smtpUser (str): Same as SMTP_USER env.
      fromEmail (str): Same as FROM_EMAIL env.
      toEmails (str): Same as TO_EMAILS env.
      subject (str): Same as SUBJECT env.
      emailBodyPath (str): Same as EMAIL_BODY_PATH.
      emailBody (str): The string content will be used as email body. Superseeds 'emailBodyPath'.

    Examples you will find under "<projectRoot>/test/unit/test_addons_python_jobs_notification.py"

    This subclass of `Job` will configure following defaults for the superclass:

    * name: send-mail
    * stage: notify
    * image: PredefinedImages.GCIP
    """

    jobName: InitVar[str] = "send-mail"
    jobStage: InitVar[str] = "notify"

    smtpServer: str | None = None
    smtpPort: int | None = None
    smtpUser: str | None = None
    fromEmail: str | None = None
    toEmails: str | None = None
    subject: str | None = None
    emailBody: str | None = None
    emailBodyPath: str | None = None

    smtpServerVar: str | None = None
    smtpPortVar: str | None = None
    smtpUserVar: str | None = None
    smtpPasswordVar: str | None = None
    fromEmailVar: str | None = None
    toEmailsVar: str | None = None
    subjectVar: str | None = None
    emailBodyVar: str | None = None
    emailBodyPathVar: str | None = None

    def __post_init__(self, jobName: str, jobStage: str) -> None:
        super().__init__(script="", name=jobName, stage=jobStage)
        self.set_image(PredefinedImages.GCIP)

    def render(self) -> Dict[str, Any]:
        command = "python3 -m gcip.tools.sendmail"

        # evaluate environment variable overrides
        if self.smtpServerVar:
            command += f' --smtp_server_var "{self.smtpServerVar}"'
        if self.smtpPortVar:
            command += f' --smtp_port_var "{self.smtpPortVar}"'
        if self.smtpUserVar:
            command += f' --smtp_user_var "{self.smtpUserVar}"'
        if self.smtpPasswordVar:
            command += f' --smtp_password_var "{self.smtpPasswordVar}"'
        if self.fromEmailVar:
            command += f' --from_email_var "{self.fromEmailVar}"'
        if self.toEmailsVar:
            command += f' --to_emails_var "{self.toEmailsVar}"'
        if self.subjectVar:
            command += f' --subject_var "{self.subjectVar}"'
        if self.emailBodyVar:
            command += f' --email_body_var "{self.emailBodyVar}"'
        if self.emailBodyPathVar:
            command += f' --email_body_path_var "{self.emailBodyPathVar}"'

        # set environment variables depending on values
        if self.smtpServer:
            self.add_variables(SMTP_SERVER=self.smtpServer)
        if self.smtpPort:
            self.add_variables(SMTP_PORT=str(self.smtpPort))
        if self.smtpUser:
            self.add_variables(SMTP_USER=self.smtpUser)
        if self.fromEmail:
            self.add_variables(FROM_EMAIL=self.fromEmail)
        if self.toEmails:
            self.add_variables(TO_EMAILS=self.toEmails)
        if self.subject:
            self.add_variables(SUBJECT=self.subject)
        if self.emailBody:
            self.add_variables(EMAIL_BODY=self.emailBody)

        if self.emailBodyPath:
            self.add_variables(EMAIL_BODY_PATH=self.emailBodyPath)

        self._scripts = [command]
        return super().render()
