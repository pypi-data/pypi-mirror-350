# Streamlit Fill-In-The-Blanks Component

[![PyPI version](https://badge.fury.io/py/streamlit-fill-in-blanks.svg)](https://badge.fury.io/py/streamlit-fill-in-blanks)

A customizable Streamlit component that allows users to create and interact with fill-in-the-blanks exercises using an intuitive drag-and-drop interface. Perfect for educational applications, quizzes, and interactive learning modules.

## Features

- **Drag-and-Drop Interface:** Users can easily drag answer options into blank spaces.
- **Flexible Sentence Input:**
  - Provide sentences as pre-segmented lists.
  - Or, use a simple string format with a customizable delimiter (default: `$`) to indicate blanks.
- **Customizable Theming:** Adapt the component's appearance (colors, fonts) to match your Streamlit app's style. Streamlit's native theme is automatically applied if no custom theme is provided.
- **Option Validation:** Optionally, assert that enough answer options are provided for the number of blanks.
- **Stateful:** Remembers the user's answers within a Streamlit session.

## Installation

Install the component using pip (or your preferred Python package manager like `uv`):

```bash
pip install streamlit-fill-in-blanks
```

Or with uv:

```bash
uv pip install streamlit-fill-in-blanks
```

> **Note:** This command assumes the package is published on PyPI. For local development, see "Development" section below.

## Usage

Import the `fill_in_blanks` function from the component package and use it in your Streamlit app.

Have a look at the [example.](example.py)

## API Reference

```python
def fill_in_blanks(
    segments_data: List[Union[List[str], str]],
    options: List[Dict[str, str]],
    delimiter: str = "$",
    theme: Optional[Dict[str, str]] = None,
    assert_enough_options: bool = True,
    key: Optional[str] = None,
) -> Dict[int, Dict[int, str]]:
```

**Arguments:**

- `segments_data`: `List[List[str]]` or `List[str]`
  - If `List[List[str]]`: Pre-segmented data. Each inner list is a sentence row, with strings representing text segments and implied blanks between them. A trailing empty string in an inner list creates a blank at the end of that sentence.
    - Example: `[["Text before blank 1", "text after blank 1."]]` (1 blank)
    - Example: `[["Text before blank 1", "text after blank 1.", ""]]` (1 blank at the end)
  - If `List[str]`: A list of sentences where blanks are indicated by the delimiter.
    - Example: `["Sentence with one $ blank."]`
    - Example: `["Sentence with a blank at the end$"]`
- `options`: `List[Dict[str, str]]`
  - A list of dictionaries, where each dictionary must have an `id` (string, unique) and a `label` (string, displayed to the user).
    - Example: `[{"id": "opt1", "label": "Option 1"}, {"id": "opt2", "label": "Option 2"}]`
- `delimiter`: `str`, optional (default: `$`)
  - The string used to mark blank locations if `segments_data` is a list of strings.
- `theme`: `Dict[str, str]`, optional (default: None)
  - A dictionary to customize appearance. Keys: `primaryColor`, `secondaryBackgroundColor`, `textColor`, `font`. If None, Streamlit's current theme is used.
- `assert_enough_options`: `bool`, optional (default: True)
  - If True, raises a ValueError if the total number of blanks across all sentences is greater than the number of unique options provided. Set to False to allow more blanks than options.
- `key`: `str`, optional (default: None)
  - A unique Streamlit key for the component instance.

**Returns:**

- `Dict[int, Dict[int, str]]`: A dictionary where:
  - Outer keys are row indices (integers, 0-based).
  - Inner keys are blank indices within that row (integers, 0-based).
  - Values are the ids of the options placed in the blanks.
  - Example: `{0: {0: "fox", 1: "dog"}, 1: {0: "easy"}}`

## Development

To set up the development environment:

Clone the repository (if applicable):

```bash
git clone https://github.com/yourusername/streamlit-fill-in-blanks.git
cd streamlit-fill-in-blanks
```

Set up Python environment and install dependencies:

It's recommended to use a virtual environment.

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
uv pip install -e ".[devel]" # Or pip install -e ".[devel]"
```

Install frontend dependencies and run the dev server:

Navigate to the frontend directory:

```bash
cd fill_in_blanks_component/frontend
npm install
npm run dev
```

This will typically start the frontend dev server on http://localhost:3001.

Run the Streamlit example app:

In a new terminal, from the project root (`streamlit-fill-in-blanks/`):

Ensure `_RELEASE = False` in `fill_in_blanks_component/__init__.py`.

```bash
streamlit run fill_in_blanks_component/__init__.py
```

Streamlit will open in your browser, and the component will load from the frontend dev server, allowing for hot-reloading of frontend changes.

## Building for Production

Build the frontend:

```bash
cd fill_in_blanks_component/frontend
npm run build
```

This creates static assets in `fill_in_blanks_component/frontend/dist/`.

Set `_RELEASE = True` in `fill_in_blanks_component/__init__.py`.

Build the Python package:

From the project root:

```bash
python setup.py sdist bdist_wheel
```

This creates distributable files in the `dist/` folder.

## Contributing

Contributions are welcome! Please feel free to submit a pull request or open an issue.

## License

This project is licensed under the MIT License - see the LICENSE file for details.
