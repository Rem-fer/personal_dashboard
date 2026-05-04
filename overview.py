import streamlit as st
import sql_queries as sq
from account_data import get_balance_w_labels
from datetime import datetime, date
import pandas as pd
from plotly_calplot import calplot


# Title
st.markdown("# Personal Dashboard")
st.button("🔄 Refresh")
tab1, tab2, tab3 = st.tabs(["Overview", "Finances", "Tracking"])


#----------OVERVIEW----------#
with tab1:
    year = datetime.now().isocalendar()[0]
    week_num= datetime.now().isocalendar()[1]
    st.markdown(f"## Week {week_num} 🗓️")

    # Key metrics
    col1,col2,col3,col4 = st.columns(4)

    with st.spinner("Loading..."):

        with col1:
            debit = sq.get_spending('week', "debit")
            credit = sq.get_spending("week", "credit")
            total = (abs(debit) + credit) if (debit is not None and credit is not None) else None
            st.metric(label="Spending", value=f"£{total:.2f}" if total is not None else "—")

        with col2:
            dw = sq.get_dw_minutes("week")
            hours, minutes = divmod(dw, 60) if dw is not None else (0, 0)
            st.metric(label="DW", value=f"{hours}h {minutes}m" if dw is not None else "—")

        with col3:
            days_meditated = sq.get_days_meditated('week')
            st.metric(label="Meditated this week",
                      value=f"{days_meditated}/{date.today().isoweekday() if days_meditated else '—'}")

        with col4:
            approaches = sq.get_approaches("week")
            st.metric(label="Approaches", value=approaches if approaches is not None else 0)

    last_cig_dt = datetime(2026,4,24)
    days = (datetime.now() - last_cig_dt).days
    st.metric(label="Days since last cig", value=days)

    # This week's focus
    st.markdown("### Focus")
    focus = sq.get_week_focus(year, week_num - 1)
    st.markdown(focus if focus else "No data")
    st.markdown("---")

    # Submit for review
    if st.button("Save metrics for review"):
        sq.save_metrics_for_review(week_num, datetime.now().isocalendar()[0], dw, days_meditated, approaches, total)


#--------------FINANCES-------------#

with tab2:
    st.markdown("## Finances 💷")
    st.markdown("### Balance")
    balances = get_balance_w_labels()
    st.metric(label="Net balance", value=sum(balances.values()))
    cols = st.columns(len(balances))
    for col, (item, value) in zip(cols, balances.items()):
        col.metric(label=item, value=f"{value:,.2f}")

    st.markdown("### Review transactions")
    needs_review = sq.need_review()
    st.table(needs_review)


#-----------TRACKING----------#
with tab3:
    st.markdown("## Tracking 🎯")

    st.markdown("### Meditation 🧘‍♂️")
    col1, col2 = st.columns(2)
    streak = sq.current_med_streak()
    med_dates = sq.get_meditation_dates()
    col1.metric("Current Streak", f"{streak or 0} days 🔥")
    col2.metric("Total Sessions", len(med_dates))

    med_df = pd.DataFrame({"date": med_dates, "value": 1})
    fig1 = calplot(
        data=med_df,
        x="date",
        y="value",
        dark_theme=True,
        gap=4,
        month_lines=True,
        colorscale=[[0, "#161b22"], [1, "#39d353"]],
        title="Meditation this year"
    )
    fig1.update_layout(
        height=180,
        margin=dict(t=40, b=0, l=0, r=0),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)"
    )
    st.plotly_chart(fig1, use_container_width=True)

    st.markdown("---")
    st.markdown("### Deep work 🧑‍💻")
    col1, col2 = st.columns(2)
    dw_minutes = sq.get_dw_minutes('year')
    hours, minutes = divmod(dw_minutes, 60)

    col1.metric(f"This year deep-work", f"{hours}h {minutes}m")
    avg_minutes = dw_minutes / week_num
    avg_hours, avg_min = divmod(avg_minutes, 60)
    col2.metric("Weekly average", f"{int(avg_hours)}h {int(avg_min)}m")

    dw_times = sq.get_dw_hours_day()
    df = pd.DataFrame(data=dw_times, columns=["date", "deep_work"])
    fig2 = calplot(data=df, x="date", y="deep_work")
    st.plotly_chart(fig2)

    st.markdown("### Approaches")
    st.metric("Approaches total", f"{sq.get_approaches('year') if sq.get_approaches('year') else 0}/100")


