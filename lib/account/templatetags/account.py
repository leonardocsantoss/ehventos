from django import template
try:
   import hashlib.md5 as md5
except ImportError:
   import md5 as md5

register = template.Library()

class GravatarUrlNode(template.Node):
    def __init__(self, email):
        self.email = template.Variable(email)

    def render(self, context):
        try:
            email = self.email.resolve(context)
        except template.VariableDoesNotExist:
            return ''

        size = 80

        gravatar_url = "http://www.gravatar.com/avatar/" + md5.md5(email.lower()).hexdigest() + "?s=" + str(size)

        return gravatar_url

@register.tag
def gravatar_url(parser, token):
    try:
        tag_name, email = token.split_contents()

    except ValueError:
        raise template.TemplateSyntaxError, "%r tag requires a single argument" % token.contents.split()[0]

    return GravatarUrlNode(email)
