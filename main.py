from flask import Flask, request, jsonify
from rasa_nlu.model import Interpreter


# create interpreter to get the intent of rasa
print("[INFO] Loading RASA Model...")
interpreter = Interpreter.load("models/nlu_model/nlu/")
app = Flask(__name__)   


@app.route('/status', methods=['GET']) 
def status():
    return '<h2>Flask-RASA Server is Running...</h2>'


@app.route('/get_question_number', methods=['POST'])
def get_question_number():
    question_number = None
    confidence = 0.0

    try:
        print("[INFO] Getting response from RASA Interpreter") 
        rasa_response = interpreter.parse(request.json['question'])
        intent_name = rasa_response['intent']['name']
        question_number = rasa_response['intent']['name'].split("_")[2]
        confidence = rasa_response['intent']['confidence']

        if confidence > .85:
            print("[INFO] Detected Question Successfully")
            print(f"[INFO] Intent:{intent_name} | Confidence:{confidence}") 
            return jsonify({"status": "success",
                            "reason": "Question matched!",
                            "question_number": question_number,
                            "confidence": confidence,
                            "question": request.json['question']})
        print(f"[DEBUG] Detection with less confidence!")
        print(f"[DEBUG] Intent:{intent_name} | Confidence:{confidence}") 
        return jsonify({"status": "little success",
                        "reason": "question matched but with low confidence",
                        "question_number": question_number,
                        "confidence": confidence,
                        "question": request.json['question']})
    except Exception as e:
        print(f"[ERROR] {e}")
        return jsonify({"status": "failure",
                        "reason": str(e),
                        "question_number": question_number,
                        "confidence": confidence,
                        "question": request.json['question']})


if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=8001)
