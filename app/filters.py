from .models import  ROLES

def register_filters(app):

    @app.template_filter()
    def user_role(role):
        for key, value in ROLES.items():
            if value == role:
                return key
        return ''
    
    @app.template_filter()
    def pretty_date(value):
        return value.strftime("%b %d %Y ")
