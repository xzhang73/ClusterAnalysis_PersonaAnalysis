# 🎯 Cluster and Persona Agent

An elegant AI-powered web application for customer segmentation and persona generation using K-means clustering.

![Cluster and Persona Agent](https://img.shields.io/badge/AI-Powered-blue) ![Python](https://img.shields.io/badge/Python-3.8%2B-green) ![Streamlit](https://img.shields.io/badge/Streamlit-1.31-red)

## 🌟 Features

- **Intelligent Clustering**: Automatically segments customers into 4 distinct clusters using K-means algorithm
- **Data-Driven Personas**: Generates comprehensive personas based on actual cluster characteristics
- **Conversion-Focused**: Ranks personas by conversion rate for immediate business value
- **Beautiful Visualizations**: Interactive charts including PCA plots and cluster analysis dashboards
- **Elegant UI**: Clean, professional interface built with Streamlit
- **Real-time Processing**: Upload data and get results instantly
- **Export Ready**: Download personas (JSON), clustered data (CSV), and visualizations (PNG)

## 📋 Prerequisites

- Python 3.8 or higher
- pip (Python package manager)

## 🚀 Installation

### Step 1: Install Dependencies

Open your terminal/command prompt and run:

```bash
pip install -r requirements.txt
```

Or install packages individually:

```bash
pip install streamlit pandas numpy scikit-learn matplotlib seaborn Pillow
```

### Step 2: Verify Installation

```bash
streamlit --version
```

You should see something like: `Streamlit, version 1.31.0`

## 💻 Running the Application

### Quick Start

Navigate to the directory containing `cluster_persona_agent.py` and run:

```bash
streamlit run cluster_persona_agent.py
```

The application will automatically open in your default web browser at `http://localhost:8501`

### Alternative Port

If port 8501 is already in use:

```bash
streamlit run cluster_persona_agent.py --server.port 8502
```

## 📊 Using the Application

### 1. Prepare Your Data

Your CSV file should contain these columns:
- `State` - Geographic location
- `Industry` - Industry sector
- `Job Title` - Professional role
- `Education Level` - Educational background
- `Age_range` - Age category
- `Years of Experience` - Professional experience
- `Gender` - Gender information
- `Lead Source` - How the lead was acquired
- `is_sale` - Conversion status (TRUE/FALSE or 1/0)

**Example CSV structure:**
```csv
Country,State,Industry,Job Title,Education Level,Age_range,Years of Experience,Gender,Lead Source,is_sale
United States,IL,Technology,Analyst,Bachelor's,25-40,5-10 Years,Male,Web,TRUE
United States,CA,Healthcare,Manager,Master's,40-55,10-15 Years,Female,Google,TRUE
...
```

### 2. Upload Your File

1. Click the "Browse files" button in the left panel
2. Select your CSV or TXT file
3. Wait for the upload confirmation

### 3. View Results

The application will automatically:
- ✅ Perform clustering analysis
- ✅ Generate 4 data-driven personas
- ✅ Create visualizations
- ✅ Display results in an elegant format

#### Left Panel:
- **Upload section** at the top
- **Cluster Analysis Dashboard** - 4-panel view showing:
  - Cluster size distribution
  - Conversion rates by cluster
  - Total conversions by cluster
  - Cluster distribution pie chart
- **PCA Visualization** - 2D scatter plot of clusters

#### Right Panel:
- **Persona Profiles** organized in tabs (ranked by conversion rate)
- Each persona shows:
  - 🎯 **Conversion Metrics** (conversion rate, value tier, conversions)
  - 👥 **Demographics** (seniority, experience, age)
  - 🌍 **Geography** (primary state, concentration)
  - 💼 **Professional** (industry, titles, education)
  - 📊 **Acquisition** (lead sources)

### 4. Download Results

Three download options available:
- **📥 Download Dashboard** - Cluster analysis charts (PNG)
- **📥 Download PCA Visualization** - Cluster scatter plot (PNG)
- **📥 Download Complete Personas** - Full persona data (JSON)
- **📥 Download Clustered Data** - Original data with cluster assignments (CSV)

## 🎨 Features Breakdown

### Clustering Algorithm
- **Method**: K-Means with 4 clusters
- **Features Used**: All demographic, professional, and behavioral attributes
- **Preprocessing**: Label encoding + standardization
- **Dimensionality Reduction**: PCA for visualization

### Persona Generation
Personas are **100% data-driven** with:
- Dynamic seniority detection (C-Suite, Senior Management, Management, Professional, Entry-Level)
- Conversion-based value tiers (PREMIUM ≥50%, HIGH ≥25%, MEDIUM ≥10%, LOW ≥5%, MINIMAL <5%)
- Geographic concentration metrics
- Industry focus analysis
- Experience distribution profiling
- Lead source attribution

### Visualizations
1. **Cluster Analysis Dashboard** (4 charts):
   - Cluster sizes with value labels
   - Conversion rates with average baseline
   - Total conversions per cluster
   - Cluster distribution

2. **PCA Visualization**:
   - 2D scatter plot of all records
   - Color-coded by cluster
   - Variance explained shown

## 🛠️ Troubleshooting

### Port Already in Use
```bash
streamlit run cluster_persona_agent.py --server.port 8502
```

### Missing Dependencies
```bash
pip install --upgrade -r requirements.txt
```

### File Upload Issues
- Ensure CSV is UTF-8 encoded
- Check that all required columns are present
- Verify `is_sale` column contains TRUE/FALSE or 1/0 values

### Memory Issues (Large Files)
For files with 100,000+ records, consider:
- Using a sample of your data
- Running on a machine with more RAM
- Reducing the number of features

## 📁 Project Structure

```
cluster-persona-agent/
│
├── cluster_persona_agent.py    # Main Streamlit application
├── requirements.txt             # Python dependencies
├── README.md                    # This file
│
└── data/                        # (Create this folder for your CSV files)
    └── your_data.csv
```

## 🎯 Value Tier Classification

Personas are automatically classified into value tiers based on conversion rate:

| Tier | Conversion Rate | Color | Priority |
|------|----------------|-------|----------|
| PREMIUM | ≥50% | Green | Highest |
| HIGH | 25-49% | Light Green | High |
| MEDIUM | 10-24% | Pink | Medium |
| LOW | 5-9% | Blue | Low |
| MINIMAL | <5% | Light Blue | Minimal |

## 💡 Tips for Best Results

1. **Data Quality**: Ensure your data is clean and complete
2. **Sample Size**: Minimum 500+ records recommended for meaningful clusters
3. **Feature Variety**: More diverse data → more distinct personas
4. **Conversion Labels**: Ensure `is_sale` column is properly labeled
5. **Regular Updates**: Re-run analysis as new data becomes available

## 🔒 Privacy & Security

- All processing is done **locally** on your machine
- No data is sent to external servers
- Files are processed in-memory only
- No data persistence (unless you download results)

## 📈 Performance

- **Small datasets** (<10K records): Near-instant results
- **Medium datasets** (10K-50K records): 5-15 seconds
- **Large datasets** (50K-100K records): 30-60 seconds
- **Very large datasets** (>100K records): Consider sampling

## 🤝 Support

For issues or questions:
1. Check the troubleshooting section
2. Verify all dependencies are installed
3. Ensure your CSV matches the required format
4. Review the example data structure

## 📄 License

This project is provided as-is for educational and commercial use.

## 🚀 Future Enhancements

Potential features for future versions:
- [ ] Variable cluster count (user-selectable)
- [ ] Alternative clustering algorithms (DBSCAN, Hierarchical)
- [ ] Time-series analysis for trend detection
- [ ] Export to PowerPoint/PDF reports
- [ ] Database integration
- [ ] API endpoint for programmatic access
- [ ] Comparative analysis across multiple datasets

## 🎓 How It Works

1. **Data Upload**: User uploads CSV file through web interface
2. **Preprocessing**: Missing values filled, categorical variables encoded, features standardized
3. **Clustering**: K-means algorithm segments data into 4 distinct clusters
4. **Analysis**: Each cluster analyzed for demographic, geographic, and professional patterns
5. **Persona Generation**: Data-driven personas created with comprehensive profiles
6. **Visualization**: Charts generated showing cluster characteristics and performance
7. **Ranking**: Personas sorted by conversion rate for business prioritization
8. **Export**: Results available for download in multiple formats

---

**Version**: 1.0.0  
**Last Updated**: January 2026  
**Built with**: ❤️ and Python
