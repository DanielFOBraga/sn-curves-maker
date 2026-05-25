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

## ⚖️ License

This project is licensed under the Apache License 2.0 - see the [LICENSE](LICENSE) file for details. 
