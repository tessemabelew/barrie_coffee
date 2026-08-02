from auth.session import is_logged_in

if not is_logged_in():

    st.warning("Please login.")

    st.stop()

import streamlit as st
from datetime import date

from repositories.payment_repository import (
    get_next_payment_code,
    insert_payment,
    get_all_payments,
    search_payments,
    get_payment,
    update_payment,
)

from repositories.purchase_repository import (
    get_purchase_dropdown,
)

from repositories.payment_type_repository import (
    get_payment_type_dropdown,
)


st.title("💰 Payment Management")

tab1, tab2, tab3 = st.tabs(
    [
        "➕ Add Payment",
        "📋 Payment List",
        "✏ Edit Payment",
    ]
)

# ======================================================
# ADD PAYMENT
# ======================================================

with tab1:

    st.subheader("➕ Add Payment")

    purchase_df = get_purchase_dropdown()
    payment_type_df = get_payment_type_dropdown()

    purchase_options = purchase_df["purchase_code"].tolist()
    payment_type_options = payment_type_df["payment_type_name"].tolist()

    payment_code = get_next_payment_code()

    with st.form("payment_form", clear_on_submit=True):

        left, right = st.columns(2)

        with left:

            st.text_input(
                "Payment Code",
                value=payment_code,
                disabled=True,
            )

            purchase = st.selectbox(
                "Purchase *",
                purchase_options,
            )

            payment_type = st.selectbox(
                "Payment Type *",
                payment_type_options,
            )

            payment_date = st.date_input(
                "Payment Date",
                value=date.today(),
            )

            payee_name = st.text_input(
                "Payee Name *",
            )

            paid_by = st.text_input(
                "Paid By *",
            )

        with right:

            payment_method = st.text_input(
                "Payment Method",
            )

            reference_number = st.text_input(
                "Reference Number",
            )

            amount_etb = st.number_input(
                "Amount (ETB)",
                min_value=0.0,
                format="%.2f",
            )

            amount_usd = st.number_input(
                "Amount (USD)",
                min_value=0.0,
                format="%.2f",
            )

            exchange_rate = st.number_input(
                "Exchange Rate",
                min_value=0.0,
                value=0.0,
                format="%.4f",
            )

            notes = st.text_area(
                "Notes",
            )

        submitted = st.form_submit_button(
            "💾 Save Payment",
            use_container_width=True,
        )
    if submitted:

        errors = []

        if not payee_name.strip():
            errors.append("Payee Name is required.")

        if not paid_by.strip():
            errors.append("Paid By is required.")

        if amount_etb <= 0 and amount_usd <= 0:
            errors.append("Enter ETB or USD amount.")

        if errors:

            for error in errors:
                st.error(error)

        else:

            purchase_id = int(
                purchase_df.loc[
                    purchase_df["purchase_code"] == purchase,
                    "purchase_id",
                ].iloc[0]
            )

            payment_type_id = int(
                payment_type_df.loc[
                    payment_type_df["payment_type_name"] == payment_type,
                    "payment_type_id",
                ].iloc[0]
            )

            insert_payment(
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
            )

            st.success("✅ Payment saved successfully!")

# ======================================================
# PAYMENT LIST
# ======================================================

with tab2:

    st.subheader("📋 Payment List")

    search_text = st.text_input(
        "🔍 Search Payments",
        placeholder="Search by Payment Code, Purchase Code, Payee Name...",
    )

    if search_text.strip():

        payment_df = search_payments(search_text)

    else:

        payment_df = get_all_payments()

    if payment_df.empty:

        st.info("No payment records found.")

    else:

        # Hide internal ID
        if "payment_id" in payment_df.columns:
            payment_df = payment_df.drop(columns=["payment_id"])

        # Rename columns
        payment_df = payment_df.rename(
            columns={
                "payment_code": "Payment Code",
                "purchase_code": "Purchase",
                "payment_type_name": "Payment Type",
                "payment_date": "Payment Date",
                "payee_name": "Payee",
                "paid_by": "Paid By",
                "payment_method": "Method",
                "reference_number": "Reference",
                "amount_etb": "Amount (ETB)",
                "amount_usd": "Amount (USD)",
                "exchange_rate": "Exchange Rate",
                "notes": "Notes",
                "created_at": "Created",
                "updated_at": "Updated",
            }
        )

        # Format currency columns
        if "Amount (ETB)" in payment_df.columns:
            payment_df["Amount (ETB)"] = payment_df["Amount (ETB)"].map(
                lambda x: f"{x:,.2f}" if x is not None else ""
            )

        if "Amount (USD)" in payment_df.columns:
            payment_df["Amount (USD)"] = payment_df["Amount (USD)"].map(
                lambda x: f"{x:,.2f}" if x is not None else ""
            )

        if "Exchange Rate" in payment_df.columns:
            payment_df["Exchange Rate"] = payment_df["Exchange Rate"].map(
                lambda x: f"{x:,.4f}" if x is not None else ""
            )

        st.dataframe(
            payment_df,
            use_container_width=True,
            hide_index=True,
        )

