# -Smart_Stock_Quality_Screener





This code builds an interactive stock screening web app using Streamlit, Pandas, and Matplotlib. The app allows users to upload a Screener CSV file, clean and process the data, apply advanced financial filters, visualize the results, and download the filtered stock list.





🔷 What the app does (high level)


Creates a web dashboard using Streamlit.

Accepts a CSV upload from the user.

Cleans messy Screener column names and converts text values (like 1,234%) into numbers.

Provides sidebar sliders so users can set financial filter criteria.

Filters stocks based on all key parameters:

ROCE

P/E

Market Cap

Sales Growth

Profit Growth

Sales size

Profit size

Dividend yield

Displays the Top 15 quality stocks in a styled table.

Shows KPI metrics (count, best ROCE, average P/E, market cap).

Draws a bar chart comparing ROCE of top stocks.

Allows downloading the filtered result as a CSV.










🔷 Main Components
Section	Purpose
Imports	Bring in Streamlit (UI), Pandas (data), Matplotlib (chart)
Page config	Makes app full-width dashboard
File uploader	Lets user upload Screener CSV
Column cleaning	Fixes hidden spaces & inconsistent names
Numeric conversion	Converts strings to proper numbers
Sidebar sliders	User-controlled financial filters
Filtering logic	Selects only high-quality stocks
KPI metrics	Quick summary insights
Data table	Shows top 15 filtered stocks
Chart	Visual ROCE comparison
Download button	Export results as CSV




