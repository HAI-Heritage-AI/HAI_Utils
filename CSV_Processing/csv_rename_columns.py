import pandas as pd

# CSV 파일 불러오기
file_path = 'national_heritage_full_data.csv'  # 파일 경로를 실제 파일 경로로 설정
heritage_data = pd.read_csv(file_path)

# 컬럼 이름 변경을 위한 매핑 딕셔너리
column_mapping = {
    'ccbaAsno': '관리번호(ccbaAsno)',
    'ccbaKdcd': '중목코드(ccbaKdcd)',
    'ccbaCtcd': '시도코드(ccbaCtcd)',
    'ccbaCpno': '국가유산연계번호(ccbaCpno)',
    'ccbaMnm1': '국가유산명_국문(ccbaMnm1)',
    'ccbaMnm2': '국가유산명_한자(ccbaMnm2)',
    'ccmaName': '국가유산종목(ccmaName)',
    'ccbaCtcdNm': '시도명(ccbaCtcdNm)',
    'ccsiName': '시군구명(ccsiName)',
    'ccceName': '시대(ccceName)',
    'imageUrl': '메인이미지URL(imageUrl)',
    'content': '내용(content)',
    'ccbaLcad': '소재지상세(ccbaLcad)'
}

# 컬럼 이름 변경
heritage_data.rename(columns=column_mapping, inplace=True)

# 변경된 데이터 확인
print(heritage_data.head())

# 변경된 데이터 저장
heritage_data.to_csv('updated_national_heritage_full_data.csv', index=False)  # 변경된 데이터 저장 경로 설정
