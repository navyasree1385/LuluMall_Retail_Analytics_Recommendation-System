import streamlit as st
import pandas as pd
from pathlib import Path
from sklearn.metrics.pairwise import cosine_similarity


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="Lulu Mall | Smart Recommendations",
    page_icon="🛍️",
    layout="wide"
)


# ============================================================
# CUSTOM CSS
# ============================================================

st.markdown("""
<style>

.main {
    background-color: #f7f8fc;
}


/* =========================================================
   HERO HEADER
   ========================================================= */

.hero {
    padding: 30px;
    border-radius: 18px;
    background: linear-gradient(
        135deg,
        #174a7c,
        #2878c8
    );
    color: white;
    margin-bottom: 30px;
    box-shadow: 0 5px 18px rgba(0,0,0,0.15);
}

.hero h1 {
    font-size: 42px;
    margin-bottom: 8px;
}

.hero p {
    font-size: 17px;
}


/* =========================================================
   PRODUCT CARDS
   ========================================================= */

.product-card {
    padding: 22px;
    border-radius: 18px;
    background: white;
    border: 1px solid #e1e5eb;
    box-shadow: 0 5px 15px rgba(0,0,0,0.08);
    min-height: 270px;
    transition: 0.2s;
}

.product-card:hover {
    box-shadow: 0 8px 22px rgba(0,0,0,0.14);
    transform: translateY(-2px);
}

.product-icon {
    font-size: 35px;
    margin-bottom: 10px;
}

.product-name {
    font-size: 20px;
    font-weight: 700;
    color: #172033;
    min-height: 55px;
}

.category-badge {
    display: inline-block;
    padding: 5px 10px;
    border-radius: 20px;
    background: #e8f1ff;
    color: #2563eb;
    font-size: 12px;
    font-weight: 600;
    margin: 8px 0;
}

.product-price {
    font-size: 20px;
    font-weight: 700;
    color: #111827;
    margin-top: 8px;
}

.score {
    font-size: 14px;
    font-weight: 700;
    color: #2563eb !important;
}

.reason {
    color: #6b7280 !important;
    font-size: 13px;
    line-height: 1.5;
}


/* =========================================================
   CUSTOMER PURCHASE CARD
   ========================================================= */

.purchase-card {
    padding: 22px;
    border-radius: 15px;
    background: white;
    border-left: 5px solid #2878c8;
    box-shadow: 0 3px 10px rgba(0,0,0,0.06);
    color: #172033 !important;
}

.purchase-card h3 {
    color: #172033 !important;
    font-size: 21px;
    margin-bottom: 15px;
}

.purchase-card p {
    color: #374151 !important;
    font-size: 15px;
    margin: 8px 0;
}

.purchase-card b {
    color: #172033 !important;
}


/* =========================================================
   CUSTOMER PROFILE
   ========================================================= */

.profile-card {
    padding: 15px;
    border-radius: 15px;
    background: white;
    border: 1px solid #e1e5eb;
}


/* =========================================================
   SECTION TITLES
   ========================================================= */

.section-title {
    font-size: 25px;
    font-weight: 700;
    color: #172033;
    margin-top: 25px;
    margin-bottom: 15px;
}

</style>
""", unsafe_allow_html=True)


# ============================================================
# LOAD DATA
# ============================================================

@st.cache_data
def load_data():

    DATA_PATH = Path(__file__).resolve().parent/"Lulu_Mall_Sales_Dataset.xlsx"

    df = pd.read_excel(DATA_PATH)

    return df


df = load_data()


# ============================================================
# CUSTOMER-PRODUCT MATRIX
# ============================================================

customer_product_matrix = df.pivot_table(
    index="Customer_ID",
    columns="Product_Name",
    values="Quantity",
    aggfunc="sum",
    fill_value=0
)


# ============================================================
# PRODUCT SIMILARITY
# ============================================================

product_similarity = cosine_similarity(
    customer_product_matrix.T
)

product_similarity_df = pd.DataFrame(
    product_similarity,
    index=customer_product_matrix.columns,
    columns=customer_product_matrix.columns
)


# ============================================================
# PRODUCT RECOMMENDATION FUNCTION
# ============================================================

def recommend_products(product_name, n=5):

    if product_name not in product_similarity_df.index:

        return pd.DataFrame(
            columns=[
                "Product_Name",
                "Score"
            ]
        )

    similar_products = (
        product_similarity_df[product_name]
        .sort_values(ascending=False)
    )

    recommendations = similar_products.iloc[1:n + 1]

    result = recommendations.reset_index()

    result.columns = [
        "Product_Name",
        "Score"
    ]

    return result


