from django.utils import timezone

def age(time):
        days=0
        hours=0
        minutes=0
        dif = (timezone.now() - time).total_seconds()
        while (dif > 86400):
            dif = dif - 86400
            days = days + 1
        while (dif > 3600):
            dif = dif - 3600
            hours = hours + 1
        while (dif > 60):
            dif = dif - 60
            minutes = minutes + 1


        if hours > 0:
            hours = f' {hours} H'
        else:
            hours = ''


        if minutes > 0:
            minutes = f' {minutes} M  '
        else:
            minutes = ''



        if days > 0:
            days = f'{days} D '
        else:
            days = ''


        return  days + hours + minutes 


