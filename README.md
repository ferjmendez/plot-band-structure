# Quantum Band Structure Plotter 📈

Elegant Python-based visualization tool for generating **publication-quality electronic structure figures** including:

* Band Structure
* Fatbands
* Density of States (DOS)
* Projected Density of States (PDOS) contribution to total DOS (comming soon)

with customizable layouts and full **LaTeX rendering support** for mathematical notation and Greek symbols.

---

## ✨ Features

✅ Publication-quality figures for papers and presentations
✅ Simultaneous plotting of:

* Band structure + DOS
* Fatbands + DOS

✅ Full LaTeX rendering support:

* Greek symbols like `Gamma`
* Mathematical notation (subscripts and superscripts)
* Custom orbital labels 

✅ Highly customizable:

* Colors
* Transparency (`alpha`)
* Energy range
* Figure size 
* Axis labels
* Line widths

✅ Compatible with outputs from:

* Quantum ESPRESSO
* SIESTA
* Wannier90
* DFT post-processing workflows

---

## 📷 Example Output File

![Example Figure](fatbands_dos_FeSe.png)

---

## 🧠 Motivation

Electronic structure analysis often requires combining multiple datasets into clear and visually consistent figures suitable for scientific publications.

This project was developed to simplify the generation of:

* Clean band structure plots
* Orbital-projected fatbands on band structure
* DOS/PDOS visualizations in right panel

with aesthetics appropriate for condensed matter physics and computational materials science research.

---

## Main libraries:

* numpy
* matplotlib
* pandas

---

## 🚀 Usage

Example:

```python
plot_fatbands(
    weight_scale=100,
    title='FeSe Band Structure',
    xlim=(0, 100),
    ylim=(-5, 5),
    alpha=0.1,
    fatbands_file='fatbands.dat'
)
```

---

## 📂 Repository Structure

```text
band-structure-plotter/
│── README.md
│── plot.py
│── 'example_plot'.png
│── example_data/
│── 'editable_notebook'.ipynb
```

---

## ⚙️ Main Capabilities

### 📉 Band Structure

* High-symmetry k-pointa plotting
* Fermi level alignment
* Custom energy windows

### 🔵 Fatbands

* Orbital-projected weights
* Adjustable marker scaling
* Multi-orbital visualization

### 📊 DOS / PDOS

* Side-by-side panel plotting
* Orbital decomposition
* Shared energy axis

### ✍️ LaTeX Rendering

Supports:

```python
r'$E-E_F$ (eV)'
r'$d_{xz}$'
r'$\Gamma$ - X - M - $\Gamma$'
```

allowing publication-quality mathematical formatting directly in the plots.

---

## 🖥️ Example Figure Generation

Run:

```bash
python plot.py
```

or you can edit file 'Use_your_info.ipynb'

---

## 🔬 Intended Applications

This project is especially useful for:

* Condensed Matter Physics
* Computational Materials Science
* DFT Analysis
* Electronic Structure Visualization
* Scientific Figure Preparation

---

## 📈 Future Improvements

Planned features:

* Interactive plotting
* Automatic parsing of Quantum ESPRESSO outputs
* Spin-polarized band structures
* SOC-aware plotting
* Automatic high-symmetry labeling
* Color maps for orbital character

---

## 👨‍💻 Author

**Fernando J. Méndez**
Physics Graduate | Computational Physics |

GitHub: [https://github.com/ferjmendez](https://github.com/ferjmendez)

---

## ⭐ Support

If you find this project useful for your research, consider giving the repository a star.