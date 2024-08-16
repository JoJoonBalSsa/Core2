from obfuscate_op import obfuscate_Op
from obfuscate_extract import JavaControlFlowExtractor

def main():
    java_code = """
for(int i = 0 ;i<50;i++){
}
"""
    expressions = JavaControlFlowExtractor(java_code).extract_all_conditions()
    ob_op = obfuscate_Op()

    for key, value in expressions.items():
        if value:  # 값이 비어있지 않은 경우만 처리
            for cond in value:
                    obfuscated = ob_op.obfuscate_expression(cond)
                    #replace(cond,obfuscated) 
                    print(obfuscated)
    
    



if __name__ == "__main__":
    main()