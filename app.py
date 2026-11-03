import streamlit as st

from core.pipeline import run_pipeline
from models.schemas import ProductInput
from scoring.config import DEFAULT_WEIGHTS
from services.email import send_email


st.set_page_config(
    page_title="Product Sales Agent",
    layout="wide",
)


st.title(
    "🔎 Product Sales Intelligence Agent"
)

st.write(
    "Research → Critic → Writer → "
    "Market → Clients → Ranking → Sales"
)


# ==========================================
# INPUT
# ==========================================

st.header("Product")

product_name = st.text_input(
    "Product name *"
)

description = st.text_area(
    "Description (optional)"
)

website = st.text_input(
    "Product website (optional)"
)

target_country = st.text_input(
    "Target country (optional)"
)


# ==========================================
# WEIGHTS
# ==========================================

st.header("Ranking weights")

col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    industry_weight = st.number_input(
        "Industry",
        0,
        100,
        DEFAULT_WEIGHTS["industry"],
    )

with col2:
    geography_weight = st.number_input(
        "Geography",
        0,
        100,
        DEFAULT_WEIGHTS["geography"],
    )

with col3:
    evidence_weight = st.number_input(
        "Evidence",
        0,
        100,
        DEFAULT_WEIGHTS["evidence"],
    )

with col4:
    relevance_weight = st.number_input(
        "Relevance",
        0,
        100,
        DEFAULT_WEIGHTS["relevance"],
    )

with col5:
    accessibility_weight = st.number_input(
        "Accessibility",
        0,
        100,
        DEFAULT_WEIGHTS["accessibility"],
    )


weights = {
    "industry": industry_weight,
    "geography": geography_weight,
    "evidence": evidence_weight,
    "relevance": relevance_weight,
    "accessibility": accessibility_weight,
}


# ==========================================
# RUN
# ==========================================

if st.button(
    "🚀 Start Research",
    type="primary",
):

    if not product_name.strip():

        st.error(
            "Product name is required."
        )

        st.stop()

    if sum(weights.values()) != 100:

        st.error(
            "Ranking weights must equal 100."
        )

        st.stop()

    product = ProductInput(
        name=product_name,
        description=description or None,
        website=website or None,
        target_country=target_country or None,
    )

    progress_box = st.empty()

    logs = []

    def update_progress(message):

        logs.append(message)

        progress_box.code(
            "\n".join(logs)
        )

    try:

        results = run_pipeline(
            product,
            weights,
            update_progress,
        )

        st.session_state[
            "results"
        ] = results

        st.success(
            "Pipeline completed."
        )

    except Exception as exc:

        st.error(
            f"Pipeline failed safely: {exc}"
        )


# ==========================================
# RESULTS
# ==========================================

results = st.session_state.get(
    "results"
)


if results:

    # ======================================
    # PRODUCT
    # ======================================

    st.header(
        "1. Final Product Overview"
    )

    st.write(
        results["writer"][
            "product_overview"
        ]
    )

    st.caption(
        f"Characters: "
        f"{len(results['writer']['product_overview'])}"
    )

    # ======================================
    # SOURCES
    # ======================================

    st.header(
        "2. Sources"
    )

    for source in results[
        "research"
    ]["sources"]:

        status = (
            "✓"
            if source["accessible"]
            else "✗"
        )

        st.write(
            f"{status} "
            f"{source['source_type'].upper()} "
            f"- {source['url']}"
        )

    # ======================================
    # CRITIC
    # ======================================

    st.header(
        "3. Critic"
    )

    critic = results[
        "critic"
    ]

    st.subheader(
        "Weaknesses"
    )

    for item in critic[
        "weaknesses"
    ]:

        st.write(
            f"- {item}"
        )

    st.subheader(
        "Unsupported claims"
    )

    for item in critic[
        "unsupported_claims"
    ]:

        st.warning(
            item
        )

    # ======================================
    # MARKET
    # ======================================

    st.header(
        "4. Market Analysis"
    )

    for index, step in enumerate(
        results["market_steps"],
        start=1,
    ):

        with st.expander(
            f"Market Step {index}"
        ):

            st.write(step)

    # ======================================
    # PROVIDER
    # ======================================

    st.header(
        "5. Provider Reasoning"
    )

    st.write(
        results["provider"]
    )

    # ======================================
    # CLIENTS
    # ======================================

    st.header(
        "6. Potential Clients"
    )

    for client in results[
        "clients"
    ]["clients"]:

        with st.expander(
            client["name"]
        ):

            st.write(
                f"Country: "
                f"{client['country']}"
            )

            st.write(
                f"Field: "
                f"{client['field']}"
            )

            st.write(
                f"Website: "
                f"{client['website']}"
            )

            st.write(
                f"Evidence status: "
                f"{client['evidence_status']}"
            )

            st.write(
                f"Reason: "
                f"{client['reason']}"
            )

            st.write(
                "Evidence:"
            )

            for evidence in client[
                "evidence"
            ]:

                st.write(
                    f"- {evidence}"
                )

    # ======================================
    # RANKING
    # ======================================

    st.header(
        "7. Client Ranking"
    )

    for index, client in enumerate(
        results["ranking"],
        start=1,
    ):

        st.subheader(
            f"#{index} "
            f"{client['name']} "
            f"— {client['score']}/100"
        )

        st.write(
            f"Industry: "
            f"{client['industry_score']}"
        )

        st.write(
            f"Geography: "
            f"{client['geography_score']}"
        )

        st.write(
            f"Evidence: "
            f"{client['evidence_score']}"
        )

        st.write(
            f"Relevance: "
            f"{client['relevance_score']}"
        )

        st.write(
            f"Accessibility: "
            f"{client['accessibility_score']}"
        )

        st.caption(
            client["explanation"]
        )

    # ======================================
    # EMAILS
    # ======================================

    st.header(
        "8. Sales Emails"
    )

    for index, email in enumerate(
        results["sales_emails"],
        start=1,
    ):

        with st.expander(
            f"Email #{index} — "
            f"{email['client_name']}"
        ):

            recipient = st.text_input(
                f"Email address "
                f"for {email['client_name']}",
                key=f"email_{index}",
            )

            st.text_input(
                "Subject",
                value=email["subject"],
                key=f"subject_{index}",
            )

            st.text_area(
                "Message",
                value=email["body"],
                height=300,
                key=f"body_{index}",
            )

            if st.button(
                "📧 Send Email",
                key=f"send_{index}",
            ):

                result = send_email(
                    recipient,
                    email["subject"],
                    email["body"],
                )

                if result["success"]:

                    st.success(
                        result["message"]
                    )

                else:

                    st.error(
                        result["message"]
                    )