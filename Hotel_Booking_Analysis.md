# Hotel Booking Data Analysis

## Project Title and Description

**Project Title:** Hotel Booking Data Analysis

**Description:**
This project analyzes historical hotel booking data to identify patterns in customer behavior, cancellation risk, revenue drivers, and seasonality. The objective is to provide actionable business insights and recommendations to increase revenue, reduce cancellation-related losses, and improve customer retention.

---

## Data Description

Below is a summary of the dataset columns, their definitions, and how they are classified.

### All Columns & Definitions

| Feature | Definition |
|---|---|
| `hotel` | Type of hotel (City Hotel / Resort Hotel) |
| `is_canceled` | Booking cancellation status (1 = canceled, 0 = not canceled) |
| `lead_time` | Number of days between booking and arrival |
| `arrival_date_year` | Year of arrival |
| `arrival_date_month` | Month of arrival (name) |
| `arrival_date_week_number` | Week number of the year for arrival |
| `arrival_date_day_of_month` | Day of month of arrival |
| `stays_in_weekend_nights` | Number of weekend nights (Sat, Sun) in the stay |
| `stays_in_week_nights` | Number of week nights (Mon–Fri) in the stay |
| `adults` | Number of adults in the booking |
| `children` | Number of children in the booking |
| `babies` | Number of babies in the booking |
| `meal` | Type of meal booking (e.g., BB, HB, FB, SC) |
| `country` | Country of origin (ISO code) |
| `market_segment` | Market segment designation (e.g., Online TA, Offline TA/TO) |
| `distribution_channel` | Booking channel (Direct, TA, GDS, etc.) |
| `is_repeated_guest` | Whether the guest has previously stayed (1 = yes, 0 = no) |
| `previous_cancellations` | Number of previous bookings canceled by the guest |
| `previous_bookings_not_canceled` | Number of previous bookings not canceled |
| `reserved_room_type` | Code of room type reserved |
| `assigned_room_type` | Code of room type assigned (actual) |
| `booking_changes` | Number of changes made to the booking |
| `deposit_type` | Whether a deposit was made (No Deposit, Refundable, Non Refund) |
| `agent` | ID of travel agent who made the booking (may be null/NaN) |
| `company` | ID of company (if corporate booking) |
| `days_in_waiting_list` | Number of days the booking was on the waiting list |
| `customer_type` | Type of customer (Contract, Group, Transient, Transient-Party) |
| `adr` | Average Daily Rate (price per night) |
| `required_car_parking_spaces` | Number of parking spaces required |
| `total_of_special_requests` | Number of special requests made by the guest |
| `reservation_status` | Reservation status (e.g., Check-Out, Canceled, No-Show) |
| `reservation_status_date` | Date of last reservation status update |

**Engineered / Derived Columns used in the project:**

| Feature | Definition |
|---|---|
| `total_stay` | Total nights in stay = `stays_in_weekend_nights` + `stays_in_week_nights` |
| `total_stay_for_calc` | `total_stay` with zero-stays replaced by 1 to avoid zero-division when calculating revenue |
| `revenue` | Booking revenue approximated as `adr * total_stay_for_calc` |
| `is_family` | Binary flag indicating family booking (children + babies > 0) |
| `is_direct` | Binary flag indicating direct distribution channel (`distribution_channel == 'Direct'`) |
| `season` | Season derived from `arrival_date_month` (Winter, Spring, Summer, Fall) |


### Numeric Features

- `lead_time`, `arrival_date_year`, `arrival_date_week_number`, `arrival_date_day_of_month`
- `stays_in_weekend_nights`, `stays_in_week_nights`, `total_stay`, `total_stay_for_calc`
- `adults`, `children`, `babies`
- `previous_cancellations`, `previous_bookings_not_canceled`
- `booking_changes`, `days_in_waiting_list`
- `adr`, `required_car_parking_spaces`, `total_of_special_requests`, `revenue`

### Categorical Features

- `hotel`, `meal`, `country`, `market_segment`, `distribution_channel`, `customer_type`
- `reserved_room_type`, `assigned_room_type`, `deposit_type`, `reservation_status`
- `is_canceled`, `is_repeated_guest`, `is_family`, `is_direct`, `season`, `agent`, `company`

### Preprocessing & Feature Engineering Applied

- Missing values: Agent and company may contain nulls; handle or filter as appropriate before visualization.
- `total_stay_for_calc` created to avoid zero-length stays when computing revenue (zero replaced by 1 night).
- `revenue` computed as `adr * total_stay_for_calc` to estimate booking value.
- `is_family` created as binary indicator for households with children/babies.
- `is_direct` created to split direct vs. indirect booking channels for revenue analyses.
- `season` derived by mapping `arrival_date_month` to seasons (Winter, Spring, Summer, Fall) to analyze seasonality.
- Sampling: For dense scatter plots (e.g., lead_time vs. adr), a random sample (up to 5k rows) may be used to keep interactive charts responsive.
- Type conversions: Ensure numeric features are numeric (`adr`, `lead_time`, etc.) and date-like fields parsed when doing time-based analyses.

---

## Pages / Analysis Sections

Below is a description of each Streamlit page (analysis section), its purpose, the charts it includes, and placeholders for insights/screenshots.

### Data Overview Page

**Purpose:** Provide a concise dataset-level summary and data quality checks for business stakeholders. This page aims to help users quickly understand the dataset scale, health, and primary numeric relationships.

**Metrics & Charts Included:**

