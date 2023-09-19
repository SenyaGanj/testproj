import subprocess
import smtplib
import logging
from django.core.mail import send_mail
from django.conf import settings
from main.celery import app
from fileman.models import Log


def get_report(file_path: str) -> str:
    # flake8 has only legacy python api, so I decided to do just syscall
    cmd = ['flake8', file_path]
    # TODO: it's better to set here timeout, but maybe next time =)
    return subprocess.run(cmd, capture_output=True, text=True).stdout


@app.task
def check_new_files():
    logs = Log.objects.filter(status=Log.STATUS_NEW)
    log_pks = logs.values_list('pk', flat=True)
    logs.update(status=Log.STATUS_PROCESS)
    for log_pk in log_pks:
        check_new_file.delay(log_pk)


@app.task(default_retry_delay=60)
def check_new_file(log_pk: int):
    log = Log.objects.select_related('file', 'file__created_by').get(pk=log_pk)

    result = get_report(log.file.file.path)
    Log.objects.filter(pk=log.pk).update(result=result, status=Log.STATUS_DONE)

    send_report_mail.delay(log.pk, log.file.created_by.email, result)


@app.task
def send_report_mail(log_pk: int, email_to: str, result: str):
    log = Log.objects.select_related('file').get(pk=log_pk)

    try:
        send_mail(
            f'File {log.file.file.name} testing result',
            result,
            settings.DEFAULT_FROM_EMAIL,
            [email_to]
        )

        log.update(is_sent_to_email=True)
    except smtplib.SMTPException as ex:
        logging.exception(ex)

