import streamlit as st
from sql_queries import get_weekly_review
from llm import generate_weekly_focus
from datetime import datetime,date
import sql_queries as sq

def display_metrics(week,year):
    weekly_metrics = get_weekly_review(week, year)
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


#----------DASHBOARD---------#
st.markdown("# Weekly review")


st.markdown(f"Current Week: {datetime.now().isocalendar()[1]}")
st.markdown(f"Current day: {datetime.now().strftime('%A')}")
year = datetime.now().isocalendar()[0]

st.markdown("## Review for week:")
with st.form("my_form 🗒️"):
    week_num = st.number_input("Week", min_value=1, max_value=52, value=datetime.now().isocalendar()[1])
    submitted = st.form_submit_button("Submit")
    if submitted:

        st.markdown(f"### Metrics for week {week_num} 📏")
        # week_num = st.number_input("Week", min_value=1, max_value=52, value=datetime.now().isocalendar()[1])

        if not sq.review_exists(week_num,year):
            st.markdown(f"Review Metrics not submitted for week {week_num}")
        else:
            # Metrics
            display_metrics(week_num,year)


#-------Plus, Minus, Next-------#
st.markdown("## Plus, Minus Next")
st.markdown("### Review you week ✍🏻")
st.markdown("---")

if sq.review_exists(week_num,year):
    if not sq.review_text_submitted(week_num, year):
        plus = st.text_area("Plus")
        minus = st.text_area("Minus")
        next_ = st.text_area("Next")

        if st.button("Submit"):
            next_focus = generate_weekly_focus(plus, minus, next_)
            sq.save_weekly_review_text(week_num,year, plus, minus, next_,next_focus)
            st.markdown(f"Review for week {week_num} submitted")
    else:
        st.markdown(f"Week {week_num} review already completed")
else:
    st.markdown("Save metrics for review")