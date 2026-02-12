import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

# -----------------------
# Page Config
# -----------------------
st.set_page_config(page_title="Hotel Booking Analytics Dashboard", layout="wide")

# -----------------------
# Load & preprocess data
# -----------------------
@st.cache_data
def load_data():
    df = pd.read_csv("hotel_bookings.csv")
    
    # Engineered columns
    df['is_family'] = (df['children'] + df['babies'] > 0).astype(int)
    df['total_stays'] = df['stays_in_weekend_nights'] + df['stays_in_week_nights']
    df['total_stays_for_calc'] = df['total_stays'].replace(0,1)
    df['total_revenue'] = df['adr'] * df['total_stays_for_calc']
    df['is_direct'] = (df['distribution_channel'] == 'Direct').astype(int)
    
    # Season
    month_to_season = {
        'January': 'Winter', 'February': 'Winter', 'March': 'Spring',
        'April': 'Spring', 'May': 'Spring', 'June': 'Summer',
        'July': 'Summer', 'August': 'Summer', 'September': 'Fall',
        'October': 'Fall', 'November': 'Fall', 'December': 'Winter'
    }
    df['season'] = df['arrival_date_month'].map(month_to_season)
    return df

df = load_data()

# -----------------------
# Sidebar Navigation
# -----------------------
st.sidebar.title("📊 Hotel Booking Analytics")
page = st.sidebar.radio("Navigation", [
    "Data Overview", 
    "Booking & Customer Insights", 
    "Revenue Insights", 
    "Recommendations & Insights"
])

# =======================
# PAGE 1: DATA OVERVIEW
# =======================
if page == "Data Overview":
    st.title("📋 Data Overview & Quality Metrics")
    
    # Key Metrics
    st.subheader("Key Dataset Metrics")
    col1, col2, col3, col4 = st.columns(4)
    total_bookings = len(df)
    cancellation_rate = df['is_canceled'].mean()*100
    avg_stay = df['total_stays'].mean()
    avg_adr = df['adr'].mean()
    
    col1.metric("Total Bookings", f"{total_bookings:,}")
    col2.metric("Cancellation Rate", f"{cancellation_rate:.2f}%")
    col3.metric("Average Stay Length", f"{avg_stay:.2f} nights")
    col4.metric("Average ADR", f"${avg_adr:.2f}")
    
    st.divider()
    
    # Correlation Heatmap
    st.subheader("Correlation Matrix - Key Numeric Features")
    cols = [
    "lead_time",
    "adr",
    "stays_in_week_nights",
    "adults",
    "children",
    "previous_cancellations",
    "total_of_special_requests",
    "is_canceled"]
    corr = df[cols].corr()

    fig = px.imshow(
    corr,
    text_auto=True,
    color_continuous_scale="RdBu_r",
    title="Correlation Between Key Hotel Booking Features", 
    width = 900 , 
    height = 700 )
    st.plotly_chart(fig, use_container_width=True)
    
    with st.expander("📌 Correlation Insights"):
        st.markdown("""
        **Key Relationships Identified:**
        - **Lead time & cancellations:** Longer lead times are associated with an increased probability of cancellation.
        - **ADR & revenue:** Higher average daily rates are positively correlated with higher booking revenue.
        - **Special requests & engagement:** A larger number of special requests can indicate higher guest engagement or more complex stays.
        - **Previous cancellations as predictor:** Prior cancellations are predictive of future cancellations and should inform risk scoring.
        - **Children & stay length:** Presence of children correlates with longer average stays.
        """)
    
    st.divider()
    
    # Dataset Features Documentation
    st.subheader("Dataset Features & Preprocessing")
    with st.expander("📖 Feature Definitions"):
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("""
            **Numeric Features:**
            - lead_time: Days between booking and arrival
            - adr: Average Daily Rate per room (€)
            - stays_in_weekend_nights: Weekend nights in stay
            - stays_in_week_nights: Weekday nights in stay
            - adults: Number of adult guests
            - children: Number of child guests
            - babies: Number of babies
            - previous_cancellations: Guest's past cancellations
            - total_of_special_requests: Special requests made
            """)
        with col2:
            st.markdown("""
            **Categorical Features:**
            - hotel: Type (City Hotel / Resort Hotel)
            - meal: Meal plan (BB, HB, FB, SC)
            - country: Guest origin country
            - market_segment: Market segment type
            - distribution_channel: Booking channel
            - customer_type: Customer classification
            - is_canceled: Cancellation status

            **Engineered Features:**
            - total_stays: Total nights (weekend + weekday)
            - total_revenue: Total booking value (ADR × nights)
            - is_family: Binary (has children/babies)
            - is_direct: Binary (direct vs OTA booking)
            - season: Derived from arrival month
            """)

