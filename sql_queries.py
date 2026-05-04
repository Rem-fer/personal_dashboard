import psycopg2
from db import get_connection



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



def get_dw_minutes(time_period):
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


def review_exists(week, year):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("""
            SELECT 1 FROM tracking.weekly_review
            WHERE week = %s AND year = %s
        """, (week, year))
        return cursor.fetchone() is not None
    except Exception as e:
        print(f"Error checking review: {e}")
        return False
    finally:
        cursor.close()



def save_metrics_for_review(week, year, dw, med, approaches, spending):
    if not review_exists(week,year):
        conn = None
        try:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO tracking.weekly_review (week, year, deep_work_mins, meditation_days, approaches, spending)
                VALUES (%s, %s, %s, %s, %s, %s)
                ON CONFLICT (week, year) DO UPDATE SET
                    deep_work_mins = EXCLUDED.deep_work_mins,
                    meditation_days = EXCLUDED.meditation_days,
                    approaches = EXCLUDED.approaches,
                    spending = EXCLUDED.spending
            """, (week, year, dw, med, approaches, spending))
            conn.commit()
            return True
        except Exception as e:
            print(f"Error saving weekly review: {e}")
            return False
        finally:
            if conn:
                conn.close()
    else:
        print(f"Review already submitted for week {week}, skipping metric update")
        return False

def save_weekly_review_text(week, year, plus, minus, next_, next_focus):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("""
            UPDATE tracking.weekly_review
            SET plus = %s, minus = %s, next = %s, next_focus = %s
            WHERE week = %s AND year = %s
        """, (plus, minus, next_,next_focus, week, year))
        conn.commit()
        return True
    except Exception as e:
        print(f"Error saving review text: {e}")
        return False
    finally:
        cursor.close()

def get_weekly_review(week, year):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("""
            SELECT deep_work_mins, meditation_days, approaches, spending::FLOAT
            FROM tracking.weekly_review
            WHERE year = %s AND week = %s
        """, (year, week))
        results = cursor.fetchone()
        return results if results else None
    except Exception as e:
        print(f"Error getting weekly review: {e}")
        return None
    finally:
        cursor.close()

def get_week_focus(year,week):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("""
            SELECT next_focus
            FROM tracking.weekly_review
            WHERE year = %s AND week = %s
        """, (year, week))
        result = cursor.fetchone()
        return result[0] if result and result[0] else None
    except Exception as e:
        print(f"Error getting weekly review: {e}")
        return None
    finally:
        cursor.close()

def review_text_submitted(week, year):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("""
            SELECT plus FROM tracking.weekly_review
            WHERE week = %s AND year = %s
        """, (week, year))
        row = cursor.fetchone()
        return row is not None and row[0] is not None
    except Exception as e:
        print(f"Error checking review: {e}")
        return False
    finally:
        cursor.close()

print(review_text_submitted(18,2026))


