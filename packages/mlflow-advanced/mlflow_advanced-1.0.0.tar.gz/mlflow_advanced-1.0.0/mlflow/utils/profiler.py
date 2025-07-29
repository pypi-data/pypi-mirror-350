
import time
import psutil
import numpy as np
from typing import Dict, Any, Callable, Optional
from functools import wraps
import threading

class PerformanceProfiler:
    """
    Advanced performance profiling for ML operations.
    
    Features:
    - Memory usage tracking
    - Execution time measurement
    - Resource utilization monitoring
    - Performance bottleneck identification
    """
    
    def __init__(self):
        self.profiles = {}
        self.active_profiles = {}
        self.lock = threading.Lock()
    
    def profile_function(self, func_name: Optional[str] = None):
        """Decorator for profiling function performance."""
        def decorator(func: Callable) -> Callable:
            @wraps(func)
            def wrapper(*args, **kwargs):
                name = func_name or func.__name__
                
                # Start profiling
                start_time = time.time()
                process = psutil.Process()
                start_memory = process.memory_info().rss / 1024 / 1024  # MB
                start_cpu = process.cpu_percent()
                
                try:
                    result = func(*args, **kwargs)
                    success = True
                    error = None
                except Exception as e:
                    result = None
                    success = False
                    error = str(e)
                    raise
                finally:
                    # End profiling
                    end_time = time.time()
                    end_memory = process.memory_info().rss / 1024 / 1024  # MB
                    end_cpu = process.cpu_percent()
                    
                    profile_data = {
                        'execution_time': end_time - start_time,
                        'memory_usage': end_memory - start_memory,
                        'peak_memory': end_memory,
                        'cpu_usage': end_cpu - start_cpu,
                        'success': success,
                        'error': error,
                        'timestamp': time.time()
                    }
                    
                    with self.lock:
                        if name not in self.profiles:
                            self.profiles[name] = []
                        self.profiles[name].append(profile_data)
                
                return result
            return wrapper
        return decorator
    
    def start_profiling(self, name: str):
        """Start profiling a code block."""
        with self.lock:
            self.active_profiles[name] = {
                'start_time': time.time(),
                'start_memory': psutil.Process().memory_info().rss / 1024 / 1024,
                'start_cpu': psutil.Process().cpu_percent()
            }
    
    def end_profiling(self, name: str) -> Dict[str, Any]:
        """End profiling a code block."""
        with self.lock:
            if name not in self.active_profiles:
                raise ValueError(f"No active profile found for {name}")
            
            start_data = self.active_profiles.pop(name)
            end_time = time.time()
            end_memory = psutil.Process().memory_info().rss / 1024 / 1024
            end_cpu = psutil.Process().cpu_percent()
            
            profile_data = {
                'execution_time': end_time - start_data['start_time'],
                'memory_usage': end_memory - start_data['start_memory'],
                'peak_memory': end_memory,
                'cpu_usage': end_cpu - start_data['start_cpu'],
                'success': True,
                'error': None,
                'timestamp': time.time()
            }
            
            if name not in self.profiles:
                self.profiles[name] = []
            self.profiles[name].append(profile_data)
            
            return profile_data
    
    def get_profile_summary(self, name: str) -> Dict[str, Any]:
        """Get performance summary for a profiled function/block."""
        if name not in self.profiles:
            return {}
        
        profiles = self.profiles[name]
        execution_times = [p['execution_time'] for p in profiles if p['success']]
        memory_usages = [p['memory_usage'] for p in profiles if p['success']]
        
        if not execution_times:
            return {'error': 'No successful executions found'}
        
        return {
            'total_calls': len(profiles),
            'successful_calls': len(execution_times),
            'failed_calls': len(profiles) - len(execution_times),
            'avg_execution_time': np.mean(execution_times),
            'min_execution_time': np.min(execution_times),
            'max_execution_time': np.max(execution_times),
            'std_execution_time': np.std(execution_times),
            'avg_memory_usage': np.mean(memory_usages),
            'max_memory_usage': np.max(memory_usages),
            'total_execution_time': np.sum(execution_times)
        }
    
    def get_all_profiles(self) -> Dict[str, Dict[str, Any]]:
        """Get summaries for all profiled functions/blocks."""
        return {name: self.get_profile_summary(name) for name in self.profiles.keys()}
    
    def clear_profiles(self, name: Optional[str] = None):
        """Clear profile data."""
        with self.lock:
            if name:
                self.profiles.pop(name, None)
            else:
                self.profiles.clear()