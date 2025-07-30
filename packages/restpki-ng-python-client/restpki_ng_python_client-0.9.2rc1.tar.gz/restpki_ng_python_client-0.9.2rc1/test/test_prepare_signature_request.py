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

from restpki_ng_python_client.models.prepare_signature_request import PrepareSignatureRequest

class TestPrepareSignatureRequest(unittest.TestCase):
    """PrepareSignatureRequest unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional) -> PrepareSignatureRequest:
        """Test PrepareSignatureRequest
            include_option is a boolean, when False only required
            params are included, when True both required and
            optional params are included """
        # uncomment below to create an instance of `PrepareSignatureRequest`
        """
        model = PrepareSignatureRequest()
        if include_optional:
            return PrepareSignatureRequest(
                file = restpki_ng_python_client.models.file_reference_model.FileReferenceModel(
                    mime_type = '', 
                    content = 'YQ==', 
                    blob_token = '', 
                    url = '', 
                    name = '', 
                    length = 56, 
                    content_type = '', 
                    location = '', ),
                certificate = restpki_ng_python_client.models.certificate_reference_model.CertificateReferenceModel(
                    id = '', 
                    content = 'YQ==', ),
                document_key = '',
                security_context_id = '',
                signature_type = 'Pdf',
                cms_signature_options = restpki_ng_python_client.models.cms_signature_options.CmsSignatureOptions(
                    detached = True, 
                    data_file = restpki_ng_python_client.models.file_reference_model.FileReferenceModel(
                        mime_type = '', 
                        content = 'YQ==', 
                        blob_token = '', 
                        url = '', 
                        name = '', 
                        length = 56, 
                        content_type = '', 
                        location = '', ), 
                    data_hashes = [
                        restpki_ng_python_client.models.digest_algorithm_and_value_model.DigestAlgorithmAndValueModel(
                            algorithm = 'MD5', 
                            value = 'YQ==', 
                            hex_value = '', )
                        ], ),
                pdf_signature_options = restpki_ng_python_client.models.pdf_signature_options.PdfSignatureOptions(
                    visual_representation = restpki_ng_python_client.models.pades_visual_representation_model.PadesVisualRepresentationModel(
                        text = restpki_ng_python_client.models.pades_visual_text_model.PadesVisualTextModel(
                            font_size = 1.337, 
                            include_signing_time = True, 
                            horizontal_align = 'Left', 
                            container = restpki_ng_python_client.models.pades_visual_rectangle_model.PadesVisualRectangleModel(
                                left = 1.337, 
                                top = 1.337, 
                                right = 1.337, 
                                bottom = 1.337, 
                                width = 1.337, 
                                height = 1.337, ), ), 
                        image = restpki_ng_python_client.models.pades_visual_image_model.PadesVisualImageModel(
                            resource = restpki_ng_python_client.models.resource_content_or_reference.ResourceContentOrReference(
                                url = '', 
                                content = 'YQ==', 
                                mime_type = '', ), 
                            opacity = 56, 
                            vertical_align = 'Top', ), 
                        position = restpki_ng_python_client.models.pades_visual_positioning_model.PadesVisualPositioningModel(
                            page_number = 56, 
                            measurement_units = 'Centimeters', 
                            page_optimization = restpki_ng_python_client.models.pades_page_optimization_model.PadesPageOptimizationModel(
                                paper_size = 'Custom', 
                                custom_paper_size = restpki_ng_python_client.models.pades_size_model.PadesSizeModel(
                                    height = 1.337, 
                                    width = 1.337, ), 
                                page_orientation = 'Auto', ), 
                            auto = restpki_ng_python_client.models.pades_visual_auto_positioning_model.PadesVisualAutoPositioningModel(
                                container = restpki_ng_python_client.models.pades_visual_rectangle_model.PadesVisualRectangleModel(
                                    left = 1.337, 
                                    top = 1.337, 
                                    right = 1.337, 
                                    bottom = 1.337, 
                                    width = 1.337, 
                                    height = 1.337, ), 
                                signature_rectangle_size = restpki_ng_python_client.models.pades_size_model.PadesSizeModel(
                                    height = 1.337, 
                                    width = 1.337, ), 
                                horizontal_direction = 'LeftToRight', 
                                vertical_direction = 'TopDown', 
                                row_spacing = 1.337, ), 
                            manual = , ), ), 
                    measurement_units = 'Centimeters', 
                    page_optimization = restpki_ng_python_client.models.pades_page_optimization_model.PadesPageOptimizationModel(), ),
                xml_signature_options = restpki_ng_python_client.models.xml_signature_options.XmlSignatureOptions(
                    type = 'XmlElement', 
                    element_to_sign_id = '', 
                    signature_element_location = restpki_ng_python_client.models.xml_element_location_model.XmlElementLocationModel(
                        x_path = '', 
                        namespaces = [
                            restpki_ng_python_client.models.namespace_model.NamespaceModel(
                                prefix = '', 
                                uri = '', )
                            ], 
                        insertion_option = 'AppendChild', ), )
            )
        else:
            return PrepareSignatureRequest(
                file = restpki_ng_python_client.models.file_reference_model.FileReferenceModel(
                    mime_type = '', 
                    content = 'YQ==', 
                    blob_token = '', 
                    url = '', 
                    name = '', 
                    length = 56, 
                    content_type = '', 
                    location = '', ),
                certificate = restpki_ng_python_client.models.certificate_reference_model.CertificateReferenceModel(
                    id = '', 
                    content = 'YQ==', ),
        )
        """

    def testPrepareSignatureRequest(self):
        """Test PrepareSignatureRequest"""
        # inst_req_only = self.make_instance(include_optional=False)
        # inst_req_and_optional = self.make_instance(include_optional=True)

if __name__ == '__main__':
    unittest.main()
