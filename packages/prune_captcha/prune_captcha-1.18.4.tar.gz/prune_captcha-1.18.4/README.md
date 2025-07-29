# Prune's Captcha

## What is it for?

Captcha helps prevent robots from spamming using your forms.

## Prerequisites

-   To be installed on a Prune Django project that uses poetry or UV

## UV project

### Installation

Run the following command in the console:

```bash
uv add prune_captcha
```

### Updating the captcha

Don't hesitate to regularly run `uv sync --upgrade`, as the captcha evolves with time and our practices!

## Poetry project

### Installation

Run the following command:

```bash
poetry add prune_captcha
```

### Updating the captcha

Don't hesitate to regularly run `poetry update`, as the captcha evolves with time and our practices!

## Captcha Integration

### Configuration

In `settings.py`, set the path to the images used for the puzzle:

```python
PUZZLE_IMAGE_STATIC_PATH = "website/static/website/images/puzzles/"
```

Important: You must import the static files (css, js) present in "prune_captcha/static/".

```html
<header>
    <link
        rel="stylesheet"
        href="{% static 'prune_captcha/css/captcha.css' %}"
    />
    <script defer src="{% static 'prune_captcha/js/captcha.js' %}"></script>
</header>
```

### Utilisation

-   GET request (form display)

    -   Use create_and_get_captcha to generate the captcha data:

        ```python
        from prune_captcha.utils import create_and_get_captcha
        ```

        ```python
        puzzle = create_and_get_captcha(request)
        ```

    -   Passes the data into the context under the puzzle variable:

        ```python
        return render(
            request,
            "website/pages/contact/page.html",
            {"form": form, "puzzle": puzzle},
        )
        ```

    -   Include the component in your template:

        ```
        {% include "prune_captcha/captcha.html" %}
        ```

-   POST request (form submission)

    -   Use verify_captcha to validate the captcha:

        ```python
        from prune_captcha.utils import verify_captcha
        ```

        ```python
        response = verify_captcha(request)
        ```

    -   True if the captcha is correct, else False.

    -   Redirects in case of incorrect captcha.

# Available Versions

| Version | Date       | Notes                              |
| ------- | ---------- | ---------------------------------- |
| 1.18.4  | 2025-05-23 | deleted var                        |
| 1.18.3  | 2025-05-22 | add puzzle info                    |
| 1.18.2  | 2025-05-22 | fix                                |
| 1.18.1  | 2025-05-22 | some improvements                  |
| 1.18.0  | 2025-05-22 | create "addHiddenInputs" func      |
| 1.17.0  | 2025-05-21 | fix pos_answer                     |
| 1.16.1  | 2025-05-21 | fix static                         |
| 1.16.0  | 2025-05-21 | fix static                         |
| 1.15.2  | 2025-05-21 | fix manifest                       |
| 1.15.1  | 2025-05-21 | fix manifest                       |
| 1.15.0  | 2025-05-21 | fix manifest                       |
| 1.14.0  | 2025-05-21 | fix static and templates dirs      |
| 1.13.0  | 2025-05-21 | use session, add static            |
| 1.12.2  | 2025-05-21 | doc fixed                          |
| 1.12.1  | 2025-05-21 | doc fixed                          |
| 1.12.0  | 2025-05-21 | removed views, added utils, ...    |
| 1.11.0  | 2025-05-21 | removed utils                      |
| 1.10.0  | 2025-05-20 | fix documentation, removed ...     |
| 1.9.0   | 2025-05-20 | puzzle images path fixed           |
| 1.8.0   | 2025-05-20 | added migrations                   |
| 1.7.0   | 2025-05-20 | PUZZLE_IMAGE_STATIC_PATH ...       |
| 1.6.0   | 2025-05-20 | added templates                    |
| 1.5.0   | 2025-05-20 | app config fixed, components ...   |
| 1.4.0   | 2025-05-20 | added BaseModel in Captcha, ...    |
| 1.3.0   | 2025-04-30 | deleted start_server, deleted ...  |
| 1.2.0   | 2025-04-30 | fixed prune_captcha command, ...   |
| 1.1.0   | 2025-04-30 | start_server was not a module, ... |
| 1.0.0   | 2025-04-29 | First version of the `captcha` ... |
