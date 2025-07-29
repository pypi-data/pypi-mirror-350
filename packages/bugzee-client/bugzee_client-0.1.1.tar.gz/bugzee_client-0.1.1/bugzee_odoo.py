"""
Bugzee Error Monitoring client for Odoo.

This module provides error monitoring capabilities for Odoo applications.
"""

import json
import uuid
import traceback
import threading
import sys
import logging
import socket
import requests
from datetime import datetime

_logger = logging.getLogger(__name__)

class BugzeeClient:
    """
    Bugzee Error Monitoring client for Odoo.
    """
    def __init__(self, public_key=None, secret_key=None, api_url=None, environment=None, server_name=None):
        self.public_key = public_key
        self.secret_key = secret_key
        self.api_url = api_url or 'https://bugzee.pro/errors/api/store/'
        self.environment = environment or 'production'
        self.server_name = server_name or socket.gethostname()
        self.enabled = self.public_key is not None
        
        # Ensure we have the necessary configuration
        if not self.enabled:
            _logger.warning("Bugzee Error Monitoring is not configured properly. Set public_key when initializing the client.")
    
    def capture_exception(self, exc_info=None, request=None, extra_context=None, tags=None):
        """
        Capture an exception and send it to Bugzee Error Monitoring.
        
        Args:
            exc_info: Exception info tuple (type, value, traceback)
            request: Odoo HTTP request object
            extra_context: Additional context to include with the error
            tags: Tags to categorize the error
        
        Returns:
            Event ID if successfully sent, None otherwise
        """
        if not self.enabled:
            return None
        
        # Get exception info if not provided
        if exc_info is None:
            exc_info = sys.exc_info()
        
        exc_type, exc_value, tb = exc_info
        
        # Don't report if exception type should be ignored
        if self._should_ignore_exception(exc_type, exc_value):
            return None
        
        # Build the error data
        error_data = self._build_error_data(exc_type, exc_value, tb, request, extra_context, tags)
        
        # Send the error data in a background thread to avoid blocking
        self._send_error_data_async(error_data)
        
        return error_data.get('event_id')
    
    def _build_error_data(self, exc_type, exc_value, tb, request, extra_context, tags):
        """Build the error data structure to send to the API."""
        event_id = str(uuid.uuid4())
        
        # Basic error info
        error_data = {
            'event_id': event_id,
            'timestamp': datetime.utcnow().isoformat(),
            'platform': 'odoo',
            'server_name': self.server_name,
            'environment': self.environment,
            'public_key': self.public_key,
            
            # Exception details
            'exception_type': exc_type.__name__ if exc_type else 'Unknown',
            'exception_value': str(exc_value) if exc_value else '',
            'module': exc_type.__module__ if exc_type else '',
            
            # Context
            'context': extra_context or {},
            'tags': tags or {},
        }
        
        # Process traceback
        if tb:
            frames = []
            for frame in traceback.extract_tb(tb):
                # For compatibility with both Python 2 and 3
                if hasattr(frame, 'filename'):
                    filename = frame.filename
                    lineno = frame.lineno
                    function = frame.name
                    context_line = frame.line
                else:
                    filename, lineno, function, context_line = frame
                
                frames.append({
                    'filename': filename,
                    'lineno': lineno,
                    'function': function,
                    'context_line': context_line,
                })
            error_data['traceback'] = frames
        
        # Process request if available
        if request and hasattr(request, 'httprequest'):
            httprequest = request.httprequest
            request_data = {
                'url': httprequest.url,
                'method': httprequest.method,
                'headers': dict(httprequest.headers),
                'query_string': httprequest.query_string.decode('utf-8') if hasattr(httprequest.query_string, 'decode') else httprequest.query_string,
                'data': {},
            }
            
            # Try to get user info if available
            if hasattr(request, 'uid') and request.uid:
                try:
                    request_data['user'] = {
                        'id': request.uid,
                    }
                    # Try to get more user info if available
                    if hasattr(request, 'env') and request.env:
                        user = request.env['res.users'].sudo().browse(request.uid)
                        if user.exists():
                            request_data['user'].update({
                                'login': user.login,
                                'name': user.name,
                            })
                except Exception:
                    pass
            
            error_data['request'] = request_data
        
        return error_data
    
    def _should_ignore_exception(self, exc_type, exc_value):
        """Determine if the exception should be ignored."""
        # Add ignore rules as needed
        ignored_exceptions = [
            'werkzeug.exceptions.NotFound',
            'odoo.exceptions.AccessDenied',
            'odoo.exceptions.AccessError',
        ]
        
        if exc_type and f"{exc_type.__module__}.{exc_type.__name__}" in ignored_exceptions:
            return True
        
        return False
    
    def _send_error_data_async(self, error_data):
        """Send the error data to the API in a background thread."""
        thread = threading.Thread(target=self._send_error_data, args=(error_data,))
        thread.daemon = True
        thread.start()
    
    def _send_error_data(self, error_data):
        """Send the error data to the API."""
        try:
            headers = {
                'Content-Type': 'application/json',
                'X-Bugzee-Secret': str(self.secret_key) if self.secret_key else '',
            }
            
            response = requests.post(
                self.api_url,
                headers=headers,
                data=json.dumps(error_data),
                timeout=5
            )
            
            if response.status_code != 200:
                _logger.error(f"Failed to send error to Bugzee: {response.status_code} {response.text}")
            
            return response.status_code == 200
        except Exception as e:
            _logger.error(f"Error sending exception to Bugzee: {str(e)}")
            return False

