import yfinance as yf
import pandas as pd
import streamlit as st

logo_image = "logo.png"
st.sidebar.image(logo_image, width=170)
st.sidebar.title("DCA vs LumpSump Estrategies")

# Seleccionamos las cryptos
tickers = ['BTC-USD', 'ETH-USD', 'BNB-USD', 'ADA-USD', 'XRP-USD',
    'SOL-USD', 'DOT-USD', 'DOGE-USD', 'AVAX-USD', 'LUNA-USD',
    'UNI-USD', 'LINK-USD', 'MATIC-USD', 'LTC-USD', 'BCH-USD',
    'ALGO-USD', 'ATOM-USD', 'XTZ-USD', 'FIL-USD', 'TRX-USD',
    'VET-USD', 'EOS-USD', 'AAVE-USD', 'XLM-USD', 'CRO-USD',
    'FTT-USD', 'MIOTA-USD', 'MKR-USD', 'XEM-USD', 'DASH-USD',
    'NEO-USD', 'BTT-USD', 'XTZ-USD', 'AAVE-USD',
    '1INCH-USD', 'ALICE-USD', 'FARM-USD', 'GALA-USD', 'POWR-USD']  # Agrega más según sea necesario

# Desarrollamos los inputs de Streamlit
dropdown = st.sidebar.selectbox("Choose a crypto:", tickers)
start = st.sidebar.date_input("Start date:", value=pd.to_datetime("2021-10-31"))
investment = st.sidebar.number_input("Choose investment per month:")

# Creamos una función para obtener datos históricos
def get_data(symbol, start):
    data = yf.download(symbol, start=start)
    return data

# Creamos el dataframe
df = get_data(dropdown, start)

# Verificamos si el DataFrame está vacío
if df.empty:
    st.error("Data not available. Please check the selected crypto symbol and start date.")
else:
    st.success("Data downloaded successfully.")

# Creación de fechas de compra y precios de compra
buydates = pd.date_range(df.index[0], df.index[-1], freq="1M")
buyprices = df[df.index.isin(buydates)].Close

# Calculo de la cantidad de criptomonedas compradas
coin_amt = investment / buyprices
coin_amt_LS = investment * len(buyprices) / buyprices[0]

# Calculo del portafolio en la estrategia DCA
coin_amt_sum = coin_amt.cumsum()
coin_amt_sum.name = "coin_amt_DCA"
df_tog = pd.concat([coin_amt_sum, df], axis=1).ffill()
df_tog["Portfolio_DCA"] = df_tog.coin_amt_DCA * df_tog.Close

# Calculo del rendimiento de la estrategia DCA
performance_DCA = (df_tog["Portfolio_DCA"][-1] / (investment * len(buyprices)) - 1)

# Calculo del portafolio en la estrategia LS
df_tog["coin_amt_LS"] = coin_amt_LS
df_tog["Portfolio_LS"] = df_tog.coin_amt_LS * df_tog.Close

# Calculo del rendimiento en la estrategia LS
performance_LS = (df_tog["Portfolio_LS"][-1] / (investment * len(buyprices)) - 1)

# Display de gráficos y performance
st.subheader("DCA performance: " + str(round(performance_DCA * 100, 2)) + " %")
st.line_chart(df_tog["Portfolio_DCA"])
st.subheader("LS performance: " + str(round(performance_LS * 100, 2)) + " %")
st.line_chart(df_tog["Portfolio_LS"])