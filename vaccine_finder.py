from config import AGES, PINCODES, DAYS
from cowin.cowin import CoWin
from hooks.slack import SlackNotification


def run():
    cw = CoWin()
    slack = SlackNotification()

    # Returns the details of states
    # result = cw.get_state_list()
    # print(result)

    # # Returns the details of districts for a given state
    # # in this case with state_id 2
    # result = cw.get_districts_list(2)
    # print(result)
    #
    # # Returns the details of districts for a given state with
    # # open slots for age group 45 and free payment for vaccination.
    # result = cw.check_by_district_id(district=651, age=45, payment="free")
    # print(result)

    # Returns the details of slots available in area with
    # pincode 462003
    result = cw.check_by_pincodes(pincodes=PINCODES, ages=AGES, payment='Free', days=DAYS)
    slack.send(centers=result)
    print(result)