# ============================================================
# CUSTOMER RECOMMENDATION FUNCTION
# ============================================================

# ============================================================
# SMART CUSTOMER RECOMMENDATION ENGINE
# ============================================================

def recommend_for_customer(customer_id, n=5):

    # --------------------------------------------------------
    # Validate customer
    # --------------------------------------------------------

    if customer_id not in customer_product_matrix.index:

        return pd.DataFrame(
            columns=["Product_Name", "Score"]
        )

    # --------------------------------------------------------
    # Customer purchase vector
    # --------------------------------------------------------

    customer_vector = (
        customer_product_matrix
        .loc[customer_id]
        .values
        .reshape(1, -1)
    )

    # --------------------------------------------------------
    # Find similar customers
    # --------------------------------------------------------

    customer_similarity = cosine_similarity(
        customer_vector,
        customer_product_matrix.values
    )[0]

    similarity_scores = pd.Series(
        customer_similarity,
        index=customer_product_matrix.index
    )

    # Remove the selected customer
    similarity_scores = similarity_scores.drop(
        customer_id,
        errors="ignore"
    )

    # Keep customers with meaningful similarity
    similar_customers = (
        similarity_scores[
            similarity_scores > 0
        ]
        .sort_values(ascending=False)
        .head(20)
    )

    # --------------------------------------------------------
    # Products already purchased by customer
    # --------------------------------------------------------

    purchased_products = set(
        customer_product_matrix
        .loc[customer_id]
        .loc[lambda x: x > 0]
        .index
    )

    # --------------------------------------------------------
    # Collaborative filtering scores
    # --------------------------------------------------------

    collaborative_scores = {}

    for similar_customer, similarity in similar_customers.items():

        customer_products = (
            customer_product_matrix
            .loc[similar_customer]
        )

        for product, quantity in customer_products.items():

            if (
                quantity > 0
                and product not in purchased_products
            ):

                collaborative_scores[product] = (
                    collaborative_scores.get(product, 0)
                    + similarity * quantity
                )

    # --------------------------------------------------------
    # Product popularity
    # --------------------------------------------------------

    product_popularity = (
        df.groupby("Product_Name")["Customer_ID"]
        .nunique()
        .to_dict()
    )

    # --------------------------------------------------------
    # Category preference
    # --------------------------------------------------------

    customer_categories = set(
        df[
            df["Customer_ID"] == customer_id
        ]["Product_Category"]
        .dropna()
        .unique()
    )

    # --------------------------------------------------------
    # Calculate final hybrid score
    # --------------------------------------------------------

    final_scores = {}

    for product, collaborative_score in (
        collaborative_scores.items()
    ):

        # Popularity score
        popularity = product_popularity.get(
            product,
            0
        )

        # Normalize popularity
        total_customers = max(
            len(customer_product_matrix),
            1
        )

        popularity_score = (
            popularity / total_customers
        )

        # Product category
        product_rows = df[
            df["Product_Name"] == product
        ]

        if len(product_rows) > 0:

            product_category = (
                product_rows[
                    "Product_Category"
                ]
                .iloc[0]
            )

        else:

            product_category = None

        # Category preference bonus
        category_bonus = (
            1.0
            if product_category in customer_categories
            else 0.0
        )

        # ----------------------------------------------------
        # Hybrid recommendation score
        # ----------------------------------------------------

        final_score = (
            collaborative_score * 0.70
            + popularity_score * 0.20
            + category_bonus * 0.10
        )

        final_scores[product] = final_score

    # --------------------------------------------------------
    # Sort recommendations
    # --------------------------------------------------------

    recommendations = (
        pd.Series(final_scores)
        .sort_values(ascending=False)
        .head(n)
        .reset_index()
    )

    # --------------------------------------------------------
    # Handle empty recommendations
    # --------------------------------------------------------

    if len(recommendations) == 0:

        return pd.DataFrame(
            columns=["Product_Name", "Score"]
        )

    recommendations.columns = [
        "Product_Name",
        "Score"
    ]

    return recommendations


# ============================================================
# CATEGORY ICON FUNCTION
# ============================================================

def get_category_icon(category):

    category = str(category).lower()

    if "electronics" in category:

        return "💻"

    elif "fashion" in category:

        return "👕"

    elif "grocery" in category:

        return "🛒"

    elif "beauty" in category:

        return "💄"

    elif "home" in category:

        return "🏠"

    else:

        return "🛍️"


# ============================================================
# HERO HEADER
# ============================================================

