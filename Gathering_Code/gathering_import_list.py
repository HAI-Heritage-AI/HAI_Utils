import os
import re

def extract_imports_from_project(project_dir, output_file):
    """
    프로젝트 내 모든 Python 파일에서 from/import 문을 추출하여 저장합니다.
    
    :param project_dir: 프로젝트 디렉토리 경로
    :param output_file: 저장할 파일 경로
    """
    try:
        import_statements = []
        for root, dirs, files in os.walk(project_dir):
            for file in files:
                if file.endswith('.py'):  # Python 파일만 처리
                    file_path = os.path.join(root, file)
                    with open(file_path, 'r', encoding='utf-8') as infile:
                        for line in infile:
                            # from/import 문인지 확인
                            if line.strip().startswith(('from ', 'import ')):
                                import_statements.append(line.strip())
        
        # 중복 제거 및 정렬
        unique_imports = sorted(set(import_statements))
        
        # 결과 저장
        os.makedirs(os.path.dirname(output_file), exist_ok=True)
        with open(output_file, 'w', encoding='utf-8') as outfile:
            outfile.write("\n".join(unique_imports))
        
        print(f"모든 from/import 문을 {output_file}에 저장했습니다.")
    except Exception as e:
        print(f"오류 발생: {e}")

# 프로젝트 디렉토리와 출력 파일 설정
project_directory = r"C:\repository\HAI_Python"  # 프로젝트 디렉토리 경로
output_txt_file = r"C:\repository\HAI_Utils\Gathering_Code\imports_list.txt"  # 결과 저장 파일 경로

# 함수 실행
extract_imports_from_project(project_directory, output_txt_file)
