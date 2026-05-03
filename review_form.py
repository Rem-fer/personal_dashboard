import streamlit as st
from sql_queries import get_weekly_review
from llm import generate_weekly_focus
from datetime import datetime
import sql_queries as sq


#----------DASHBOARD---------#
st.markdown("# Weekly review")

st.markdown(f"Today: Week{datetime.now().isocalendar()[1]}, {datetime.now().strftime('%A')}")

st.markdown("## Review for:")
week_num = st.number_input("Week", min_value=1, max_value=52, value=datetime.now().isocalendar()[1])
year  = datetime.now().isocalendar()[0]
if sq.review_exists(week_num,year):
    st.markdown(f"")

# Metrics
weekly_metrics = get_weekly_review(week_num, year)
if weekly_metrics:
    dw_min, med_days, approaches, spending = weekly_metrics
    hours, minutes = divmod(dw_min, 60)

    values = [f"{hours}h {minutes}m", med_days, approaches, f"£{spending:,.2f}"]
    labels = ["Deep Work", "Meditation Days", "Approaches", "Spending"]

    cols = st.columns(len(labels))
    for col, label, value in zip(cols, labels, values):
        col.metric(label, value)

else:
    st.markdown("No data for that week")

st.markdown("## Plus, Minus Next")
st.markdown("---")
plus = st.text_area("Plus")
minus = st.text_area("Minus")
next_ = st.text_area("Next")

if st.button("Submit"):
    next_focus = generate_weekly_focus(plus, minus, next_)
    sq.save_weekly_review_text(week_num,year, plus, minus, next_,next_focus)
    st.markdown(f"Review for week {week_num} submitted")
