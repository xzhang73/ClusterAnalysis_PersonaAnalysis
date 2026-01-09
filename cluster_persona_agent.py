import streamlit as st
import pandas as pd
import numpy as np
from sklearn.cluster import KMeans
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt
import seaborn as sns
import json
from collections import Counter
import warnings
import io
import base64
from PIL import Image

warnings.filterwarnings('ignore')

# Page configuration
st.set_page_config(
    page_title="Cluster & Persona Agent",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS for elegant styling
st.markdown("""
    <style>
    .main {
        background-color: #f8f9fa;
    }
    .stApp {
        max-width: 100%;
    }
    .title-text {
        font-size: 42px;
        font-weight: bold;
        color: #1e3a8a;
        text-align: center;
        margin-bottom: 10px;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }
    .subtitle-text {
        font-size: 18px;
        color: #64748b;
        text-align: center;
        margin-bottom: 30px;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }
    .upload-section {
        background-color: white;
        padding: 25px;
        border-radius: 10px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        margin-bottom: 25px;
    }
    .persona-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 20px;
        border-radius: 12px;
        margin-bottom: 20px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.15);
    }
    .persona-card-high {
        background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%);
    }
    .persona-card-medium {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
    }
    .persona-card-low {
        background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
    }
    .persona-title {
        font-size: 24px;
        font-weight: bold;
        margin-bottom: 15px;
        border-bottom: 2px solid rgba(255,255,255,0.3);
        padding-bottom: 10px;
    }
    .metric-box {
        background-color: rgba(255,255,255,0.2);
        padding: 15px;
        border-radius: 8px;
        margin: 10px 0;
    }
    .metric-label {
        font-size: 14px;
        opacity: 0.9;
        margin-bottom: 5px;
    }
    .metric-value {
        font-size: 28px;
        font-weight: bold;
    }
    .section-header {
        font-size: 18px;
        font-weight: bold;
        margin-top: 20px;
        margin-bottom: 10px;
        border-left: 4px solid rgba(255,255,255,0.8);
        padding-left: 10px;
    }
    .info-text {
        font-size: 14px;
        line-height: 1.6;
        opacity: 0.95;
    }
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
    }
    .stTabs [data-baseweb="tab"] {
        background-color: #e2e8f0;
        border-radius: 8px 8px 0 0;
        padding: 10px 20px;
        font-weight: 600;
    }
    .stTabs [aria-selected="true"] {
        background-color: #3b82f6;
        color: white;
    }
    </style>
""", unsafe_allow_html=True)


# ========== CLUSTERING AND PERSONA FUNCTIONS ==========

def analyze_cluster_characteristics(cluster_data):
    """Dynamically analyze cluster characteristics to extract meaningful insights."""
    profile = {}
    
    # Geographic analysis
    state_dist = cluster_data['State'].value_counts()
    profile['primary_state'] = state_dist.index[0] if len(state_dist) > 0 else 'Unknown'
    profile['state_concentration'] = (state_dist.iloc[0] / len(cluster_data) * 100) if len(state_dist) > 0 else 0
    profile['top_states'] = state_dist.head(3).to_dict()
    
    # Industry analysis
    industry_dist = cluster_data['Industry'].value_counts()
    profile['primary_industry'] = industry_dist.index[0] if len(industry_dist) > 0 else 'Unknown'
    profile['industry_concentration'] = (industry_dist.iloc[0] / len(cluster_data) * 100) if len(industry_dist) > 0 else 0
    profile['top_industries'] = industry_dist.head(3).to_dict()
    
    # Job title analysis and seniority determination
    title_dist = cluster_data['Job Title'].value_counts()
    profile['top_titles'] = title_dist.head(5).to_dict()
    
    # Dynamic seniority detection based on actual job titles
    all_titles = ' '.join(cluster_data['Job Title'].astype(str).tolist()).lower()
    
    seniority_scores = {
        'C-Suite': 0,
        'Senior Management': 0,
        'Management': 0,
        'Professional': 0,
        'Entry-Level': 0
    }
    
    # C-Suite keywords
    c_suite_keywords = ['ceo', 'chief', 'president', 'founder', 'owner', 'partner', 'cto', 'cfo', 'coo', 'cmo']
    for keyword in c_suite_keywords:
        seniority_scores['C-Suite'] += all_titles.count(keyword)
    
    # Senior Management keywords
    senior_mgmt_keywords = ['vp', 'vice president', 'director', 'head of', 'senior manager']
    for keyword in senior_mgmt_keywords:
        seniority_scores['Senior Management'] += all_titles.count(keyword)
    
    # Management keywords
    mgmt_keywords = ['manager', 'supervisor', 'lead', 'coordinator']
    for keyword in mgmt_keywords:
        seniority_scores['Management'] += all_titles.count(keyword)
    
    # Professional keywords
    prof_keywords = ['analyst', 'specialist', 'consultant', 'engineer', 'developer', 'architect']
    for keyword in prof_keywords:
        seniority_scores['Professional'] += all_titles.count(keyword)
    
    # Entry-level keywords
    entry_keywords = ['intern', 'junior', 'associate', 'assistant', 'trainee']
    for keyword in entry_keywords:
        seniority_scores['Entry-Level'] += all_titles.count(keyword)
    
    # Determine dominant seniority
    profile['seniority'] = max(seniority_scores, key=seniority_scores.get)
    profile['seniority_confidence'] = max(seniority_scores.values())
    
    # If no clear seniority, use "Mixed Professional"
    if max(seniority_scores.values()) == 0:
        profile['seniority'] = 'Mixed Professional'
    
    # Experience analysis
    exp_dist = cluster_data['Years of Experience'].value_counts()
    profile['primary_experience'] = exp_dist.index[0] if len(exp_dist) > 0 else 'Unknown'
    profile['experience_distribution'] = exp_dist.head(5).to_dict()
    
    # Lead source analysis
    source_dist = cluster_data['Lead Source'].value_counts()
    profile['primary_lead_source'] = source_dist.index[0] if len(source_dist) > 0 else 'Unknown'
    profile['lead_source_distribution'] = source_dist.to_dict()
    
    # Gender analysis
    gender_dist = cluster_data['Gender'].value_counts()
    profile['gender_distribution'] = gender_dist.to_dict()
    
    # Education analysis
    edu_dist = cluster_data['Education Level'].value_counts()
    profile['primary_education'] = edu_dist.index[0] if len(edu_dist) > 0 else 'Unknown'
    profile['education_distribution'] = edu_dist.head(3).to_dict()
    
    # Age range analysis
    age_dist = cluster_data['Age_range'].value_counts()
    profile['primary_age_range'] = age_dist.index[0] if len(age_dist) > 0 else 'Unknown'
    profile['age_distribution'] = age_dist.to_dict()
    
    return profile


def calculate_conversion_metrics(cluster_data):
    """Calculate comprehensive conversion metrics for a cluster."""
    total_records = len(cluster_data)
    conversions = cluster_data['is_sale'].sum()
    conversion_rate = (conversions / total_records * 100) if total_records > 0 else 0
    
    # Determine value tier based on conversion rate
    if conversion_rate >= 50:
        value_tier = "PREMIUM"
    elif conversion_rate >= 25:
        value_tier = "HIGH"
    elif conversion_rate >= 10:
        value_tier = "MEDIUM"
    elif conversion_rate >= 5:
        value_tier = "LOW"
    else:
        value_tier = "MINIMAL"
    
    return {
        'total_records': int(total_records),
        'conversions': int(conversions),
        'non_conversions': int(total_records - conversions),
        'conversion_rate': float(conversion_rate),
        'value_tier': value_tier
    }


def generate_persona_name(profile, conversion_metrics):
    """Generate a descriptive persona name based on cluster characteristics."""
    industry = profile['primary_industry']
    state = profile['primary_state']
    seniority = profile['seniority']
    conv_tier = conversion_metrics['value_tier']
    
    # Create a meaningful name
    if industry != 'Unknown' and state != 'Unknown':
        base_name = f"{seniority} in {industry}"
    elif industry != 'Unknown':
        base_name = f"{seniority} - {industry} Sector"
    elif state != 'Unknown':
        base_name = f"{seniority} ({state})"
    else:
        base_name = f"{seniority} Professionals"
    
    # Add conversion tier indicator
    name_with_tier = f"{base_name} [{conv_tier} VALUE]"
    
    return name_with_tier


def create_persona(cluster_data, cluster_id, total_records):
    """Generate a comprehensive, data-driven persona for a cluster."""
    # Analyze cluster characteristics
    profile = analyze_cluster_characteristics(cluster_data)
    
    # Calculate conversion metrics
    conversion_metrics = calculate_conversion_metrics(cluster_data)
    
    # Generate persona name
    persona_name = generate_persona_name(profile, conversion_metrics)
    
    # Create comprehensive persona dictionary
    persona = {
        # Identification
        'persona_name': persona_name,
        'cluster_id': int(cluster_id),
        'cluster_size': int(len(cluster_data)),
        'cluster_percentage': float(len(cluster_data) / total_records * 100),
        
        # Conversion Metrics (PRIMARY FOCUS)
        'conversion_metrics': conversion_metrics,
        
        # Demographics
        'demographics': {
            'seniority': profile['seniority'],
            'seniority_confidence': int(profile['seniority_confidence']),
            'primary_experience': profile['primary_experience'],
            'experience_distribution': {str(k): int(v) for k, v in profile['experience_distribution'].items()},
            'primary_age_range': profile['primary_age_range'],
            'age_distribution': {str(k): int(v) for k, v in profile['age_distribution'].items()},
            'gender_distribution': {str(k): int(v) for k, v in profile['gender_distribution'].items()},
        },
        
        # Geographic Profile
        'geography': {
            'primary_state': profile['primary_state'],
            'state_concentration': float(profile['state_concentration']),
            'top_states': {str(k): int(v) for k, v in profile['top_states'].items()},
        },
        
        # Professional Profile
        'professional': {
            'primary_industry': profile['primary_industry'],
            'industry_concentration': float(profile['industry_concentration']),
            'top_industries': {str(k): int(v) for k, v in profile['top_industries'].items()},
            'top_job_titles': {str(k): int(v) for k, v in profile['top_titles'].items()},
            'primary_education': profile['primary_education'],
        },
        
        # Acquisition Profile
        'acquisition': {
            'primary_lead_source': profile['primary_lead_source'],
            'lead_source_distribution': {str(k): int(v) for k, v in profile['lead_source_distribution'].items()},
        },
    }
    
    return persona


def perform_clustering(df, n_clusters=4):
    """Perform K-means clustering on the dataset."""
    # Fill missing values
    df['Industry'] = df['Industry'].fillna('Unknown')
    df['Job Title'] = df['Job Title'].fillna('Unknown')
    df['Years of Experience'] = df['Years of Experience'].fillna('Unknown')
    df['Education Level'] = df['Education Level'].fillna('Unknown')
    df['Age_range'] = df['Age_range'].fillna('Unknown')
    df['State'] = df['State'].fillna('Unknown')
    df['Gender'] = df['Gender'].fillna('Unknown')
    df['Lead Source'] = df['Lead Source'].fillna('Unknown')
    
    # Encode categorical variables
    encoded_cols = ['State', 'Industry', 'Job Title', 
                    'Education Level', 'Age_range', 'Years of Experience', 
                    'Gender', 'Lead Source']
    
    df_encoded = df.copy()
    le_dict = {}
    
    for col in encoded_cols:
        le = LabelEncoder()
        df_encoded[col + '_encoded'] = le.fit_transform(df_encoded[col].astype(str))
        le_dict[col] = le
    
    # Prepare features for clustering
    feature_cols = [col + '_encoded' for col in encoded_cols]
    X = df_encoded[feature_cols].values
    
    # Standardize the features
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    
    # Perform K-Means clustering
    kmeans = KMeans(n_clusters=n_clusters, random_state=42, n_init=10)
    cluster_labels = kmeans.fit_predict(X_scaled)
    
    # Add cluster labels to dataframe
    df['Cluster'] = cluster_labels
    
    return df, kmeans, X_scaled


def create_visualizations(df, kmeans, X_scaled, n_clusters=4):
    """Create visualization charts."""
    
    # 1. PCA Visualization
    pca = PCA(n_components=2)
    X_pca = pca.fit_transform(X_scaled)
    
    fig1, ax = plt.subplots(figsize=(10, 7))
    scatter = ax.scatter(X_pca[:, 0], X_pca[:, 1], 
                        c=df['Cluster'], cmap='viridis', 
                        alpha=0.6, edgecolors='w', linewidth=0.5, s=50)
    
    ax.set_title(f'K-Means Clustering Visualization ({n_clusters} Clusters)\nPCA Reduction', 
                 fontsize=14, fontweight='bold', pad=15)
    ax.set_xlabel(f'First Principal Component ({pca.explained_variance_ratio_[0]:.1%} variance)', 
                  fontsize=11)
    ax.set_ylabel(f'Second Principal Component ({pca.explained_variance_ratio_[1]:.1%} variance)', 
                  fontsize=11)
    
    cbar = plt.colorbar(scatter, ax=ax)
    cbar.set_label('Cluster ID', rotation=270, labelpad=20, fontsize=11)
    plt.tight_layout()
    
    # Save to buffer
    buf1 = io.BytesIO()
    plt.savefig(buf1, format='png', dpi=150, bbox_inches='tight')
    buf1.seek(0)
    plt.close()
    
    # 2. Cluster Analysis Dashboard
    fig2, axes = plt.subplots(2, 2, figsize=(14, 10))
    
    # Cluster sizes
    ax = axes[0, 0]
    cluster_sizes = df['Cluster'].value_counts().sort_index()
    colors = plt.cm.viridis(np.linspace(0, 1, n_clusters))
    bars = ax.bar(range(n_clusters), cluster_sizes.values, color=colors, edgecolor='black', linewidth=1.5)
    ax.set_title('Cluster Size Distribution', fontsize=12, fontweight='bold', pad=12)
    ax.set_xlabel('Cluster ID', fontsize=10)
    ax.set_ylabel('Number of Records', fontsize=10)
    ax.set_xticks(range(n_clusters))
    ax.grid(axis='y', alpha=0.3, linestyle='--')
    
    for bar in bars:
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height,
                f'{int(height):,}',
                ha='center', va='bottom', fontsize=9, fontweight='bold')
    
    # Conversion rates by cluster
    ax = axes[0, 1]
    conversion_rates = []
    for cluster_id in range(n_clusters):
        cluster_mask = df['Cluster'] == cluster_id
        rate = (df[cluster_mask]['is_sale'].sum() / cluster_mask.sum() * 100)
        conversion_rates.append(rate)
    
    bars = ax.bar(range(n_clusters), conversion_rates, color='coral', edgecolor='darkred', linewidth=1.5)
    ax.set_title('Conversion Rate by Cluster', fontsize=12, fontweight='bold', pad=12)
    ax.set_xlabel('Cluster ID', fontsize=10)
    ax.set_ylabel('Conversion Rate (%)', fontsize=10)
    ax.set_xticks(range(n_clusters))
    ax.grid(axis='y', alpha=0.3, linestyle='--')
    ax.axhline(y=np.mean(conversion_rates), color='red', linestyle='--', 
               linewidth=2, label=f'Average: {np.mean(conversion_rates):.1f}%')
    ax.legend(fontsize=9)
    
    for bar in bars:
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height,
                f'{height:.1f}%',
                ha='center', va='bottom', fontsize=9, fontweight='bold')
    
    # Total conversions by cluster
    ax = axes[1, 0]
    total_conversions = []
    for cluster_id in range(n_clusters):
        cluster_mask = df['Cluster'] == cluster_id
        conversions = df[cluster_mask]['is_sale'].sum()
        total_conversions.append(conversions)
    
    bars = ax.bar(range(n_clusters), total_conversions, color='lightgreen', 
                  edgecolor='darkgreen', linewidth=1.5)
    ax.set_title('Total Conversions by Cluster', fontsize=12, fontweight='bold', pad=12)
    ax.set_xlabel('Cluster ID', fontsize=10)
    ax.set_ylabel('Number of Conversions', fontsize=10)
    ax.set_xticks(range(n_clusters))
    ax.grid(axis='y', alpha=0.3, linestyle='--')
    
    for bar in bars:
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height,
                f'{int(height):,}',
                ha='center', va='bottom', fontsize=9, fontweight='bold')
    
    # Cluster value distribution (pie chart)
    ax = axes[1, 1]
    # We'll calculate this from personas later, for now show cluster distribution
    labels = [f'Cluster {i}' for i in range(n_clusters)]
    ax.pie(cluster_sizes.values, labels=labels, autopct='%1.1f%%', 
           startangle=90, colors=colors, textprops={'fontsize': 9})
    ax.set_title('Cluster Distribution', fontsize=12, fontweight='bold', pad=12)
    
    plt.tight_layout()
    
    # Save to buffer
    buf2 = io.BytesIO()
    plt.savefig(buf2, format='png', dpi=150, bbox_inches='tight')
    buf2.seek(0)
    plt.close()
    
    return buf1, buf2


