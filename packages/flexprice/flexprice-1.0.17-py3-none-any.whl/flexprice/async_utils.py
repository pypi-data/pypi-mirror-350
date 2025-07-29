
import asyncio
import threading
import logging
from typing import Dict, Any, Optional, List, Union, Callable
from queue import Queue, Empty
import time
import random
import traceback

logger = logging.getLogger(__name__)

class AsyncEventProcessor:
    """Handler for asynchronous event processing with retries."""
    
    def __init__(self, 
                 max_retries: int = 3, 
                 retry_delay: float = 1.0,
                 max_queue_size: int = 1000,
                 workers: int = 2):
        """
        Initialize the async event processor.
        
        Args:
            max_retries: Maximum number of retry attempts for failed requests
            retry_delay: Base delay between retries (exponential backoff is applied)
            max_queue_size: Maximum number of events to queue
            workers: Number of worker threads to process events
        """
        self.max_retries = max_retries
        self.retry_delay = retry_delay
        self.event_queue = Queue(maxsize=max_queue_size)
        self.workers = workers
        self._worker_threads = []
        self._running = False
        
    def start(self):
        """Start the event processing workers."""
        if self._running:
            return
            
        self._running = True
        for i in range(self.workers):
            thread = threading.Thread(
                target=self._process_queue,
                name=f"event-worker-{i}",
                daemon=True
            )
            thread.start()
            self._worker_threads.append(thread)
        
        logger.info(f"Started {self.workers} async event processor workers")
    
    def stop(self):
        """Stop the event processing."""
        self._running = False
        for thread in self._worker_threads:
            thread.join(timeout=1.0)
        self._worker_threads = []
        
    def _process_queue(self):
        """Worker thread function to process events from the queue."""
        while self._running:
            try:
                event_data = self.event_queue.get(block=True, timeout=0.5)
                if event_data is None:
                    continue
                
                # Validate event_data structure
                if not isinstance(event_data, tuple) or len(event_data) != 3:
                    logger.error(f"Invalid event data format: {event_data}")
                    self.event_queue.task_done()
                    continue
                    
                event, api_instance, callback = event_data
                self._process_event(event, api_instance, callback)
                self.event_queue.task_done()
            except Empty:
                # Empty queue is normal, just continue polling
                pass
            except Exception as e:
                if not isinstance(e, asyncio.TimeoutError):
                    error_details = traceback.format_exc()
                    logger.error(f"Error in event processor: {str(e)}\n{error_details}")
    
    def _process_event(self, event, api_instance, callback):
        """Process a single event with retries."""
        attempt = 0
        last_error = None
        
        while attempt <= self.max_retries:
            try:
                if attempt > 0:
                    # Exponential backoff with jitter
                    delay = self.retry_delay * (2 ** (attempt - 1)) 
                    delay = delay * (0.5 + random.random())
                    time.sleep(delay)
                    
                logger.debug(f"Sending event (attempt {attempt+1}/{self.max_retries+1})")
                result = api_instance.events_post(event=event)
                
                if callback:
                    callback(result=result, error=None, success=True)
                
                logger.info(f"Successfully sent event to FlexPrice API")
                return
            except Exception as e:
                last_error = e
                error_details = traceback.format_exc()
                logger.warning(f"Event delivery failed (attempt {attempt+1}/{self.max_retries+1}): {str(e)}\n{error_details}")
                attempt += 1
                
        # All retries failed
        logger.error(f"Event delivery permanently failed after {self.max_retries+1} attempts: {str(last_error)}")
        if callback:
            callback(result=None, error=last_error, success=False)
    
    def submit_event(self, event, api_instance, callback=None):
        """
        Submit an event for asynchronous processing.
        
        Args:
            event: The event data to process
            api_instance: The API client instance to use for processing
            callback: Optional callback function that receives (result, error, success) params
            
        Returns:
            bool: True if the event was queued, False if the queue is full
        """
        try:
            # Validate inputs
            if event is None:
                logger.error("Cannot submit None event")
                return False
            if api_instance is None:
                logger.error("Cannot submit event with None api_instance")
                return False
                
            self.event_queue.put_nowait((event, api_instance, callback))
            logger.debug(f"Event queued for async processing")
            return True
        except Exception as e:
            logger.error(f"Failed to queue event: {str(e)}\n{traceback.format_exc()}")
            return False

# Global processor instance
_processor = AsyncEventProcessor()
_processor.start()

def submit_event_async(event, api_instance, callback=None):
    """
    Submit an event for asynchronous processing with automatic retries.
    
    Args:
        event: The event data to process
        api_instance: The API client instance to use
        callback: Optional callback function with signature (result, error, success)
        
    Returns:
        bool: True if the event was queued successfully, False otherwise
    """
    return _processor.submit_event(event, api_instance, callback)

# Ensure the processor is stopped when the program exits
import atexit
atexit.register(_processor.stop)
