
from flask import Flask, request, jsonify
import mmap
import os

app = Flask(__name__)

def search_in_files(folder_path, search_string):
    isFound = False
    for root,dirs,files in os.walk(folder_path):
        for file in files:
            if file.endswith(".txt"):
                file_path = os.path.join(root, file)
                with open(file_path, "r", encoding="utf-8") as f:
                    mm = mmap.mmap(f.fileno(), 0, access=mmap.ACCESS_READ)
                    for line in iter(mm.readline, b''):
                        if  search_string.encode('utf-8') in line:
                            res=line.decode('utf-8')
                            values = res.strip().split(",")
                            document = {
                                "id": values[0].strip('"'),
                                "phone_number": values[3].strip('"'),
                                "name": values[6].strip('"'),
                                "facebook_url": values[9].strip('"'),
                            }
                            isFound = True
                            return jsonify({"data":document})
                            
                            
                if isFound:
                    break

    if not isFound:
        return None
    


@app.route('/', methods=['GET'])
def home():
    return jsonify({"dev": "@usfnassar","itsWork":False,"msg":"https://t.me/datahunter0/24"})
@app.route('/s', methods=['GET'])
def search_api_id():
    folder_path = r"usf"
    search_string = request.args.get('key')

    if  not search_string:
        return jsonify({"error": "you should give the id or phone number are required."}), 400

    result = search_in_files(folder_path, search_string)

    if result:
        return result
    else:
        return jsonify({"message": "NOT FOUND"}),404
    


if __name__ == '__main__':
    app.run(debug=True)
