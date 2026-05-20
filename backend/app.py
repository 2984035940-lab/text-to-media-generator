from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_restful import Api, Resource
import os
from datetime import datetime
from config import config, Config
from runway_client import RunwayClient
from leonardo_client import LeonardoClient

app = Flask(__name__)
app.config.from_object(config['development'])
CORS(app)
api = Api(app)

# Initialize clients
runway_client = RunwayClient()
leonardo_client = LeonardoClient()

# Create required directories
for folder in [Config.UPLOAD_FOLDER, Config.OUTPUT_FOLDER, Config.TEMP_FOLDER]:
    os.makedirs(folder, exist_ok=True)


class HealthCheck(Resource):
    def get(self):
        """Health check endpoint"""
        return {
            'status': 'healthy',
            'timestamp': datetime.now().isoformat(),
            'service': 'text-to-media-generator'
        }, 200


class GenerateVideo(Resource):
    def post(self):
        """Generate video from text prompt"""
        try:
            data = request.get_json()
            
            if not data or 'prompt' not in data:
                return {'error': 'Prompt is required'}, 400
            
            prompt = data.get('prompt')
            duration = data.get('duration', 5)
            fps = data.get('fps', 24)
            width = data.get('width', 1280)
            height = data.get('height', 720)
            
            result = runway_client.generate_video(
                prompt=prompt,
                duration=duration,
                fps=fps,
                width=width,
                height=height
            )
            
            return result, 200
            
        except Exception as e:
            return {'error': str(e)}, 500


class GenerateImage(Resource):
    def post(self):
        """Generate image from text prompt"""
        try:
            data = request.get_json()
            
            if not data or 'prompt' not in data:
                return {'error': 'Prompt is required'}, 400
            
            prompt = data.get('prompt')
            negative_prompt = data.get('negative_prompt', '')
            num_images = data.get('num_images', 1)
            width = data.get('width', 768)
            height = data.get('height', 768)
            guidance_scale = data.get('guidance_scale', 7.5)
            
            result = leonardo_client.generate_image(
                prompt=prompt,
                negative_prompt=negative_prompt,
                num_images=num_images,
                width=width,
                height=height,
                guidance_scale=guidance_scale
            )
            
            return result, 200
            
        except Exception as e:
            return {'error': str(e)}, 500


class TaskStatus(Resource):
    def get(self, task_id):
        """Get video generation task status"""
        try:
            result = runway_client.get_task_status(task_id)
            return result, 200
        except Exception as e:
            return {'error': str(e)}, 500


class GenerationStatus(Resource):
    def get(self, generation_id):
        """Get image generation status"""
        try:
            result = leonardo_client.get_generation_status(generation_id)
            return result, 200
        except Exception as e:
            return {'error': str(e)}, 500


# Register API endpoints
api.add_resource(HealthCheck, '/health')
api.add_resource(GenerateVideo, '/api/generate-video')
api.add_resource(GenerateImage, '/api/generate-image')
api.add_resource(TaskStatus, '/api/tasks/<task_id>')
api.add_resource(GenerationStatus, '/api/generations/<generation_id>')


@app.route('/')
def index():
    """Welcome endpoint"""
    return {
        'message': 'Text-to-Media Generator API',
        'version': '1.0.0',
        'endpoints': {
            'health': '/health',
            'generate_video': 'POST /api/generate-video',
            'generate_image': 'POST /api/generate-image',
            'task_status': 'GET /api/tasks/<task_id>',
            'generation_status': 'GET /api/generations/<generation_id>'
        }
    }, 200


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
