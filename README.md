# 프로젝트 소개
브랜드 지점별 컨설팅 대시보드 제작
  단, 대전 맥도날드 지점들에 한하여 프로젝트 진행
  
# 프로젝트 목적 
각 지점을 통해 브랜드가 얼마나 건강한지 평가하고 현재 고객들이 브랜드에 대해서 느끼는 강점과 약점을 파악하여 브랜드 컨설팅 플랫폼 구축

# 실험설계
1. 데이터수집
   - 크롤링
   - 공공데이터포털
   - 레인포털
2. 감성분석
   -  GRU 모델 학습
   -  긍정/부정 라벨 생성
   -  긍정/부정 라벨을 통한 gauge chart 생성
   -  긍정/부정 라벨을 통한 wordcloud 생성
3. 입지분석
   - 데이터전처리
   - 모델 학습을 통한 입지분석
4. 대시보드 제작
   - streamlit을 통한 웹페이지 제작
