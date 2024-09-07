import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Function to generate the plot for the selected drug
def create_single_drug_plot(data, drug, color='#99004f'):
    # Get the value counts for the selected drug
    usage = data[drug].value_counts().sort_index()
    
    # Mapping of drug usage categories
    usage_texts = ['Never Used', 'Used Over a Decade Ago', 'Used in Last Decade', 
                   'Used Last Year', 'Used Last Month', 'Used Last Week', 'Used Last Day']
    
    # Define the positions for bars
    width = 0.35
    xpos = np.arange(len(usage), dtype='float64')

    fig, ax = plt.subplots(figsize=(10, 6))
    ax.bar(xpos, usage.values, width=width, color=color)

    # Add text labels on top of each bar
    rects = ax.patches
    for rect, usage_val in zip(rects, usage):
        x = rect.get_x() + rect.get_width() / 2
        y = rect.get_height() + 0.5
        ax.text(x, y, usage_val, ha='center', va='bottom', fontsize=9)

    # Add labels and title
    ax.set_ylim(bottom=0, top=max(usage) + 10)
    ax.set_xticks(xpos)
    ax.set_xticklabels(usage_texts[:len(usage)])
    ax.tick_params(axis='y', labelsize=10)
    ax.tick_params(axis='x', labelrotation=15, labelsize=10, width=0.7)
    ax.set_title(f"Usage of {drug}")
    st.pyplot(fig)

# Main function to handle user selection and plot generation
def generate_drug_plot(data):
    # Dropdown for drug selection
    drug = st.selectbox('Select a drug to visualize', [
        'Caff', 'Alcohol', 'Cannabis', 'Nicotine', 'Amphet', 'Mushrooms', 'Benzos', 
        'Ecstacy', 'Coke', 'LSD', 'Legalh', 'Amyl', 'Meth', 'VSA', 'Ketamine', 'Heroin', 'Crack'
    ])
    
    # Button to trigger the plot display
    if st.button('Show Drug Inventory'):
        create_single_drug_plot(data, drug)

# Streamlit app title
st.title('MAX Hospital Drug inventory and tracking')

# Read the dataset
plot_data = pd.read_csv(r"drug_consumption.csv")

# Preprocessing: replace 'CL' prefixes with numerical categories
for column in plot_data.loc[:, 'Alcohol':'VSA']:
    plot_data[column] = plot_data[column].str.replace('CL', '').astype(int)

# Drop unnecessary columns
plot_data.drop(columns=['ID', 'Choc', 'Semer'], inplace=True)

# Generate plot based on selected drug and button click
generate_drug_plot(plot_data)
