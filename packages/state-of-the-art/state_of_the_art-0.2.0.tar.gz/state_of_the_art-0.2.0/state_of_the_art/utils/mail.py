import os
from subprocess import PIPE, Popen
import subprocess
from typing import Optional

from state_of_the_art.infrastructure.shell import ShellRunner


class EmailService:
    default_destination = "j34nc4rl0@gmail.com"
    SEND_FROM_EMAIL = "j34nc4rl0@gmail.com"

    def send(self, content=None, subject=None, attachment=None, recepient=None) -> str:
        # write content o file

        recepient = recepient or EmailService.default_destination
        if not content and not attachment:
            raise ValueError("You must provide content or attachment to send an email")

        if content and attachment:
            raise ValueError("You must provide content or attachment, not both")

        if attachment:
            return self._send_email(
                to=recepient, subject=subject, content=content, attachement=attachment
            )

        return self._send_email(
            to=recepient, subject=subject, content=content, attachement=attachment
        )

    def _send_email(
        self, *, to: str, subject=None, content: Optional[str] = None, attachement=None
    ):
        if content:
            content = content.replace("'", "")

        password = os.environ["SECOND_MAIL_APPS_PASSWORD"]
        body_content = f"""From: {self.SEND_FROM_EMAIL}
To: {to}
Subject: {subject}
Content-Type: text/html; charset="UTF-8"

<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN" "http://www.w3.org/TR/html4/loose.dtd">
<html>
<head>
<meta http-equiv="Content-Type" content="text/html; charset=UTF-8" />
</head>
<body>
{content}
</body>
</html>
"""
        with open("/tmp/foo", "w") as myfile:
            myfile.write(body_content)

        attachement_part = ""
        if attachement:
            if not os.path.exists(attachement):
                raise FileNotFoundError(f"File {attachement} not found")
            attachement_part = f" -F 'file=@{attachement};type=application/octet-string;encoder=base64' "
            cmd = f"""curl --url 'smtps://smtp.gmail.com:465' --ssl-reqd --mail-from '{self.SEND_FROM_EMAIL}' -H "Subject: {subject}" --mail-rcpt '{to}' --user '{self.SEND_FROM_EMAIL}:{password}' {attachement_part}  """

        else:
            cmd = f"""curl --url 'smtps://smtp.gmail.com:465' --ssl-reqd --mail-from '{self.SEND_FROM_EMAIL}' --mail-rcpt '{to}' --user '{self.SEND_FROM_EMAIL}:{password}' -T /tmp/foo  """

        print("Command to run:", cmd)
        if os.environ.get("SOTA_TEST"):
            print("Skipping email send during test")
            return

        result = ShellRunner().run_waiting(cmd)
        result = "Command run : " + cmd + "\n" + result
        return result

        

def main():
    import fire

    fire.Fire(EmailService)


if __name__ == "__main__":
    main(0)
