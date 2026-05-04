from datetime import datetime
import sql_queries as sq

now = datetime.now()
week = now.isocalendar()[1]
year = now.isocalendar()[0]

dw = sq.get_dw_minutes("week")
med = sq.get_days_meditated("week")
approaches = sq.get_approaches("week")
debit = sq.get_spending("week", "debit")
credit = sq.get_spending("week", "credit")
spending = (abs(debit) + credit) if debit and credit else 0

sq.save_metrics_for_review(week, year, dw, med, approaches, spending)
print(f"Weekly snapshot saved for week {week}")