# =======================
# PAGE 2: BOOKING & CUSTOMER INSIGHTS
# =======================
elif page == "Booking & Customer Insights":
    st.title("🎫 Booking & Customer Insights")
    
    # Lead Time Distribution
    st.subheader("Lead Time Distribution by Cancellation Status")
    fig = px.histogram(df, x="lead_time", color="is_canceled",
                       nbins=50, title="Lead Time Distribution by Cancellation Status",
                       labels={"is_canceled":"Canceled","lead_time":"Lead Time (days)"})
    st.plotly_chart(fig, use_container_width=True)
    
    with st.expander("💡 Insights"):
        st.markdown("""
        - The majority of bookings occur within a 0–100 day window prior to arrival.
        - Bookings with lead times greater than 150 days exhibit materially higher cancellation rates , the longer guests book ahead, the higher the risk of cancellation.
        - Recommendation: require a partial or non-refundable deposit for bookings with lead time >150 days to mitigate cancellation risk , setting policies or forecasting demand, since it shows that cancellations are not random but linked to how far in advance the booking was made.
        """)
    
    st.divider()
    
    # Repeat vs New Revenue
    st.subheader("Average Revenue: Repeat vs New Guests")
    repeat_revenue = df.groupby("is_repeated_guest")["total_revenue"].mean().reset_index()
    repeat_revenue["is_repeated_guest"] = repeat_revenue["is_repeated_guest"].map({0:"New Guests",1:"Repeat Guests"})
    fig = px.bar(repeat_revenue, x="is_repeated_guest", y="total_revenue", title="Average Revenue: Repeat vs New Guests")
    st.plotly_chart(fig, use_container_width=True)
    
    with st.expander("💡 Insights"):
        st.markdown("""
        - New guests bring in much higher average revenue compared to repeat guests. 
                    Repeat guests spend less per booking, but they add value through loyalty and consistency. 
                    The main takeaway is that attracting new customers drives revenue growth, while repeat customers help sustain long‑term stability.
        """)
    
    st.divider()
    
    # Family Revenue
    st.subheader("Average Revenue: Family vs Non-Family Guests")
    family_revenue = df.groupby("is_family")["total_revenue"].mean().reset_index()
    family_revenue["is_family"] = family_revenue["is_family"].map({0:"Non-Family Guests",1:"Family Guests"})
    fig = px.bar(family_revenue, x="is_family", y="total_revenue", title="Average Revenue: Family vs Non-Family")
    st.plotly_chart(fig, use_container_width=True)
    
    with st.expander("💡 Insights"):
        st.markdown("""
        - Family bookings demonstrate higher average spend and longer stay durations.
        - Recommendation: develop family-focused packages, promotions, and on-site amenities to capture incremental revenue from this segment.
        """)
    
    #cancellation by deposite type 
    st.subheader("Cancellation Rate by Deposit Type")
    cancellation_by_deposit = df.groupby('deposit_type')['is_canceled'].mean().reset_index()
    fig = px.bar(
    cancellation_by_deposit,
    x='deposit_type',
    y='is_canceled',
    title='Cancellation Rate by Deposit Type',
    labels={'is_canceled': 'Cancellation Rate'},
    color='deposit_type') 
    st.plotly_chart(fig, use_container_width=True)
    with st.expander("💡 Insights"):
        st.markdown("""
            **Insights:**
            
            Bookings with no deposit or refundable deposits show moderate cancellation rates (~30%).
            The non-refundable deposit type surprisingly has the highest cancellation rate, reaching 100%, which suggests possible data anomalies or misuse of this category.
            
            **Recommendations:**
            
            Reassess how non-refundable deposits are applied, since they should normally deter cancellations.
            Encourage refundable or partial deposits for long lead-time bookings to balance guest flexibility with reduced cancellation risk.
        """)


    #what customer type dominate hotel bookings 
    st.subheader("Booking Distribution by Customer Type")
    customer_counts = df['customer_type'].value_counts().reset_index()
    customer_counts.columns = ['customer_type', 'count']
    customer_counts = customer_counts.sort_values(by='count', ascending=False)
    fig = px.histogram(
    customer_counts,
    x='customer_type',
    y='count',
    title='Customer Type Frequency',
    color='customer_type',)
    st.plotly_chart(fig, use_container_width=True)
    with st.expander("💡 Insights"):
        st.markdown("""
            **Insights:**
            
            The majority of bookings come from Transient customers, far exceeding other types. Transient-Party follows at a much lower level, while Contract and Group customers contribute the least. This shows that individual travelers dominate hotel demand.
            
            **Recommendations:**
            
            Hotels should tailor marketing and offers toward transient travelers, while also exploring ways to grow Contract and Group segments to diversify revenue streams.
        """)




