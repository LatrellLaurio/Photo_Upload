from flask import Flask, request, render_template, url_for, json, redirect

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('upload.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    image = request.files['image']
    image.save('uploads/' + image.filename)
    return 'Image uploaded successfully'

@app.route('/friends_list', methods=["GET"])
def friends_list():
    status = {}
    with open('friends_list.json') as f:
        data = json.load(f)
    for names in data:
        from_member = "@laurio"
        to_member = names
        social_graph = data

        if from_member in social_graph[to_member]["following"] and to_member in social_graph[from_member]["following"]:
            answer = "friends"
        elif from_member in social_graph[to_member]["following"]:
            answer = "You are being followed by"
        elif to_member in social_graph[from_member]["following"]:
            answer = "You are now following them"
        else:
            answer = "no relationship"
        status[names] = answer
    return render_template('add_friend.html', data=data, status=status)

@app.route('/add_friend', methods=["POST"])
def add_friend():
    if request.method == "POST":
        with open('friends_list.json') as f:
            data = json.load(f)
        req = request.form
        person_to_add = req.get("Person")
        data["@laurio"]["following"].append(person_to_add)
        with open('friends_list.json', 'w') as f:
            json.dump(data, f)
    return redirect('/friends_list')

@app.route('/remove_friend', methods=["POST"])
def remove_friend():
    if request.method == "POST":
        with open('friends_list.json') as f:
            data = json.load(f)
        req = request.form
        person_to_add = req.get("Person")
        data["@laurio"]["following"].remove(person_to_add)
        with open('friends_list.json', 'w') as f:
            json.dump(data, f)
    return redirect('/friends_list')

if __name__ == '__main__':
    app.run(debug=True)
