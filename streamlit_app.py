
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import re
import hashlib
from agents.gemini_agent import ask_gemini
# --------------------------------------------------
# PAGE CONFIGURATION
# --------------------------------------------------

st.set_page_config(
    page_title="Data Intelligence",
    page_icon="✦",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --------------------------------------------------
# CUSTOM DESIGN SYSTEM - MIDNIGHT AURORA
# --------------------------------------------------

st.markdown("""
<style>

@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700;800&family=Space+Grotesk:wght@400;500;600;700&display=swap');

:root {
    --bg: #080d1b;
    --panel: #111a2e;
    --panel2: #15213a;
    --border: rgba(148,163,184,0.16);
    --cyan: #48e5e0;
    --lime: #c4f56b;
    --purple: #9c8cff;
    --muted: #91a0b8;
    --white: #f4f7ff;
}

html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
}

.stApp {
    background:
        radial-gradient(ellipse at 10% 0%, rgba(53, 91, 170, 0.19), transparent 34%),
        radial-gradient(ellipse at 90% 15%, rgba(72, 229, 224, 0.08), transparent 30%),
        var(--bg);
    color: var(--white);
}

[data-testid="stHeader"] {
    background: rgba(8,13,27,0.85);
}

.block-container {
    max-width: 1450px;
    padding-top: 2rem;
    padding-bottom: 4rem;
}

/* SIDEBAR */

[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #101a30 0%, #0a1122 100%);
    border-right: 1px solid var(--border);
}

[data-testid="stSidebar"] > div:first-child {
    padding-top: 2rem;
}

[data-testid="stSidebar"] * {
    color: #e5edff;
}

[data-testid="stSidebar"] [data-testid="stRadio"] label {
    border-radius: 10px;
    padding: 9px 12px;
}

[data-testid="stSidebar"] [data-testid="stFileUploader"] {
    background: #16233a;
    border: 1px dashed #52647e;
    border-radius: 15px;
    padding: 12px;
}

/* TYPOGRAPHY */

h1, h2, h3 {
    font-family: 'Space Grotesk', sans-serif !important;
    color: #f4f7ff !important;
    letter-spacing: -0.5px;
}

p, label, span {
    color: inherit;
}

/* HERO */

.hero {
    position: relative;
    overflow: hidden;
    padding: 35px 38px;
    border-radius: 24px;
    margin-bottom: 28px;
    background:
        radial-gradient(circle at 85% 20%, rgba(72,229,224,0.22), transparent 28%),
        linear-gradient(115deg, #172b4c 0%, #202b54 55%, #18243e 100%);
    border: 1px solid rgba(148,163,184,0.22);
    box-shadow: 0 18px 55px rgba(0,0,0,0.23);
}

.hero-label {
    color: #c4f56b;
    font-size: 11px;
    font-weight: 800;
    letter-spacing: 3px;
    text-transform: uppercase;
}

.hero-title {
    font-family: 'Space Grotesk', sans-serif;
    font-size: clamp(27px, 4vw, 43px);
    font-weight: 700;
    line-height: 1.15;
    color: white;
    margin-top: 13px;
}

.hero-title span {
    color: #48e5e0;
}

.hero-sub {
    color: #b9c8e1;
    font-size: 14px;
    margin-top: 12px;
}

.hero-chip {
    display: inline-block;
    margin-top: 18px;
    padding: 7px 13px;
    background: rgba(196,245,107,0.12);
    border: 1px solid rgba(196,245,107,0.35);
    border-radius: 30px;
    color: #d6ff96;
    font-size: 11px;
    font-weight: 700;
}

/* SECTION HEADER */

.section-label {
    color: #48e5e0;
    font-size: 11px;
    letter-spacing: 2px;
    text-transform: uppercase;
    font-weight: 800;
    margin-bottom:6px;
}

.section-title {
    font-family: 'Space Grotesk', sans-serif;
    font-size: 24px;
    color: #f4f7ff;
    font-weight: 700;
    margin-bottom: 5px;
}

.section-description {
    color: #91a0b8;
    font-size: 13px;
    margin-bottom: 20px;
}

/* METRIC CARDS */

[data-testid="stMetric"] {
    background: linear-gradient(145deg, #16233b, #10192b);
    border: 1px solid rgba(148,163,184,0.17);
    border-radius: 18px;
    padding: 20px 21px;
    box-shadow: 0 10px 28px rgba(0,0,0,0.16);
    transition: transform 0.2s ease, border-color 0.2s ease;
}

[data-testid="stMetric"]:hover {
    transform: translateY(-4px);
    border-color: rgba(72,229,224,0.5);
}

[data-testid="stMetricLabel"] {
    color: #9eafc9 !important;
    font-size: 12px !important;
    font-weight: 600 !important;
}

[data-testid="stMetricValue"] {
    color: #f4f7ff !important;
    font-family: 'Space Grotesk', sans-serif;
    font-size: 29px !important;
    font-weight: 700 !important;
}

/* CONTAINERS */

div[data-testid="stVerticalBlockBorderWrapper"] {
    background: rgba(17,26,46,0.8);
    border: 1px solid var(--border);
    border-radius: 18px;
}

/* BUTTONS */

.stButton > button,
.stDownloadButton > button {
    background: linear-gradient(100deg, #48e5e0, #a7ed91);
    color: #071522 !important;
    border: none;
    border-radius: 11px;
    padding: 10px 21px;
    font-weight: 800;
    transition: all 0.2s ease;
}

.stButton > button:hover,
.stDownloadButton > button:hover {
    transform: translateY(-2px);
    box-shadow: 0 8px 24px rgba(72,229,224,0.2);
    color: #071522 !important;
}

/* INPUTS */

.stTextInput input,
.stSelectbox div[data-baseweb="select"] > div {
    background: #142039 !important;
    color: white !important;
    border: 1px solid #354866 !important;
    border-radius: 11px !important;
}

.stTextInput input:focus {
    border-color: #48e5e0 !important;
}

/* TABLES */

[data-testid="stDataFrame"] {
    border: 1px solid var(--border);
    border-radius: 13px;
    overflow: hidden;
}

/* TABS AND DIVIDERS */

.stTabs [data-baseweb="tab"] {
    color: #aab8ce;
    font-weight: 700;
}

.stTabs [aria-selected="true"] {
    color: #48e5e0 !important;
}

hr {
    border-color: rgba(148,163,184,0.16);
}

/* STATUS */

[data-testid="stAlert"] {
    border-radius: 13px;
}

footer {
    visibility: hidden;
}

#MainMenu {
    visibility: hidden;
}

</style>
""", unsafe_allow_html=True)


# --------------------------------------------------
# REUSABLE DESIGN ELEMENTS
# --------------------------------------------------

def hero(title, subtitle, label="DATA INTELLIGENCE WORKSPACE"):
    st.markdown(f"""
    <div class="hero">
        <div class="hero-label">{label}</div>
        <div class="hero-title">{title}</div>
        <div class="hero-sub">{subtitle}</div>
        <div class="hero-chip">✦ INSIGHT STARTS WITH DATA</div>
    </div>
    """, unsafe_allow_html=True)


def section_heading(title, description, label="ANALYTICS"):
    st.markdown(f"""
    <div class="section-label">{label}</div>
    <div class="section-title">{title}</div>
    <div class="section-description">{description}</div>
    """, unsafe_allow_html=True)


# --------------------------------------------------
# DATA CLEANING
# --------------------------------------------------

def clean_dataset(data):
    cleaned = data.copy()

    for column in cleaned.columns:
        if cleaned[column].isnull().any():

            if pd.api.types.is_numeric_dtype(cleaned[column]):
                median_value = cleaned[column].median()

                if pd.notna(median_value):
                    cleaned[column] = cleaned[column].fillna(median_value)

            else:
                mode_values = cleaned[column].mode(dropna=True)

                if not mode_values.empty:
                    cleaned[column] = cleaned[column].fillna(
                        mode_values.iloc[0]
                    )

    return cleaned.drop_duplicates()


# --------------------------------------------------
# QUESTION ANSWERING
# --------------------------------------------------
def answer_question(data, question):
    df = data.copy()
    q = question.lower().strip()

    numeric_columns = df.select_dtypes(include="number").columns.tolist()

    # Detect the column mentioned in the question
    column = None
    for col in sorted(df.columns, key=lambda x: len(str(x)), reverse=True):
        if re.search(r"(?<!\w)" + re.escape(str(col).lower()) + r"(?!\w)", q):
            column = col
            break

    # 1. Dynamic record filtering
    if column is not None:
        col_pattern = re.escape(str(column))

        # Numeric comparison operators
        operators = {
            "greater than or equal to": ">=",
            "at least": ">=",
            "less than or equal to": "<=",
            "at most": "<=",
            "greater than": ">",
            "more than": ">",
            "above": ">",
            "over": ">",
            "less than": "<",
            "below": "<",
            "under": "<",
            "equal to": "==",
            "equals": "==",
        }

        operator_pattern = "|".join(
            re.escape(op) for op in sorted(operators, key=len, reverse=True)
        )

        numeric_match = re.search(
            col_pattern + r"\s+(?:is\s+)?(" + operator_pattern +
            r"|>=|<=|>|<|=)\s*(-?\d+(?:\.\d+)?)",
            q
        )

        if numeric_match:
            operator = numeric_match.group(1)
            value = float(numeric_match.group(2))
            operator = operators.get(operator, operator)

            values = pd.to_numeric(df[column], errors="coerce")

            if operator == ">":
                result = df[values > value]
            elif operator == "<":
                result = df[values < value]
            elif operator == ">=":
                result = df[values >= value]
            elif operator == "<=":
                result = df[values <= value]
            else:
                result = df[values == value]

            return (
                f"Found {len(result)} matching records:\n\n"
                + result.to_string(index=False)
                if not result.empty
                else f"No records found where {column} {operator} {value}"
            )

        # Text or exact-value filtering
        exact_match = re.search(
            col_pattern + r"\s+(?:is|equals|equal to|=|:)\s*(.+?)\s*$",
            q
        )

        if exact_match:
            value = exact_match.group(1).strip().strip("'\"").rstrip("?.!")

            result = df[
                df[column].astype(str).str.strip().str.casefold()
                == value.casefold()
            ]

            if not result.empty:
                return (
                    f"Found {len(result)} matching records:\n\n"
                    + result.to_string(index=False)
                )

            # Also allow partial text matches
            result = df[
                df[column].astype(str).str.contains(
                    re.escape(value), case=False, na=False
                )
            ]

            if not result.empty:
                return (
                    f"Found {len(result)} matching records:\n\n"
                    + result.to_string(index=False)
                )

            return f"No records found for {column} = {value}"

    # 2. Total records
    if any(word in q for word in [
        "total rows", "total records", "number of rows",
        "how many rows", "how many records", "count records"
    ]):
        return f"Total records: {len(df)}"

    # 3. Total columns
    if any(word in q for word in [
        "total columns", "number of columns", "how many columns"
    ]):
        return f"Total columns: {len(df.columns)}"

    # 4. Missing values
    if any(word in q for word in ["missing", "null values", "empty values"]):
        if column is not None:
            return f"Missing values in {column}: {df[column].isnull().sum()}"
        return df.isnull().sum().to_string()

    # 5. Duplicate records
    if "duplicate" in q:
        return f"Duplicate records: {df.duplicated().sum()}"

    # 6. Correlation
    if "correlation" in q or "correlate" in q:
        mentioned = [
            c for c in numeric_columns if str(c).lower() in q
        ]

        if len(mentioned) >= 2:
            value = df[mentioned[0]].corr(df[mentioned[1]])
            return f"Correlation between {mentioned[0]} and {mentioned[1]}: {value:.3f}"

        if len(numeric_columns) >= 2:
            return df[numeric_columns].corr().round(3).to_string()

        return "At least two numeric columns are required."

    # 7. Grouped analysis: total Sales by Region
    group_match = re.search(r"\bby\s+(.+?)\s*$", q)

    if group_match and any(word in q for word in ["total", "sum", "average", "mean", "count"]):
        group_text = group_match.group(1).strip()

        group_col = next(
            (c for c in df.columns if str(c).lower() == group_text),
            None
        )

        value_col = next(
            (c for c in numeric_columns if str(c).lower() in q),
            None
        )

        if group_col is not None:
            if "count" in q:
                return df.groupby(group_col).size().to_string()

            if value_col is not None:
                if "average" in q or "mean" in q:
                    return df.groupby(group_col)[value_col].mean().to_string()

                return df.groupby(group_col)[value_col].sum().to_string()
    
    # 8. Top and bottom records
    if any(word in q for word in ["top", "highest", "maximum", "most"]):
        if column is not None and column in numeric_columns:
            numbers = re.findall(r"\d+", q)
            count = int(numbers[0]) if numbers else 1
            result = df.nlargest(count, column)
            return (
                f"Highest {column}:\n"
                + result.to_string(index=False)
            )

    if any(word in q for word in ["bottom", "lowest", "minimum", "least"]):
        if column is not None and column in numeric_columns:
            numbers = re.findall(r"\d+", q)
            count = int(numbers[0]) if numbers else 1
            result = df.nsmallest(count, column)
            return (
                f"Lowest {column}:\n"
                + result.to_string(index=False)
            )

    # 9. Numeric calculations
    if column in numeric_columns:
        if "average" in q or "mean" in q:
            return f"Average {column}: {df[column].mean():.2f}"

        if "median" in q:
            return f"Median {column}: {df[column].median():.2f}"

        if "standard deviation" in q or "std" in q:
            return f"Standard deviation of {column}: {df[column].std():.2f}"

        if "sum" in q or "total" in q:
            return f"Total {column}: {df[column].sum():.2f}"

        if "maximum" in q or "highest" in q:
            return f"Maximum {column}: {df[column].max()}"

        if "minimum" in q or "lowest" in q:
            return f"Minimum {column}: {df[column].min()}"

        if "summary" in q or "describe" in q:
            return df[column].describe().to_string()

    # 10. Unique values
    if "unique" in q or "distinct" in q:
        if column is not None:
            return str(df[column].dropna().unique().tolist())
        return df.nunique().to_string()

    # 11. Sorting
    if "sort" in q or "order" in q:
        if column is not None:
            ascending = not any(
                word in q for word in ["descending", "highest", "largest"]
            )
            return df.sort_values(
                by=column, ascending=ascending
            ).to_string(index=False)

    # 12. General help
    return (
        "I could not understand that question.\n\n"
        "Examples:\n"
        "- Show records where sales_rep is Bob\n"
        "- Show records where Quantity_Sold is above 20\n"
        "- Show records where Sales is less than 500\n"
        "- What is the total Sales?\n"
        "- What is the average Profit?\n"
        "- Show top 5 by Sales\n"
        "- Show total Sales by Region"
    )

# --------------------------------------------------
# SIDEBAR
# --------------------------------------------------

st.sidebar.markdown("""
<div style="padding:5px 4px 25px 4px;">
    <div style="font-size:12px;color:#48e5e0;letter-spacing:3px;font-weight:800;">
    </div>
    <div style="font-family:Space Grotesk;font-size:22px;font-weight:700;color:white;margin-top:5px;">
        Data Studio
    </div>
    <div style="font-size:11px;color:#8294b1;margin-top:5px;">
        INTELLIGENCE • ANALYSIS • INSIGHTS
    </div>
</div>
""", unsafe_allow_html=True)

st.sidebar.markdown(
    '<div style="font-size:10px;color:#48e5e0;letter-spacing:2px;font-weight:800;">WORKSPACE MENU</div>',
    unsafe_allow_html=True
)

page = st.sidebar.radio(
    "Navigation",
    [
        "Overview",
        "Data Cleaning",
        "Analysis & Charts",
        "AI Assistant",
        "Reports"
    ],
    label_visibility="collapsed"
)

st.sidebar.divider()

st.sidebar.markdown(
    '<div style="font-size:10px;color:#48e5e0;letter-spacing:2px;font-weight:800;">YOUR DATASET</div>',
    unsafe_allow_html=True
)

uploaded_file = st.sidebar.file_uploader(
    "Upload CSV or Excel",
    type=["csv", "xlsx"]
)

if uploaded_file is not None:
    st.sidebar.success("Dataset selected")

st.sidebar.divider()

st.sidebar.markdown("""
<div style="background:#15213a;padding:15px;border-radius:13px;border:1px solid #31425d;">
    <div style="font-size:11px;color:#48e5e0;font-weight:800;"></div>
    <div style="font-size:12px;color:#aebbd0;margin-top:7px;">
        Turn raw data into meaningful insights.
    </div>
    <div style="font-size:10px;color:#71839f;margin-top:12px;">
        VERSION 4.0
    </div>
</div>
""", unsafe_allow_html=True)


# --------------------------------------------------
# LOAD DATASET
# --------------------------------------------------

if uploaded_file is None:
    hero(
        "Your data. <span>Your intelligence.</span>",
        "Upload a dataset to explore, clean, visualize and understand your data."
    )

    st.markdown("### Start your analysis")

    st.info("Upload a CSV or Excel file using the left sidebar to get started.")

    st.stop()

try:
    file_bytes = uploaded_file.getvalue()
    file_signature = hashlib.md5(file_bytes).hexdigest()

    if st.session_state.get("file_signature") != file_signature:

        uploaded_file.seek(0)

        if uploaded_file.name.lower().endswith(".csv"):
            original_df = pd.read_csv(uploaded_file)
        else:
            original_df = pd.read_excel(uploaded_file)

        st.session_state["original_df"] = original_df
        st.session_state["cleaned_df"] = None
        st.session_state["file_signature"] = file_signature

    df = st.session_state["original_df"]

except Exception as error:
    st.error(f"Unable to load dataset: {error}")
    st.stop()

if df.empty:
    st.error("The uploaded dataset is empty.")
    st.stop()


# --------------------------------------------------
# OVERVIEW
# --------------------------------------------------


if page == "Overview":

    hero(
        "Your data. <span>Your intelligence.</span>",
        f"Explore your dataset: {uploaded_file.name}",
        "OVERVIEW / DATA PROFILE"
    )

    section_heading(
        "Dataset at a glance",
        "A quick snapshot of the quality and structure of your data."
    )

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Total Records", f"{len(df):,}", "Rows")
    col2.metric("Data Columns", f"{len(df.columns):,}", "Features")
    col3.metric("Missing Values", f"{int(df.isnull().sum().sum()):,}")
    col4.metric("Duplicate Rows", f"{int(df.duplicated().sum()):,}")

    st.write("")

    with st.container(border=True):
        section_heading(
            "Dataset preview",
            "Your first ten records."
        )
        st.dataframe(df.head(10), width="stretch")


# --------------------------------------------------
# DATA CLEANING
# --------------------------------------------------

elif page == "Data Cleaning":

    hero(
        "Clean data. <span>Clear decisions.</span>",
        "Prepare your dataset for reliable analysis.",
        "DATA QUALITY / CLEANING"
    )

    section_heading(
        "Data quality check",
        "Review missing values and duplicate records before cleaning."
    )

    col1, col2, col3 = st.columns(3)

    col1.metric("Original Records", len(df))
    col2.metric("Missing Values", int(df.isnull().sum().sum()))
    col3.metric("Duplicate Rows", int(df.duplicated().sum()))

    with st.container(border=True):
        section_heading(
            "Cleaning workspace",
            "Missing numeric values are filled using the median. "
            "Other missing values use the most frequent value."
        )

        if st.button("✦ Clean My Dataset", type="primary"):

            st.session_state["cleaned_df"] = clean_dataset(df)

            st.success("Dataset cleaned successfully!")

    cleaned = st.session_state.get("cleaned_df")

    if cleaned is not None:

        section_heading(
            "Cleaning results",
            "Compare the quality of your cleaned dataset."
        )

        col1, col2, col3 = st.columns(3)

        col1.metric("Final Records", len(cleaned))
        col2.metric(
            "Remaining Missing",
            int(cleaned.isnull().sum().sum())
        )
        col3.metric(
            "Remaining Duplicates",
            int(cleaned.duplicated().sum())
        )

        with st.container(border=True):
            st.subheader("Cleaned dataset preview")
            st.dataframe(cleaned, width="stretch")


# --------------------------------------------------
# ANALYSIS & CHARTS
# --------------------------------------------------

elif page == "Analysis & Charts":

    hero(
        "Discover the <span>story in your data.</span>",
        "Explore patterns, distributions and relationships through interactive charts.",
        "ANALYTICS / VISUALIZATION"
    )

    cleaned = st.session_state.get("cleaned_df")

    if cleaned is None:
        st.warning("Please clean your dataset first.")
        st.stop()

    numeric_columns = cleaned.select_dtypes(
        include="number"
    ).columns.tolist()

    categorical_columns = cleaned.select_dtypes(
        exclude="number"
    ).columns.tolist()

    if numeric_columns:

        section_heading(
            "Statistical intelligence",
            "Choose a calculation and numerical column."
        )

        with st.container(border=True):

            stat_options = {
                "Average": "mean",
                "Sum": "sum",
                "Maximum": "max",
                "Minimum": "min",
                "Median": "median",
                "Standard Deviation": "std",
                "Variance": "var",
                "Count": "count"
            }

            col1, col2 = st.columns(2)

            selected_stat = col1.selectbox(
                "Select calculation",
                list(stat_options.keys()),
                key="stat_calculation"
            )

            selected_column = col2.selectbox(
                "Select numerical column",
                numeric_columns,
                key="stat_column"
            )

            result = getattr(
                cleaned[selected_column],
                stat_options[selected_stat]
            )()

            st.metric(
                f"{selected_stat} of {selected_column}",
                f"{result:,.2f}" if pd.notna(result) else "Not available"
            )

    st.divider()

    section_heading(
        "Visual exploration studio",
        "Choose a chart, select your columns and explore your data."
    )

    with st.container(border=True):

        chart_type = st.selectbox(
            "Select visualization",
            [
                "Bar Chart",
                "Pie Chart",
                "Line Chart",
                "Histogram",
                "Box Plot",
                "Scatter Plot",
                "Correlation Heatmap"
            ]
        )

        fig, ax = plt.subplots(figsize=(10, 5))

        fig.patch.set_facecolor("#111a2e")
        ax.set_facecolor("#15213a")

        ax.tick_params(colors="#c5d1e5")
        ax.xaxis.label.set_color("#c5d1e5")
        ax.yaxis.label.set_color("#c5d1e5")
        ax.title.set_color("#ffffff")

        for spine in ax.spines.values():
            spine.set_color("#43536d")

        try:

            if chart_type == "Bar Chart":

                if not categorical_columns or not numeric_columns:
                    st.warning(
                        "Bar chart requires at least one categorical "
                        "and one numeric column."
                    )
                else:

                    col1, col2, col3 = st.columns(3)

                    category = col1.selectbox(
                        "Category",
                        categorical_columns,
                        key="bar_category"
                    )

                    value = col2.selectbox(
                        "Numeric column",
                        numeric_columns,
                        key="bar_value"
                    )

                    aggregation = col3.selectbox(
                        "Aggregation",
                        ["Sum", "Average", "Count"],
                        key="bar_aggregation"
                    )

                    if aggregation == "Sum":
                        chart_data = cleaned.groupby(category)[value].sum()
                    elif aggregation == "Average":
                        chart_data = cleaned.groupby(category)[value].mean()
                    else:
                        chart_data = cleaned.groupby(category)[value].count()

                    chart_data = chart_data.head(20)

                    ax.bar(
                        chart_data.index.astype(str),
                        chart_data.values,
                        color="#48e5e0",
                        width=0.65
                    )

                    ax.set_title(f"{aggregation} of {value} by {category}")
                    ax.set_xlabel(category)
                    ax.set_ylabel(aggregation)
                    plt.xticks(rotation=40, ha="right")

                    st.pyplot(fig)

            elif chart_type == "Pie Chart":

                if not categorical_columns:
                    st.warning("Pie chart requires a categorical column.")
                else:

                    category = st.selectbox(
                        "Category",
                        categorical_columns,
                        key="pie_category"
                    )

                    chart_data = (
                        cleaned[category]
                        .astype(str)
                        .value_counts()
                        .head(10)
                    )

                    ax.pie(
                        chart_data.values,
                        labels=chart_data.index,
                        autopct="%1.1f%%",
                        startangle=90,
                        textprops={"color": "white"},
                        wedgeprops={"edgecolor": "#111a2e"}
                    )

                    ax.set_title(f"Distribution of {category}")

                    st.pyplot(fig)

            elif chart_type == "Line Chart":

                if not numeric_columns:
                    st.warning("Line chart requires a numeric column.")
                else:

                    x_options = ["Row Number"] + list(cleaned.columns)

                    col1, col2 = st.columns(2)

                    x_column = col1.selectbox(
                        "X-axis",
                        x_options,
                        key="line_x"
                    )

                    y_column = col2.selectbox(
                        "Y-axis",
                        numeric_columns,
                        key="line_y"
                    )

                    x_values = (
                        range(1, len(cleaned) + 1)
                        if x_column == "Row Number"
                        else cleaned[x_column]
                    )

                    ax.plot(
                        x_values,
                        cleaned[y_column],
                        color="#48e5e0",
                        marker="o",
                        linewidth=2,
                        markersize=4
                    )

                    ax.set_title(f"{y_column} Trend")
                    ax.set_xlabel(x_column)
                    ax.set_ylabel(y_column)

                    plt.xticks(rotation=40, ha="right")

                    st.pyplot(fig)

            elif chart_type == "Histogram":

                if not numeric_columns:
                    st.warning("Histogram requires a numeric column.")
                else:

                    column = st.selectbox(
                        "Numeric column",
                        numeric_columns,
                        key="hist_column"
                    )

                    ax.hist(
                        cleaned[column].dropna(),
                        bins=15,
                        color="#9c8cff",
                        edgecolor="#111a2e"
                    )

                    ax.set_title(f"Distribution of {column}")
                    ax.set_xlabel(column)
                    ax.set_ylabel("Frequency")

                    st.pyplot(fig)

            elif chart_type == "Box Plot":

                if not numeric_columns:
                    st.warning("Box plot requires a numeric column.")
                else:

                    column = st.selectbox(
                        "Numeric column",
                        numeric_columns,
                        key="box_column"
                    )

                    ax.boxplot(
                        cleaned[column].dropna(),
                        patch_artist=True,
                        boxprops={"facecolor": "#48e5e0"},
                        medianprops={"color": "#17213a"}
                    )

                    ax.set_title(f"Box Plot of {column}")
                    ax.set_ylabel(column)

                    st.pyplot(fig)

            elif chart_type == "Scatter Plot":

                if len(numeric_columns) < 2:
                    st.warning(
                        "Scatter plot requires at least two numeric columns."
                    )
                else:

                    col1, col2 = st.columns(2)

                    x_column = col1.selectbox(
                        "X-axis",
                        numeric_columns,
                        key="scatter_x"
                    )

                    y_column = col2.selectbox(
                        "Y-axis",
                        numeric_columns,
                        key="scatter_y"
                    )

                    ax.scatter(
                        cleaned[x_column],
                        cleaned[y_column],
                        color="#c4f56b",
                        alpha=0.75,
                        edgecolors="#111a2e"
                    )

                    ax.set_title(f"{x_column} vs {y_column}")
                    ax.set_xlabel(x_column)
                    ax.set_ylabel(y_column)

                    st.pyplot(fig)

            elif chart_type == "Correlation Heatmap":

                if len(numeric_columns) < 2:
                    st.warning(
                        "Heatmap requires at least two numeric columns."
                    )
                else:

                    correlation = cleaned[numeric_columns].corr()

                    image = ax.imshow(
                        correlation,
                        cmap="coolwarm",
                        vmin=-1,
                        vmax=1
                    )

                    ax.set_xticks(range(len(correlation.columns)))
                    ax.set_yticks(range(len(correlation.columns)))

                    ax.set_xticklabels(
                        correlation.columns,
                        rotation=45,
                        ha="right"
                    )

                    ax.set_yticklabels(correlation.columns)

                    for i in range(len(correlation.columns)):
                        for j in range(len(correlation.columns)):
                            ax.text(
                                j,
                                i,
                                f"{correlation.iloc[i, j]:.2f}",
                                ha="center",
                                va="center",
                                color="white"
                            )

                    ax.set_title("Correlation Heatmap")
                    fig.colorbar(image, ax=ax)

                    st.pyplot(fig)

        except Exception as error:
            st.error(f"Unable to create chart: {error}")

        finally:
            plt.close(fig)


# --------------------------------------------------
# AI ASSISTANT
# --------------------------------------------------

elif page == "AI Assistant":

    hero(
        "Ask your data. <span>Get answers.</span>",
        "Explore your dataset using natural-language questions.",
        "INTELLIGENCE / ASSISTANT"
    )

    cleaned = st.session_state.get("cleaned_df")

    if cleaned is None:
        st.warning("Please clean your dataset first.")

    else:

        with st.container(border=True):

            section_heading(
                "Your analysis assistant",
                "Ask questions about your uploaded dataset."
            )

            question = st.text_input(
                "What would you like to know?",
                placeholder="Ask anything about your data..."
            )

            if st.button("✦ Generate Answer", type="primary"):

                if question.strip():

                    with st.spinner("AI is analysing your question..."):

                        dataset_csv = cleaned.to_csv(index=False)

                        if len(dataset_csv) <= 20000:
                            dataset_context = (
                                "Complete dataset:\n" + dataset_csv
                            )
                        else:
                            dataset_context = (
                                "Dataset is too large to send completely.\n"
                                f"Total rows: {len(cleaned)}\n"
                                f"Columns: {cleaned.columns.tolist()}\n"
                                f"Data types:\n{cleaned.dtypes.to_string()}\n"
                                f"Summary:\n{cleaned.describe(include='all').to_string()}\n"
                                f"Sample records:\n{cleaned.head(10).to_string(index=False)}\n"
                                "This is only a summary and sample, not the complete dataset."
                            )

                        result = ask_gemini(
                            question,
                            dataset_context
                        )

                    st.success("AI Response")
                    st.write(result)

                else:
                    st.warning("Please enter a question.")

        st.caption(
            "Powered by Google AI and your uploaded dataset."
        )


# --------------------------------------------------
# REPORTS
# --------------------------------------------------

elif page == "Reports":

    hero(
        "Insights ready. <span>Reports delivered.</span>",
        "Download your cleaned dataset and analysis summary.",
        "OUTPUT / REPORT CENTER"
    )

    cleaned = st.session_state.get("cleaned_df")

    if cleaned is None:
        st.warning("Please clean your dataset first.")
        st.stop()

    section_heading(
        "Export center",
        "Your analysis files are ready to download."
    )

    col1, col2 = st.columns(2)

    csv_data = cleaned.to_csv(index=False).encode("utf-8")

    with col1:
        with st.container(border=True):

            st.markdown("### 📁 Cleaned Dataset")
            st.write("Download your cleaned data in CSV format.")

            st.download_button(
                "Download CSV",
                data=csv_data,
                file_name="cleaned_dataset.csv",
                mime="text/csv"
            )

    numeric = cleaned.select_dtypes(include="number")

    report = [
        " DATA INTELLIGENCE REPORT",
        "================================",
        "",
        "DATASET INFORMATION",
        f"Total Rows: {len(cleaned)}",
        f"Total Columns: {len(cleaned.columns)}",
        "",
        "DATA QUALITY",
        f"Missing Values: {cleaned.isnull().sum().sum()}",
        f"Duplicate Rows: {cleaned.duplicated().sum()}",
        "",
        "COLUMN INFORMATION",
        cleaned.dtypes.to_string(),
        "",
        "NUMERICAL SUMMARY",
        (
            numeric.describe().to_string()
            if not numeric.empty
            else "No numeric columns available."
        )
    ]

    report_text = "\n".join(report)

    with col2:
        with st.container(border=True):

            st.markdown("### 📄 Analysis Report")
            st.write("Download the analysis summary in TXT format.")

            st.download_button(
                "Download Report",
                data=report_text,
                file_name="analysis_report.txt",
                mime="text/plain"
            )


# --------------------------------------------------
# FOOTER
# --------------------------------------------------

st.markdown("""
<div style="
    margin-top:45px;
    padding:22px;
    text-align:center;
    border-top:1px solid rgba(148,163,184,0.16);
">
    <div style="font-family:Space Grotesk;font-size:17px;font-weight:700;color:#48e5e0;">
        ✦DATA STUDIO
    </div>
    <div style="font-size:11px;color:#8294b1;margin-top:8px;letter-spacing:1px;">
        TRANSFORMING DATA INTO INTELLIGENCE
    </div>
</div>
""", unsafe_allow_html=True)