st.markdown("""
<div class="hero">

<h1>🛍️ Lulu Mall</h1>

<p>
Smart Product Recommendation System
</p>

<p>
Discover products based on customer purchasing behavior.
</p>

</div>
""", unsafe_allow_html=True)


# ============================================================
# SIDEBAR
# ============================================================

st.sidebar.title(
    "⚙️ Recommendation Settings"
)

recommendation_type = st.sidebar.radio(
    "Recommendation Type",
    [
        "Product Based",
        "Personalized Customer"
    ]
)

number_of_recommendations = st.sidebar.slider(
    "Number of Recommendations",
    min_value=3,
    max_value=10,
    value=5
)
# ===========================================================
# BUDGET FILTER
# ===========================================================
max_budget = st.sidebar.slider(
    "💰 Maximum Budget",
    min_value=500,
    max_value=100000,
    value=10000,
    step=500,
    format="₹%d"
)


# ============================================================
# PRODUCT BASED MODE
# ============================================================

if recommendation_type == "Product Based":

    st.subheader(
        "🔎 Find Similar Products"
    )

    # --------------------------------------------------------
    # PRODUCT LIST
    # --------------------------------------------------------

    product_list = sorted(
        df["Product_Name"]
        .dropna()
        .unique()
    )

    # --------------------------------------------------------
    # SEARCH PRODUCT
    # --------------------------------------------------------

    search_product = st.text_input(
        "🔎 Search for a product",
        placeholder="Type a product name..."
    )

    if search_product:

        filtered_products = [
            product
            for product in product_list
            if search_product.lower()
            in product.lower()
        ]

    else:

        filtered_products = product_list

    # --------------------------------------------------------
    # PRODUCT SELECTION
    # --------------------------------------------------------

    if filtered_products:

        selected_product = st.selectbox(
            "Select a product you like",
            filtered_products
        )

        # ----------------------------------------------------
        # RECOMMENDATION BUTTON
        # ----------------------------------------------------

        recommend_button = st.button(
            "✨ Get Recommendations",
            use_container_width=True
        )

        # ----------------------------------------------------
        # GENERATE RECOMMENDATIONS
        # ----------------------------------------------------

        if recommend_button:

            recommendations = recommend_products(
                selected_product,
                number_of_recommendations
            )
            recommendations = recommendations[
                recommendations["Product_Name"].map(
                    df.groupby("Product_Name")["Unit_Price"].first()
                ) <= max_budget
            ]

            st.subheader(
                f"⭐ Products similar to: "
                f"{selected_product}"
            )

            if len(recommendations) == 0:

                st.warning(
                    "No recommendations available."
                )

            else:

                # ------------------------------------------------
                # DISPLAY MAXIMUM 5 CARDS PER ROW
                # ------------------------------------------------

                for start in range(
                    0,
                    len(recommendations),
                    5
                ):

                    batch = recommendations.iloc[
                        start:start + 5
                    ]

                    cols = st.columns(
                        len(batch)
                    )

                    for col, (_, row) in zip(
                        cols,
                        batch.iterrows()
                    ):

                        product_name = (
                            row["Product_Name"]
                        )

                        score = row["Score"]

                        # ----------------------------------------
                        # PRODUCT INFORMATION
                        # ----------------------------------------

                        product_info = df[
                            df["Product_Name"]
                            == product_name
                        ]

                        if len(product_info) > 0:

                            category = (
                                product_info[
                                    "Product_Category"
                                ].iloc[0]
                            )

                            price = (
                                product_info[
                                    "Unit_Price"
                                ].iloc[0]
                            )

                        else:

                            category = "Other"

                            price = 0

                        icon = get_category_icon(
                            category
                        )

                        similarity_percentage = (
                            score * 100
                        )

                        # ----------------------------------------
                        # PRODUCT CARD HTML
                        # ----------------------------------------

                        html = f"""<div class="product-card">
                        <div class="product-icon">{icon}</div>
                        <div class="product-name">{product_name}</div>
                        <div class="category-badge">{category}</div>
                        <div class="product-price">₹{price:,.0f}</div>
                        <p class="score">⭐ Similarity: {similarity_percentage:.1f}%</p>
                        <p class="reason">💡 Recommended based on similar customer purchasing patterns.</p>
                        </div>"""

                        col.markdown(
                            html,
                            unsafe_allow_html=True
                        )

    else:

        st.warning(
            "No matching products found."
        )


# ============================================================
# PERSONALIZED CUSTOMER MODE
# ============================================================

