from auth.session import is_logged_in

if not is_logged_in():

    st.warning("Please login.")

    st.stop()

import streamlit as st

from repositories.payment_type_repository import (
    insert_payment_type,
    get_all_payment_types,
    search_payment_types,
    get_payment_type,
    update_payment_type,
    deactivate_payment_type
)

PAYMENT_TYPE = [	
    "Down Payment",	
    "Final Payment",	
    "Building Materials",	
    "Labor",	
    "Transportation",	
    "Warehouse Construction",	
    "Equipment",
]

PAYMENT_CATEGORIES = [
    "Coffee Purchase",
    "Operating Expense",
    "Capital Expenditure",
    "Other"
]

st.title("💳 Payment Types")

tab_add, tab_list, tab_edit = st.tabs(
    [
        "➕ Add Payment Type",
        "📋 Payment Type List",
        "✏ Edit Payment Type"
    ]
)

with tab_add:

    st.subheader("Add Payment Type")

    col1, col2 = st.columns(2)

    with col1:
        payment_type_name = st.selectbox(
            "Payment Type Name",
            PAYMENT_TYPE
        )

    with col2:
        payment_category = st.selectbox(
            "Payment Category",
            PAYMENT_CATEGORIES
        )

    description = st.text_area(
        "Description",
        height=120
    )

    st.write("")

    save = st.button(
        "💾 Save Payment Type",
        type="primary"
    )

    if save:

        if payment_type_name == "":

            st.warning("Payment Type Name is required.")

        else:

            try:

                payment_type_id = insert_payment_type(
                    payment_type_name,
                    payment_category,
                    description
                )

                st.success(
                    f"Payment Type '{payment_type_name}' saved successfully."
                )

                st.rerun()

            except Exception as e:

                if "payment_types_payment_type_name_key" in str(e):

                    st.warning(
                        f"Payment Type '{payment_type_name}' already exists."
                    )

                else:

                    st.error(e)

with tab_list:
    

    st.subheader("📋 Payment Type List")

    search = st.text_input(
        "🔍 Search",
        placeholder="Search by Payment Type or Category..."
    )

    if search:

        df = search_payment_types(search)

    else:

        df = get_all_payment_types()

    df["active"] = df["active"].map(
        {
            True: "✅ Active",
            False: "❌ Inactive"
        }
    )
    df.columns = [
        "ID",
        "Payment Type",
        "Category",
        "Description",
        "Status"
    ]

    st.dataframe(

    df,

    use_container_width=True,

    hide_index=True,

    column_config={

        "ID": st.column_config.NumberColumn(
            width="small"
        ),

        "Payment Type": st.column_config.TextColumn(
            width="medium"
        ),

        "Category": st.column_config.TextColumn(
            width="medium"
        ),

        "Description": st.column_config.TextColumn(
            width="large"
        ),

        "Status": st.column_config.TextColumn(
            width="small"
        )
    }
)

with tab_edit:

    st.subheader("✏ Edit Payment Type")
    if st.session_state.pop("payment_type_updated", False):
        st.success("Payment Type updated successfully.")
    payment_types = get_all_payment_types()

    if payment_types.empty:

        st.info("No Payment Types found.")

    else:

        selected = st.selectbox(
            "Select Payment Type to Edit",
            payment_types["payment_type_id"],
            format_func=lambda x:
                payment_types.loc[
                    payment_types["payment_type_id"] == x,
                    "payment_type_name"
                ].values[0]
        )

        payment = get_payment_type(selected)

        col1, col2 = st.columns(2)

        with col1:

            payment_type_name = st.text_input(
                "Payment Type",
                value=payment["payment_type_name"]
            )

        with col2:

            PAYMENT_CATEGORIES = [
                "Coffee Purchase",
                "Overhead",
                "Operating Expense",
                "Capital Expenditure",
                "Other"
            ]

            category_index = PAYMENT_CATEGORIES.index(
                payment["payment_category"]
            )

            payment_category = st.selectbox(
                "Payment Category",
                PAYMENT_CATEGORIES,
                index=category_index
            )

        description = st.text_area(
            "Description",
            value=payment["description"],
            height=120
        )

        col1, col2 = st.columns(2)

        with col1:

            if st.button("💾 Update Payment Type", type="primary"):

                try:

                    update_payment_type(
                        selected,
                        payment_type_name,
                        payment_category,
                        description
                    )

                    st.session_state["payment_type_updated"] = True
                    st.rerun()

                except Exception as e:

                    if "payment_types_payment_type_name_key" in str(e):
                        st.warning("Payment Type already exists.")
                    else:
                        st.error(e)

        with col2:

            if st.button("🗑 Deactivate Payment Type"):

                deactivate_payment_type(selected)

                st.success("Payment Type deactivated.")
                st.rerun()
