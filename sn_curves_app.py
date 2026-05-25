import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import io
import os

# Streamlit Page Config (Must be the very first Streamlit command)
st.set_page_config(
    page_title="S-N Curves Maker (pyLife)",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for Premium Design & Micro-animations
st.markdown("""
<style>
    /* Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;800&family=Space+Grotesk:wght@400;700&display=swap');
    
    /* Global styles */
    .main .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
    }
    
    h1, h2, h3 {
        font-family: 'Outfit', sans-serif !important;
        font-weight: 700 !important;
    }
    
    .stButton>button {
        background: linear-gradient(135deg, #6366f1 0%, #4f46e5 100%);
        color: white;
        border: none;
        padding: 0.6rem 1.8rem;
        border-radius: 12px;
        font-weight: 600;
        font-family: 'Outfit', sans-serif;
        box-shadow: 0 4px 15px rgba(99, 102, 241, 0.3);
        transition: all 0.3s ease;
    }
    
    .stButton>button:hover {
        background: linear-gradient(135deg, #4f46e5 0%, #4338ca 100%);
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(99, 102, 241, 0.4);
    }
    
    .stDownloadButton>button {
        background: linear-gradient(135deg, #10b981 0%, #059669 100%);
        color: white;
        border: none;
        padding: 0.6rem 1.8rem;
        border-radius: 12px;
        font-weight: 600;
        font-family: 'Outfit', sans-serif;
        box-shadow: 0 4px 15px rgba(16, 185, 129, 0.3);
        transition: all 0.3s ease;
    }
    
    .stDownloadButton>button:hover {
        background: linear-gradient(135deg, #059669 0%, #047857 100%);
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(16, 185, 129, 0.4);
    }
    
    /* Elegant Dashboard Cards */
    .metric-card {
        background: rgba(255, 255, 255, 0.05);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 16px;
        padding: 1.5rem;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
        backdrop-filter: blur(10px);
        transition: transform 0.3s ease;
    }
    
    .metric-card:hover {
        transform: translateY(-4px);
        border-color: rgba(99, 102, 241, 0.4);
    }
    
    .metric-value {
        font-size: 2.2rem;
        font-weight: 800;
        color: #6366f1;
        font-family: 'Space Grotesk', sans-serif;
        margin-bottom: 0.2rem;
    }
    
    .metric-label {
        font-size: 0.9rem;
        font-weight: 600;
        color: #9ca3af;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }
</style>
""", unsafe_allow_html=True)

# Imports that could fail if packages are missing
try:
    import pylife.materialdata.woehler as woehler
    from pylife.materiallaws import WoehlerCurve
    packages_available = True
except ImportError as e:
    packages_available = False
    package_error_msg = str(e)

# Header Section
st.markdown("""
<div style='text-align: center; margin-bottom: 2.5rem;'>
    <h1 style='font-size: 3rem; background: linear-gradient(135deg, #6366f1 0%, #a855f7 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent;'>
        S-N Curves Maker
    </h1>
    <p style='font-size: 1.1rem; color: #9ca3af; font-family: "Outfit", sans-serif; max-width: 800px; margin: 0.5rem auto;'>
        A professional engineering tool to import fatigue testing results from Excel, fit S-N (Wöhler) curves using <b>pyLife</b>, and export high-DPI TIFF files for publication.
    </p>
</div>
""", unsafe_allow_html=True)

if not packages_available:
    st.error(f"**Required scientific libraries are not fully installed.**\n\nError: `{package_error_msg}`\n\nPlease run the `run_app.bat` script to automatically set up the virtual environment and install all dependencies.")
    st.info("If you are running this app manually, please run: `pip install pylife openpyxl pandas numpy matplotlib streamlit`")
    st.stop()

# Sidebar: Controls & Customization
st.sidebar.markdown("""
<div style='text-align: center; margin-bottom: 1.5rem;'>
    <h2 style='font-size: 1.6rem; color: #6366f1; font-family: "Outfit", sans-serif;'>Settings & Controls</h2>
</div>
""", unsafe_allow_html=True)

# File Uploader
st.sidebar.subheader("📂 1. Select Data Source")
uploaded_file = st.sidebar.file_uploader("Upload Excel file (.xlsx, .xls)", type=["xlsx", "xls"])

# Demo data check
use_demo = False
if uploaded_file is None:
    if os.path.exists("sample_data.xlsx"):
        use_demo = st.sidebar.checkbox("Use generated sample_data.xlsx for testing", value=True)
        if use_demo:
            uploaded_file = "sample_data.xlsx"
    else:
        st.sidebar.info("Generate mock data to test instantly:")
        if st.sidebar.button("Generate Sample Excel File"):
            try:
                from sample_generator import generate_sample_fatigue_data
                generate_sample_fatigue_data()
                st.rerun()
            except Exception as ex:
                st.sidebar.error(f"Error generating sample file: {ex}")

# Main Layout: Two Panels
if uploaded_file is not None:
    # Read Excel sheet
    try:
        if isinstance(uploaded_file, str):
            df = pd.read_excel(uploaded_file)
            filename = uploaded_file
        else:
            df = pd.read_excel(uploaded_file)
            filename = uploaded_file.name
            
        st.sidebar.success(f"Loaded: {filename}")
    except Exception as e:
        st.error(f"Error reading Excel file: {e}")
        st.stop()

    # Column Mapping Configuration in Sidebar
    st.sidebar.markdown("---")
    st.sidebar.subheader("🎯 2. Column Mapping")
    
    # Auto-detection helper
    cols = list(df.columns)
    
    def guess_col(choices, possibilities):
        for p in possibilities:
            for c in choices:
                if p.lower() in c.lower():
                    return c
        return choices[0] if choices else None

    guess_load = guess_col(cols, ["load", "stress", "amplitude", "force"])
    guess_cycles = guess_col(cols, ["cycle", "number of cycles", "n_f", "n", "lifetime"])
    guess_runout = guess_col(cols, ["runout", "survival", "survived", "failed"])

    load_col = st.sidebar.selectbox("Load / Stress column:", cols, index=cols.index(guess_load) if guess_load in cols else 0)
    cycles_col = st.sidebar.selectbox("Cycles column:", cols, index=cols.index(guess_cycles) if guess_cycles in cols else 0)
    runout_col = st.sidebar.selectbox("Runout / Survival column:", cols, index=cols.index(guess_runout) if guess_runout in cols else 0)

    # Runout Mapping Rule
    st.sidebar.subheader("⚙️ 3. Runout Interpretation")
    runout_rule = st.sidebar.selectbox(
        "Which value represents a Runout (specimen survived)?",
        ["1 or True represents Runout", "0 or False represents Runout"]
    )

    # Advanced Fitting Options
    st.sidebar.markdown("---")
    st.sidebar.subheader("🧠 4. Fitting Parameters")
    fit_method = st.sidebar.selectbox(
        "pyLife Analyzer Method:",
        ["Maximum Likelihood (Full)", "Elementary / Pearl Chain Only"]
    )
    
    # Probabilistic Mode
    prob_type = st.sidebar.radio(
        "Curve Representation:",
        ["Probability of Failure (Pf)", "Probability of Survival (Ps)"]
    )
    
    # Multiselect for user choice
    prob_options = [5, 10, 50, 90, 95, 99]
    selected_vals = st.sidebar.multiselect(
        "Curves to Plot (%):",
        options=prob_options,
        default=[50, 90, 95]
    )
    
    # If no curves are selected, prevent error by choosing 50% default
    if not selected_vals:
        selected_vals = [50]

    # Plot Style Customizer
    st.sidebar.markdown("---")
    st.sidebar.subheader("🎨 5. Plot Aesthetics")
    
    plot_title = st.sidebar.text_input("Plot Title:", "S-N / Wöhler Curve Fit (pyLife)")
    x_label = st.sidebar.text_input("X-Axis Label:", "Cycles to Failure (N)")
    y_label = st.sidebar.text_input("Y-Axis Label:", "Stress Amplitude (MPa)")
    
    log_scale = st.sidebar.checkbox("Use Log-Log scale (instead of Semi-Log)", value=True)
    show_grid = st.sidebar.checkbox("Show Grid Lines", value=True)
    
    # Theme colors
    color_fractures = st.sidebar.color_picker("Fracture Points Color:", "#ef4444")
    color_runouts = st.sidebar.color_picker("Runout Points Color:", "#3b82f6")

    # TIFF Export Settings
    st.sidebar.markdown("---")
    st.sidebar.subheader("💾 6. Export TIFF settings")
    tiff_dpi = st.sidebar.slider("TIFF Resolution (DPI):", min_value=150, max_value=600, value=300, step=50)
    tiff_width = st.sidebar.slider("Width (inches):", min_value=4, max_value=12, value=8)
    tiff_height = st.sidebar.slider("Height (inches):", min_value=3, max_value=10, value=6)

    # Prepare data for pyLife
    df_pylife = pd.DataFrame()
    df_pylife['load'] = df[load_col].astype(float)
    df_pylife['cycles'] = df[cycles_col].astype(float)
    
    # Convert runout to fracture (True = Fracture, False = Runout)
    if "1 or True" in runout_rule:
        df_pylife['fracture'] = df[runout_col].apply(lambda x: False if x in [True, 1, '1', 'True', 'yes', 'y'] else True)
    else:
        df_pylife['fracture'] = df[runout_col].apply(lambda x: False if x in [False, 0, '0', 'False', 'no', 'n'] else True)

    # Display clean table preview in first tab
    tab_plot, tab_data, tab_params = st.tabs(["📈 S-N Fit & Plot", "📊 Mapped Data Table", "⚙️ pyLife Fit Parameters"])

    with tab_data:
        st.subheader("Experimental Data Preview")
        st.write(df.head(10))
        st.markdown("**Mapped for pyLife (First 10 Rows):**")
        st.write(df_pylife.head(10))
        st.info("Note: in pyLife, 'fracture = True' represents sample failure, while 'fracture = False' represents runout (survival).")

    # Fit Wöhler Curve
    try:
        fatigue_data = woehler.FatigueData(df_pylife)
        
        # Elementary Analyzer (always run to provide start values)
        elem_analyzer = woehler.Elementary(fatigue_data)
        elem_res = elem_analyzer.analyze()
        
        if "Maximum Likelihood" in fit_method:
            # Full MLE fitting using the Elementary results as starting values
            mle_analyzer = woehler.MaxLikeFull(fatigue_data)
            fit_res = mle_analyzer.analyze()
        else:
            fit_res = elem_res
            
        # Ensure k_2 exists (flat endurance limit)
        if 'k_2' not in fit_res:
            fit_res['k_2'] = np.inf
            
        # Instantiate the WoehlerCurve
        wc = WoehlerCurve(fit_res)
        
        # Show parameters in the parameters tab and as summary cards
        with tab_params:
            st.subheader("Fitted S-N Curve Parameters")
            col1, col2 = st.columns(2)
            with col1:
                st.write("**Fitted Series:**")
                st.dataframe(pd.DataFrame(fit_res, columns=["Fitted Value"]))
            with col2:
                st.markdown("""
                ### Parameter Legend:
                - **k_1**: Slope of the finite fatigue life region.
                - **SD**: Load/stress amplitude at the fatigue endurance limit (50% failure).
                - **ND**: Cycle limit of the fatigue endurance limit.
                - **TN**: Scatter band in cycle direction (N_90 / N_10).
                - **TS**: Scatter band in load direction (S_90 / S_10).
                """)

    except Exception as e:
        st.error(f"**pyLife Fitting Failed.**")
        st.info("This is usually due to insufficient data points, or no fractures/runouts in the respective fatigue regimes. Please verify your column mappings and runout configuration.")
        st.write(f"Detailed Error: `{e}`")
        st.stop()

    # Generate layout for main tab
    with tab_plot:
        # Beautiful dashboard metrics
        st.markdown("<div style='margin-bottom: 1.5rem;'></div>", unsafe_allow_html=True)
        col_m1, col_m2, col_m3, col_m4 = st.columns(4)
        with col_m1:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-value">{fit_res.get('k_1', 0.0):.2f}</div>
                <div class="metric-label">Curve Slope (k₁)</div>
            </div>
            """, unsafe_allow_html=True)
        with col_m2:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-value">{fit_res.get('SD', 0.0):.1f} MPa</div>
                <div class="metric-label">Endurance Limit (S_D)</div>
            </div>
            """, unsafe_allow_html=True)
        with col_m3:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-value">{fit_res.get('ND', 0.0):.2e}</div>
                <div class="metric-label">Endurance Cycles (N_D)</div>
            </div>
            """, unsafe_allow_html=True)
        with col_m4:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-value">{fit_res.get('TN', 1.0):.2f}</div>
                <div class="metric-label">Cycle Scatter (T_N)</div>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("<div style='margin-bottom: 2rem;'></div>", unsafe_allow_html=True)

        # Plot S-N Curve
        fig, ax = plt.subplots(figsize=(tiff_width, tiff_height))
        
        # Plot data points
        fractures = df_pylife[df_pylife['fracture'] == True]
        runouts = df_pylife[df_pylife['fracture'] == False]
        
        # Scatter for fractures
        ax.scatter(
            fractures['cycles'], fractures['load'],
            color=color_fractures, marker='o', s=60, label='Fractures (Failure)',
            edgecolors='black', zorder=5
        )
        
        # Scatter for runouts with right-pointing arrows
        ax.scatter(
            runouts['cycles'], runouts['load'],
            facecolors='none', edgecolors=color_runouts, marker='o', s=60,
            label='Runouts (Survival)', linewidths=1.5, zorder=5
        )
        
        for idx, row in runouts.iterrows():
            ax.annotate(
                '',
                xy=(row['cycles'] * 1.6, row['load']),
                xytext=(row['cycles'], row['load']),
                arrowprops=dict(arrowstyle="->", color=color_runouts, lw=1.5, shrinkA=0, shrinkB=0)
            )

        # Generate smooth cycle list for plotting Wöhler curves
        # Use log spacing to cover the whole fatigue lifetime range
        min_cycles = max(1e2, df_pylife['cycles'].min() * 0.1)
        max_cycles = df_pylife['cycles'].max() * 5.0
        cycles_plot = np.logspace(np.log10(min_cycles), np.log10(max_cycles), 500)
        
        # Define style configuration for each percentage
        curve_styles = {
            5:  {"color": "#06b6d4", "linestyle": (0, (5, 5)), "linewidth": 1.6},   # Cyan, dashed
            10: {"color": "#0ea5e9", "linestyle": (0, (5, 2)),  "linewidth": 1.6},   # Sky Blue, fine-dashed
            50: {"color": "#6366f1", "linestyle": "-",          "linewidth": 2.2},   # Indigo, solid
            90: {"color": "#8b5cf6", "linestyle": "--",         "linewidth": 1.8},   # Purple, dashed
            95: {"color": "#d946ef", "linestyle": "-.",         "linewidth": 1.8},   # Magenta, dash-dot
            99: {"color": "#ef4444", "linestyle": ":",          "linewidth": 2.0}    # Red, dotted
        }

        # Determine labeling and probability calculations
        if "Failure" in prob_type:
            label_suffix = "Failure"
            sorted_selected = sorted(selected_vals)
            
            for v in sorted_selected:
                p_fail = v / 100.0
                style = curve_styles.get(v, {"color": "gray", "linestyle": "-", "linewidth": 1.5})
                loads_curve = wc.load(cycles_plot, failure_probability=p_fail)
                ax.plot(
                    cycles_plot, loads_curve,
                    color=style["color"], linestyle=style["linestyle"], linewidth=style["linewidth"],
                    label=f'{v}% {label_suffix} (Pf={p_fail:.2f})'
                )
        else:
            label_suffix = "Survival"
            sorted_selected = sorted(selected_vals)
            
            for v in sorted_selected:
                p_surv = v / 100.0
                p_fail = 1.0 - p_surv
                style = curve_styles.get(v, {"color": "gray", "linestyle": "-", "linewidth": 1.5})
                loads_curve = wc.load(cycles_plot, failure_probability=p_fail)
                ax.plot(
                    cycles_plot, loads_curve,
                    color=style["color"], linestyle=style["linestyle"], linewidth=style["linewidth"],
                    label=f'{v}% {label_suffix} (Ps={p_surv:.2f})'
                )

        # Formatting
        ax.set_title(plot_title, fontsize=14, fontweight='bold', family='sans-serif', pad=15)
        ax.set_xlabel(x_label, fontsize=11, fontweight='semibold')
        ax.set_ylabel(y_label, fontsize=11, fontweight='semibold')
        
        if log_scale:
            ax.set_xscale('log')
            ax.set_yscale('log')
        else:
            ax.set_xscale('log') # Cycles are always log-scale
            
        if show_grid:
            ax.grid(True, which="both", ls="-", color="lightgray", alpha=0.5, zorder=0)

        # Adjust axes boundaries nicely
        ax.set_xlim(min_cycles, max_cycles)
        y_margin = (df_pylife['load'].max() - df_pylife['load'].min()) * 0.15
        if y_margin == 0:
            y_margin = df_pylife['load'].max() * 0.15
        ax.set_ylim(max(10.0, df_pylife['load'].min() - y_margin), df_pylife['load'].max() + y_margin)

        ax.legend(loc='best', framealpha=0.9, edgecolor='gray')
        plt.tight_layout()

        # Display the matplotlib figure in Streamlit
        st.pyplot(fig)

        # Save to TIFF buffer for direct download
        tiff_buf = io.BytesIO()
        fig.savefig(
            tiff_buf,
            format="tiff",
            dpi=tiff_dpi,
            bbox_inches="tight",
            pil_kwargs={"compression": "tiff_lzw"} # Standard compression to keep file size reasonable
        )
        tiff_buf.seek(0)
        
        # Download button
        st.markdown("<div style='text-align: center; margin-top: 1.5rem;'></div>", unsafe_allow_html=True)
        col_btn1, col_btn2, col_btn3 = st.columns([1, 2, 1])
        with col_btn2:
            st.download_button(
                label=f"💾 Download Publication-Ready TIFF ({tiff_dpi} DPI)",
                data=tiff_buf,
                file_name="sn_curve_pylife.tiff",
                mime="image/tiff",
                use_container_width=True
            )
            st.caption("The downloaded TIFF uses LZW lossless compression, perfect for importing into LaTeX documents, journals, and technical reports.")
else:
    # Blank State
    st.info("👋 **Welcome! Please select or upload an Excel file containing your cyclic fatigue testing data using the sidebar to get started.**")
    st.markdown("""
    ### Expected Data Format:
    Your Excel sheet should contain at least three columns:
    1. **Load level / Stress Amplitude** (e.g. in MPa)
    2. **Number of Cycles** (representing fatigue life)
    3. **Runout indicator** (identifying if the specimen survived the test without fracturing, e.g. `1` or `True` for survival, `0` or `False` for fracture)
    """)
    
    # Generate mockup preview if not loaded
    st.markdown("---")
    st.markdown("### Example S-N Curve Visualization:")
    
    # Show dummy graphic placeholder
    try:
        from PIL import Image
        if os.path.exists("mockup_preview.png"):
            st.image("mockup_preview.png", caption="Sample pyLife Probabilistic S-N curves")
    except:
        pass
