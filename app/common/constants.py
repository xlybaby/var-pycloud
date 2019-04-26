# -*- coding: utf-8 -*-
import sys,os

class RequestMapping(object):
    fetch_template_by_id = r'/tbi'
    fetch_template_by_uid = r'/tbui'
    fetch_shared_templates = r'/st'
    fetch_template_by_keywords = r'/tbks'
                     
    submit_template_with_uid = r'/sbi'
    save_template_with_uid = r'/sbui'
    
    user_sign_in = r'/uli'
    user_sign_up = r'/ure'
    user_sign_out = r'/uso'

    get_image_code = r'/uiic'
    get_dynamic_code = r'/uddc'
    get_human_identify = r'/uhi'