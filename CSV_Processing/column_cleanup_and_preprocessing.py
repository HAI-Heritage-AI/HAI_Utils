import pandas as pd
import re

# CSV 파일 불러오기
file_path = 'updated_national_heritage_full_data.csv'  # 파일 경로를 실제 파일 경로로 설정
heritage_data = pd.read_csv(file_path)

# 변경전 데이터 확인
print("변경전")
print(heritage_data.head())

# '소재지상세' 컬럼의 전처리: 불필요한 개행 문자와 탭 문자 제거
heritage_data['소재지상세(ccbaLcad)'] = heritage_data['소재지상세(ccbaLcad)'].apply(lambda x: re.sub(r'\s+', ' ', str(x)).strip())

# 변경된 데이터 확인
print("변경후")
print(heritage_data.head())

# 변경된 데이터 저장
heritage_data.to_csv('updated01_national_heritage_full_data.csv', index=False)  # 변경된 데이터 저장 경로 설정
