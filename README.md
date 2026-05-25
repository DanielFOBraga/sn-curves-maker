# S-N Curves Maker (pyLife)

An interactive Python application designed to import cyclic fatigue test data from Excel, perform Wöhler (S-N) curve fitting using the **pyLife** library, and export high-resolution **TIFF** files.

---

## ✨ Features

- **Open-Source Architecture**: Built on standard Python scientific libraries.
- **Double-Stage Wöhler Fitting**: Performs standard finite fatigue-life slope fitting (`Elementary` pearl chain analysis) followed by full Maximum Likelihood Estimation (`MaxLikeFull`) to optimize the endurance limits ($S_D$, $N_D$) and scatter values ($T_N$, $T_S$).
- **Multi-Select Probabilistic Curves**: Enables dynamic selection and plotting of multiple failure or survival curves ($5\%$, $10\%$, $50\%$, $90\%$, $95\%$, and $99\%$).
- **S-N Visualizations**: Plots fractures as filled circles and runouts as hollow circles with right-pointing arrows adjusted for log-scale coordinates.
- **TIFF Graphics Export**: Saves plots directly as LZW-compressed high-DPI TIFF files.
- **Automated Windows Setup**: Launcher batch script automatically manages environment isolation and launches the application.

---

## 🚀 Quick Start (Windows)

Double-click on the launcher script in the project directory:
👉 **`run_app.bat`**

This will automatically:
1. Detect Python and initialize a local virtual environment (`.venv`).
2. Verify all package dependencies (`streamlit`, `pylife`, `openpyxl`, `pandas`, `numpy`, `matplotlib`).
3. Clean up any corrupted installation caches.
4. Launch the Streamlit dashboard in your default browser at `http://localhost:8501`.

---

## 📊 Expected Excel File Format
Your uploaded spreadsheet should contain at least three columns:
1. **Load / Stress Amplitude** (e.g. in MPa)
2. **Cycles to Failure**
3. **Runout Indicator** (identifying survived tests, where you can configure in the sidebar if `1` or `0` represents a runout)

---

## 📜 Licenses & Dependencies
This project operates entirely on permissive open-source software, making it **100% safe to publish on GitHub**:

| Library | License | Primary Purpose |
| :--- | :--- | :--- |
| **pyLife** | [Apache-2.0](https://github.com/boschrst/pyLife/blob/main/LICENSE) | Fatigue & Lifetime Assessment |
| **Streamlit** | [Apache-2.0](https://github.com/streamlit/streamlit/blob/main/LICENSE) | Interactive Web Framework |
| **pandas** | [3-Clause BSD](https://github.com/pandas-dev/pandas/blob/main/LICENSE) | Data Manipulation |
| **numpy** | [3-Clause BSD](https://github.com/numpy/numpy/blob/main/LICENSE) | Scientific Computing |
| **matplotlib** | [Matplotlib License](https://matplotlib.org/stable/users/project/license.html) (BSD-compatible) | Data Plotting |
| **openpyxl** | [MIT](https://github.com/thebillydev/openpyxl/blob/master/LICENCE) | Excel Parsing |

---

## ⚖️ Custom License Recommendation
For publishing your repository on GitHub, we recommend selecting a highly permissive license that aligns with your dependencies:
- **MIT License**: Excellent for short, simple, permissive sharing.
- **Apache License 2.0**: Excellent if you want explicit patent protection and want to align with the base licenses of `pyLife` and `Streamlit`.
