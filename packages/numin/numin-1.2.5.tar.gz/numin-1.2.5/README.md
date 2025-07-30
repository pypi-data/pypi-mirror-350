# numin Package

**numin** is a Python package designed for algorithmic trading and backtesting providing an API called **NuminAPI**.

## Features

- **Data Retrieval:** Download training, round, and validation data.
- **Prediction Submission:** Upload prediction CSVs to the server with built-in validation.
- **Real-Time Round Management:** Fetch the current trading round from the server.
- **Backtesting:** Run backtests on user-defined strategies with support for additional features and discretization.
- **File Management:** Upload and deploy files via Anvil's server.
- **Returns Summary:** Retrieve and format live (or simulation) trading returns.

## Supported Methods

- **Data Download:**
  - `get_data(data_type: str)`
    - Fetches data from the server based on the type (`training`, `round`, or `validation`).

- **Prediction Submission:**
  - `submit_predictions(file_path: str)`
    - Submits a CSV file of predictions to the server.  
    - **Note:** The file must include mandatory columns `["id", "predictions", "round_no"]` and optional columns `["stop", "target", "tLimit"]` (if provided, they must be integers between 1 and 100).

- **Round and Validation Data:**
  - `get_current_round()`
    - Retrieves the current round number from the server.
  - `fetch_validation_data(date: str)`
    - Downloads validation data for a given date.
  - `get_validation_dates()`
    - Lists available validation dates on the server.

- **Backtesting:**
  - `run_backtest(user_strategy : str, date:str, val_data:str, result_type="results" or "returns")`
    - Executes a backtest using a user-provided strategy function on the given date.
  - `display_results(backtest_results: results as above, validation_dataframe: dataFrame, indicators: list of indicators to show e.g. used for entry by strategy )`
    - Displays results of a backtest in a readable format with entry, exit prices, p/l etc.


- **File Upload and Deployment:**
  - `upload_file(file, user_id, filename)`
    - Uploads a file to remote storage via the Anvil server.
  - `deploy_file(filename: str, user_id: str)`
    - Deploys a file for a given user.

- **Live Returns Summary:**
  - `show_returns(user_id, mode="live"/"sim")`
    - Retrieves and displays a formatted summary of returns for the strategy associated with the given user ID

## Installation

Install numin using pip:

```bash
pip install numin

