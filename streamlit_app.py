import streamlit
import pandas as pd

streamlit.title('New Parents New Health Diner')

streamlit.header('Breakfast Menu')
streamlit.text('\N{bowl with spoon} Omega 3 & Blueberry Oatmeal')
streamlit.text('\N{leafy green} Kale, Spinach and Rocket Smoothie')
streamlit.text('\N{egg} Hard-boiled Egg on Wholewheat Toast')
streamlit.text('\N{avocado} Smashed Avocado on Toast')

streamlit.header('\N{banana} \N{grapes} Build your own fruit smoothies 🍓🍏')
my_fruit_list = pd.read_csv('https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt')
#add a pick list for selecting fruit
streamlit.multiselect('Pick some fruits: ' , list(my_fruit_list.index))
streamlit.dataframe(my_fruit_list)