# Global client instance
client = None

def initialize(public_key, secret_key=None, api_url=None, environment=None):
    """
    Initialize the global Bugzee client.
    
    This should be called early in your Odoo module's initialization.
    """
    global client
    client = BugzeeClient(
        public_key=public_key,
        secret_key=secret_key,
        api_url=api_url,
        environment=environment
    )
    return client

def get_client():
    """Get the global Bugzee client instance."""
    global client
    if client is None:
        client = BugzeeClient()
    return client

def capture_exception(exc_info=None, request=None, extra_context=None, tags=None):
    """
    Capture and report an exception to Bugzee Error Monitoring.
    
    This function is the main entry point for manually reporting exceptions.
    """
    return get_client().capture_exception(exc_info, request, extra_context, tags)

def install_exception_hook():
    """Install a global exception hook to capture unhandled exceptions."""
    original_excepthook = sys.excepthook
    
    def excepthook(exc_type, exc_value, tb):
        client = get_client()
        if client.enabled:
            client.capture_exception((exc_type, exc_value, tb))
        original_excepthook(exc_type, exc_value, tb)
    
    sys.excepthook = excepthook

class BugzeeModelExceptionLogger:
    """
    Mixin to add to Odoo models for automatic exception logging.
    
    Example usage:
    ```
    from odoo import models
    from bugzee_odoo import BugzeeModelExceptionLogger
    
    class MyModel(models.Model, BugzeeModelExceptionLogger):
        _name = 'my.model'
    ```
    """
    def _handle_exception(self, exception):
        """Override this method to capture exceptions from model methods."""
        client = get_client()
        if client.enabled:
            # Get the current request if we're in a web context
            request = None
            if hasattr(self, 'env') and hasattr(self.env, 'context') and self.env.context.get('request'):
                request = self.env.context.get('request')
            
            # Add model info to context
            extra_context = {
                'model': self._name,
                'model_method': sys._getframe(1).f_code.co_name,
            }
            
            # Add record info if this is a single record
            if hasattr(self, 'id') and isinstance(self.id, int):
                extra_context['record_id'] = self.id
            
            # Capture the exception
            client.capture_exception(
                exc_info=(type(exception), exception, exception.__traceback__),
                request=request,
                extra_context=extra_context,
                tags={'model': self._name}
            )
        
        # Call the original method to preserve normal exception handling
        return super(BugzeeModelExceptionLogger, self)._handle_exception(exception) 