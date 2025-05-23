import os
from datetime import datetime

def save_all_code_to_txt(project_dir, output_dir):
    """
    프로젝트 디렉토리 내 모든 Python 파일 코드를 프로젝트명과 날짜 및 시간을 포함한 txt 파일로 저장합니다.
    
    :param project_dir: 프로젝트의 최상위 디렉토리 경로
    :param output_dir: 저장할 디렉토리 경로
    """
    try:
        # 프로젝트 디렉토리명 추출 및 날짜+시간 추가
        project_name = os.path.basename(os.path.normpath(project_dir))
        current_datetime = datetime.now().strftime('%Y%m%d_%H%M%S')  # 날짜+시간
        output_file = os.path.join(output_dir, f"{project_name}_{current_datetime}.txt")
        
        # 출력 디렉토리 생성
        os.makedirs(output_dir, exist_ok=True)
        
        with open(output_file, 'w', encoding='utf-8') as outfile:
            for root, dirs, files in os.walk(project_dir):
                for file in files:
                    if file.endswith('.py'):  # Python 파일만 처리
                        file_path = os.path.join(root, file)
                        with open(file_path, 'r', encoding='utf-8') as infile:
                            code = infile.read()
                            # 파일명과 경로 추가
                            outfile.write(f"### {file_path} ###\n")
                            outfile.write(code)
                            outfile.write("\n\n")  # 파일 간 간격
        print(f"모든 Python 파일 코드를 {output_file}에 저장했습니다.")
    except Exception as e:
        print(f"오류 발생: {e}")

# 프로젝트 디렉토리와 출력 디렉토리 설정
project_directory = r"C:\repository\HAI_Python"  # 프로젝트 디렉토리 경로
output_directory = r"C:\repository\HAI_Utils\Gathering_Code"  # 결과 저장 디렉토리 경로

# 함수 실행
save_all_code_to_txt(project_directory, output_directory)
