from flask import Blueprint, request, jsonify, session
from services.chatbot_data import get_biblical_response, get_app_help_response, get_greeting_response
from services.openai_client import get_openai_response
from services.chatbot_training import get_training_report, evaluate_chatbot_performance
from services.translation_service import translation_service
import logging

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
    
    # Log user interaction
    user_id = session.get('user_id')
    logging.info(f"User {user_id} asked: {question}")
    
    # Get user's language preference
    user_language = translation_service.get_current_language()
    
    # First, check for greetings (enhanced interactivity)
    greeting_response = get_greeting_response(question, user_language)
    if greeting_response:
        return jsonify({
            'response': greeting_response,
            'source': 'greeting',
            'interactive': True,
            'followup_questions': get_followup_questions(question),
            'services_offered': get_services_offered()
        })
    
    # Try to find biblical response (includes greetings now)
    biblical_response = get_biblical_response(question)
    if biblical_response:
        return jsonify({
            'response': biblical_response,
            'source': 'biblical_knowledge',
            'interactive': True,
            'related_topics': get_related_topics(question),
            'followup_questions': get_spiritual_followup_questions(question)
        })
    
    # Check for app help questions
    app_response = get_app_help_response(question)
    if app_response:
        return jsonify({
            'response': app_response,
            'source': 'app-help',
            'interactive': True,
            'help_categories': get_help_categories()
        })
    
    # If no pre-loaded response, use OpenAI with enhanced context
    try:
        enhanced_question = enhance_question_with_context(question)
        openai_response = get_openai_response(enhanced_question, user_language)
        return jsonify({
            'response': openai_response,
            'source': 'openai',
            'interactive': True,
            'suggested_topics': get_suggested_topics(question)
        })
    except Exception as e:
        logging.error(f"OpenAI error: {str(e)}")
        fallback_response = get_intelligent_fallback_response(question)
        return jsonify({
            'response': fallback_response,
            'source': 'fallback',
            'interactive': True,
            'suggested_actions': get_suggested_actions(),
            'error': str(e)
        }), 200

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
        topic_data = BIBLICAL_TOPICS[topic_name]
        
        # Format the response properly
        formatted_response = f"## {topic_name.title()}\n\n"
        
        # Add verses
        formatted_response += "### Versets bibliques:\n"
        for verse in topic_data['versets']:
            formatted_response += f"**{verse['reference']}**: {verse['text']}\n\n"
        
        # Add interpretations
        formatted_response += "### Interprétations:\n"
        for interpretation in topic_data['interpretations']:
            formatted_response += f"• {interpretation}\n\n"
        
        return jsonify({
            'response': formatted_response,
            'topic': topic_name
        })
    else:
        return jsonify({'error': 'Sujet non trouvé'}), 404

@chatbot_bp.route('/training-report', methods=['GET'])
@login_required_api
def get_chatbot_training_report():
    """Get comprehensive training performance report"""
    try:
        report = get_training_report()
        return jsonify({
            'report': report,
            'timestamp': '2025-07-17'
        })
    except Exception as e:
        logging.error(f"Erreur rapport: {str(e)}")
        return jsonify({'error': 'Erreur du serveur'}), 500

@chatbot_bp.route('/performance', methods=['GET'])
@login_required_api
def get_chatbot_performance():
    """Get current chatbot performance metrics"""
    try:
        performance = evaluate_chatbot_performance()
        return jsonify(performance)
    except Exception as e:
        logging.error(f"Erreur performance: {str(e)}")
        return jsonify({'error': 'Erreur du serveur'}), 500

# Helper functions for enhanced interactivity
def get_followup_questions(question):
    """Generate contextual follow-up questions"""
    question_lower = question.lower()
    
    if any(greeting in question_lower for greeting in ['bonjour', 'salut', 'hello']):
        return [
            "Avez-vous une question biblique particulière ?",
            "Souhaitez-vous explorer un sujet spirituel ?",
            "Comment va votre marche avec Dieu ?"
        ]
    elif any(word in question_lower for word in ['comment', 'ça va', 'allez-vous']):
        return [
            "Comment va votre relation avec Dieu ?",
            "Y a-t-il quelque chose pour lequel vous aimeriez que je prie ?",
            "Avez-vous des préoccupations spirituelles ?"
        ]
    else:
        return [
            "Avez-vous d'autres questions ?",
            "Souhaitez-vous approfondir ce sujet ?",
            "Puis-je vous aider avec autre chose ?"
        ]

def get_services_offered():
    """Get list of services offered by Kadosh.ia"""
    return [
        "📖 Questions bibliques avec versets et interprétations",
        "🌟 Plus de 75 sujets spirituels à explorer",
        "💬 Conseils pratiques pour la vie chrétienne",
        "🔧 Support technique pour l'application BENJ INSIDE",
        "🙏 Prière et encouragement spirituel",
        "📚 Guidance biblique personnalisée"
    ]

