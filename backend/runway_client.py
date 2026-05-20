import os
import requests
import json
from typing import Dict, Any, Optional
from config import Config

class RunwayClient:
    """Runway API Client for text-to-video generation"""
    
    def __init__(self, api_key: str = None):
        self.api_key = api_key or Config.RUNWAY_API_KEY
        self.base_url = Config.RUNWAY_API_URL
        self.headers = {
            'Authorization': f'Bearer {self.api_key}',
            'Content-Type': 'application/json'
        }
    
    def generate_video(self, 
                      prompt: str,
                      duration: int = 5,
                      fps: int = 24,
                      width: int = 1280,
                      height: int = 720,
                      **kwargs) -> Dict[str, Any]:
        """
        Generate video from text prompt using Runway API
        
        Args:
            prompt (str): Text description for video generation
            duration (int): Video duration in seconds (default: 5)
            fps (int): Frames per second (default: 24)
            width (int): Video width in pixels (default: 1280)
            height (int): Video height in pixels (default: 720)
            **kwargs: Additional parameters
        
        Returns:
            Dict with task info and video URL
        """
        try:
            payload = {
                'prompt': prompt,
                'duration': duration,
                'fps': fps,
                'width': width,
                'height': height,
                **kwargs
            }
            
            response = requests.post(
                f'{self.base_url}/text_to_video',
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
    
    def get_task_status(self, task_id: str) -> Dict[str, Any]:
        """
        Get the status of a video generation task
        
        Args:
            task_id (str): Task ID from generation request
        
        Returns:
            Dict with task status and result
        """
        try:
            response = requests.get(
                f'{self.base_url}/tasks/{task_id}',
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
        List available Runway video generation models
        
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
