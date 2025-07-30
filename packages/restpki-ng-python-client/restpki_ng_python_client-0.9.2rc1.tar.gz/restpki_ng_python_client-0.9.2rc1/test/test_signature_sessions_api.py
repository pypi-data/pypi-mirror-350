# coding: utf-8

"""
    Rest PKI Core API

    <b><i>Para Português, <a href=\"https://docs.lacunasoftware.com/pt-br/articles/rest-pki/core/integration/get-started\">clique aqui</a></i></b>  <p>   <a href=\"https://docs.lacunasoftware.com/en-us/articles/rest-pki/core/\">Rest PKI Core</a> is an upcoming version of   <a href=\"https://docs.lacunasoftware.com/en-us/articles/rest-pki/\">Rest PKI</a> that will have extended compatibility with environments and databases.  </p>  <p>   In addition to Windows Server (which is already supported by Rest PKI), Rest PKI Core will also run on <b>Linux</b> (Debian- and RedHat-based distributions)   and on <b>Docker</b>. As for database servers, in addition to SQL Server, <b>PostgreSQL</b> will also be supported.  </p>  <p>   <b>Before getting started, see the integration overview on the <a href=\"https://docs.lacunasoftware.com/en-us/articles/rest-pki/core/integration/\">Integration Guide</a></b>  </p>  <p>   For questions regarding the usage of this API, please reach us at <a href=\"https://lacuna.help/\">lacuna.help</a>  </p>    <h2>Parameters</h2>  <p>   You will need the following parameters:  </p>  <ul>   <li><b>Endpoint</b>: address of the Rest PKI Core instance that will be used</li>   <li><b>API Key</b>: authorization key for using the API</li>  </ul>  <p>   The <span class=\"model\">endpoint</span> must be prefixed to all relative URLs mentioned here. As for the <span class=\"model\">API Key</span>, see how to use it below.  </p>    <h2>Authentication</h2>  <p>   The API key must be sent on the <span class=\"model\">X-Api-Key</span> header on each request:  </p>    <!-- unfortunately, class \"example microlight\" doesn't seem to work here -->  <pre style=\"font-size: 12px; padding: 10px; border-radius: 4px; background: #41444e; font-weight: 600; color: #fff;\">  X-Api-Key: yourapp|xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx  </pre>    <h2>HTTP Codes</h2>    <p>   The APIs will return the following HTTP codes:  </p>    <table>   <thead>    <tr>     <th>Code</th>     <th>Description</th>    </tr>   </thead>   <tbody>    <tr>     <td><strong class=\"model-title\">200 (OK)</strong></td>     <td>Request processed successfully. The response is different for each API, please refer to the operation's documentation</td>    </tr>    <tr>     <td><strong class=\"model-title\">400 (Bad Request)</strong></td>     <td>Syntax error. For instance, when a required field was not provided</td>    </tr>    <tr>     <td><strong class=\"model-title\">401 (Unauthorized)</strong></td>     <td>API key not provided or invalid</td>    </tr>    <tr>     <td><strong class=\"model-title\">403 (Forbidden)</strong></td>     <td>API key is valid, but the application has insufficient permissions to complete the requested operation</td>    </tr>    <tr>     <td><strong class=\"model-title\">422 (Unprocessable Entity)</strong></td>     <td>API error. The response body is an <a href=\"#model-ErrorModelV2\" class=\"model\">ErrorModelV2</a>    </tr>    <tr>     <td><strong class=\"model-title\">500 (Internal Server Error)</strong></td>     <td>An unexpected error occurred. The <span class=\"model\">exceptionCode</span> contained on the response body may be of help for our support team during diagnostic.</td>    </tr>   </tbody>  </table>    <h3>Error Codes</h3>    <p>   Some of the error codes returned in the <span class=\"model\">code</span> field of an <a href=\"#model-ErrorModelV2\" class=\"model\">ErrorModelV2</a>   (body of responses with HTTP status code 422) are provided below*:  </p>    <table>   <thead>    <tr>     <th>Code</th>     <th>Description</th>    </tr>   </thead>   <tbody>    <tr>     <td class=\"model\">DocumentNotFound</td>     <td>A referenced document was not found (check the document ID)</td>    </tr>    <tr>     <td class=\"model\">SecurityContextNotFound</td>     <td>A referenced security context was not found (check the security context ID)</td>    </tr>    <tr>     <td class=\"model\">SignatureSessionNotFound</td>     <td>A referenced signature session was not found (check the signature session ID)</td>    </tr>    <tr>     <td class=\"model\">BadSignatureSessionOperation</td>     <td>The operation is invalid for the current signature session or document status. For instance, trying to await the session's completion if it is still <span class=\"model\">Pending</span> results in this error</td>    </tr>    <tr>     <td class=\"model\">BackgroundProcessing</td>     <td>The operation cannot be completed at this time because the resource is being processed in background</td>    </tr>    <tr>     <td class=\"model\">SignatureSessionTokenRequired</td>     <td>The signature session token was not passed on the <span class=\"model\">X-Signature-Session-Token</span> request header</td>    </tr>    <tr>     <td class=\"model\">BadSignatureSessionToken</td>     <td>An invalid signature session token was passed on the <span class=\"model\">X-Signature-Session-Token</span> request header. Check your application for possible corruption of the session token, which may contain characters <span class=\"code\">-</span> (hyphen) and <span class=\"code\">_</span> (underscore)</td>    </tr>    <tr>     <td class=\"model\">ExpiredSignatureSessionToken</td>     <td>An expired signature session token was passed on the <span class=\"model\">X-Signature-Session-Token</span> request header. Signature session tokens are normally valid for 4 hours.</td>    </tr>   </tbody>  </table>    <p style=\"font-size: 0.9em\">   *The codes shown above are the most common error codes. Nonetheless, this list is not comprehensive. New codes may be added anytime without previous warning.  </p>    <h2>Culture / Internationalization (i18n)</h2>  <p>The <span class=\"model\">Accept-Language</span> request header is observed by this API. The following cultures are supported:</p>  <ul>   <li><span class=\"code\">en-US</span> (or simply <span class=\"code\">en</span>)</li>   <li><span class=\"code\">pt-BR</span> (or simply <span class=\"code\">pt</span>)</li>  </ul>  <p><i>Notice: error messages are not affected by this header and therefore should not be displayed to users, being better suited for logging.</i></p>  

    The version of the OpenAPI document: 2.1.0
    Generated by OpenAPI Generator (https://openapi-generator.tech)

    Do not edit the class manually.
"""  # noqa: E501


