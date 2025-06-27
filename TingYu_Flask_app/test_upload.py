import requests

url = 'http://localhost:5000/api/upload'
file_path = 'd:/PROJECT/TingYu/TingYu_Flask_app/test_file.txt'  # 使用项目目录下的测试文件

try:
    with open(file_path, 'rb') as f:
        files = {'file': f}
        response = requests.post(url, files=files)
    print('Status Code:', response.status_code)
    print('Response Body:', response.text)
except FileNotFoundError:
    print(f"文件 {file_path} 未找到，请检查路径是否正确。")