- Key metrics (top KPI cards):
  - Total bookings
  - Cancellation rate
  - Average stay length (`total_stay`)
  - Average ADR (`adr`)
  - Total revenue
- Correlation heatmap of key numeric features (e.g., `lead_time`, `adr`, `stays_in_week_nights`, `adults`, `children`, `previous_cancellations`, `total_of_special_requests`, `is_canceled`).

**Notes / Screenshot placeholders:**

- Insert screenshot of KPIs: `screenshots/data_overview_kpis.png`
- Insert screenshot of correlation heatmap: `screenshots/data_overview_corr.png`

**Space for Insights / Observations:**

- Observations about data completeness (missing `agent`/`company` values).
- Notable correlations (e.g., lead_time vs. cancellations).
- Potential data quality action items (e.g., impute/clean country codes, ADR outliers).

---

### Booking Behavior Page

**Purpose:** Explore how customers book (timing, customer type, family behavior) and how those behaviors relate to cancellations and revenue.

**Charts Included:**

- Lead time distribution by cancellation status (histogram)
  - Placeholder screenshot: `screenshots/booking_lead_time_hist.png`
- Average revenue by repeat guests (bar chart: `New Guest` vs `Repeat Guest`)
  - Placeholder screenshot: `screenshots/booking_repeat_revenue.png`
- Average revenue by family status (bar chart: `Family` vs `Non-Family`)
  - Placeholder screenshot: `screenshots/booking_family_revenue.png`

**Space for Insights:**

- Assess cancellation risk by lead time buckets (e.g., >150 days)
- Compare revenue uplift from repeat guests vs new guests and recommend retention efforts
- Evaluate family booking share and recommended packages

---

### Revenue Insights Page

**Purpose:** Diagnose revenue drivers and geographic/channel contributions to total revenue to inform pricing, distribution, and marketing.

**Charts Included:**

- Total revenue by season (bar chart) — uses `season` derived from `arrival_date_month`
  - Placeholder screenshot: `screenshots/revenue_by_season.png`
- Revenue contribution by booking channel (pie chart: Direct vs Indirect)
  - Placeholder screenshot: `screenshots/revenue_by_channel.png`
- Top 10 revenue-generating countries (horizontal bar chart)
  - Placeholder screenshot: `screenshots/top_countries_revenue.png`

**Space for Insights:**

- Identify peak and low seasons and quantify seasonality (%)
- Measure direct booking share and recommend direct-booking incentives if direct revenue is low
- Identify geographic concentration risk (top countries share) and advise on diversification

---

### Summary & Insights Page

**Purpose:** Provide an executive-friendly summary of the analysis, key findings, and prioritized business recommendations.

**Contents:**

- Executive KPIs and summary metrics (Total Revenue, Cancellation Rate, Repeat Guest Rate, Average Booking Value)
- Narrative of findings and supporting bullet points
- Prioritized action list (e.g., Cancellation Risk Management, Loyalty Program, Dynamic Pricing, Direct Booking Push, Family Packages)

**Space for Insights / Visual Summary:**

- Snapshot charts supporting recommendations: `screenshots/summary_kpis.png`, `screenshots/summary_charts.png`

---

## Conclusion and Business Recommendations

**Key Trends & Patterns:**

- Customers often book within a finite window (majority within 0–100 days), but long lead times (>150 days) show materially higher cancellation rates.
- Repeat guests generate higher average revenue versus new guests — a clear opportunity to increase loyalty and retention.
- Family bookings (presence of children/babies) typically correlate with longer stays and higher revenue per booking.
- Seasonality is a major driver of revenue; identify peak (e.g., Summer) and low (e.g., Winter/Fall depending on region) seasons and align pricing and staffing accordingly.
- Direct bookings yield higher margin (lower OTA commissions); current direct share may be suboptimal.

**Business Recommendations (Prioritized):**

1. Cancellation Risk Management (High priority)
   - Require partial or non-refundable deposits for bookings with lead time >150 days.
   - Apply graduated cancellation windows (stricter for long lead times).
   - Trigger reminder and engagement emails at 30/14/7 days before arrival to reduce no-shows and cancellations.

2. Loyalty & Retention (High priority)
   - Launch a tiered loyalty program to increase repeat guest rate and lift lifetime revenue.
   - Offer targeted promotions to previous high-value guests.

3. Revenue Management & Dynamic Pricing (Medium priority)
   - Implement seasonally-aware pricing and demand forecasting to increase ADR during peak windows and stimulate demand in low seasons.
   - Test room/package bundles for families to increase average booking value.

4. Direct Booking Strategy (Medium priority)
   - Increase direct booking incentives (discounts, perks) and improve website UX to convert OTA traffic.
   - Use email remarketing and retargeting ads to convert OTA browsers.

5. Geographic Diversification & Marketing (Medium priority)
   - Identify under-indexed markets with growth potential and allocate marketing budget to diversify the revenue mix.

6. Data & Measurement Improvements (Operational)
   - Improve capture and cleanliness of `agent` and `company` fields.
   - Monitor ADR outliers and validate `adr` accuracy (possible currency/decimal issues).
   - Add dashboards to monitor cancellations in real-time by lead time bucket and channel.

---

## How to Use This Document

- Place exported chart screenshots in the `screenshots/` folder and update the placeholder image links above.
- Use this file as the project README for non-technical stakeholders and as a handoff document for implementation teams.

---

*Prepared for the Hotel Booking Analytics project — use this as the basis for presentations, executive briefings, and roadmap planning.*
