
import streamlit as st 
import pandas as pd 
import numpy as np 
import requests
import matplotlib.pyplot as plt 
import matplotlib
matplotlib.use("Agg")
import seaborn as sns 


def main():
	custom_css = """
	<style>
	body {
		background-color: #F5E8E8; /* Set background color */
	}
	h1, h2, h3 {
		color: #FFC3A0; /* Set heading color */
	}
	</style>
	"""

	# Render the custom CSS
	st.markdown(custom_css, unsafe_allow_html=True)

	activities = ["Karakteristik","Grafik"]	
	choice = st.sidebar.selectbox("Select Activities",activities)

	if choice == 'Karakteristik':
		st.subheader("Exploratory Data Analysis")

		data = st.file_uploader("Upload a Dataset", type=["csv", "txt"])
		if data is not None:
			df = pd.read_csv(data)
			data_raw = df.copy()
			st.dataframe(df.head())
			string_columns = df.select_dtypes(include=['object']).columns
			for column in string_columns:
				unique_values = df[column].unique()
				mapping = {value: i for i, value in enumerate(unique_values)}
				df[column] = df[column].map(mapping)

			if st.checkbox("Show Shape"):
				st.write(df.shape)

			if st.checkbox("Summary"):
				st.write(data_raw.describe())

			if st.checkbox("Show Selected Columns"):
				all_columns = data_raw.columns.to_list()
				selected_columns = st.multiselect("Select Columns",all_columns)
				new_df = data_raw[selected_columns]
				st.dataframe(new_df)

			if st.checkbox("Show Value Counts"):
				string_columns = data_raw.select_dtypes(include=['object']).columns
				for column in string_columns:
					st.write(data_raw[column].value_counts())

			if st.checkbox("Correlation Plot(Matplotlib)"):
					plt.matshow(df.corr())
					st.pyplot()
				

			if st.checkbox("Correlation Plot(Seaborn)"):
				st.write(sns.heatmap(df.corr(),annot=True))
				st.pyplot()


			if st.checkbox("Pie Plot"):
				all_columns = data_raw.columns.to_list()
				column_to_plot = st.selectbox("Select 1 Column",all_columns)
				pie_plot = data_raw[column_to_plot].value_counts().plot.pie(autopct="%1.1f%%")
				st.write(pie_plot)
				st.pyplot()
			



	elif choice == 'Grafik':
		st.subheader("Data Visualization")
		data = st.file_uploader("Upload a Dataset", type=["csv", "txt", "xlsx"])
		if data is not None:
			df = pd.read_csv(data)
			df_raw = df.copy()
			st.dataframe(df.head())
			string_columns = df.select_dtypes(include=['object']).columns
			for column in string_columns:
				unique_values = df_raw[column].unique()
				mapping = {value: i for i, value in enumerate(unique_values)}
				df_raw[column] = df_raw[column].map(mapping)

			if st.checkbox("Show Value Counts"):
				string_columns = df.select_dtypes(include=['object']).columns
				for column in string_columns:
					value_counts = df[column].value_counts()
					st.write(f"Value Counts for {column}:")
					st.bar_chart(value_counts)	
		
			all_columns_names = df_raw.columns.tolist()
			type_of_plot = st.selectbox("Select Type of Plot",["area","bar","line","hist","box","kde"])
			selected_columns_names = st.multiselect("Select Columns For X Value",all_columns_names)
			
			if st.button("Generate Plot"):
				st.success("Generating Customizable Plot of {} for {} ".format(type_of_plot,selected_columns_names))

				if type_of_plot == 'area':
					cust_data = df_raw[selected_columns_names]
					st.area_chart(cust_data)
					st.write(cust_data)

				elif type_of_plot == 'bar':
					cust_data = df[selected_columns_names]
					st.bar_chart(cust_data)

				elif type_of_plot == 'line':
					cust_data = df[selected_columns_names]
					st.line_chart(cust_data)

				elif type_of_plot:
					cust_plot= df[selected_columns_names].plot(kind=type_of_plot)
					st.write(cust_plot)
					st.pyplot()
    


if __name__ == '__main__':
	main()