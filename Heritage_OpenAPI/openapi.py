import requests
import xml.etree.ElementTree as ET
import pandas as pd
import os

# 목록 조회 API URL
list_url = "https://www.cha.go.kr/cha/SearchKindOpenapiList.do"

# 상세 조회 API URL
detail_url = "https://www.cha.go.kr/cha/SearchKindOpenapiDt.do"

# 페이지 단위 설정
page_unit = 5000

# 전체 국가유산 목록을 저장할 리스트
all_heritage_list = []

# 페이지 인덱스 설정
page_index = 1

# 전체 데이터를 순차적으로 가져오기 위한 루프
while True:
    list_params = {
        'ccbaKdcd': '',   # 필수 파라미터로 종목코드 지정
        'pageUnit': page_unit,
        'pageIndex': page_index
    }

    response = requests.get(list_url, params=list_params)

    if response.status_code != 200:
        print(f"API 호출 실패: 상태 코드 {response.status_code}")
        print(f"응답 내용: {response.text}")
        break

    try:
        root = ET.fromstring(response.content)
    except ET.ParseError as e:
        print(f"XML 파싱 실패: {e}")
        break

    items = root.findall('.//item')

    if not items:
        print("더 이상 데이터가 없습니다.")
        break

    for item in items:
        heritage = {
            'ccbaAsno': item.findtext('ccbaAsno', ''),
            'ccbaKdcd': item.findtext('ccbaKdcd', ''),
            'ccbaCtcd': item.findtext('ccbaCtcd', ''),
            'ccbaCpno': item.findtext('ccbaCpno', ''),
            'ccbaMnm1': item.findtext('ccbaMnm1', ''),
            'ccbaMnm2': item.findtext('ccbaMnm2', ''),
            'ccmaName': item.findtext('ccmaName', ''),
            'ccbaCtcdNm': item.findtext('ccbaCtcdNm', ''),
            'ccsiName': item.findtext('ccsiName', '')
        }
        all_heritage_list.append(heritage)

    page_index += 1
    print(f"{len(all_heritage_list)} 건 처리 중...")

# 목록 DataFrame 생성
columns = ['ccbaAsno', 'ccbaKdcd', 'ccbaCtcd', 'ccbaCpno', 'ccbaMnm1', 'ccbaMnm2', 'ccmaName', 'ccbaCtcdNm', 'ccsiName']

# 빈 필드를 추가해 중복 방지
additional_columns = ['ccceName', 'imageUrl', 'content', 'ccbaLcad']
df_list = pd.DataFrame(all_heritage_list, columns=columns)

# 추가 컬럼을 빈 값으로 미리 생성해 중복 방지
for col in additional_columns:
    df_list[col] = ""

# 상세 조회 데이터를 바로바로 병합하는 방식
def fetch_and_merge_detail_data(df, row):
    detail_params = {
        'ccbaKdcd': row['ccbaKdcd'],
        'ccbaAsno': row['ccbaAsno'],
        'ccbaCtcd': row['ccbaCtcd']
    }

    try:
        detail_response = requests.get(detail_url, params=detail_params, timeout=5)

        if detail_response.status_code != 200:
            print(f"상세 조회 실패: 상태 코드 {detail_response.status_code}, 국가유산연계번호: {row['ccbaCpno']}")
            return df

        detail_root = ET.fromstring(detail_response.content)
        detail_item = detail_root.find('.//item')

        # 상세 데이터 추출
        detail_data = {
            'ccbaCpno': row['ccbaCpno'],
            'ccceName': detail_item.findtext('ccceName', ''),
            'imageUrl': detail_item.findtext('imageUrl', ''),
            'content': detail_item.findtext('content', ''),
            'ccbaLcad': detail_item.findtext('ccbaLcad', '')
        }

        # DataFrame으로 변환 후 병합 (중복 컬럼 덮어쓰기)
        df.loc[df['ccbaCpno'] == row['ccbaCpno'], ['ccceName', 'imageUrl', 'content', 'ccbaLcad']] = \
            [detail_data['ccceName'], detail_data['imageUrl'], detail_data['content'], detail_data['ccbaLcad']]

        return df

    except requests.exceptions.Timeout:
        print(f"상세 조회 타임아웃: 국가유산연계번호: {row['ccbaCpno']}")
        return df
    except Exception as e:
        print(f"상세 조회 실패: {e}, 국가유산연계번호: {row['ccbaCpno']}")
        return df

# 목록의 각 항목에 대해 상세 정보를 바로 병합, 100개 단위로 진행 상황 출력 및 저장
output_file = 'national_heritage_full_data.csv'
batch_size = 100  # 100개 단위로 저장

if os.path.exists(output_file):
    os.remove(output_file)  # 기존 파일이 있으면 삭제

for index, row in df_list.iterrows():
    df_list = fetch_and_merge_detail_data(df_list, row)

    # 100개 단위로 CSV 파일에 저장
    if (index + 1) % batch_size == 0:
        df_list.iloc[index - batch_size + 1:index + 1].to_csv(output_file, mode='a', index=False, header=(index == 99))
        print(f"{index + 1}개 데이터가 {output_file}에 저장되었습니다.")

# 병합 후 DataFrame 확인
print(f"최종 병합된 df_list 크기: {df_list.shape}")
print(df_list.head())

# 남은 데이터를 저장
df_list.iloc[(index // batch_size) * batch_size:].to_csv(output_file, mode='a', index=False, header=False)
print(f"총 {len(df_list)} 건의 데이터를 성공적으로 {output_file} 파일로 저장했습니다.")