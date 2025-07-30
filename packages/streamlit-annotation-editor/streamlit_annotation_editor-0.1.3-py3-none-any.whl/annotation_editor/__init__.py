import os
import streamlit.components.v1 as components
from .helper import EntityType, Annotation, AnnotationData

# Create a _RELEASE constant. We'll set this to False while we're developing
# the component, and True when we're ready to package and distribute it.
# (This is, of course, optional - there are innumerable ways to manage your
# release process.)
_RELEASE = True

# Declare a Streamlit component. `declare_component` returns a function
# that is used to create instances of the component. We're naming this
# function "_component_func", with an underscore prefix, because we don't want
# to expose it directly to users. Instead, we will create a custom wrapper
# function, below, that will serve as our component's public API.

# It's worth noting that this call to `declare_component` is the
# *only thing* you need to do to create the binding between Streamlit and
# your component frontend. Everything else we do in this file is simply a
# best practice.

if not _RELEASE:
    _component_func = components.declare_component(
        # We give the component a simple, descriptive name
        "annotation_editor",
        # Pass `url` here to tell Streamlit that the component will be served
        # by the local dev server that you run via `npm run start`.
        # (This is useful while your component is in development.)
        url="http://localhost:3001",
    )
else:
    # When we're distributing a production version of the component, we'll
    # replace the `url` param with `path`, and point it to the component's
    # build directory:
    parent_dir = os.path.dirname(os.path.abspath(__file__))
    build_dir = os.path.join(parent_dir, "frontend/build")
    _component_func = components.declare_component(
        "annotation_editor", path=build_dir)


# Create a wrapper function for the component. This is an optional
# best practice - we could simply expose the component function returned by
# `declare_component` and call it done. The wrapper allows us to customize
# our component's API: we can pre-process its input args, post-process its
# output value, and add a docstring for users.
def annotation_editor(
        annotation_data: list[AnnotationData], 
        entity_types: list[EntityType], 
        key=None):
    """Create a new instance of "annotation_editor".

    Parameters
    ----------
    annotation_data: list of AnnotationData
        A list of AnnotationData objects that define the text and the
        annotations for the component. Each AnnotationData object must
        contain a "text" key with the text to be annotated and an "annotations"
        key with a list of Annotation objects. Each Annotation object
        must contain a "start" key with the start index of the annotation, an
        "end" key with the end index of the annotation, an "entityType" key
        with the entity type of the annotation, an optional "confidence_score"
        key with the confidence score of the annotation and an optional "text"
        key with the text of the annotation. The "entityType" key can be a
        string or an EntityType object. If it is a string, the entity type
        must be one of the entity types defined in the "entity_types" argument.
        The "confidence_score" key should be a float between 0 and 1. The
        "text" key will replace the text of the annotation in the component.
    entity_types: list of EntityType
        A list of EntityType objects that define the entity types that can be
        highlighted. Each EntityType object must contain a "name" key with the
        name of the entity type, a "primary_color" key with the primary color
        of the entity type and an optional "secondary_color" key with the
        secondary color of the entity type.
    key: str or None
        An optional key that uniquely identifies this component. If this is
        None, and the component's arguments are changed, the component will
        be re-mounted in the Streamlit frontend and lose its current state.

    Returns
    -------
    annotation_data: list of AnnotationData
        The same list that was passed in, but including any changes made by
        the user.
    """
    # Call through to our private component function. Arguments we pass here
    # will be sent to the frontend, where they'll be available in an "args"
    # dictionary.
    #
    # "default" is a special argument that specifies the initial return
    # value of the component before the user has interacted with it.

    # TODO: All annotation lists must be sorted before sending them to the
    # frontend. Also make sure that no annotations overlap.

    serialized_annotation_data = [ad.to_dict() for ad in annotation_data]
    serialized_entity_types = [et.to_dict() for et in entity_types]
    component_value = _component_func(
        annotationData=serialized_annotation_data, 
        entityTypes=serialized_entity_types, 
        key=key, 
        default=serialized_annotation_data)

    # We could modify the value returned from the component if we wanted.
    # There's no need to do this in our simple example - but it's an option.
    return component_value