# =======================
# PAGE 3: REVENUE INSIGHTS
# =======================
elif page == "Revenue Insights":
    st.title("💰 Revenue Insights")
    
    # Revenue by Season
    st.subheader("Total Revenue by Season")
    revenue_by_season = df.groupby("season")["total_revenue"].sum().reset_index()
    fig = px.bar(revenue_by_season, x="season", y="total_revenue", color="season", title="Total Revenue by Season")
    st.plotly_chart(fig, use_container_width=True)
    
    with st.expander("💡 Insights"):
        st.markdown("""
        - Seasonal analysis indicates a peak revenue season (e.g., Summer) and identifiable low seasons.
        - Recommendation: apply seasonal pricing and targeted promotions to smooth demand across the year.
        """)
    
    # Revenue by Channel
    st.subheader("Revenue Contribution by Booking Channel")
    channel_revenue = df.groupby("is_direct")["total_revenue"].sum().reset_index()
    channel_revenue["is_direct"] = channel_revenue["is_direct"].map({0:"Indirect (OTA / Agency)",1:"Direct Booking"})
    fig = px.pie(channel_revenue, names="is_direct", values="total_revenue", title="Revenue Contribution by Channel")
    st.plotly_chart(fig, use_container_width=True)
    
    with st.expander("💡 Insights"):
        st.markdown(""" 
        -This shows a heavy reliance on third‑party platforms, with direct channels underutilized.
        - Direct bookings typically reduce distribution costs and improve operating margins.
        - Recommendation: increase direct-booking incentives (e.g., member rates, perks) and optimize the booking funnel to grow direct share.
        """)
    
    # Top 10 Countries
    st.subheader("Top 10 Revenue Generating Countries")
    top_countries = df.groupby("country")["total_revenue"].sum().sort_values(ascending=False).head(10).reset_index()
    fig = px.bar(top_countries, x="country", y="total_revenue", color="total_revenue", title="Top 10 Revenue Generating Countries")
    st.plotly_chart(fig, use_container_width=True)
    
    with st.expander("💡 Insights"):
        st.markdown("""
        - Revenue is concentrated in a small number of countries; top markets drive a significant share of revenue.
        - Portugal dominates revenue generation with over 14M, far ahead of the United Kingdom (~5M) and other countries, showing a strong concentration of revenue in one market.
        - Recommendation: invest in targeted marketing for top-performing markets while testing acquisition channels in secondary markets to diversify geographic risk.
        """)
    # Revenue by hotel type 
    st.subheader("Revenue by Hotel Type")
    fig = px.pie(
    df,
    names='hotel',
    values='total_revenue',
    title='Revenue Distribution by Hotel Type')
    st.plotly_chart(fig, use_container_width=True)
    
    with st.expander("💡 Insights"):
        st.markdown("""
        - The revenue distribution across hotel types shows a clear dominance of Resort hotels, which generate the highest revenue.
        - City hotels and Resort hotels are the most profitable segments, while Conference hotels generate the least revenue.
        - Recommendation: focus marketing efforts on Resort and City hotels, while exploring opportunities to improve performance in Conference hotels.
        """)
    #stay duration and total revenue 
    st.subheader("Total Revenue by Stay Duration")
    df_sorted = df.sort_values(by='total_stays')
    fig = px.scatter(
    df_sorted,
    x='total_stays',
    y='total_revenue',
    title='Impact of Stay Duration on Total Revenue',
    labels={'total_stays': 'Total Stays (Nights)', 'total_revenue': 'Total Revenue'})
    st.plotly_chart(fig, use_container_width=True)
    
    with st.expander("💡 Insights"):
        st.markdown("""
        - Longer stays generally correlate with higher total revenue.
        - Recommendation: implement loyalty programs or packages that encourage longer stays, such as weekend-long stays or multi-night discounts.
        """)
    
    #canceled bookings and total revenue
    st.subheader("Total Revenue by Cancellation Status")
    fig = px.box(
    df,
    x='is_canceled',
    y='total_revenue',
    title='Canceled vs Non-Canceled Bookings: Total Revenue',
    labels={'is_canceled': 'Booking Status (0=Not Canceled, 1=Canceled)', 
            'total_revenue': 'Total Revenue'},
    color='is_canceled')

    st.plotly_chart(fig, use_container_width=True)
    with st.expander("💡 Insights"):
        st.markdown("""
        - Canceled bookings show a wide range of total revenue, with some cancellations associated with high potential revenue.
        - Recommendation: implement cancellation policies that protect high-value bookings, such as requiring deposits or offering flexible rescheduling options to retain revenue from at-risk bookings.
        """)


