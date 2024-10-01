import javalang
import os
import re
import random
import string
import secrets
import json
from typing import List, Dict
'''
0.json파일 읽기
1.file_path로 파일읽기
2.method_name을 찾아서 수정할 부분 찾기
3.source_code내 body부분 식별 및 각 구문 구분하기(찾기)
4.body부분 수정(함수호출 형식)
5.각 요소에 맞게 각 new_method 삽입
6.저장
-------식별-------
defult값 -> body 전체 함수분할
if, for, while, swhich -> 변수가 있는 부분만 한줄씩 함수분할
try-catch -> try의 body부분만 함수분할
-------삽입-------
기존 메서드의 끝부분에서('}') +\n 후 만들어진 new_method 삽입
new_method의 이름은 랜덤으로 삽입
가져와야할 소스 -> 파라미터
----new_method----
1. 전체 함수 분할
2. 각 구문에 맞게 분할
3. 분할시 필요한 파라미터 가져오기
'''

def read_and_process_json(file_path: str) -> List[Dict[str, str]]:
    result = []
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
        
        for item in data:
            for tainted_item in item.get('tainted', []):
                processed_item = {
                    'file_path': tainted_item.get('file_path', 'No file path provided'),
                    'method_name': tainted_item.get('method_name', 'No method name provided'),
                    'source_code': tainted_item.get('source_code', 'No source code provided')
                }
                result.append(processed_item)

    except FileNotFoundError:
        print(f"파일을 찾을 수 없습니다: {file_path}")
    except json.JSONDecodeError:
        print(f"유효하지 않은 JSON 파일입니다: {file_path}")
    except Exception as e:
        print(f"파일을 읽는 중 오류가 발생했습니다: {str(e)}")
    
    return result

def main():
    json_file_path = 'analysis_result.json'
    processed_data = read_and_process_json(json_file_path)

    if processed_data:
        for item in processed_data:
            print(f"File Path: {item['file_path']}")
            print(f"Method Name: {item['method_name']}")
            print(f"Source Code:\n{item['source_code']}")
            print("-" * 50)  # 구분선 출력
    else:
        print("처리된 데이터가 없습니다.")

if __name__ == "__main__":
    main()