import streamlit as st
from rag_pipeline import DataFlowDoctorRAG
from lineage import downstream_assets, upstream_assets

st.set_page_config(page_title="DataFlow Doctor", page_icon="🩺", layout="wide")
st.title("DataFlow Doctor - Data Pipeline & ETL Debugging RAG")
st.caption("Sir's Labs 1-6 flow: split -> embed -> Chroma -> hybrid retrieval -> structured output -> LangGraph")

@st.cache_resource
def get_rag():
    return DataFlowDoctorRAG()

rag = get_rag()
left, right = st.columns([2, 1])
with left:
    pipeline = st.selectbox("Pipeline scope", ["all", "orders", "customers", "clickstream", "inventory", "platform"])
    method = st.selectbox("Retrieval", ["hybrid", "similarity", "mmr"])
    question = st.text_area(
        "Pipeline question",
        "The orders schema validation says discount_code is unexpected. What happened and what should I check?",
        height=120,
    )
    if st.button("Diagnose pipeline"):
        try:
            answer, docs = rag.ask(pipeline, question, method)
            st.subheader("Evidence-grounded diagnosis")
            st.json(answer.model_dump())
            st.subheader("Retrieved evidence")
            for d in docs:
                with st.expander(d.metadata.get("source", "source")):
                    st.write(d.page_content)
                    st.caption(str(d.metadata))
        except Exception as e:
            st.error(str(e))

with right:
    st.subheader("Lineage impact")
    asset = st.text_input("Asset", "raw.orders")
    if st.button("Trace downstream"):
        result = downstream_assets(asset)
        st.dataframe(result if result else [{"message": "No downstream assets found"}], use_container_width=True)
    if st.button("Trace upstream"):
        result = upstream_assets(asset)
        st.dataframe(result if result else [{"message": "No upstream assets found"}], use_container_width=True)