# ========== STREAMLIT APP ==========

def main():
    # Title section
    st.markdown('<div class="title-text">🎯 Cluster and Persona Agent</div>', unsafe_allow_html=True)
    st.markdown('<div class="subtitle-text">AI-Powered Customer Segmentation & Persona Generation</div>', unsafe_allow_html=True)
    
    # Create two columns
    col_left, col_right = st.columns([1, 1])
    
    with col_left:
        # Upload section
        st.markdown('<div class="upload-section">', unsafe_allow_html=True)
        st.markdown("### 📁 Please upload your file here:")
        
        uploaded_file = st.file_uploader(
            "Choose a CSV or TXT file",
            type=['csv', 'txt'],
            help="Upload your customer data file (CSV or TXT format)"
        )
        st.markdown('</div>', unsafe_allow_html=True)
        
        if uploaded_file is not None:
            try:
                # Read the file
                df = pd.read_csv(uploaded_file, encoding='utf-8')
                
                # Drop unnamed index column if it exists
                if 'Unnamed: 0' in df.columns:
                    df = df.drop(columns='Unnamed: 0')
                
                # Validate required columns
                required_cols = ['State', 'Industry', 'Job Title', 'Education Level', 
                               'Age_range', 'Years of Experience', 'Gender', 'Lead Source', 'is_sale']
                
                missing_cols = [col for col in required_cols if col not in df.columns]
                
                if missing_cols:
                    st.error(f"❌ Missing required columns: {', '.join(missing_cols)}")
                    return
                
                # Show success message
                st.success(f"✅ File uploaded successfully! ({len(df):,} records)")
                
                # Perform clustering
                with st.spinner('🔄 Performing clustering analysis...'):
                    df_clustered, kmeans, X_scaled = perform_clustering(df)
                
                # Generate personas
                with st.spinner('🎭 Generating personas...'):
                    personas = []
                    for cluster_id in range(4):
                        cluster_data = df_clustered[df_clustered['Cluster'] == cluster_id]
                        persona = create_persona(cluster_data, cluster_id, len(df_clustered))
                        personas.append(persona)
                    
                    # Sort by conversion rate
                    personas_sorted = sorted(personas, key=lambda x: x['conversion_metrics']['conversion_rate'], reverse=True)
                
                # Create visualizations
                with st.spinner('📊 Creating visualizations...'):
                    viz_buf, dashboard_buf = create_visualizations(df_clustered, kmeans, X_scaled)
                
                # Display charts
                st.markdown("### 📊 Analysis Visualizations")
                
                # Show cluster analysis dashboard
                st.markdown("#### Cluster Analysis Dashboard")
                st.image(dashboard_buf, use_container_width=True)
                
                # Show PCA visualization
                st.markdown("#### K-Means Cluster Visualization")
                st.image(viz_buf, use_container_width=True)
                
                # Download buttons for charts
                st.download_button(
                    label="📥 Download Dashboard",
                    data=dashboard_buf,
                    file_name="cluster_analysis_dashboard.png",
                    mime="image/png"
                )
                
                st.download_button(
                    label="📥 Download PCA Visualization",
                    data=viz_buf,
                    file_name="kmeans_clusters_visualization.png",
                    mime="image/png"
                )
                
            except Exception as e:
                st.error(f"❌ Error processing file: {str(e)}")
                return
    
    # Right column - Persona summaries
    with col_right:
        if uploaded_file is not None and 'personas_sorted' in locals():
            st.markdown("### 🎭 Persona Profiles (Ranked by Conversion Rate)")
            
            # Create tabs for each persona
            tabs = st.tabs([f"Rank #{i+1}" for i in range(len(personas_sorted))])
            
            for idx, (tab, persona) in enumerate(zip(tabs, personas_sorted)):
                with tab:
                    # Determine card class based on value tier
                    tier = persona['conversion_metrics']['value_tier']
                    if tier in ['PREMIUM', 'HIGH']:
                        card_class = 'persona-card-high'
                    elif tier == 'MEDIUM':
                        card_class = 'persona-card-medium'
                    else:
                        card_class = 'persona-card-low'
                    
                    # Persona card
                    st.markdown(f'<div class="persona-card {card_class}">', unsafe_allow_html=True)
                    
                    # Title
                    st.markdown(f'<div class="persona-title">🏆 {persona["persona_name"]}</div>', 
                              unsafe_allow_html=True)
                    
                    # Basic info
                    st.markdown(f'<div class="info-text">Cluster ID: {persona["cluster_id"]} | '
                              f'Size: {persona["cluster_size"]:,} '
                              f'({persona["cluster_percentage"]:.1f}% of total)</div>', 
                              unsafe_allow_html=True)
                    
                    # Conversion metrics
                    cm = persona['conversion_metrics']
                    col1, col2 = st.columns(2)
                    with col1:
                        st.markdown(f'''
                            <div class="metric-box">
                                <div class="metric-label">🎯 Conversion Rate</div>
                                <div class="metric-value">{cm["conversion_rate"]:.2f}%</div>
                            </div>
                        ''', unsafe_allow_html=True)
                    with col2:
                        st.markdown(f'''
                            <div class="metric-box">
                                <div class="metric-label">💎 Value Tier</div>
                                <div class="metric-value">{cm["value_tier"]}</div>
                            </div>
                        ''', unsafe_allow_html=True)
                    
                    col3, col4 = st.columns(2)
                    with col3:
                        st.markdown(f'''
                            <div class="metric-box">
                                <div class="metric-label">✅ Conversions</div>
                                <div class="metric-value">{cm["conversions"]:,}</div>
                            </div>
                        ''', unsafe_allow_html=True)
                    with col4:
                        st.markdown(f'''
                            <div class="metric-box">
                                <div class="metric-label">📊 Total Records</div>
                                <div class="metric-value">{cm["total_records"]:,}</div>
                            </div>
                        ''', unsafe_allow_html=True)
                    
                    # Demographics
                    demo = persona['demographics']
                    st.markdown('<div class="section-header">👥 Demographics</div>', unsafe_allow_html=True)
                    st.markdown(f'''
                        <div class="info-text">
                        <strong>Seniority:</strong> {demo["seniority"]}<br>
                        <strong>Experience:</strong> {demo["primary_experience"]}<br>
                        <strong>Age Range:</strong> {demo["primary_age_range"]}<br>
                        </div>
                    ''', unsafe_allow_html=True)
                    
                    # Top experience levels
                    if demo['experience_distribution']:
                        exp_top3 = sorted(demo['experience_distribution'].items(), key=lambda x: x[1], reverse=True)[:3]
                        exp_text = ", ".join([f"{exp}: {count}" for exp, count in exp_top3])
                        st.markdown(f'<div class="info-text"><strong>Top Experience:</strong> {exp_text}</div>', 
                                  unsafe_allow_html=True)
                    
                    # Geography
                    geo = persona['geography']
                    st.markdown('<div class="section-header">🌍 Geography</div>', unsafe_allow_html=True)
                    st.markdown(f'''
                        <div class="info-text">
                        <strong>Primary State:</strong> {geo["primary_state"]}<br>
                        <strong>Concentration:</strong> {geo["state_concentration"]:.1f}%<br>
                        </div>
                    ''', unsafe_allow_html=True)
                    
                    # Professional
                    prof = persona['professional']
                    st.markdown('<div class="section-header">💼 Professional</div>', unsafe_allow_html=True)
                    st.markdown(f'''
                        <div class="info-text">
                        <strong>Industry:</strong> {prof["primary_industry"]}<br>
                        <strong>Industry Focus:</strong> {prof["industry_concentration"]:.1f}%<br>
                        <strong>Education:</strong> {prof["primary_education"]}<br>
                        </div>
                    ''', unsafe_allow_html=True)
                    
                    # Top job titles (exclude Unknown)
                    top_titles = [title for title in list(prof['top_job_titles'].keys())[:5] if title != 'Unknown'][:3]
                    if top_titles:
                        st.markdown(f'<div class="info-text"><strong>Common Titles:</strong> {", ".join(top_titles)}</div>', 
                                  unsafe_allow_html=True)
                    
                    # Acquisition
                    acq = persona['acquisition']
                    st.markdown('<div class="section-header">📊 Acquisition</div>', unsafe_allow_html=True)
                    st.markdown(f'''
                        <div class="info-text">
                        <strong>Primary Lead Source:</strong> {acq["primary_lead_source"]}<br>
                        </div>
                    ''', unsafe_allow_html=True)
                    
                    # Top lead sources
                    source_top3 = sorted(acq['lead_source_distribution'].items(), key=lambda x: x[1], reverse=True)[:3]
                    source_text = ", ".join([f"{src}: {count}" for src, count in source_top3])
                    st.markdown(f'<div class="info-text"><strong>Lead Sources:</strong> {source_text}</div>', 
                              unsafe_allow_html=True)
                    
                    st.markdown('</div>', unsafe_allow_html=True)
            
            # Download personas JSON
            st.markdown("---")
            personas_json = json.dumps(personas_sorted, indent=2)
            st.download_button(
                label="📥 Download Complete Personas (JSON)",
                data=personas_json,
                file_name="personas_analysis.json",
                mime="application/json"
            )
            
            # Download clustered CSV
            csv_output = df_clustered.to_csv(index=False)
            st.download_button(
                label="📥 Download Clustered Data (CSV)",
                data=csv_output,
                file_name="clustered_output.csv",
                mime="text/csv"
            )
        
        else:
            # Show placeholder when no file uploaded
            st.markdown("""
                <div style="background-color: white; padding: 40px; border-radius: 10px; 
                            text-align: center; box-shadow: 0 2px 8px rgba(0,0,0,0.1);">
                    <h3 style="color: #64748b;">👈 Upload a file to get started</h3>
                    <p style="color: #94a3b8; margin-top: 20px;">
                        Your persona profiles will appear here once the analysis is complete.
                    </p>
                    <p style="color: #94a3b8; margin-top: 10px; font-size: 14px;">
                        The system will automatically:
                    </p>
                    <ul style="color: #94a3b8; text-align: left; display: inline-block; margin-top: 10px;">
                        <li>Perform K-means clustering (4 clusters)</li>
                        <li>Generate data-driven personas</li>
                        <li>Rank by conversion rate</li>
                        <li>Create visualizations</li>
                    </ul>
                </div>
            """, unsafe_allow_html=True)


if __name__ == "__main__":
    main()
