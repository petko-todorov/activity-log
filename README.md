# Activity Log

A desktop application for logging and tracking activities.

This application allows users to quickly log activities with timestamps and view them in a sortable list. It provides functionality to edit and delete entries, and offers a date selection for when the activity occurred.

## Tech Stack

* PySide6

## Quick Start

To install and run the application:

1. Clone the repository.
2. Install dependencies:
 ```bash
 pip install -r requirements.txt
 ```
3. Run the application:
 ```bash
 python main.py
 ```

## Project Structure

```
.
├── main.py
├── storage.py
├── activities.json
└── ui
 ├── main_window.py
 └── ui_main_window.py
```

## Key Concepts

* **`main.py`**: The entry point of the application, responsible for initializing the Qt application and the main window.
* **`storage.py`**: Handles the persistence of activity data. It reads from and writes to `activities.json`.
* **`ui/main_window.py`**: Contains the main application window logic, including handling user input, displaying activities, and managing context menus.
* **`ui/ui_main_window.py`**: Auto-generated Python code from a Qt Designer UI file, defining the visual elements of the main window.
* **`activities.json`**: Stores the activity log data in JSON format.

## License

This project is licensed under the MIT License.