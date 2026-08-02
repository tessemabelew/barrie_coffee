import streamlit as st
from auth.session import is_logged_in

if not is_logged_in():

    st.warning("Please login.")

    st.stop()



from repositories.coffee_form_repository import (
    insert_coffee_form,
    get_all_coffee_forms,
    search_coffee_forms,
    get_coffee_form,
    update_coffee_form,
    deactivate_coffee_form,
)

# ==========================================================
# PAGE TITLE
# ==========================================================

st.set_page_config(
    page_title="Coffee Forms",
    page_icon="☕",
    layout="wide",
)

st.title("☕ Coffee Forms")

# ==========================================================
# SESSION STATE
# ==========================================================

if "coffee_form_success" not in st.session_state:
    st.session_state.coffee_form_success = ""

if st.session_state.coffee_form_success:

    st.success(st.session_state.coffee_form_success)

    st.session_state.coffee_form_success = ""

# ==========================================================
# TABS
# ==========================================================

tab_add, tab_list, tab_edit = st.tabs(
    [
        "➕ Add Coffee Form",
        "📋 Coffee Form List",
        "✏ Edit Coffee Form",
    ]
)

# ==========================================================
# ADD COFFEE FORM
# ==========================================================

with tab_add:

    st.subheader("Add Coffee Form")

    with st.form("add_coffee_form"):

        coffee_form_name = st.text_input(
            "Coffee Form Name",
            placeholder="Example: Cherry",
        )

        description = st.text_area(
            "Description",
            placeholder="Optional description",
        )

        submitted = st.form_submit_button("Save")

        if submitted:

            if coffee_form_name.strip() == "":

                st.warning("Coffee Form Name is required.")

            else:

                try:

                    insert_coffee_form(
                        coffee_form_name=coffee_form_name.strip(),
                        description=description.strip(),
                    )

                    st.success("Coffee Form added successfully.")

                except Exception as e:

                    if "duplicate" in str(e).lower():

                        st.warning(
                            "Coffee Form already exists."
                        )

                    else:

                        st.error(str(e))
# ==========================================================
# COFFEE FORM LIST
# ==========================================================

with tab_list:

    st.subheader("Coffee Form List")

    search = st.text_input(
        "Search Coffee Forms",
        placeholder="Search by coffee form name or description...",
    )

    try:

        if search.strip() == "":
            df = get_all_coffee_forms()
        else:
            df = search_coffee_forms(search)

        if df.empty:

            st.info("No Coffee Forms found.")

        else:

            display_df = df.rename(
                columns={
                    "coffee_form_id": "ID",
                    "coffee_form_name": "Coffee Form",
                    "description": "Description",
                    "active": "Active",
                }
            )

            st.dataframe(
                display_df,
                use_container_width=True,
                hide_index=True,
            )

            st.divider()

            selected_id = st.selectbox(
                "Select Coffee Form",
                df["coffee_form_id"],
                format_func=lambda x: df.loc[
                    df["coffee_form_id"] == x,
                    "coffee_form_name"
                ].values[0],
            )

            col1, col2 = st.columns(2)

            with col1:

                if st.button(
                    "Edit Selected",
                    use_container_width=True,
                ):

                    st.session_state.edit_coffee_form_id = selected_id

                    st.success(
                        "Open the 'Edit Coffee Form' tab."
                    )

            with col2:

                if st.button(
                    "Deactivate Selected",
                    type="secondary",
                    use_container_width=True,
                ):

                    deactivate_coffee_form(selected_id)

                    st.session_state.coffee_form_success = (
                        "Coffee Form deactivated successfully."
                    )

                    st.rerun()

    except Exception as e:

        st.error(str(e))

# ==========================================================
# EDIT COFFEE FORM
# ==========================================================

with tab_edit:

    st.subheader("Edit Coffee Form")

    if "edit_coffee_form_id" not in st.session_state:

        st.info(
            "Select a Coffee Form from the Coffee Form List tab."
        )

    else:

        coffee_form = get_coffee_form(
            st.session_state.edit_coffee_form_id
        )

        if coffee_form is None:

            st.error("Coffee Form not found.")

        else:

            with st.form("edit_coffee_form"):

                coffee_form_name = st.text_input(
                    "Coffee Form Name",
                    value=coffee_form["coffee_form_name"],
                )

                description = st.text_area(
                    "Description",
                    value=coffee_form["description"] or "",
                )

                col1, col2 = st.columns(2)

                with col1:

                    update_btn = st.form_submit_button(
                        "💾 Update",
                        use_container_width=True,
                    )

                with col2:

                    cancel_btn = st.form_submit_button(
                        "Cancel",
                        use_container_width=True,
                    )

                if cancel_btn:

                    del st.session_state["edit_coffee_form_id"]

                    st.rerun()

                if update_btn:

                    if coffee_form_name.strip() == "":

                        st.warning(
                            "Coffee Form Name is required."
                        )

                    else:

                        try:

                            update_coffee_form(
                                coffee_form_id=coffee_form["coffee_form_id"],
                                coffee_form_name=coffee_form_name.strip(),
                                description=description.strip(),
                            )

                            st.session_state.coffee_form_success = (
                                "Coffee Form updated successfully."
                            )

                            del st.session_state["edit_coffee_form_id"]

                            st.rerun()

                        except Exception as e:

                            if "duplicate" in str(e).lower():

                                st.warning(
                                    "Coffee Form already exists."
                                )

                            else:

                                st.error(str(e))                       