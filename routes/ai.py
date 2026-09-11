# ============================================================================
# AI Routes
# Multi-engine LLM routing and AI services
# ============================================================================

from flask import Blueprint, request, jsonify
import asyncio
from sbrcore.ai import AIRouter
from sbrcore.api.decorators import require_auth, rate_limit, log_request
from sbrcore.api.utils import format_error_response, format_success_response
from sbrcore.logging import get_logger

ai_bp = Blueprint('ai', __name__)
logger = get_logger(__name__)

# Initialize AI Router
ai_router = AIRouter()

@ai_bp.route('/generate', methods=['POST'])
@log_request
@rate_limit(max_requests=100, window_seconds=60)
def generate_response():
    """
    Generate AI response with multi-engine routing
    """
    try:
        data = request.get_json()
        
        if not data.get('prompt'):
            return format_error_response('Missing prompt', 'MISSING_PROMPT', 422)
        
        # Get parameters
        prompt = data['prompt']
        use_case = data.get('use_case', 'general')
        preferred_engine = data.get('preferred_engine')
        temperature = float(data.get('temperature', 0.7))
        max_tokens = int(data.get('max_tokens', 1024))
        
        # Run async AI request
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        
        try:
            result = loop.run_until_complete(
                ai_router.route_request(
                    prompt=prompt,
                    use_case=use_case,
                    preferred_engine=preferred_engine,
                    temperature=temperature,
                    max_tokens=max_tokens
                )
            )
        finally:
            loop.close()
        
        if result.get('status') == 'failed':
            return format_error_response(
                result.get('error', 'AI request failed'),
                'AI_ERROR',
                500
            )
        
        logger.info(f"AI request processed via {result['engine']}")
        
        return format_success_response(
            result,
            'Response generated successfully'
        )
    
    except Exception as e:
        logger.error(f"AI generation error: {str(e)}")
        return format_error_response('AI generation failed', 'AI_ERROR', 500)

@ai_bp.route('/translate', methods=['POST'])
@log_request
@rate_limit(max_requests=200, window_seconds=60)
def translate():
    """
    Translate text to any language using fastest engine (Groq)
    """
    try:
        data = request.get_json()
        
        if not data.get('text') or not data.get('target_language'):
            return format_error_response(
                'Missing text or target_language',
                'MISSING_PARAMS',
                422
            )
        
        prompt = f"Translate this to {data['target_language']}: {data['text']}"
        
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        
        try:
            result = loop.run_until_complete(
                ai_router.route_request(
                    prompt=prompt,
                    use_case='translation',
                    preferred_engine='groq',
                    max_tokens=500
                )
            )
        finally:
            loop.close()
        
        return format_success_response(
            {
                'original': data['text'],
                'translated': result.get('response'),
                'target_language': data['target_language']
            },
            'Translation completed'
        )
    
    except Exception as e:
        logger.error(f"Translation error: {str(e)}")
        return format_error_response('Translation failed', 'TRANSLATION_ERROR', 500)

@ai_bp.route('/engines', methods=['GET'])
@log_request
def get_available_engines():
    """
    Get list of available AI engines
    """
    engines = ai_router.get_available_engines()
    
    return format_success_response(
        {'engines': engines, 'default': ai_router.primary_engine},
        'Available engines retrieved'
    )
