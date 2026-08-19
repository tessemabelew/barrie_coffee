import streamlit as st

from auth.session import is_logged_in
from services.onedrive_service import upload_file

if not is_logged_in():

    st.warning("Please login.")

    st.stop()


from datetime import date

from repositories.purchase_repository import (
    insert_purchase,
    get_next_purchase_code,
    get_all_purchases,
    search_purchases,
    get_purchase,
    update_purchase,
    deactivate_purchase,
)

from repositories.farmer_repository import get_farmer_dropdown
from repositories.farm_repository import get_farm_dropdown
from repositories.coffee_form_repository import get_coffee_form_dropdown


# ======================================================
# PAGE CONFIG
# ======================================================

# st.set_page_config(
#     page_title="Purchases",
#     page_icon="🛒",
#     layout="wide",
# )

st.title("🛒 Coffee Purchases")


# ======================================================
# SESSION STATE
# ======================================================

if "purchase_success" not in st.session_state:
    st.session_state.purchase_success = ""

if st.session_state.purchase_success:

    st.success(st.session_state.purchase_success)

    st.session_state.purchase_success = ""

if "purchase_update_success" not in st.session_state:
    st.session_state.purchase_update_success = ""

if st.session_state.purchase_update_success:

    st.success(st.session_state.purchase_update_success)

    st.session_state.purchase_update_success = ""


# ======================================================
# LOAD DROPDOWNS
# ======================================================

farmers = get_farmer_dropdown()
farms = get_farm_dropdown()
coffee_forms = get_coffee_form_dropdown()


# ======================================================
# TABS
# ======================================================

tab_add, tab_list, tab_edit = st.tabs(
    [
        "➕ Add Purchase",
        "📋 Purchase List",
        "✏ Edit Purchase",
    ]
)

# ======================================================
# ADD PURCHASE
# ======================================================

with tab_add:

    st.subheader("Add Purchase")

    purchase_code = get_next_purchase_code()

    with st.form("purchase_form"):

        st.text_input(
            "Purchase Code",
            value=purchase_code,
            disabled=True,
        )

        purchase_date = st.date_input(
            "Purchase Date",
            value=date.today(),
        )

        farmer = st.selectbox(
            "Farmer",
            farmers["farmer_id"],
            format_func=lambda x:
                farmers.loc[
                    farmers["farmer_id"] == x,
                    "farmer_name"
                ].values[0],
        )

        farm = st.selectbox(
            "Farm",
            farms["farm_id"],
            format_func=lambda x:
                farms.loc[
                    farms["farm_id"] == x,
                    "farm_name"
                ].values[0],
        )

        coffee_form = st.selectbox(
            "Coffee Form",
            coffee_forms["coffee_form_id"],
            format_func=lambda x:
                coffee_forms.loc[
                    coffee_forms["coffee_form_id"] == x,
                    "coffee_form_name"
                ].values[0],
        )

        col1, col2 = st.columns(2)

        with col1:

            weight = st.number_input(
                "Weight (kg)",
                min_value=0.0,
                step=0.50,
            )

        with col2:

            price = st.number_input(
                "Price per kg",
                min_value=0.0,
                step=0.50,
            )

        total = weight * price

        st.metric(
            "Total Amount",
            f"{total:,.2f} ETB"
        )

        notes = st.text_area(
            "Notes"
        )

        receipt = st.file_uploader(
            "Receipt / Invoice",
            type=["jpg", "jpeg", "png", "pdf"],
            help="Take a photo of the receipt or choose an existing file."
        )

        submitted = st.form_submit_button(
            "Save Purchase"
        )

        if submitted:

            try:

                purchase_id = insert_purchase(
                    farmer_id=farmer,
                    farm_id=farm,
                    purchase_date=purchase_date,
                    coffee_form_id=coffee_form,
                    weight_kg=weight,
                    price_per_kg=price,
                    notes=notes,
                )
                if receipt is not None:
                    st.info("Receipt detected")

                    file_bytes = receipt.getvalue()

                    filename = f"{purchase_code}_{purchase_id}_{receipt.name}"

                    result = upload_file(
                        file_bytes=file_bytes,
                        filename=filename
                    )
                    st.success("Upload completed")
                    st.write(result)
                st.session_state.purchase_success = (
                    "Purchase saved successfully."
                )

                st.rerun()

            except Exception as e:

                st.error(str(e))
# ======================================================
# PURCHASE LIST
# ======================================================

