import streamlit
import pandas
import requests
import snowflake.connector
from urllib.error import URLError

streamlit.title('New Parents New Health Diner')

streamlit.header('Breakfast Menu')
streamlit.text('\N{bowl with spoon} Omega 3 & Blueberry Oatmeal')
streamlit.text('\N{leafy green} Kale, Spinach and Rocket Smoothie')
streamlit.text('\N{egg} Hard-boiled Egg on Wholewheat Toast')
streamlit.text('\N{avocado} Smashed Avocado on Toast')

streamlit.header('\N{banana} \N{grapes} Build your own fruit smoothies 🍓🍏')
my_fruit_list = pandas.read_csv('https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt')
my_fruit_list = my_fruit_list.set_index('Fruit')

#add a pick list for selecting fruit
fruits_selected=streamlit.multiselect('Pick some fruits: ' , list(my_fruit_list.index), ['Avocado', 'Strawberries'])
fruits_to_show = my_fruit_list.loc[fruits_selected]

#display the table on the page
streamlit.dataframe(fruits_to_show)

def get_fruit_advice(fruit):
    fruityvice_response = requests.get("https://fruityvice.com/api/fruit/"+fruit_choice)
    fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())
    return fruityvice_normalized

streamlit.header("Fruityvice Fruit Advice!")
try:
    fruit_choice = streamlit.text_input('What fruit would you like information about?')
    if not fruit_choice:
      streamlit.error("Please select a fruit to get information")
    else:
      selected_fruit = get_fruit_advice(fruit_choice)
      streamlit.dataframe(selected_fruit)

except URLError as e:
    streamlit.error()
    

streamlit.header("View our fruit list - Add your favourites!")

def get_fruit_load_list():
    with my_cnx.cursor() as my_cur:
        my_cur.execute("SELECT * from fruit_load_list")
        my_cnx.close()
        return my_cur.fetchall()

if streamlit.button('Get fruit list'):
    my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
    my_data_rows = get_fruit_load_list()
    streamlit.dataframe(my_data_rows)


def insert_row_sf(new_fruit):
    with my_cnx.cursor() as my_cur:
        my_cur.execute("insert into fruit_load_list values ('"+new_fruit+"')")
    return "Thanks for adding: "+new_fruit
 
add_my_fruit = streamlit.text_input('What fruit would you like to add?') 
if streamlit.button("Add a fruit to the list"):
    my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
    back_from_function = insert_row_sf(add_my_fruit)
    my_cnx.close()
    streamlit.write('The user entered ', add_my_fruit)


