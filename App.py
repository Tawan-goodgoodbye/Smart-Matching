import streamlit as st
from streamlit_sortables import sort_items

st.set_page_config(page_title="Gale–Shapley Drag & Drop Dashboard", layout="wide")

st.title("🎓 Gale–Shapley Stable Matching (Company-Proposing)")
st.write("Reorder preferences using drag-and-drop, then run the simulation.")

# Default names
students = ["A", "B", "C"]
companies = ["X", "Y", "Z"]

# Default preferences
default_student_prefs = {
    "A": ["X", "Y", "Z"],
    "B": ["Y", "X", "Z"],
    "C": ["X", "Z", "Y"]
}

default_company_prefs = {
    "X": ["B", "A", "C"],
    "Y": ["A", "C", "B"],
    "Z": ["C", "B", "A"]
}

# =========================
#  DRAG & DROP UI
# =========================
st.subheader("📌 Step 1: Set Preferences (Drag to reorder)")

col1, col2 = st.columns(2)

with col1:
    st.markdown("### 🧑‍🎓 Student Preferences")
    student_prefs = {}
    for s in students:
        student_prefs[s] = sort_items(
            default_student_prefs[s],
            direction="vertical",
            key=f"student_{s}"
        )

with col2:
    st.markdown("### 🏢 Company Preferences")
    company_prefs = {}
    for c in companies:
        company_prefs[c] = sort_items(
            default_company_prefs[c],
            direction="vertical",
            key=f"company_{c}"
        )

st.write("---")

def gale_shapley_company_proposing(st_prefs, co_prefs):
    student_rank = {
        s: {c: i for i, c in enumerate(prefs)}
        for s, prefs in st_prefs.items()
    }

    student_match = {s: None for s in st_prefs}
    company_match = {c: None for c in co_prefs}
    free_companies = list(co_prefs.keys())
    next_proposal_index = {c: 0 for c in co_prefs}

    log = []
    round_num = 1

    while free_companies:
        log.append(f"### 🔵 Round {round_num}")
        company = free_companies[0]

        student = co_prefs[company][next_proposal_index[company]]
        next_proposal_index[company] += 1

        log.append(f"**{company} ➝ proposes to ➝ {student}**")

        current = student_match[student]

        if current is None:
            student_match[student] = company
            company_match[company] = student
            free_companies.remove(company)
            log.append(f"✔ {student} accepts **{company}** (free)")
        else:
            if student_rank[student][company] < student_rank[student][current]:
                log.append(f"🔄 {student} prefers **{company}** over **{current}**")
                student_match[student] = company
                company_match[company] = student

                free_companies.append(current)
                free_companies.remove(company)
                log.append(f"✔ {student} switches to **{company}**")
            else:
                log.append(f"❌ {student} keeps **{current}**, rejects **{company}**")

        log.append("---")
        round_num += 1

    return student_match, company_match, log

if st.button("🚀 Run Gale–Shapley Algorithm"):
    student_match, company_match, log = gale_shapley_company_proposing(
        student_prefs,
        company_prefs
    )

    st.subheader("📘 Matching Process Log")
    for entry in log:
        st.markdown(entry)

    st.subheader("🏁 Final Stable Match (Company-Proposing)")
    for c, s in company_match.items():
        st.write(f"**{c} → {s}**")
