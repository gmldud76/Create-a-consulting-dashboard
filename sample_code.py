import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import folium
from folium.plugins import MarkerCluster
from shapely.wkt import loads
import geopandas as gpd
from streamlit_folium import folium_static

# Load Excel data for Review
excel_file_path_review = "D:/Capstone_Design/data/McDonald's_Review_Crawling_data.xlsx"
excel_data_review = pd.read_excel(excel_file_path_review, sheet_name=None)
Review = {}

# Create dataframes for each sheet
for sheet_name, sheet_data in excel_data_review.items():
    Review[sheet_name] = sheet_data
    # 이상값 제거 202년 1월
    if sheet_name == '센트럴DT점':
        Review[sheet_name].drop([1380], axis=0, inplace=True)

# Load Excel data for Better_Review
excel_file_path_better = "D:/Capstone_Design/data/McDonald's_Better_Review_Crawling_data.xlsx"
excel_data_better = pd.read_excel(excel_file_path_better, sheet_name=None)
Better_Review = {}

# Load GeoData
GEO_DATA = pd.read_csv("D:/Capstone_Design/data/GEO_DATA.csv")

# Load McDonald's location data
aa = pd.read_csv("D:/Capstone_Design/data/좌표_동일업체 (1).csv")

# '동일업체' 열이 1이 아닌 상위 4개의 지리 정보를 추출
top_4_geometries = GEO_DATA[GEO_DATA['동일업체'] != 1].head(4)

# 지리 정보의 문자열 표현을 실제 지리 객체로 변환
top_4_geometries['geometry'] = top_4_geometries['geometry'].apply(loads)

# 지리 정보를 담은 GeoDataFrame을 생성
top_4_gdf = gpd.GeoDataFrame(top_4_geometries, geometry='geometry')

# Folium 지도 생성
mymap = folium.Map(location=[36.3504119, 127.3845475], zoom_start=13)

# 지리 정보를 Folium 지도에 추가
for idx, row in top_4_gdf.iterrows():
    folium.GeoJson(row['geometry']).add_to(mymap)

# 데이터에 대한 MarkerCluster를 생성
marker_cluster_aa = MarkerCluster().add_to(mymap)

# 지점에 대한 마커를 추가
for idx, row in aa.iterrows():
    folium.Marker([row['위도'], row['경도']], popup=row['Name']).add_to(marker_cluster_aa)

# Streamlit 앱
st.title("McDonald's Dashboard")

# Folium 지도를 Streamlit 앱에 표시
folium_static(mymap)

# Dropdown 메뉴로 McDonald's 지점 선택
selected_branch = st.selectbox('Select McDonald`s branch:', list(Review.keys()))

# Create dataframes for each sheet
for sheet_name, sheet_data in excel_data_better.items():
    Better_Review[sheet_name] = sheet_data
    if 'count' in Better_Review[sheet_name].columns:
        Better_Review[sheet_name]['count'] = Better_Review[sheet_name]['count'].str.replace('이 키워드를 선택한 인원', '').astype(int)


# Process date column if applicable for Review data
if 'date' in Review[selected_branch].columns:
    Review[selected_branch]['date'] = Review[selected_branch]['date'].str[:-7]
    Review[selected_branch]['date'] = Review[selected_branch]['date'].str.strip()
    Review[selected_branch]['date'] = pd.to_datetime(Review[selected_branch]['date'], format='%Y년 %m월')
    Review[selected_branch]['YearMonth'] = Review[selected_branch]['date'].dt.to_period('M')

# Count data per YearMonth for Review data
counts_review = Review[selected_branch]['YearMonth'].value_counts().sort_index()

# Plot the data using Plotly for Review data
fig_review = px.line(x=counts_review.index.astype(str), y=counts_review.values, markers=True,
                  title=f'년월별 데이터 개수 - {selected_branch}', labels={'x': '년월', 'y': '데이터 개수'})
fig_review.update_xaxes(type='category')  # x축을 카테고리 형태로 표시

# Display line chart for Review data
st.plotly_chart(fig_review)

if 'count' in Better_Review[selected_branch].columns:
    # Get the top 8 reasons
    top_8_reasons = Better_Review[selected_branch].nlargest(8, 'count')

    # Extract categories and values
    categories_better = top_8_reasons['better']
    values_better = top_8_reasons['count']

    # Plot radar chart for Better_Review data
    fig_better = go.Figure()

    fig_better.add_trace(go.Scatterpolar(
        r=values_better.tolist() + values_better.tolist()[:1],
        theta=categories_better.tolist() + categories_better.tolist()[:1],
        fill='toself',
        name=f'Top 8 Reasons - {selected_branch}'
    ))

    fig_better.update_layout(
        polar=dict(
            radialaxis=dict(visible=True),
        ),
        showlegend=True,
        title=f"Top 8 Reasons Why People Like {selected_branch}",
    )

    # Display radar chart for Better_Review data
    st.plotly_chart(fig_better)
