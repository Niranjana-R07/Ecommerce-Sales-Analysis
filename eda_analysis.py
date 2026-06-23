import pandas as pd
import sweetviz as sv

df = pd.read_csv(r"D:\Data analytics\ecommerce_sales_data.csv")

report = sv.analyze(df)
report.show_html("EDA_Report.html")