# ======================================================
# EDIT PAYMENT
# ======================================================

with tab3:

    st.subheader("✏ Edit Payment")

    payment_df = get_all_payments()

    if payment_df.empty:

        st.info("No payment records found.")

    else:

        payment_lookup = dict(
            zip(
            payment_df["payment_code"],
            payment_df["payment_id"],
            )
        )

        selected_payment = st.selectbox(
            "Select Payment",
            payment_lookup.keys(),
        )

        payment = get_payment(
            payment_lookup[selected_payment]
        )
        # Load dropdown data
        purchase_df = get_purchase_dropdown()
        payment_type_df = get_payment_type_dropdown()

        purchase_options = purchase_df["purchase_code"].tolist()
        payment_type_options = payment_type_df["payment_type_name"].tolist()

        # Determine which option should be pre-selected
        purchase_index = purchase_df[
            purchase_df["purchase_id"] == payment["purchase_id"]
        ].index[0]

        payment_type_index = payment_type_df[
            payment_type_df["payment_type_id"] == payment["payment_type_id"]
        ].index[0]

        with st.form("edit_payment_form"):

            left, right = st.columns(2)

            with left:

                st.text_input(
                    "Payment Code",
                    value=payment["payment_code"],
                    disabled=True,
                )

                purchase = st.selectbox(
                    "Purchase *",
                    purchase_options,
                    index=purchase_index,
                )

                payment_type = st.selectbox(
                    "Payment Type *",
                    payment_type_options,
                    index=payment_type_index,
                )

                payment_date = st.date_input(
                    "Payment Date",
                    value=payment["payment_date"],
                )

                payee_name = st.text_input(
                    "Payee Name *",
                    value=payment["payee_name"],
                )

                paid_by = st.text_input(
                    "Paid By *",
                    value=payment["paid_by"],
                )

            with right:

                payment_method = st.text_input(
                    "Payment Method",
                    value=payment["payment_method"] or "",
                )

                reference_number = st.text_input(
                    "Reference Number",
                    value=payment["reference_number"] or "",
                )

                amount_etb = st.number_input(
                    "Amount (ETB)",
                    min_value=0.0,
                    value=float(payment["amount_etb"] or 0),
                    format="%.2f",
                )

                amount_usd = st.number_input(
                    "Amount (USD)",
                    min_value=0.0,
                    value=float(payment["amount_usd"] or 0),
                    format="%.2f",
                )

                exchange_rate = st.number_input(
                    "Exchange Rate",
                    min_value=0.0,
                    value=float(payment["exchange_rate"] or 0),
                    format="%.4f",
                )

                notes = st.text_area(
                    "Notes",
                    value=payment["notes"] or "",
                )

            submitted = st.form_submit_button(
                "💾 Update Payment",
                use_container_width=True,
            )

            if submitted:

                errors = []

                if not payee_name.strip():
                    errors.append("Payee Name is required.")

                if not paid_by.strip():
                    errors.append("Paid By is required.")

                if amount_etb <= 0 and amount_usd <= 0:
                    errors.append("Enter ETB or USD amount.")

                if errors:

                    for error in errors:
                        st.error(error)

                else:

                    purchase_id = int(
                        purchase_df.loc[
                            purchase_df["purchase_code"] == purchase,
                            "purchase_id",
                        ].iloc[0]
                    )

                    payment_type_id = int(
                        payment_type_df.loc[
                            payment_type_df["payment_type_name"] == payment_type,
                            "payment_type_id",
                        ].iloc[0]
                    )

                    update_payment(
                        payment["payment_id"],
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
                    )

                    st.success("✅ Payment updated successfully!")

        