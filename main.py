from obfuscate_op import obfuscate_Op
from obfuscate_extract import JavaControlFlowExtractor

def main():
    java_code = """
    
if((a+b == 34) && (!a-b == -6 )){
}

"""
    expressions = JavaControlFlowExtractor(java_code).extract_all_conditions()
    ob_op = obfuscate_Op()

    for i in range(len(expressions)):
        obfuscated = ob_op.obfuscate_expression(expressions[i])
        #replace(cond,obfuscated) 
        print(expressions[i])
        print(obfuscated)
    
    



if __name__ == "__main__":
    main()