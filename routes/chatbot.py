from flask import Blueprint, request, jsonify, session
from services.chatbot_data import get_biblical_response, get_app_help_response
from services.openai_client import get_openai_response

chatbot_bp = Blueprint('chatbot', __name__)

def login_required_api(f):
    def wrapper(*args, **kwargs):
        if 'user_id' not in session:
            return jsonify({'error': 'Authentification requise'}), 401
        return f(*args, **kwargs)
    wrapper.__name__ = f.__name__
    return wrapper

@chatbot_bp.route('/ask', methods=['POST'])
@login_required_api
def ask_kadosh():
    data = request.get_json()
    question = data.get('question', '').strip()
    
    if not question:
        return jsonify({'error': 'Question vide'}), 400
    
    # First, try to find a pre-loaded response
    biblical_response = get_biblical_response(question)
    if biblical_response:
        return jsonify({
            'response': biblical_response,
            'source': 'pre-loaded'
        })
    
    # Check for app help questions
    app_response = get_app_help_response(question)
    if app_response:
        return jsonify({
            'response': app_response,
            'source': 'app-help'
        })
    
    # If no pre-loaded response, use OpenAI
    try:
        openai_response = get_openai_response(question)
        return jsonify({
            'response': openai_response,
            'source': 'openai'
        })
    except Exception as e:
        return jsonify({
            'response': "Je suis désolé, je ne peux pas répondre à cette question pour le moment. Veuillez réessayer plus tard.",
            'error': str(e)
        }), 500

@chatbot_bp.route('/topics', methods=['GET'])
@login_required_api
def get_topics():
    from services.chatbot_data import BIBLICAL_TOPICS
    topics = list(BIBLICAL_TOPICS.keys())
    return jsonify({'topics': topics})

@chatbot_bp.route('/topic/<topic_name>', methods=['GET'])
@login_required_api
def get_topic_response(topic_name):
    from services.chatbot_data import BIBLICAL_TOPICS
    
    if topic_name in BIBLICAL_TOPICS:
        return jsonify({
            'response': BIBLICAL_TOPICS[topic_name],
            'topic': topic_name
        })
    else:
        return jsonify({'error': 'Sujet non trouvé'}), 404
