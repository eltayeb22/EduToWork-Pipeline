import requests
import pandas as pd
import re
import sqlite3
import json

APP_ID = "5aba56e7"      
APP_KEY = "e1f26fcd8c2dd9feb2aa9d9b98c90d68"    
COUNTRY = "us"  

def run_data_engineering_pipeline():
    data_roles = ["Data Engineer", "Data Analyst", "Data Product Manager", "Data Integration Specialist", "Data Mining Specialist", "Data Warehouse Developer", 'ai engineer', 'data scientist', 'machine learning engineer', 'business intelligence analyst', 'data architect', 'big data engineer']
    all_jobs = []
    
    print("1. Starting Data Ingestion for All Data Roles (Remote)...")
    
    for role in data_roles:
        search_query = f"{role} remote"
        url = f"https://api.adzuna.com/v1/api/jobs/{COUNTRY}/search/1?app_id={APP_ID}&app_key={APP_KEY}&results_per_page=15&what={search_query}&content-type=application/json"
        
        try:
            response = requests.get(url)
            if response.status_code == 200:
                raw_data = response.json()
                jobs_list = raw_data.get('results', [])
                all_jobs.extend(jobs_list)
                print(f"-> Successfully fetched {len(jobs_list)} jobs for role: {role}")
            else:
                print(f"-> Failed to fetch jobs for role: {role}. Status: {response.status_code}")
        except Exception as e:
            print(f"-> Error fetching jobs for role {role}: {e}")
            
    if not all_jobs:
        print("No jobs found for any data roles.")
        return None
        
    print(f"Total raw jobs collected: {len(all_jobs)}")
    
    print("2. Starting Data Transformation and Location Extraction...")
    df = pd.DataFrame(all_jobs)
    
    df = df.drop_duplicates(subset=['id'])
    
    if 'company' in df.columns:
        df['company'] = df['company'].apply(lambda x: x.get('display_name') if isinstance(x, dict) else (x if pd.notna(x) else 'Unknown'))
    else:
        df['company'] = 'Unknown'
        
    if 'location' in df.columns:
        df['location'] = df['location'].apply(lambda x: ", ".join(x.get('area', [])) if isinstance(x, dict) else 'Global/Remote')
    else:
        df['location'] = 'Global/Remote'
        
    columns_to_keep = ['id', 'title', 'description', 'created', 'company', 'location', 'redirect_url']
    df = df[columns_to_keep]
    
    df['clean_description'] = df['description'].str.lower()
    
    skills_to_track = ['python', 'sql', 'etl', 'pandas', 'numpy', 'aws', 'spark', 'tableau', 'powerbi', 'machine learning', 'scikit-learn', 'r']
    
    for skill in skills_to_track:
        pattern = r'\b' + re.escape(skill) + r'\b'
        df[f'skill_{skill}'] = df['clean_description'].apply(
            lambda x: 1 if re.search(pattern, str(x)) else 0
        )
        
    df = df.drop(columns=['clean_description'])
    print("Data transformation completed successfully.")
    return df

def store_jobs_in_db(df, db_name="edutowork_jobs.db"):
    if df is None or df.empty:
        print("No valid data available for storage.")
        return
        
    print(f"3. Starting Data Storage into local database ({db_name})...")
    try:
        conn = sqlite3.connect(db_name)
        df.to_sql('processed_jobs', conn, if_exists='replace', index=False)
        conn.close()
        print("Success! Database has been updated with location data.")
    except Exception as e:
        print(f"Error occurred during database storage: {e}")

if __name__ == "__main__":
    final_dataset = run_data_engineering_pipeline()
    store_jobs_in_db(final_dataset)