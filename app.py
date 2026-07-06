import streamlit as str
import pandas as pd
import sqlite3
import plotly.express as px

str.set_page_config(page_title="EduToWork Global Data Jobs", layout="wide")

str.title("EduToWork: Global Data Jobs For Sudanese Talent")
str.subheader("Empowering Sudanese Talent across Data Engineering, Analytics, Science & ML")

def load_data_from_db():
    conn = sqlite3.connect("edutowork_jobs.db")
    df = pd.read_sql_query("SELECT * FROM processed_jobs", conn)
    conn.close()
    return df

try:
    df = load_data_from_db()
    
    search_term = str.text_input("Search by role (e.g., Analyst, Engineer, Scientist) or company name:", "")
    
    if search_term:
        df = df[df['title'].str.contains(search_term, case=False, na=False) | 
                df['company'].str.contains(search_term, case=False, na=False)]
                
    total_jobs = len(df)
    total_companies = df['company'].nunique()
    
    col1, col2 = str.columns(2)
    with col1:
        str.metric(label="Available Remote Opportunities", value=total_jobs)
    with col2:
        str.metric(label="Global Companies Hiring", value=total_companies)
        
    str.markdown("---")
    
    if not df.empty:
        skill_columns = [col for col in df.columns if col.startswith('skill_')]
        skill_counts = df[skill_columns].sum().sort_values(ascending=False)
        
        skill_data = pd.DataFrame({
            'Skill': [col.replace('skill_', '').upper() for col in skill_counts.index],
            'Market Demand': skill_counts.values
        })
        
        fig = px.bar(
            skill_data, 
            x='Skill', 
            y='Market Demand', 
            title='Most Demanded Tech Skills Across Data Roles',
            labels={'Market Demand': 'Job Count', 'Skill': 'Technology'},
            color='Market Demand',
            color_continuous_scale='Viridis'
        )
        
        str.plotly_chart(fig, use_container_width=True)
    else:
        str.warning("No data jobs match your filter criteria.")
        
    str.markdown("---")
    str.subheader("Remote Job Board")
    
    if not df.empty:
        str.data_editor(
            df[['title', 'company', 'location', 'created', 'redirect_url']],
            column_config={
                "title": str.column_config.TextColumn("Job Title"),
                "company": str.column_config.TextColumn("Company"),
                "location": str.column_config.TextColumn("Job Location"),
                "created": str.column_config.TextColumn("Date Posted"),
                "redirect_url": str.column_config.LinkColumn(
                    "Application Link",
                    help="Click to open the application page",
                    display_text="Apply Now"
                )
            },
            disabled=True,
            use_container_width=True,
            hide_index=True
        )
    
except Exception as e:
    str.error(f"Could not load database. Make sure pipeline.py has run successfully. Error: {e}")