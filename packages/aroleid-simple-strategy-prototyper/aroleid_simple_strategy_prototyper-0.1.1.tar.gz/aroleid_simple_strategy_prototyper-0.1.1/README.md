# Aroleid Simple Strategy Prototyper


A Python package for backtesting trading strategies with OHLCV data.


---
**Table of Contents**

- [Quickstart Guide](#quickstart-guide)
- [Documentation](#documentation)
  - [Core Architecture](#core-architecture)
  - [Flow of Data](#flow-of-data)
  - [Historical Market Data](#historical-market-data)
- [Development](#development)
  - [Feature Roadmap](#feature-roadmap)
  - [Issue Tracking](#issue-tracking)
  - [CI/CD Workflow](#cicd-workflow-v010)
  - [Release Process](#release-process)

---

THE INFORMATION PROVIDED IS FOR EDUCATIONAL AND INFORMATIONAL PURPOSES ONLY. IT DOES NOT CONSTITUTE FINANCIAL, INVESTMENT, OR TRADING ADVICE. TRADING INVOLVES SUBSTANTIAL RISK, AND YOU MAY LOSE MORE THAN YOUR INITIAL INVESTMENT.

THIS SOFTWARE AND ITS DOCUMENTATION PAGES (HOSTED ON ONESECONDTRADER.COM) ARE PROVIDED "AS IS," WITHOUT ANY WARRANTIES, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO MERCHANTABILITY OR FITNESS FOR A PARTICULAR PURPOSE. THE AUTHORS AND COPYRIGHT HOLDERS ASSUME NO LIABILITY FOR ANY CLAIMS, DAMAGES, OR OTHER LIABILITIES ARISING FROM THE USE OR DISTRIBUTION OF THIS SOFTWARE OR DOCUMENTATION PAGES. USE AT YOUR OWN RISK. ONESECONDTRADER AND ITS DOCUMENTATION PAGES ARE LICENSED UNDER THE GNU GENERAL PUBLIC LICENSE V3.0 (GPL-3.0). SEE THE GPL-3.0 FOR DETAILS.

## Quickstart Guide

### Load Market Data into Pandas DataFrame

If you are using the package in a Google Colab notebook, you can mount your Google Drive to access your CSV files:

```python
from google.colab import drive
drive.mount('/content/drive')
```

Install the package from PyPI (using pip or poetry, use `!` in Google Colab before running the pip command in a cell):
```python
!pip install aroleid-simple-strategy-prototyper
```

Import the necessary packages:
```python
import aroleid_simple_strategy_prototyper as assp
import pandas as pd
```

If you want to see debug messages, you can set the logging level to DEBUG (default is INFO):
```python
import logging
logging.getLogger("aroleid_simple_strategy_prototyper").setLevel(logging.DEBUG)
```

Subclass the `Backtester` class and implement the two abstract methods (since we just want to use the ``load_historical_market_data()`` method, we can just use `pass` in the body of the methods that need to be implemented):
```python
class DummyStrategy(assp.Backtester):
    def add_indicators(self) -> None:
        pass

    def strategy(self, row: pd.Series) -> None:
        pass
```

After instantiating the `DummyStrategy` class, the `load_historical_market_data()` method can be used to load the historical market data into a pandas DataFrame (adjust path to your CSV file and the optional symbol filter as needed):
```python
backtester = DummyStrategy()
backtester.load_historical_market_data(
    path_to_dbcsv="/content/drive/MyDrive/csv_port/glbx-mdp3-20241202-20241205.ohlcv-1s.csv",
    symbol="MNQZ4",
)
```

## Documentation

### Core Architecture

The Aroleid Simple Strategy Prototyper is architected around a single abstract base class, `Backtester`, which encapsulates the entire backtesting workflow.
To implement a custom strategy, users subclass `Backtester` and define the two required abstract methods: `add_indicators()` and `strategy()`.
This design ensures that users do not need to reimplement the underlying mechanics of the backtesting engine and it enforces a clear separation between infrastructure and strategy logic.

```python
# ...

class Backtester(abc.ABC):
    
    # ...

    @abc.abstractmethod
    def add_indicators(self) -> None:
        pass

    @abc.abstractmethod
    def strategy(self, row: pd.Series) -> None:
        pass

    # ...
```

### Flow of Data

After the `Backtester` class has been subclassed by the user by implementing the two necessary abstract methods, the historical market data can be loaded into a pandas dataframe from a local CSV file (in Databento format, see [Historical Market Data](#historical-market-data)) via the `load_historical_market_data()` method (an optional symbol filter can be applied if necessary).

```python
# ...

# Subclass Backtester abstract base class and implement the two abstract methods
class MyBacktester(Backtester):
    def add_indicators(self) -> None:
        # ...
        
    def strategy(self, row: pd.Series) -> None:
        # ...

# Instantiate the Backtester class and load historical market data
backtester = MyBacktester()
backtester.load_historical_data("path/to/csv/file.csv")
```

### Historical Market Data

The Aroleid Simple Strategy Prototyper is designed with compatibility with the [Databento](https://databento.com/) historical market data formats.
This does not necessarily mean that historical market data needs to be obtained from Databento, but rather that databento's schemas, dataformats, standards, and conventions are observed and data obtained from other sources is converted to the databento format before it is used within ARBE.

The backtester expects historical data to be provided in CSV format with the following columns: `ts_event`, `rtype`, `open`, `high`, `low`, `close`, `volume`, and `symbol`.
To convert your existing CSV files to this format, you can use the `convert_csv_to_databento_format()` function from `aroleid_simple_strategy_prototyper.helpers`.

The backtester supports the following Databento OHLCV bar types (the numbers correspond to Databento record type integer IDs): 1-second (32), 1-minute (33), 1-hour (34), 1-day (35). These record types are used when loading historical price data for backtesting. Unconventional record types are labelled as `Unknown (<rtype id>)`, but will not raise an error when attempting to load data.


## Development

### Feature Roadmap

Each feature is listed in the order in which it should be implemented, with the most significant features listed first.
Each feature is assigned a number, such as `#03`, and a short name, such as `price-feed`.
This number and name will be used when creating Git branches (e.g., `feature/03-price-feed`), or writing commit messages, so that the user can easily track what feature each change is related to.

- `#01-Github-workflow-in-README` Add GitHub workflow to README.
- `#02-csv-to-pandas_df` Read external CSV file in databento format into a pandas DataFrame.


### Issue Tracking

Each issue is documented and addressed in the order of importance or urgency.
Like features, issues are assigned a number and a short name, such as `#i05-fix-timestamp-format`, prepended with `i` to indicate that it is an issue and not a feature.
This identifier will be used in Git branches (e.g., `fix/i05-fix-timestamp-format`), commit messages, or pull request titles to make it easy to trace which changes resolve which issues.


### CI/CD Workflow (v0.1.0)

This project follows a simplified [**GitHub Flow**](https://docs.github.com/en/get-started/using-github/github-flow) for solo development:

1. **Create a feature branch** from `master`:
   ```bash
   git checkout master
   git pull origin master
   git checkout -b feature/#<feature-number>-<feature-short-name>
   ```

2. **Make changes and commit** regularly:
   ```bash
   git add .
   git commit -m "Feature #<feature-number>: <commit-message>"
   ```

3. **Verify code quality**:
   ```bash
   ./scripts/precheck-featuremerge.sh
   ```
   
4. **Merge to master** when feature is complete:
   ```bash
   git checkout master
   git pull origin master
   git merge feature/#<feature-number>-<feature-short-name>
   git push origin master
   ```

5. **Cleanup**:
   ```bash
   git branch -d feature/#<feature-number>-<feature-short-name>
   ```

For bug fixes, use the same workflow but with branch naming `fix/i<issue-number>-<issue-short-name>` and commit message `Fix #<issue-number>: <commit-message>`.

### Release Process

When ready to release a new version:

1. **Update version number** in `pyproject.toml`:
   ```bash
   poetry version patch  # For bug fixes (0.1.0 -> 0.1.1)
   poetry version minor  # For new features (0.1.0 -> 0.2.0)
   poetry version major  # For breaking changes (0.1.0 -> 1.0.0)
   ```

2. **Update dependencies** if needed:
   ```bash
   poetry update
   ```

3. **Build the package**:
   ```bash
   poetry build
   ```

4. **Test the package locally**:
   ```bash
   pip install dist/*.whl
   ```

5. **Upload to TestPyPI** (optional):
   ```bash
   poetry config repositories.testpypi https://test.pypi.org/legacy/
   poetry publish -r testpypi
   ```

6. **Create a Git tag** for the release:
   ```bash
   git tag -a v$(poetry version -s) -m "Release v$(poetry version -s)"
   git push origin v$(poetry version -s)
   ```

7. **Publish to PyPI**:
   ```bash
   poetry publish
   ```

8. **Create a GitHub Release** with release notes.
