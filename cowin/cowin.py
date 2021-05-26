import datetime
from datetime import date, timedelta
from typing import List

from cowin.utils.logit import get_logger
from cowin.utils.RESTAPI import RestAPI as API


class CoWin(API):
    def __init__(self):
        self.logger = get_logger(__name__)
        cowin_base_url = "https://cdn-api.co-vin.in/api/v2/"
        self.urls = {
            "states":  ("get", f"{cowin_base_url}admin/location/states"),
            "districts":  ("get", f"{cowin_base_url}admin/location/districts/" +
                           "{criteria}"),
            "pincode": ("get", f"{cowin_base_url}" +
                        "appointment/sessions/public/calendarByPin?pincode=" +
                        "{criteria}&date={today}"),
            "district": ("get", f"{cowin_base_url}" +
                         "appointment/sessions/public/calendarByDistrict?district_id=" +
                         "{criteria}&date={today}")
        }

    def call_cowin(self, criteria_type, criteria, filters=None, date_=None):
        self.logger.info(f"{criteria_type}, {criteria}, {filters}, {date_}")
        today = date_
        if not today:
            today = date.today().strftime("%d-%m-%Y")
        flg, result = self.call(self.urls[criteria_type][0],
                                self.urls[criteria_type][1].format(criteria=criteria,
                                                                   today=today))
        self.logger.debug(f"API call result: {flg}, {result}")
        if criteria_type in ("pincode", "district"):
            ret_val = result['centers'] if flg else result
        else:
            ret_val = result[criteria_type] if flg else result
        self.logger.debug(f"returning {ret_val}")
        return ret_val

    # Lets apply filter
    def apply_filter(self, centers, age, payment="any"):
        selected_centers = []
        self.logger.debug(f"Searching for age: {age} - {payment}")
        for center in centers:
            _sessions = []
            self.logger.debug(f"Searching for age: {age} in center: {center['name']}")
            if payment.lower() != center['fee_type'].lower():
                continue

            for session in (center.get('sessions', False)):
                if session['available_capacity'] > 0:
                    if int(session['min_age_limit']) == int(age):
                        self.logger.debug(
                            f"Adding in center {center['name']} session: {session}")
                        _sessions.append(session)
            if _sessions:
                center['sessions'] = _sessions
                selected_centers.append(center)
        return selected_centers

    def check_by_pincodes(self, pincodes: List[int], payment="any", ages: List[int]=None, days=None):
        if not ages:
            ages = [45]
        res = {}
        if not days:
            days = 1
        count = 0
        curr: datetime = datetime.datetime.today() + timedelta(3)
        count += 3
        while True:
            if count >= days:
                break
            if curr.weekday() >= 5:
                curr += timedelta(1)
                continue

            for x in pincodes:
                if x not in res:
                    res[x] = {}
                for a in ages:
                    if a not in res[x]:
                        res[x][a] = {}

                    res[x][a][curr.strftime("%d-%m-%Y")] = self.check_by_pincode(pincode=x, age=a, payment=payment, date_=curr.strftime("%d-%m-%Y"))
                    pass
                pass
            curr += timedelta(1)
            count += 1
            pass
        return res

    def check_by_pincode(self, pincode: int, age: int = 45, payment="any", date_=None):
        # centers = self.call_cowin("pincode", pincode, date_=date_)
        from cowin.dummy_resp import get_dummy_slots, get_dummy_no_slots
        centers = get_dummy_slots()
        if type(centers) is not list:
            return []
        result = self.apply_filter(centers, age, payment)
        return result

    def check_by_district_id(self, district: int, age: int = 45, payment="any"):
        centers = self.call_cowin("district", district)
        result = self.apply_filter(centers, age, payment)
        return result

    def get_state_list(self):
        return self.call_cowin("states", None)

    def get_districts_list(self, state_id):
        return self.call_cowin("districts", state_id)


# # Demo Usage
# if __name__ == "__main__":
#     cw = CoWin()
#     result = cw.check_by_pincode(462003)
#     print(result)
#     print("*"*20)
#     result = cw.check_by_district_id(650)
#     print(result)
#     result = cw.get_state_list()
#     print(result)
#     result = cw.get_districts_list(2)
#     print(result)
