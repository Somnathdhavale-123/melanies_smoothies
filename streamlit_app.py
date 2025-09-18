# Import python packages
import streamlit as st

from snowflake.snowpark.context import get_active_session
from snowflake.snowpark.functions import col

# Write directly to the app
st.title(f":cup_with_straw: Customise your smoothies :cup_with_straw: {st.__version__}")
st.write(
  "Choose the fruit you want in your custom smoothies."
)



name_on_order = st.text_input('name on smoothie:')
st.write('Name on th smoothie will be', name_on_order)

session = get_active_session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col("FRUIT_NAME"))
#st.dataframe(data=my_dataframe, use_container_width=True)
ingredients_list= st.multiselect('choose upto 5 ingredients', my_dataframe)

if ingredients_list:  
    # join all items into a single string, separated by commas
    ingredients_string = ", ".join(ingredients_list)

    # Show the final string
    st.write(ingredients_string)

    # Prepare SQL insert statement
    my_insert_stmt = f"""
        INSERT INTO smoothies.public.orders (ingredients,name_on_order)
        VALUES (' """ + ingredients_string + """','""" +name_on_order + """')"""
    st.write(my_insert_stmt)
    time_to_insert = st.button('submit order')

    # run the insert here if you want
    # session.sql(my_insert_stmt).collect()

    if time_to_insert:
        session.sql(my_insert_stmt).collect()
        st.success(f"Your Smoothie is ordered, {name_on_order}!")

