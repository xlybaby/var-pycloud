# -*- coding: utf-8 -*-
import sys,os
from app.context.initializedInstancePool import ApplicationContext 

def controller_process_agent(*args, **kwargs):
    def proxy(origin_func):
        def wrapper(self):
            try:
                iname = args[0]
                service = ApplicationContext.getContext().getInstance(p_name=iname)
                result = service.execute(self.args)
                self.write(result)
                self.flush()
                origin_func(self)
            except Exception:
                return 'an Exception raised.'
        return wrapper
    return proxy


def injectComponent(*args, **kwargs):
    def proxy(origin_func):
        def wrapper(self):
            try:
                iname = args[0]
                comp = ApplicationContext.getContext().getInstance(p_name=iname)
                return comp
            except Exception:
                return 'an Exception raised.'
        return wrapper
    return proxy
