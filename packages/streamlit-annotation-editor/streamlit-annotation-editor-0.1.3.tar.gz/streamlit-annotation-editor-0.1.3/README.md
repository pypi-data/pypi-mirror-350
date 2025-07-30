# streamlit-annotation-editor

This Streamlit component allows you to display and edit annotated text.

## Installation instructions

```sh
pip install streamlit-annotation-editor
```

## Usage instructions

```python
import streamlit as st
from annotation_editor import (
    annotation_editor,
    AnnotationData,
    Annotation, 
    EntityType
)

annotation_data = [
     AnnotationData(
           text="A line of text containing several words.",
           annotations=[
                Annotation(start=0, end=1, entity_type="SINGLE_LETTER", confidence_score=0.99, text="A"),
                ...
           ]
     ),
     ...
]

entity_types = [
    EntityType(name="PERSON", primary_color="#e5381d", secondary_color="#c12b14"),
    ...
]

edited_annotation_data = annotation_editor(annotation_data, entity_types)
```