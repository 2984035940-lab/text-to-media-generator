import os
import requests
import json
from typing import Dict, Any, List, Optional
from config import Config

class LeonardoClient:
    """Leonardo API Client for text-to-image generation"""
    
    def __init__(self, api_key: str = None):
        self.api_key = api_key or Config.LEONARDO_API_KEY
        self.base_url = Config.LEONARDO_API_URL
        self.headers = {
            'Authorization': f'Bearer {self.api_key}',
            'Content-Type': 'application/json'
        }
    
    def generate_image(self,
                      prompt: str,
                      negative_prompt: str = '',
                      num_images: int = 1,
                      width: int = 768,
                      height: int = 768,
                      guidance_scale: float = 7.5,
                      model_id: str = 'default',
                      **kwargs) -> Dict[str, Any]:
        """
        Generate image from text prompt using Leonardo API
        
        Args:
            prompt (str): Text description for image generation
            negative_prompt (str): What to avoid in the image
            num_images (int): Number of images to generate (default: 1)
            width (int): Image width in pixels (default: 768)
            height (int): Image height in pixels (default: 768)
            guidance_scale (float): Guidance scale for generation (default: 7.5)
            model_id (str): Model ID to use (default: 'default')
            **kwargs: Additional parameters
        
        Returns:
            Dict with generation info and image URLs
        """
        try:
            payload = {
                'prompt': prompt,
                'negative_prompt': negative_prompt,
                'num_images': num_images,
                'width': width,
                'height': height,
                'guidance_scale': guidance_scale,
                'model_id': model_id,
                **kwargs
            }
            
            response = requests.post(
                f'{self.base_url}/generations',
                headers=self.headers,
                json=payload,
                timeout=30
            )
            
            response.raise_for_status()
            return response.json()
            
        except requests.exceptions.RequestException as e:
            return {
                'error': str(e),
                'status': 'failed'
            }
    
    def get_generation_status(self, generation_id: str) -> Dict[str, Any]:
        """
        Get the status of an image generation task
        
        Args:
            generation_id (str): Generation ID from request
        
        Returns:
            Dict with generation status and images
        """
        try:
            response = requests.get(
                f'{self.base_url}/generations/{generation_id}',
                headers=self.headers,
                timeout=10
            )
            
            response.raise_for_status()
            return response.json()
            
        except requests.exceptions.RequestException as e:
            return {
                'error': str(e),
                'status': 'failed'
            }
    
    def list_models(self) -> Dict[str, Any]:
        """
        List available Leonardo image generation models
        
        Returns:
            Dict with available models
        """
        try:
            response = requests.get(
                f'{self.base_url}/models',
                headers=self.headers,
                timeout=10
            )
            
            response.raise_for_status()
            return response.json()
            
        except requests.exceptions.RequestException as e:
            return {
                'error': str(e),
                'models': []
            }
    
    def batch_generate_images(self, 
                             prompts: List[str],
                             **kwargs) -> List[Dict[str, Any]]:
        """
        Generate multiple images from a list of prompts
        
        Args:
            prompts (List[str]): List of text prompts
            **kwargs: Additional parameters for generation
        
        Returns:
            List of generation results
        """
        results = []
        for prompt in prompts:
            result = self.generate_image(prompt, **kwargs)
            results.append(result)
        return results
