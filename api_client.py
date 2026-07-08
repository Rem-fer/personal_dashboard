import requests

BASE_URL = "https://personalapi-production.up.railway.app/"
# BASE_URL = "http://127.0.0.1:8000/"


#----------OVERVIEW----------#

def get_spending(time_period: str, acc_type: str):
    response = requests.get(
        f"{BASE_URL}spending",
            params={"time_period": time_period, "acc_type": acc_type}
        )
    return  response.json() or 0


def get_dw_minutes(time_period: str):
    response = requests.get(
        f"{BASE_URL}deep_work",
            params={"time_period": time_period}
        )
    return response.json()

def get_days_meditated(time_period: str):
    response = requests.get(
        f"{BASE_URL}meditation",
            params={"time_period": time_period}
        )
    return response.json()

def get_approaches(time_period: str):
    response = requests.get(
        f"{BASE_URL}approaches",
            params={"time_period": time_period}
        )
    return response.json()

def get_week_focus(year:int, week_num:int):
    response = requests.get(
        f"{BASE_URL}focus",
            params={"year": year, "week_num": week_num}
        )
    return response.json()


def save_metrics_for_review(week, year, dw, med, approaches, spending):
    response = requests.post(
        f"{BASE_URL}metrics",
        json={
            "week": week,
            "year": year,
            "dw": dw,
            "med": med,
            "approaches": approaches,
            "spending": spending
        }
    )
    return response.status_code == 200

#--------------FINANCES-------------#

def get_balance_w_labels():
    response = requests.get(f"{BASE_URL}/banking/balances")
    return response.json()

def need_review():
    response = requests.get(f"{BASE_URL}/banking/need_review")
    return response.json()

#-----------TRACKING----------#
def current_med_streak():
    response = requests.get(f"{BASE_URL}meditation/streak")
    return response.json()

def get_meditation_dates():
    response = requests.get(f"{BASE_URL}meditation/dates")
    return response.json()


def get_dw_per_day():
    response = requests.get(f"{BASE_URL}deep_work/per_day")
    return response.json()

#--------REVIEW FORM----------#
def get_weekly_review_metrics(week,year):
    response = requests.get(
        f"{BASE_URL}review/metrics",
        params={"week": week, "year": year}
    )
    return response.json().get("value") or {}


def review_exists(week, year):
    response = requests.get(
        f"{BASE_URL}review/review-exists",
        params={"week": week, "year": year}
    )
    return response.json() or {}

def review_text_submitted(week, year):
    response = requests.get(
        f"{BASE_URL}review/submitted",
        params={"week": week, "year": year}
    )
    return response.json() or {}


def generate_weekly_focus(plus, minus, next_):
    response = requests.post(
        f"{BASE_URL}generate-focus",
        json={"plus":plus, "minus": minus, "next_": next_}
    )
    return response.json()

def save_weekly_review_text(week, year, plus, minus, next_, next_focus):
    response = requests.post(
        f"{BASE_URL}review/save-text",
        json={
            "week": week,
            "year": year,
            "plus": plus,
            "minus": minus,
            "next_": next_,
            "next_focus": next_focus
        }
    )
    return response.status_code == 200




