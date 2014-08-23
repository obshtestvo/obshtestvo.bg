from django import template

from assetstack import AssetStack

register = template.Library()

class AssetsNode(template.Node):
    is_master = False
    nodelist = None
    name = None

    def __init__(self, nodelist, stackname, is_master=False):
        self.nodelist = nodelist
        self.name = stackname
        self.is_master = is_master

    def __repr__(self):
        return "<Block Node: %s. Contents: %r>" % (self.name, self.nodelist)

    def get_original_content(self, context):
        return self.nodelist.render(context)

    def render(self, context):
        stack = AssetStack.Instance(self.name)
        if stack.has_master():
            if self.is_master:
                return self.get_original_content(context) + stack.get_content()
            else:
                stack.add_content(self.get_original_content(context))
                return ''
        else:
            return self.get_original_content(context)


@register.tag
def assets(parser, token):
    nodelist = parser.parse(('endassets',))
    parser.next_token()
    args = token.split_contents()
    stack = AssetStack.Instance(args[1])
    # paths = []
    # for n in nodelist:
    #     if isinstance(n, StaticNode):
    #         stack.register(n.path)

    try:
        master = args[2] == 'master'
    except:
        master = False

    if master:
        stack.set_master(True)
    return AssetsNode(nodelist, args[1], master)