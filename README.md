# Horario Project

This is a Django project that provides a simple web interface for a calculator, a logarithm table, and a color configuration tool for the menu.

## Features

*   **Calculator:** A simple calculator that supports basic arithmetic operations, square root, and logarithms.
*   **Logarithm Table:** A page that displays a table of logarithms for numbers from 0 to 10.
*   **Color Configuration:** A settings page that allows you to customize the colors of the menu. The colors are saved in the session and applied to all pages.

## Installation

1.  Clone the repository:
    ```bash
    git clone <repository-url>
    ```
2.  Install the dependencies:
    ```bash
    pip install -r requirements.txt
    ```
3.  Run the development server:
    ```bash
    python manage.py runserver
    ```
4.  Open your browser and go to `http://127.0.0.1:8000/`.

## Styling

The project's styling is centralized in the `styles/base.css` file. The colors of the menu can be customized in the settings page. The default colors are defined in the `calculator/views.py` and `calculator/context_processors.py` files.

**Note:** There are a couple of duplicated files in the root directory: `requeriments.txt` (a typo of `requirements.txt`) and `,gitignore` (a typo of `.gitignore`). These files should be ignored. Please use `requirements.txt` to install the dependencies and `.gitignore` as the git ignore file.