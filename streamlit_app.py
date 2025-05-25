import streamlit as st
import matplotlib.pyplot as plt
import numpy as np

st.set_page_config(page_title="Diagnostic Reasoning: Chest Pain Case", layout="centered")
st.title("📝 Diagnostic Reasoning Tool: Chest Pain to Dysphagia")

st.markdown("""
This tool walks through a diagnostic reasoning path from a general symptom (chest pain) to a specific etiology 
(scleroderma-related esophageal dysmotility), using key clinical features and tracking entropy reduction.
""")

# Initialize entropy tracking
entropy_steps = [1.0]  # Start at maximal uncertainty
entropy = 1.0

# Step 1: Symptom refinement
st.header("Step 1: Chest Pain → Swallowing Trouble")
if st.checkbox("Trouble swallowing (dysphagia)?"):
    entropy -= 0.1
    entropy_steps.append(entropy)

    if st.checkbox("Food gets stuck below the throat (esophageal dysphagia)?"):
        entropy -= 0.1
        entropy_steps.append(entropy)

        # Step 2: Determine the pattern
        st.header("Step 2: Characterize the Dysphagia")
        if st.checkbox("Dysphagia to both solids and liquids (suggests dysmotility)?"):
            entropy -= 0.2
            entropy_steps.append(entropy)

            # Step 3: Assess for systemic signs
            st.header("Step 3: Systemic Features Suggesting Autoimmunity")
            raynauds = st.checkbox("Raynaud's phenomenon")
            telangiectasias = st.checkbox("Telangiectasias")
            joint_pain = st.checkbox("Inflammatory joint pain")
            skin_thickening = st.checkbox("Skin thickening / sclerodactyly")

            systemic_count = sum([raynauds, telangiectasias, joint_pain, skin_thickening])

            if systemic_count > 0:
                st.success("Systemic autoimmune features present — consider scleroderma (CREST syndrome)")
                entropy -= 0.2 * min(systemic_count, 2)  # Cap reduction for redundancy
                entropy_steps.append(entropy)

# Final entropy display
st.markdown(f"### 📊 Final Entropy Score: **{round(entropy, 2)}**")

# Plot entropy reduction trajectory
st.header("Entropy Reduction Over Diagnostic Path")
steps = list(range(len(entropy_steps)))
plt.figure(figsize=(6, 4))
plt.plot(steps, entropy_steps, marker='o')
plt.xlabel("Step")
plt.ylabel("Entropy")
plt.title("Entropy Reduction During Diagnostic Reasoning")
plt.grid(True)
st.pyplot(plt)

# Educational takeaway
st.info("Entropy starts high when little is known. As features are identified, the diagnostic path becomes more focused, reducing entropy and narrowing the differential.")