import unittest
import datetime
import base64
import threading
import http.server
import socketserver
import urllib.parse
import time
import os

from restpki_ng_python_client.api.signature_sessions_api import SignatureSessionsApi
from restpki_ng_python_client.models.create_signature_session_request import CreateSignatureSessionRequest
from restpki_ng_python_client.models.signature_session_document_data import SignatureSessionDocumentData
from restpki_ng_python_client.models.file_reference_model import FileReferenceModel
from restpki_ng_python_client.models.pdf_signature_options import PdfSignatureOptions
from restpki_ng_python_client.models.pades_visual_representation_model import PadesVisualRepresentationModel
from restpki_ng_python_client.models.pades_visual_text_model import PadesVisualTextModel
from restpki_ng_python_client.models.pades_visual_rectangle_model import PadesVisualRectangleModel
from restpki_ng_python_client.models.pades_visual_positioning_model import PadesVisualPositioningModel
from restpki_ng_python_client.models.pades_visual_auto_positioning_model import PadesVisualAutoPositioningModel
from restpki_ng_python_client.models.pades_size_model import PadesSizeModel
from restpki_ng_python_client.models.pades_page_optimization_model import PadesPageOptimizationModel
from restpki_ng_python_client.models.pades_measurement_units import PadesMeasurementUnits
from restpki_ng_python_client.models.pades_horizontal_align import PadesHorizontalAlign
from restpki_ng_python_client.models.pades_vertical_align import PadesVerticalAlign
from restpki_ng_python_client.models.auto_positioning_horizontal_directions import AutoPositioningHorizontalDirections
from restpki_ng_python_client.models.auto_positioning_vertical_directions import AutoPositioningVerticalDirections
from restpki_ng_python_client.models.signature_types import SignatureTypes
from test import rest_pki_client

class CallbackHandler(http.server.SimpleHTTPRequestHandler):
    """Handler for the callback URL"""
    callback_received = False
    callback_data = None

    def do_GET(self):
        """Handle GET request to the callback URL"""
        # Parse the query parameters
        query_components = urllib.parse.parse_qs(urllib.parse.urlparse(self.path).query)
        
        # Store the callback data
        CallbackHandler.callback_received = True
        CallbackHandler.callback_data = query_components
        
        # Send response
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(b"Callback received successfully!")

def start_callback_server(port=8000):
    """Start a local HTTP server to handle the callback"""
    handler = CallbackHandler
    with socketserver.TCPServer(("", port), handler) as httpd:
        print(f"Serving at port {port}")
        httpd.serve_forever()

class TestSignatureSessionsApi(unittest.TestCase):
    """SignatureSessionsApi unit test stubs"""

    @classmethod
    def setUpClass(cls):
        # Start the callback server in a separate thread
        cls.server_thread = threading.Thread(target=start_callback_server, daemon=True)
        cls.server_thread.start()
        # Give the server a moment to start
        time.sleep(1)

    def setUp(self) -> None:
        pass

    def tearDown(self) -> None:
        pass

    def test_api_signature_sessions_id_get(self) -> None:
        """Test case for api_signature_sessions_id_get

        Retrieves a signature session's details
        """
        pass

    def test_api_signature_sessions_id_when_completed_get(self) -> None:
        """Test case for api_signature_sessions_id_when_completed_get

        Waits for the completion of a signature session
        """
        pass

    def test_api_signature_sessions_post(self) -> None:
        """Test case for api_signature_sessions_post

        Creates a signature session
        """
        # Create a sample PDF file content (minimal valid PDF)
        pdf_content = base64.b64encode(b'%PDF-1.4\n1 0 obj\n<<>>\nendobj\ntrailer\n<<>>\n%%EOF').decode('utf-8')

        # Create the request
        request = CreateSignatureSessionRequest(
            return_url='http://localhost:8000/callback'
        )

        # Call the API
        response = rest_pki_client.create_signature_session(create_signature_session_request=request)

        # Assert the response
        self.assertIsNotNone(response)
        self.assertIsNotNone(response.session_id)
        self.assertIsNotNone(response.redirect_url)
        self.assertTrue(response.redirect_url.startswith('http'))

        # Print the redirect URL for manual testing
        print(f"\nPlease visit this URL to complete the signature: {response.redirect_url}")
        print("The callback server is running at http://localhost:8000/callback")
        print("Press Ctrl+C to stop the test when done\n")

        # Wait for callback (with timeout)
        timeout = 300  # 5 minutes timeout
        start_time = time.time()
        while not CallbackHandler.callback_received:
            if time.time() - start_time > timeout:
                self.fail("Timeout waiting for callback")
            time.sleep(1)

        # Verify callback data
        self.assertTrue(CallbackHandler.callback_received)
        self.assertIsNotNone(CallbackHandler.callback_data)
        print(f"Callback received with data: {CallbackHandler.callback_data}")


if __name__ == '__main__':
    unittest.main()
