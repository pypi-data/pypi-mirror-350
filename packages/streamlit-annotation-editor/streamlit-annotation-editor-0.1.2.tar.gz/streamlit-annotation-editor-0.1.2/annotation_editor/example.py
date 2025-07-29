import streamlit as st
from annotation_editor import (annotation_editor, AnnotationData, Annotation, 
                               EntityType)

# During development, we can run this just as we would any other Streamlit
# app: `$ streamlit run annotation_editor/example.py`

annotation_data = [
     AnnotationData(
           "This streamlit component was developed by Noah Dettki.",
           [
                Annotation(5, 14, "STREAMLIT", 0.99, "streamlit"),
                Annotation(42, 53, "PERSON"),
           ]
     ),
     AnnotationData(
           "You can reach me under my-real@email.com to discuss this project.",
           [
                 Annotation(23, 40, "EMAIL", 0.8),
           ]
     ),
     AnnotationData(
           "Or visit http://www.this-is-definitely-a-real-website.com.",
           [
                    Annotation(9, 57, "URL", 0.743),
           ]
     )
]

entity_types = [
    EntityType("PERSON", "#e5381d", "#c12b14"),
    EntityType("IP_ADDRESS", "#ea580c", "#c2410c"),
    EntityType("USER_ID", "#65a30d", "#4d7c0f"),
    EntityType("URL", "#059669", "#047857"),
    EntityType("AUTH_KEY", "#0891b2", "#0e7490"),
    EntityType("EMAIL", "#2563eb", "#1d4ed8"),
    EntityType("STREAMLIT", "#7c3aed", "#6d28d9"),
]

# The annotation editor component
output = annotation_editor(
     annotation_data=annotation_data,
     entity_types=entity_types,
     key="keepalive")

st.json(output)
