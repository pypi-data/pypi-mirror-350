"""
script_notifier.py - Simple script exit notifications

Usage:
    import script_notifier
    
    def on_success():
        print("Script completed successfully!")
        
    def on_error(error_info):
        print(f"Script failed: {error_info}")
    
    script_notifier.on_exit(on_success, on_error)
"""

import atexit
import sys
import traceback


class ExitHandler:
    def __init__(self):
        self.exception_occurred = False
        self.exception_info = None
        self.success_handler = None
        self.error_handler = None
        self.original_excepthook = sys.excepthook
        self._install()
    
    def _install(self):
        sys.excepthook = self._handle_exception
        atexit.register(self._handle_exit)
    
    def _handle_exception(self, exc_type, exc_value, exc_traceback):
        self.exception_occurred = True
        self.exception_info = {
            'type': exc_type.__name__,
            'message': str(exc_value),
            'traceback': ''.join(traceback.format_exception(exc_type, exc_value, exc_traceback))
        }
        self.original_excepthook(exc_type, exc_value, exc_traceback)
    
    def _handle_exit(self):
        try:
            if self.exception_occurred and self.error_handler:
                self.error_handler(self.exception_info)
            elif not self.exception_occurred and self.success_handler:
                self.success_handler()
        except Exception as e:
            print(f"Warning: Exit handler failed: {e}")
    
    def on_exit(self, success_func=None, error_func=None):
        """Register functions to call on success/error
        
        Args:
            success_func: Function to call on successful completion (no args)
            error_func: Function to call on error (receives error_info dict)
        """
        # Validate success function
        if success_func is not None:
            if not callable(success_func):
                raise TypeError("success_func must be callable")
            
        # Validate error function
        if error_func is not None:
            if not callable(error_func):
                raise TypeError("error_func must be callable")
        
        self.success_handler = success_func
        self.error_handler = error_func


# Global instance
_handler = ExitHandler()
on_exit = _handler.on_exit