# =======================
# PAGE 4: RECOMMENDATIONS & INSIGHTS
# =======================
elif page == "Recommendations & Insights":
    st.title("🎯 Recommendations & Strategic Insights")
    
    # Cancellation Risk
    st.subheader("Cancellation Risk Management")
    # Use lead_time > 150 days to identify long lead-time bookings (previous implementation incorrectly used total_stays)
    high_risk_lead = df[df['lead_time']>150]['is_canceled'].mean()*100
    st.markdown(f"- Bookings with lead time >150 days have a higher observed cancellation rate ({high_risk_lead:.1f}%).")
    st.markdown("- Recommendations: require a partial or non-refundable deposit for long lead-time bookings (e.g., 10–20%), implement tiered cancellation windows, and send automated reminder communications at 30/14/7 days.")
    
    st.divider()
    
    # Repeat Guest Strategy
    st.subheader("Repeat Guest Strategy")
    repeat_pct = df['is_repeated_guest'].mean()*100
    st.markdown(f"- Repeat guest rate: {repeat_pct:.1f}% — there is measurable opportunity to increase lifetime value through retention.")
    st.markdown("- Recommendations: launch a tiered loyalty program, implement personalized retention campaigns for past high-value guests, and track cohort retention metrics.")
    
    st.divider()
    
    # Family Segment
    st.subheader("Family Segment Focus")
    family_pct = df['is_family'].mean()*100
    st.markdown(f"- Family bookings represent {family_pct:.1f}% of total bookings and show higher average revenue and longer stays.")
    st.markdown("- Recommendations: design family packages and targeted promotions, enhance family-friendly amenities, and measure package uptake and incremental revenue.")
    
    st.divider()
    
    # Channel Optimization
    st.subheader("Booking Channel Optimization")
    direct_pct = df['is_direct'].mean()*100
    st.markdown(f"- Direct bookings currently represent {direct_pct:.1f}% of bookings. Growing direct share can improve margins by reducing OTA commissions.")
    st.markdown("- Recommendations: improve the direct booking experience, offer exclusive direct-booking incentives, and monitor conversion lift from direct-marketing campaigns.")
    
    st.divider()
    
    # Seasonality Strategy
    st.subheader("Seasonality & Revenue Optimization")
    season_revenue = df.groupby("season")["total_revenue"].sum()
    st.markdown(f"- Peak revenue season: {season_revenue.idxmax()} (${season_revenue.max():,.0f}).")
    st.markdown(f"- Lowest revenue season: {season_revenue.idxmin()} (${season_revenue.min():,.0f}).")
    st.markdown("- Recommendations: adopt dynamic pricing and demand forecasting, deploy targeted promotions during low seasons, and align staffing/operations with expected demand.")