with tab_list:

    st.subheader("Purchase List")

    search = st.text_input(
        "Search Purchase",
        placeholder="Purchase Code, Farmer, Farm..."
    )

    if search.strip():
        purchases = search_purchases(search)
    else:
        purchases = get_all_purchases()

    if purchases.empty:

        st.info("No purchases found.")

    else:

        # Hide internal ID
        purchases = purchases.drop(columns=["purchase_id"])

        # Format currency
        purchases["price_per_kg"] = purchases["price_per_kg"].apply(
            lambda x: f"{x:,.2f} ETB"
        )

        purchases["total_amount"] = purchases["total_amount"].apply(
            lambda x: f"{x:,.2f} ETB"
        )

        # Rename columns
        purchases = purchases.rename(
            columns={
                "purchase_code": "Purchase Code",
                "farmer_name": "Farmer",
                "farm_name": "Farm",
                "coffee_form_name": "Coffee Form",
                "purchase_date": "Date",
                "weight_kg": "Weight (kg)",
                "price_per_kg": "Price/kg",
                "total_amount": "Total",
                "notes": "Notes",
            }
        )

        # Reorder columns
        purchases = purchases[
            [
                "Purchase Code",
                "Date",
                "Farmer",
                "Farm",
                "Coffee Form",
                "Weight (kg)",
                "Price/kg",
                "Total",
                "Notes",
            ]
        ]

        st.dataframe(
            purchases,
            use_container_width=True,
            hide_index=True,
        )
# ======================================================
# EDIT PURCHASE
# ======================================================

with tab_edit:

    st.subheader("Edit Purchase")

    purchases = get_all_purchases()

    if purchases.empty:

        st.info("No purchases found.")

    else:

        purchase_id = st.selectbox(
            "Select Purchase",
            purchases["purchase_id"],
            format_func=lambda x:
                purchases.loc[
                    purchases["purchase_id"] == x,
                    "purchase_code"
                ].values[0],
        )

        purchase = get_purchase(purchase_id)

        if purchase is None:
            st.error("Purchase not found.")
            st.stop()

        with st.form("edit_purchase"):

            purchase_date = st.date_input(
                "Purchase Date",
                value=purchase["purchase_date"],
            )

            farmer = st.selectbox(
                "Farmer",
                farmers["farmer_id"],
                index=farmers.index[
                    farmers["farmer_id"] == purchase["farmer_id"]
                ][0],
                format_func=lambda x:
                    farmers.loc[
                        farmers["farmer_id"] == x,
                        "farmer_name"
                    ].values[0],
            )

            farm = st.selectbox(
                "Farm",
                farms["farm_id"],
                index=farms.index[
                    farms["farm_id"] == purchase["farm_id"]
                ][0],
                format_func=lambda x:
                    farms.loc[
                        farms["farm_id"] == x,
                        "farm_name"
                    ].values[0],
            )

            coffee_form = st.selectbox(
                "Coffee Form",
                coffee_forms["coffee_form_id"],
                index=coffee_forms.index[
                    coffee_forms["coffee_form_id"] ==
                    purchase["coffee_form_id"]
                ][0],
                format_func=lambda x:
                    coffee_forms.loc[
                        coffee_forms["coffee_form_id"] == x,
                        "coffee_form_name"
                    ].values[0],
            )

            weight = st.number_input(
                "Weight (kg)",
                value=float(purchase["weight_kg"])
            )

            price = st.number_input(
                "Price per kg",
                value=float(purchase["price_per_kg"])
            )

            total = weight * price

            st.metric(
                "Total Amount",
                f"{total:,.2f} ETB"
            )

            notes = st.text_area(
                "Notes",
                value=purchase["notes"] or ""
            )

            col1, col2 = st.columns(2)

            with col1:

                update_btn = st.form_submit_button(
                    "Update Purchase"
                )

            with col2:

                deactivate_btn = st.form_submit_button(
                    "Deactivate Purchase"
                )

            # ==========================================
            # BUTTON ACTIONS
            # ==========================================

            if update_btn:

                update_purchase(
                    purchase_id=purchase_id,
                    farmer_id=farmer,
                    farm_id=farm,
                    purchase_date=purchase_date,
                    coffee_form_id=coffee_form,
                    weight_kg=weight,
                    price_per_kg=price,
                    notes=notes,
                )

                st.session_state.purchase_update_success = (
                    "Purchase updated successfully."
                )

                st.rerun()

            if deactivate_btn:
                if st.checkbox("I confirm I want to deactivate this purchase"):
                    deactivate_purchase(purchase_id)

                    st.session_state.purchase_update_success = (
                        "Purchase deactivated successfully."
                    )

                    st.rerun()
                 