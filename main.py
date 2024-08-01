from search_str import searchString
from encrypt_str import encryptString
from insert_str import insertStr
def main(java_folder_path, output_folder):
    search_str = searchString(java_folder_path)
    random_classes = search_str.random_class(search_str.class_names)

    encrypt_str = encryptString(search_str.Literals)

    insert_str = insertStr(search_str.Literals,encrypt_str.encrypted_Literals,random_classes,java_folder_path)

    

if __name__ == "__main__":

    #java_folder_path = '/home/namaek_2/java-christmas-6-scienceNH'
    java_folder_path = './test/christmas'  
    main(java_folder_path, java_folder_path)