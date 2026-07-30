import pandas as pd

from db import get_connection


# ======================================================
# NEXT PAYMENT CODE
# ======================================================

def get_next_payment_code():

    conn = get_connection()

    cur = conn.cursor()

    cur.execute(
        """
        SELECT MAX(payment_id)
        FROM barrie.payments;
        """
    )

    result = cur.fetchone()[0]

    cur.close()
    conn.close()

    if result is None:
        return "PAY-000001"

    return f"PAY-{result + 1:06d}"


# ======================================================
# INSERT PAYMENT
# ======================================================

def insert_payment(
    purchase_id,
    payment_type_id,
    payment_date,
    payee_name,
    paid_by,
    payment_method,
    reference_number,
    amount_etb,
    amount_usd,
    exchange_rate,
    notes,
):

    payment_code = get_next_payment_code()

    conn = get_connection()

    cur = conn.cursor()

    cur.execute(
        """
        INSERT INTO barrie.payments (

            payment_code,
            purchase_id,
            payment_type_id,
            payment_date,
            payee_name,
            paid_by,
            payment_method,
            reference_number,
            amount_etb,
            amount_usd,
            exchange_rate,
            notes

        )

        VALUES (

            %s,
            %s,
            %s,
            %s,
            %s,
            %s,
            %s,
            %s,
            %s,
            %s,
            %s,
            %s

        );
        """,
        (
            payment_code,
            purchase_id,
            payment_type_id,
            payment_date,
            payee_name,
            paid_by,
            payment_method,
            reference_number,
            amount_etb,
            amount_usd,
            exchange_rate,
            notes,
        ),
    )

    conn.commit()

    cur.close()
    conn.close()
# ======================================================
# GET ALL PAYMENTS
# ======================================================

def get_all_payments():

    conn = get_connection()

    query = """
        SELECT

            p.payment_id,
            p.payment_code,
            pu.purchase_code,
            pt.payment_type_name,
            p.payment_date,
            p.payee_name,
            p.paid_by,
            p.payment_method,
            p.reference_number,
            p.amount_etb,
            p.amount_usd,
            p.exchange_rate,
            p.notes

        FROM barrie.payments p

        JOIN barrie.purchases pu
            ON p.purchase_id = pu.purchase_id

        JOIN barrie.payment_types pt
            ON p.payment_type_id = pt.payment_type_id

        ORDER BY
            p.payment_date DESC,
            p.payment_id DESC;
    """

    df = pd.read_sql(query, conn)

    conn.close()

    return df 

# ======================================================
# SEARCH PAYMENTS
# ======================================================

def search_payments(search):

    conn = get_connection()

    query = """
        SELECT

            p.payment_id,
            p.payment_code,
            pu.purchase_code,
            pt.payment_type_name,
            p.payment_date,
            p.payee_name,
            p.paid_by,
            p.payment_method,
            p.reference_number,
            p.amount_etb,
            p.amount_usd,
            p.exchange_rate,
            p.notes

        FROM barrie.payments p

        JOIN barrie.purchases pu
            ON p.purchase_id = pu.purchase_id

        JOIN barrie.payment_types pt
            ON p.payment_type_id = pt.payment_type_id

        WHERE

            p.payment_code ILIKE %s
            OR pu.purchase_code ILIKE %s
            OR p.payee_name ILIKE %s
            OR p.reference_number ILIKE %s

        ORDER BY
            p.payment_date DESC,
            p.payment_id DESC;
    """

    like = f"%{search}%"

    df = pd.read_sql(
        query,
        conn,
        params=(like, like, like, like),
    )

    conn.close()

    return df  

# ======================================================
# GET PAYMENT
# ======================================================

def get_payment(payment_id):

    conn = get_connection()

    cur = conn.cursor()

    cur.execute(
        """
        SELECT

            payment_id,
            payment_code,
            purchase_id,
            payment_type_id,
            payment_date,
            payee_name,
            paid_by,
            payment_method,
            reference_number,
            amount_etb,
            amount_usd,
            exchange_rate,
            notes

        FROM barrie.payments

        WHERE payment_id = %s;
        """,
        (payment_id,),
    )

    row = cur.fetchone()

    cur.close()
    conn.close()

    if row is None:
        return None

    return {
        "payment_id": row[0],
        "payment_code": row[1],
        "purchase_id": row[2],
        "payment_type_id": row[3],
        "payment_date": row[4],
        "payee_name": row[5],
        "paid_by": row[6],
        "payment_method": row[7],
        "reference_number": row[8],
        "amount_etb": row[9],
        "amount_usd": row[10],
        "exchange_rate": row[11],
        "notes": row[12],
    } 
# ======================================================
# UPDATE PAYMENT
# ======================================================

def update_payment(
    payment_id,
    purchase_id,
    payment_type_id,
    payment_date,
    payee_name,
    paid_by,
    payment_method,
    reference_number,
    amount_etb,
    amount_usd,
    exchange_rate,
    notes,
):

    conn = get_connection()

    cur = conn.cursor()

    cur.execute(
        """
        UPDATE barrie.payments

        SET

            purchase_id = %s,
            payment_type_id = %s,
            payment_date = %s,
            payee_name = %s,
            paid_by = %s,
            payment_method = %s,
            reference_number = %s,
            amount_etb = %s,
            amount_usd = %s,
            exchange_rate = %s,
            notes = %s,
            updated_at = CURRENT_TIMESTAMP

        WHERE payment_id = %s;
        """,
        (
            purchase_id,
            payment_type_id,
            payment_date,
            payee_name,
            paid_by,
            payment_method,
            reference_number,
            amount_etb,
            amount_usd,
            exchange_rate,
            notes,
            payment_id,
        ),
    )

    conn.commit()

    cur.close()
    conn.close()