# Jeesum680 📊

*Jeesum680* is a lightweight and easy-to-use Python library built to accelerate Exploratory Data Analysis (EDA) and preliminary dataset inspection for data science projects. It wraps essential Pandas, NumPy, Seaborn, and Matplotlib utilities to help you quickly understand the structure, quality, and relationships within your dataset.

---

## ✨ Features

- ✅ Quick DataFrame summary: shape, datatypes, missing values, and statistics  
- ✅ Visualize correlation matrix with heatmaps  
- ✅ Detect outliers using the IQR method  
- ✅ Plot numeric feature distributions  
- ✅ Report missing values as proportions  
- ✅ Get value counts for all categorical columns  

---

## 📦 Installation


bash
pip install Jeesum680


Since this is a custom library, clone or copy the source code into your project directory or package it using setuptools if needed.

bash
# Clone this repository or include the file directly
git clone https://github.com/jeevan7674/Jeesum680.git




In your Python project:




from Jeesum680 import df_summary, missing_report, correlation_matrix, outlier_summary, plot_distributions, value_counts_all




🧪 How to Use


1. df_summary(df)
Provides an overall summary of the DataFrame including shape, data types, missing values, and descriptive statistics.



import pandas as pd
from Jeesum680 import df_summary

df = pd.read_csv("your_data.csv")
df_summary(df)


2. missing_report(df)
Returns a Series with the proportion of missing values in each column (sorted descending).


from Jeesum680 import missing_report

missing_report(df)


3. correlation_matrix(df)
Plots a heatmap of correlation coefficients for all numeric features in the DataFrame.


from Jeesum680 import correlation_matrix

correlation_matrix(df)



4. outlier_summary(df)
Returns a count of outliers per numeric column using the IQR method.

from Jeesum680 import outlier_summary

outlier_summary(df)


5. plot_distributions(df)
Displays histograms of all numeric columns in the DataFrame.


from Jeesum680 import plot_distributions

plot_distributions(df)


6. value_counts_all(df)
Returns a dictionary with value counts for all object (categorical) columns.


from Jeesum680 import value_counts_all

value_counts_all(df)



🧑‍💻 Developer
Reddy Jeevan Reddy
Computer Science & Engineering | Web design & Web Dev Enthusiast

📜 License
This project is licensed under the MIT License. Feel free to use and modify!

🙌 Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you'd like to change.

🧠 Future Features
Advanced outlier detection (Z-score, Isolation Forest)

Interactive plots using Plotly

Automatic report generation using pandas-profiling or sweetviz


Let me know if you'd like help setting this up as a proper Python package