import requests

def face_detect(image):
    url = 'https://api-us.faceplusplus.com/facepp/v3/detect'
    payload = {'api_key':'kKY41H3UqheoMahxmeFH1Ch6Eka1ICKR', 'api_secret':'5cMkrEIeuQUQEpaJ9IQF1nTjOn9SEctS',\
             'image_base64': image, 'return_attributes': 'gender,age,ethnicity,beauty'}

    try:
        r = requests.post(url, data=payload)
        r = r.json()
        face_list = []

        for face in r["faces"]:
            faces = {}
            if "attributes" in face:
                faces["gender"] = face["attributes"]["gender"]["value"]
                faces["age"] = face["attributes"]["age"]["value"]

                if faces["gender"] == "Male":
                    faces["beauty"] = face["attributes"]["beauty"]["male_score"]
                    faces["gender"] = "男性"
                else:
                    faces["beauty"] = face["attributes"]["beauty"]["female_score"]
                    faces["gender"] = "女性"
                faces["x_axis"] = face["face_rectangle"]["left"]  # 並び替え用に画像上の顔のX座標の位置を代入
                face_list.append(faces)
        face_list = sorted(face_list, key=lambda x: x["x_axis"])  # 左から順に並び変える

        # LineBot出力処理
        msg = ""
        for i, f in enumerate(face_list, 1):
            msg += "{}人目の情報\n".format(i)
            msg += "X軸の位置:{}\n".format(f["x_axis"])
            msg += "性別: {}\n".format(f["gender"])
            msg += "年齢: {}歳\n".format(f["age"])
            msg += "偏差値: {}\n\n".format(int(f['beauty']))
        msg = msg.rstrip()
        if not msg:
            msg = "画像から顔データを検出できませんでした。"
        return msg
    except:
        return "サーバーの接続に失敗したか画像を正しく認識できませんでした。"