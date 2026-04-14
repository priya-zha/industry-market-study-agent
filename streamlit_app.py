import streamlit as st
from pathlib import Path
from market_study_agent import generator


def list_industries():
    data_dir = Path(__file__).parent / "market_study_agent" / "data"
    return sorted([p.stem.replace("sample_", "") for p in data_dir.glob("sample_*.json")])


st.set_page_config(page_title="Industry Market Study Agent", layout="wide")
st.title("Industry Market Study Agent (MVP)")

industries = list_industries()
if not industries:
    st.error("No sample industries found. Add JSON files under market_study_agent/data/")
    st.stop()

industry = st.selectbox("Choose industry", industries)

col1, col2 = st.columns([1, 2])

with col1:
    st.header("Controls")
    if st.button("Generate Report"):
        try:
            data = generator.load_sample_data(industry)
            md = generator.generate_report(industry, data)
            st.session_state['last_md'] = md
            st.success("Report generated")
        except Exception as e:
            st.error(f"Error: {e}")

    if 'last_md' in st.session_state:
        st.download_button("Download Markdown", st.session_state['last_md'], file_name=f"market_study_{industry}.md", mime="text/markdown")

with col2:
    st.header("Generated Report")
    if 'last_md' in st.session_state:
        st.markdown(st.session_state['last_md'])
    else:
        st.info("Select an industry and click 'Generate Report' to create a market study.")
