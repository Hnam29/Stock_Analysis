import streamlit as st
import yfinance as yf 
import pandas as pd 
import requests
import pandas_datareader as pdr

st.set_page_config(layout="wide")


def convert_df(df):
    # IMPORTANT: Cache the conversion to prevent computation on every rerun
    return df.to_csv().encode('utf-8')

with st.sidebar:
    st.header('Predictive Stock Indicators')
    st.radio('Choose your indicators:',options=('Simple Moving Average', 'Bollinger Bands', '52-Week High/Low', 'P/E Ratio', 'Parabolic Stop-And-Reverse'))

c1,c2 = st.columns([1,2])
c2.title('Finance Dashboard :cool:')

#tickers = ('TSLA', 'AAPL', 'MSFT', 'BTC-USD', 'ETH-USD')


# Fetch the raw HTML content of the S&P 500 index composition table
sp500_url = 'https://en.wikipedia.org/wiki/List_of_S%26P_500_companies'
sp500_html = requests.get(sp500_url).text
sp500_table = pd.read_html(sp500_html)[0]

# Extract the list of tickers
tickers = sp500_table['Symbol'].tolist()

# Print the list of tickers
print(tickers)

dropdown = st.multiselect('Pick your stock item: ', tickers)

start = st.date_input('Start', value=pd.to_datetime('2021-01-01'))
end = st.date_input('End', value=pd.to_datetime('today'))


# y2019 = pd.to_datetime('2019-01-01')
# y2020 = pd.to_datetime('2020-01-01')
# y2021 = pd.to_datetime('2021-01-01')
# y2022 = pd.to_datetime('2022-01-01')
# y2023 = pd.to_datetime('2023-01-01')
# now = pd.to_datetime('now')
# start, end = st.select_slider('Select the time you want',options=[y2019,y2020,y2021,y2022,y2023,now],value=(y2019,now))

if len(dropdown) > 0:
    col1, col2 = st.columns([5,5])
    df = yf.download(dropdown, start, end)['Open']
    df1 = yf.download(dropdown, start, end)['Adj Close']
    col1.subheader('Open')
    col1.write(df.head())
    col2.subheader('Adj Close')
    col2.write(df1.head())
    #
    col1.divider()
    col2.divider()
    col1.line_chart(df)
    col2.line_chart(df1)
    #
    col1.divider()
    col2.divider()
    col1.bar_chart(df)
    col2.bar_chart(df1)
    #
    col1.divider()
    col2.divider()
    col1.area_chart(df)
    col2.area_chart(df1)

    csv = convert_df(df)
    st.download_button(
            label="Download data",
            data=csv,
            file_name='stock_data.csv',
            mime='text/csv',
        )

file = st.file_uploader('Upload your dataset:')
data = pd.DataFrame()
if file is not None:
    data = pd.read_csv(file)

dropdown1 = st.multiselect('Select columns:',data.columns)

if len(dropdown1) > 0:
    # x_col = st.selectbox('Choose column x:',dropdown1)
    # y_cols = st.multiselect('Select columns y:',dropdown1)
    # data1 = pd.DataFrame(data[dropdown1],columns=y_cols)
    # data1 = data1.set_index(x_col)
    # st.line_chart(data1)

    x_col = st.selectbox('Choose column x:', dropdown1)
    y_cols = st.multiselect('Select columns y:', dropdown1)

    # Slice the dataframe to fetch only the selected x and y columns
    data1 = data.loc[:, [x_col] + y_cols]
    data1 = data1.set_index(x_col)

    # Plot the line chart
    st.line_chart(data1)

