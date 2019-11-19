"""Generic interceptor for SAML auth responses.

Since the process of handling SAML responses is the same we can actually have a
generic interceptor"""

import base64
import re

from mitmproxy import http, ctx


class SamlInterceptor(object):
    MATCH_EXPR = re.compile(r'''name=['"]SAMLResponse['"]''')

    def response(self, flow):
        requestObj = flow.request
        responseObj = flow.response
        origContents = responseObj.get_text()
        if self.MATCH_EXPR.search(origContents):
            ctx.log.warn('Intercepted SAML ProcessAuth response')
            origEncoded = base64.standard_b64encode(origContents.encode())
            newContents = ('<html><body><p name="SAMLResponse">'
                           'Login Successful'
                           '</p>'
                           '<script type="text/javascript">/* __START_ORIGINAL_RESPONSE__:')
            newContents += origEncoded.decode()
            newContents += (':__END_ORIGINAL_RESPONSE__ */</script>'
                            '</body></html>')
            ctx.log.info('response headers:{}'.format(responseObj.headers.items()))
            ctx.log.info('setting contents to:{}'.format(newContents))
            responseObj.set_text(newContents)

addons = [SamlInterceptor()]