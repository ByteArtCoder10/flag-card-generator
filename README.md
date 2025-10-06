# 🌎 **FLAG CARD GENERATOR**

A Python tool to create **printable world-flag flashcards**.  
Each card displays a **flag** on one side and **country details** (including name, capital, continent, and languages) on the other. Perfect for learning geography & educational purposes!
---

# 🧩 **FEATURES**

- Automatic Flag Download & Conversion – Downloads SVG flags and converts them to PNG.  
- Uniform Size – Flags resized to **9 × 6 cm** for printing.  
- Country Data Support – Uses Microsoft Word tables to fetch:  
  - Country name  
  - Capital  
  - Continent  
  - Languages  
- PDF Output – Double-sided printing:  
  - **Front:** Flags, 8 per page.
  - **Back:** Country info aligned behind each flag.
- Educational – Ideal for flashcards or learning materials/


# ⚙️ **TECHNOLOGIES USED**

- Python 3
- Pillow (PIL) – image processing
- requests – download SVGs
- reportlab – PDF generation
- pandas – read Microsoft Word file data

---

# 🚀 **INSTALLATION & USAGE**

1. **Clone the repository**
```bash
git clone https://github.com/ByteArtCoder10/flag-card-generator.git
cd flag-card-generator
```

3. **Install dependencies:**
```bash
pip install -r requirements.txt
```

5. **Run the script**
```bash
python main.py
```

All required assets (flags, fonts, JSON data) are already included. You do not need the old scripts to run the program.

🛠️ **LEGACY SCRIPTS**

These scripts were used in earlier versions to prepare assets, but are no longer needed for normal use:
  -crop.py – cropped and normalized flag images/
  -generate_flags_folder_and_country_data.py – generated the flags/ folder and countries_data.txt file/

The program now includes all assets, allowing you to generate PDFs directly without needing to run these scripts.

📄 **LICENSE**
Public License.
