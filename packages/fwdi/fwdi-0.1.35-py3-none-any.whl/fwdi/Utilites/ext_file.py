import os

class ExtFile():
    
    @staticmethod
    def save_file(full_path_file:str, data_bytes:bytes) -> bool:
        try:
            with open(full_path_file, 'wb') as f:
                f.write(data_bytes)
            return True
        except Exception as ex:
            return False

    @staticmethod
    def exists(file_path:str)->bool:
        return os.path.exists(file_path)

    @staticmethod
    def delete(file_path:str)->bool:
        try:
            if ExtFile.exists(file_path):
                os.remove(file_path)
                return True
            
            return False
        except Exception as ex:
            print(ex)
            return False
    
    @staticmethod
    def write(full_path_file:str, datas:list) -> bool:
        try:
            with open(full_path_file, 'w') as f:
                for item in datas:
                    f.write(f'"{item}",\n')
                
            return True
        except Exception as ex:
            return False
