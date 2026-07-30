import pandas as pd

from db import get_connection


# ======================================================
# HELPERS
# ======================================================

def get_next_purchase_code():
    """
    Generates the next purchase code.

    Example:
        PUR-000001
        PUR-000002
    """

    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        """
        SELECT
            MAX(purchase_id)
        FROM barrie.purchases;
        """
    )

    row = cur.fetchone()

    cur.close()
    conn.close()

    if row[0] is None:
        next_id = 1
    else:
        next_id = row[0] + 1

    return f"PUR-{next_id:06d}"


# ======================================================
# INSERT
# ======================================================

def insert_purchase(
    farmer_id,
    farm_id,
    purchase_date,
    coffee_form_id,
    weight_kg,
    price_per_kg,
    notes,
):
    """
    Inserts a new purchase.
    """

    purchase_code = get_next_purchase_code()

    total_amount = float(weight_kg) * float(price_per_kg)

    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        """
        INSERT INTO barrie.purchases
        (
            purchase_code,
            farmer_id,
            farm_id,
            purchase_date,
            coffee_form_id,
            weight_kg,
            price_per_kg,
            total_amount,
            notes
        )

        VALUES
        (
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
            purchase_code,
            farmer_id,
            farm_id,
            purchase_date,
            coffee_form_id,
            weight_kg,
            price_per_kg,
            total_amount,
            notes,
        ),
    )

    conn.commit()

    cur.close()
    conn.close()
# ======================================================
# SELECT
# ======================================================

def get_all_purchases():

    conn = get_connection()

    query = """
        SELECT

            p.purchase_id,
            p.purchase_code,

            f.first_name || ' ' || f.last_name AS farmer_name,

            fm.farm_name,

            cf.coffee_form_name,

            p.purchase_date,
            p.weight_kg,
            p.price_per_kg,
            p.total_amount,

            COALESCE(p.notes,'') AS notes

        FROM barrie.purchases p

        INNER JOIN barrie.farmers f
            ON p.farmer_id = f.farmer_id

        INNER JOIN barrie.farms fm
            ON p.farm_id = fm.farm_id

        INNER JOIN barrie.coffee_forms cf
            ON p.coffee_form_id = cf.coffee_form_id

        ORDER BY
            p.purchase_date DESC,
            p.purchase_code;
    """

    df = pd.read_sql(query, conn)

    conn.close()

    return df


def search_purchases(search):

    conn = get_connection()

    query = """
        SELECT

            p.purchase_id,
            p.purchase_code,

            f.first_name || ' ' || f.last_name AS farmer_name,

            fm.farm_name,

            cf.coffee_form_name,

            p.purchase_date,
            p.weight_kg,
            p.price_per_kg,
            p.total_amount,

            COALESCE(p.notes,'') AS notes

        FROM barrie.purchases p

        INNER JOIN barrie.farmers f
            ON p.farmer_id = f.farmer_id

        INNER JOIN barrie.farms fm
            ON p.farm_id = fm.farm_id

        INNER JOIN barrie.coffee_forms cf
            ON p.coffee_form_id = cf.coffee_form_id

        WHERE

            p.purchase_code ILIKE %s

            OR

            f.first_name || ' ' || f.last_name ILIKE %s

            OR

            fm.farm_name ILIKE %s

            OR

            cf.coffee_form_name ILIKE %s

        ORDER BY
            p.purchase_date DESC,
            p.purchase_code;
    """

    value = f"%{search}%"

    df = pd.read_sql(
        query,
        conn,
        params=(
            value,
            value,
            value,
            value,
        ),
    )

    conn.close()

    return df


def get_purchase(purchase_id):

    conn = get_connection()

    cur = conn.cursor()

    cur.execute(
        """
        SELECT

            purchase_id,
            purchase_code,
            farmer_id,
            farm_id,
            purchase_date,
            coffee_form_id,
            weight_kg,
            price_per_kg,
            total_amount,
            notes

        FROM barrie.purchases

        WHERE purchase_id = %s;
        """,
        (purchase_id,),
    )

    row = cur.fetchone()

    cur.close()
    conn.close()

    if row is None:
        return None

    return {
        "purchase_id": row[0],
        "purchase_code": row[1],
        "farmer_id": row[2],
        "farm_id": row[3],
        "purchase_date": row[4],
        "coffee_form_id": row[5],
        "weight_kg": row[6],
        "price_per_kg": row[7],
        "total_amount": row[8],
        "notes": row[9],
    }    

# ======================================================
# UPDATE
# ======================================================

def update_purchase(
    purchase_id,
    farmer_id,
    farm_id,
    purchase_date,
    coffee_form_id,
    weight_kg,
    price_per_kg,
    notes,
):
    """
    Updates an existing purchase.
    """

    total_amount = float(weight_kg) * float(price_per_kg)

    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        """
        UPDATE barrie.purchases

        SET

            farmer_id = %s,
            farm_id = %s,
            purchase_date = %s,
            coffee_form_id = %s,
            weight_kg = %s,
            price_per_kg = %s,
            total_amount = %s,
            notes = %s

        WHERE purchase_id = %s;
        """,
        (
            farmer_id,
            farm_id,
            purchase_date,
            coffee_form_id,
            weight_kg,
            price_per_kg,
            total_amount,
            notes,
            purchase_id,
        ),
    )

    conn.commit()

    cur.close()
    conn.close()


# ======================================================
# DEACTIVATE
# ======================================================

def deactivate_purchase(purchase_id):
    """
    Deactivates a purchase.

    NOTE:
    This requires an 'active' column in barrie.purchases.
    If you have not added that column yet, either:
        1. Add the active column, or
        2. Skip using this function for now.
    """

    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        """
        UPDATE barrie.purchases

        SET
            active = FALSE

        WHERE purchase_id = %s;
        """,
        (purchase_id,),
    )

    conn.commit()

    cur.close()
    conn.close()

def get_purchase_dropdown():

    conn = get_connection()

    query = """
        SELECT
            purchase_id,
            purchase_code
        FROM barrie.purchases
        ORDER BY purchase_code;
    """

    df = pd.read_sql(query, conn)

    conn.close()

    return df