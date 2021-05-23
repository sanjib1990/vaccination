import requests

from config import SLACK_HOOK_URL
from helper import DateTimeHelper


class SlackNotification(object):
    def __init__(self, **kwargs):
        pass

    def send(self, **kwargs):
        available_centers = kwargs['centers']
        attachments = []
        valid = False

        for pincode, age_center_map in available_centers.items():
            for age, centers in age_center_map.items():
                for x in centers:
                    available = 0
                    dose1 = 0
                    dose2 = 0
                    dates = []

                    for a in x.get('sessions', []):
                        available += int(a['available_capacity'])
                        dose1 += int(a['available_capacity_dose1'])
                        dose2 += int(a['available_capacity_dose2'])
                        dates.append(a['date'])
                        pass
                    if available > 0:
                        valid = True
                    tt = f"*PINCODE:* {pincode} *Age:* {age}\n"
                    tt += f"*{x.get('name')} ({' | '.join(dates)}):* {available}\n*Dose 1:* {dose1}\n*Dose 2:* {dose2}\n----------------\n"
                    attachments.append({
                        "blocks": [
                            {
                                "type": "section",
                                "fields": [
                                    {
                                        "type": "mrkdwn",
                                        "text": tt
                                    }
                                ]
                            }
                        ]
                    })
                    pass
                pass
            pass
        data = {
            "blocks": [
                {
                    "type": "header",
                    "text": {
                        "type": "plain_text",
                        "text": f"<@sanjib> COWIN SCHEDULE JOB RUN @ {DateTimeHelper.now()}"
                    }
                }],
            "attachments": attachments,
        }
        if not valid:
            return

        requests.post(SLACK_HOOK_URL, json=data)
        pass
