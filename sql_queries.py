import psycopg2
from db import get_connection

import pandas as pd
import random

def get_spending(time_period, account_type):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(f"SELECT SUM(amount) FROM finance.{account_type}_spending "
                       "WHERE transaction_date >= date_trunc(%s, current_date)"
                       ,(time_period,))

        result = cursor.fetchone()
        return result[0] if result and result[0] else None
    except psycopg2.Error as e:
        print(f"Failed to get spending: {e}")
    finally:
        cursor.close()



def get_dw_hours(time_period):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT SUM(duration_minutes) FROM tracking.deep_work"
                       " WHERE date >= date_trunc (%s, CURRENT_DATE)"
                       ,(time_period,))

        result = cursor.fetchone()
        return result[0] if result and result[0] else None

    except psycopg2.Error as e:
        print(f"Failed to get spending: {e}")
    finally:
        cursor.close()

def current_med_streak():
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("""SELECT streak_length
                        FROM tracking.meditation_streaks
                        WHERE last_date = CURRENT_DATE OR last_date = CURRENT_DATE -1
                        ORDER BY last_date DESC
                        LIMIT 1
                        """)

        result = cursor.fetchone()
        return result[0] if result and result[0] else None

    except psycopg2.Error as e:
        print(f"Failed to get spending: {e}")
    finally:
        cursor.close()

def get_approaches(time_period):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT COUNT(*) FROM tracking.approaches"
                       " WHERE date >= date_trunc (%s, CURRENT_DATE)"
                       ,(time_period,))

        result = cursor.fetchone()
        return result[0] if result and result[0] else None

    except psycopg2.Error as e:
        print(f"Failed to get spending: {e}")
    finally:
        cursor.close()

def get_meditation_dates():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT DISTINCT date FROM tracking.meditation ORDER BY date")
    return [row[0] for row in cur.fetchall()]


def get_days_meditated(time_period):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT COUNT(DISTINCT date) FROM tracking.meditation "
                    "WHERE date >= date_trunc(%s, CURRENT_DATE)",
                       (time_period,))


        result = cursor.fetchone()
        return result[0] if result and result[0] else None

    except psycopg2.Error as e:
        print(f"Failed to get spending: {e}")
    finally:
        cursor.close()

def get_dw_hours_day():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
    SELECT date, SUM(duration_minutes)
    FROM tracking.deep_work
    GROUP BY date
    """)
    return [row for row in cursor.fetchall()]


def need_review():
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT description, merchant_name, category "
                       "FROM finance.merchants WHERE needs_review = TRUE")

        results = [row for row in cursor.fetchall()]
        return results if results else None

    except psycopg2.Error as e:
        print(f"Failed to get spending: {e}")
        return None
    finally:
        cursor.close()
