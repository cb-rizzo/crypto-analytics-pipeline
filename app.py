import os
import streamlit as st
import pandas as pd
from sqlalchemy import create_engine
from dotenv import load_dotenv

# Load environment variables (for local development)
load_dotenv()

# Get database URL from environment variables (GitHub/Streamlit secrets or local .env)
DATABASE_URL = os.getenv("DATABASE_URL")

# Page configuration
st.set_page_config(
    page_title="Crypto Real-Time Analytics",
    page_icon="📈",
    layout="wide"
)

st.title("🚀 Real-Time Crypto Pipeline & Analytics")
st.markdown("Live monitoring dashboard powered by Python, PostgreSQL (Neon.tech), GitHub Actions, and Streamlit.")

# Function to load data from PostgreSQL
@st.cache_data(ttl=60) # Cache data for 60 seconds to optimize performance
def load_data():
    if not DATABASE_URL:
        st.error("DATABASE_URL is not set.")
        return pd.DataFrame()
    
    try:
        engine = create_engine(DATABASE_URL)
        query = "SELECT symbol, price, timestamp FROM crypto_prices ORDER BY timestamp ASC;"
        df = pd.read_sql(query, con=engine)
        return df
    except Exception as e:
        st.error(f"Error loading data from database: {e}")
        return pd.DataFrame()

# Load the data
df = load_data()

if df.empty:
    st.warning("No data found in the database yet. Wait for the first automated pipeline run or trigger it manually from GitHub!")
else:
    # Sidebar filters & metrics
    st.sidebar.header("Configuration")
    selected_symbol = st.sidebar.selectbox("Select Symbol", df["symbol"].unique())
    
    filtered_df = df[df["symbol"] == selected_symbol]
    
    # Latest price metric
    latest_price = filtered_df["price"].iloc[-1]
    previous_price = filtered_df["price"].iloc[-2] if len(filtered_df) > 1 else latest_price
    price_delta = latest_price - previous_price

    col1, col2, col3 = st.columns(3)
    col1.metric(label=f"Latest Price ({selected_symbol})", value=f"${latest_price:,.2f}", delta=f"${price_delta:,.2f}")
    col2.metric(label="Total Records Logged", value=len(filtered_df))
    col3.metric(label="Last Update", value=str(filtered_df["timestamp"].iloc[-1]))

    st.markdown("---")

    # Time series chart
    st.subheader(f"Price Evolution Over Time - {selected_symbol}")
    st.line_chart(filtered_df.set_index("timestamp")["price"])

    # Raw data table expander
    with st.expander("View Raw Data Table"):
        st.dataframe(filtered_df, use_container_width=True)