def get_related_topics(current_topic):
    """Get related biblical topics"""
    from services.chatbot_data import BIBLICAL_TOPICS
    
    topic_relationships = {
        'foi': ['espérance', 'confiance', 'prière'],
        'amour': ['compassion', 'charité', 'miséricorde'],
        'prière': ['foi', 'intercession', 'jeûne'],
        'paix': ['réconciliation', 'pardon', 'paix'],
        'espérance': ['foi', 'persévérance', 'patience'],
        'pardon': ['miséricorde', 'réconciliation', 'repentance'],
        'guérison': ['foi', 'miracles', 'prière'],
        'mariage': ['famille', 'amour', 'unité'],
        'famille': ['mariage', 'éducation', 'amour']
    }
    
    related = topic_relationships.get(current_topic, ['foi', 'amour', 'prière'])[:3]
    return [topic for topic in related if topic in BIBLICAL_TOPICS]

def get_spiritual_followup_questions(question):
    """Generate spiritual follow-up questions"""
    return [
        "Souhaitez-vous approfondir ce sujet ?",
        "Avez-vous d'autres questions bibliques ?",
        "Comment puis-je vous accompagner dans votre foi ?",
        "Voulez-vous que je prie pour vous ?"
    ]

def get_help_categories():
    """Get help categories for app assistance"""
    return [
        "Connexion et inscription",
        "Profil et paramètres",
        "Témoignages",
        "Playlist audio",
        "Finances et cotisations",
        "Contact WhatsApp"
    ]

def get_suggested_topics(question):
    """Get suggested biblical topics based on question"""
    from services.chatbot_data import BIBLICAL_TOPICS
    
    question_lower = question.lower()
    
    if any(word in question_lower for word in ['dieu', 'seigneur', 'créateur']):
        return [topic for topic in ['foi', 'adoration', 'prière'] if topic in BIBLICAL_TOPICS]
    elif any(word in question_lower for word in ['jésus', 'christ', 'sauveur']):
        return [topic for topic in ['salut', 'foi', 'amour'] if topic in BIBLICAL_TOPICS]
    elif any(word in question_lower for word in ['problème', 'difficulté', 'souffrance']):
        return [topic for topic in ['espérance', 'patience', 'prière'] if topic in BIBLICAL_TOPICS]
    elif any(word in question_lower for word in ['famille', 'mariage', 'couple']):
        return [topic for topic in ['mariage', 'famille', 'amour'] if topic in BIBLICAL_TOPICS]
    else:
        return [topic for topic in ['foi', 'amour', 'prière'] if topic in BIBLICAL_TOPICS]

def get_suggested_actions():
    """Get suggested actions for fallback responses"""
    return [
        "Choisissez un sujet dans le menu déroulant",
        "Reformulez votre question",
        "Demandez-moi des versets sur un thème",
        "Explorez nos 75+ sujets bibliques"
    ]

def enhance_question_with_context(question):
    """Enhance question with biblical context for OpenAI"""
    context = """Tu es Kadosh.ia, assistant biblique chrétien de BENJ INSIDE. 
    Réponds selon la Bible et la foi chrétienne évangélique. 
    Utilise des versets bibliques quand c'est approprié. 
    Sois encourageant et spirituel dans tes réponses."""
    
    return f"{context}\n\nQuestion: {question}"

def get_intelligent_fallback_response(question):
    """Generate intelligent fallback response with helpful suggestions"""
    return f"""🕊️ **Shalom bien-aimé(e) !**

Je comprends votre question et j'aimerais vous aider du mieux possible. Bien que je ne trouve pas de réponse spécifique dans ma base de connaissances bibliques, permettez-moi de vous guider :

💡 **Suggestions pour mieux vous servir :**
• Reformulez votre question avec des mots-clés bibliques
• Choisissez un sujet dans le menu déroulant (92+ sujets disponibles)
• Demandez-moi des versets sur un thème particulier
• Explorez nos sujets populaires : foi, amour, prière, paix, espérance

✨ **Exemples de questions que je peux traiter :**
• "Que dit la Bible sur la confiance en soi ?"
• "Comment surmonter la peur selon la Bible ?"
• "Versets sur l'amour de Dieu"
• "Comment avoir la paix intérieure ?"
• "Prêche-moi sur la foi"

💝 **Je suis votre ami spirituel :**
En tant qu'enseignant biblique, coach chrétien et psychologue spirituel, je suis là pour vous accompagner avec empathie et compassion dans votre cheminement.

🙏 *"Demandez, et l'on vous donnera; cherchez, et vous trouverez; frappez, et l'on vous ouvrira."* - Matthieu 7:7

*Que Dieu vous bénisse et vous guide dans votre recherche de Sa vérité !*"""
