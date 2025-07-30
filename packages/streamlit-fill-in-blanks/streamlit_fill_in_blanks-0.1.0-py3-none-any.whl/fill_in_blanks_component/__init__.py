# In fill_in_blanks_component/__init__.py

import os
import streamlit.components.v1 as components
from typing import List, Dict, Any  # Added for type hinting

# --- (Keep your _RELEASE and _component_func declaration as is) ---
_RELEASE = True

if not _RELEASE:
    _component_func = components.declare_component(
        "fill_in_blanks_streamlit",
        url="http://localhost:3001",
    )
else:
    parent_dir = os.path.dirname(os.path.abspath(__file__))
    build_dir = os.path.join(parent_dir, "frontend/dist")
    _component_func = components.declare_component(
        "fill_in_blanks_streamlit", path=build_dir
    )


# --- NEW HELPER FUNCTION ---
def _parse_sentences_with_delimiter(
    sentences_with_delimiters: List[str], delimiter: str
) -> List[List[str]]:
    parsed_segments = []
    for sentence in sentences_with_delimiters:
        parts = []
        current_part = ""
        i = 0
        while i < len(sentence):
            if sentence.startswith(delimiter, i):
                parts.append(current_part)
                current_part = ""
                i += len(delimiter)
            else:
                current_part += sentence[i]
                i += 1
        parts.append(current_part)  # Add the last part

        # Ensure that if a sentence ends with a delimiter, an empty string is added
        # to signify a blank at the end.
        # The React component expects a segment after the last blank if it's at the end.
        if sentence.endswith(delimiter):
            parts.append("")
        parsed_segments.append(parts)
    return parsed_segments


def fill_in_blanks(
    segments_data: List[Any],  # Can be List[List[str]] or List[str]
    options: List[Dict[str, str]],
    delimiter: str = "$",
    theme: Dict[str, str] = None,
    assert_enough_options: bool = True,  # New parameter
    key: str = None,
) -> List[Dict[int, str]]:  # Corrected return type hint to match previous logic
    """
    Streamlit component to render a fill-in-the-blanks exercise.

    Parameters
    ----------
    segments_data : List[List[str]] or List[str]
        If List[List[str]], it's the pre-segmented data:
            Each inner list represents a sentence row.
            e.g., [["Text before blank 1", "text after blank 1, before blank 2", ...]]
        If List[str], it's a list of sentences with delimiters:
            e.g., ["Yesterday I $ playing football and I $ it very much$"]
            The delimiter indicates where a blank should be.
    options : list of dicts
        Each dict should have 'id' and 'label'.
        e.g., [{"id": "word1", "label": "Word 1"}]
    delimiter : str, optional
        The delimiter used in `segments_data` if it's a list of strings.
        Defaults to "$".
    theme : dict, optional
        A dictionary to customize the appearance.
        Keys: primaryColor, secondaryBackgroundColor, textColor, font.
    assert_enough_options : bool, optional
        If True (default), raises a ValueError if the number of blanks
        exceeds the number of available options.
    key : str, optional
        Streamlit key for the component.

    Returns
    -------
    dict
        A dictionary representing the placed items in the blanks.
        e.g. {0: {0: "played", 1: "enjoyed"}, 1: {0: "play"}}
        Outer key is row index (int), inner key is blank index (int) within the row.
    """
    processed_segments: List[List[str]]

    if not segments_data:  # Handle case where segments_data is empty or None
        processed_segments = []
    elif isinstance(segments_data[0], str):
        processed_segments = _parse_sentences_with_delimiter(segments_data, delimiter)
    elif isinstance(segments_data[0], list):
        processed_segments = segments_data
    else:
        processed_segments = []  # Fallback for unexpected type

    # Calculate total number of blanks
    # Each row has len(row) - 1 blanks.
    total_blanks = 0
    for row in processed_segments:
        if len(row) > 1:  # A row needs at least 2 segments to have 1 blank
            total_blanks += len(row) - 1

    if assert_enough_options and total_blanks > len(options):  # Corrected condition
        raise ValueError(
            f"You have {total_blanks} blanks but only {len(options)} options. "
            f"Please add {total_blanks - len(options)} more option(s) or set assert_enough_options = False."
        )

    component_value = _component_func(
        segments=processed_segments,  # Pass the processed segments
        options=options,
        theme=theme,
        key=key,
        default={},
    )

    if component_value is None:
        return component_value

    return [{int(key): val for key, val in item.items()} for item in component_value]