else:

    st.subheader(
        "👤 Personalized Recommendations"
    )

    # --------------------------------------------------------
    # CUSTOMER LIST
    # --------------------------------------------------------

    customer_list = sorted(
        customer_product_matrix.index
    )

    selected_customer = st.selectbox(
        "Select Customer ID",
        customer_list
    )

    # --------------------------------------------------------
    # CUSTOMER DATA
    # --------------------------------------------------------

    customer_data = df[
        df["Customer_ID"]
        == selected_customer
    ].copy()

    # --------------------------------------------------------
    # CUSTOMER PROFILE
    # --------------------------------------------------------

    st.markdown(
        "### 👤 Customer Profile"
    )

    col1, col2, col3 = st.columns(3)

    with col1:

        st.metric(
            "Customer Orders",
            customer_data[
                "Order_ID"
            ].nunique()
        )

    with col2:

        st.metric(
            "Products Purchased",
            customer_data[
                "Product_Name"
            ].nunique()
        )

    with col3:

        st.metric(
            "Customer Revenue",
            f"₹{customer_data['Revenue'].sum():,.0f}"
        )

    # --------------------------------------------------------
    # PURCHASE HISTORY
    # --------------------------------------------------------

    st.markdown(
        "### 🛒 Purchase History"
    )

    purchase_history = (
        customer_data
        .groupby(
            [
                "Product_Name",
                "Product_Category"
            ],
            as_index=False
        )
        .agg(
            Quantity=(
                "Quantity",
                "sum"
            ),
            Revenue=(
                "Revenue",
                "sum"
            )
        )
        .sort_values(
            "Revenue",
            ascending=False
        )
    )

    if len(purchase_history) > 0:

        for _, purchase in (
            purchase_history.iterrows()
        ):

            purchase_html = f"""<div class="purchase-card">
            <h3>🛍️ {purchase["Product_Name"]}</h3>
            <p><b>Category:</b> {purchase["Product_Category"]}</p>
            <p><b>Quantity:</b> {purchase["Quantity"]}</p>
            <p><b>Amount Spent:</b> ₹{purchase["Revenue"]:,.0f}</p>
            </div>"""

            st.markdown(
                purchase_html,
                unsafe_allow_html=True
            )

    # --------------------------------------------------------
    # PERSONALIZED RECOMMENDATION BUTTON
    # --------------------------------------------------------

    recommend_button = st.button(
        "✨ Get Personalized Recommendations",
        use_container_width=True
    )

    # --------------------------------------------------------
    # PERSONALIZED RECOMMENDATIONS
    # --------------------------------------------------------

    if recommend_button:

        recommendations = recommend_for_customer(
            selected_customer,
            number_of_recommendations
        )
        recommendations = recommendations[
            recommendations["Product_Name"].map(
                df.groupby("Product_Name")["Unit_Price"].first()
            ) <= max_budget
        ]

        st.markdown(
            "### ⭐ Recommended For You"
        )

        if len(recommendations) == 0:

            st.warning(
                "No personalized recommendations available."
            )

        else:

            # ------------------------------------------------
            # MAXIMUM 5 CARDS PER ROW
            # ------------------------------------------------

            for start in range(
                0,
                len(recommendations),
                5
            ):

                batch = recommendations.iloc[
                    start:start + 5
                ]

                cols = st.columns(
                    len(batch)
                )

                for col, (_, row) in zip(
                    cols,
                    batch.iterrows()
                ):

                    product_name = (
                        row["Product_Name"]
                    )

                    score = row["Score"]

                    # ----------------------------------------
                    # PRODUCT INFORMATION
                    # ----------------------------------------

                    product_info = df[
                        df["Product_Name"]
                        == product_name
                    ]

                    if len(product_info) > 0:

                        category = (
                            product_info[
                                "Product_Category"
                            ].iloc[0]
                        )

                        price = (
                            product_info[
                                "Unit_Price"
                            ].iloc[0]
                        )

                    else:

                        category = "Other"

                        price = 0

                    icon = get_category_icon(
                        category
                    )

                    # ----------------------------------------
                    # PERSONALIZED CARD
                    # ----------------------------------------

                    html = f"""<div class="product-card">
                    <div class="product-icon">{icon}</div>
                    <div class="product-name">{product_name}</div>
                    <div class="category-badge">{category}</div>
                    <div class="product-price">₹{price:,.0f}</div>
                    <p class="score">⭐ Recommendation Score: {score:.2f}</p>
                    <p class="reason">💡 Customers with similar purchasing behavior purchased this product.</p>
                    </div>"""

                    col.markdown(
                        html,
                        unsafe_allow_html=True
                    )


# ============================================================
# FOOTER
# ============================================================

st.markdown("---")

st.caption(
    "Lulu Mall Retail Analytics | "
    "Python • Machine Learning • Streamlit"
)