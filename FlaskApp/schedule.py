from hashlib import md5
from getpass import getuser


from crontab import CronTab
from logger import get_logger

user = getuser()
my_cron = CronTab(user=user)
logger = get_logger(__name__)


def create(domain, email, hours=None, minutes=None):
    command = f"python3 /opt/In0ri/main.py {domain} {email}"
    comment = md5(domain.encode()).hexdigest()
    check = 0
    for job in my_cron:
        if job.comment == comment:
            check = 1
    if check == 1:
        logger.info("This domain is avaliable!")
    else:
        job = my_cron.new(command=command, comment=comment)
        if hours is not None:
            job.hour.every(hours)
        if minutes is not None:
            job.minute.every(minutes)
        my_cron.write(user=user)
        logger.info("%s", job.is_valid())


def edit(domain, email, hours=None, minutes=None):
    command = f"python3 /opt/In0ri/main.py {domain} {email}"
    comment = md5(domain.encode()).hexdigest()
    check = 0
    for job in my_cron:
        if job.comment == comment:
            check = 1
            my_cron.remove(job)
            job = my_cron.new(command=command, comment=comment)
            if hours is not None:
                job.hour.every(hours)
            if minutes is not None:
                job.minute.every(minutes)
            my_cron.write(user=user)
            logger.info("Sucessfull!")
    if check == 0:
        logger.warning("Domain not found!")


def delete(domain):
    comment = md5(domain.encode()).hexdigest()
    check = 0
    for job in my_cron:
        if job.comment == comment:
            check = 1
            my_cron.remove(job)
            my_cron.write(user=user)
            logger.info("Sucessfull!")
    if check == 0:
        logger.warning("Domain not found!")

