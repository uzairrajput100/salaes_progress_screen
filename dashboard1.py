import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Title and description
st.title("Sales Progress Dashboard")
st.markdown("""
This dashboard allows you to upload your sales data and visualize various metrics. 
Upload your file using the sidebar, and the sales performance will be displayed along with other insightful charts.
You can order one for your business and customize as per your requirements.
""")

# Sidebar header for file upload
st.sidebar.header("Upload your CSV, XLSX, XLS file")
uploaded_file = st.sidebar.file_uploader("", type="csv")

if uploaded_file is not None:
    # Read the uploaded CSV file
    data = pd.read_csv(uploaded_file, encoding= "ISO-8859-1")
    
    st.write("Data Preview")
    st.dataframe(data.head())

    # Perform some basic data analysis
    st.write("Sales Summary")
    st.write(data.describe())

    col1, col2 = st.columns((2))
    data["Order Date"]= pd.to_datetime(data["Order Date"])

    # Min and Max date selection
    startdate = pd.to_datetime(data["Order Date"]).min()
    enddate = pd.to_datetime(data["Order Date"]).max()

    with col1:
        date1 = pd.to_datetime(st.date_input('Start Date', startdate))
    with col2:
        date2 = pd.to_datetime(st.date_input('End Date', enddate))

    df = data[(data["Order Date"]>= date1) & (data["Order Date"]>= date2)].copy()

    
        # Check if required columns exist in the data
    if 'City' in data.columns and 'Sales' in data.columns:
            # Calculate top 20 cities by sales
        top_20_cities = data.groupby('City')['Sales'].sum().sort_values(ascending=False).head(20)
            
            # Display top 20 city sales performance
        st.write("Below Pie Chart shows the sales performance city wise to easily compare, this visualization helps alot for the directors to understand data in few seconds.")
            
            # Plotting the pie chart using Plotly
        fig_pie = px.pie(values=top_20_cities, names=top_20_cities.index, title='Indicating Top City Sales Performance and select/deselect cities too')
        st.plotly_chart(fig_pie)
            
        # Additional Plotly charts for more insights
        st.write("Sales Distribution Countrywide which helps in looking the sales for particular period")
        fig_bar = px.bar(data, x='City', y='Sales', title='Sales Distribution by City')
        st.plotly_chart(fig_bar)
        
        st.write("Below chart shows the Quarterly, Yealry report to analyze the business progress")
        if 'Ship Date' in data.columns:
            data['Ship Date'] = pd.to_datetime(data['Ship Date'])
            fig_line = px.scatter(data, x='Ship Date', y='Sales', title='Sales over Time', color='City')
            st.plotly_chart(fig_line)
        else:
            st.write("No date column found in the data to plot Sales over Time.")

        st.write("Below chart represents the total sales and the profit generated on it")
        if 'Category' in data.columns:
            fig = px.scatter(data, x='Sales', y='Profit', size='Sales', color='City',
                            hover_name='City', log_x=True, size_max=60, 
                            title='Sales vs Profit')
            st.plotly_chart(fig)
        else:
            st.write("No date column found in the data to plot Sales vs Profit.")
            
            st.write("Lets have a look on Category/Product wise Sales which reflects City to understand in deep")
        if 'Category' in data.columns:
            fig_sunburst = px.sunburst(data, path=['Category', 'City'], values='Sales', title='Sales by Category/Product and City')
            st.plotly_chart(fig_sunburst)
        else:
            st.write("No category column found in the data to plot Sales by Category.")

    else:
        st.error("The uploaded CSV file must contain 'city' and 'sales' columns.")
else:
    st.info("Please upload a CSV file to get started.")

# Footer
st.markdown(""" 
---
**Contact Us:** For any sales queries or support, feel free to reach out at +92 333 6611988 or email uzairrajput100@gmail.com
""")