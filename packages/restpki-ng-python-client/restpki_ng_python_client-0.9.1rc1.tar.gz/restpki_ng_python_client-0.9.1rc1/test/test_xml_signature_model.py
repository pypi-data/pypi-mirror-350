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

from restpki_ng_python_client.models.xml_signature_model import XmlSignatureModel

class TestXmlSignatureModel(unittest.TestCase):
    """XmlSignatureModel unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional) -> XmlSignatureModel:
        """Test XmlSignatureModel
            include_option is a boolean, when False only required
            params are included, when True both required and
            optional params are included """
        # uncomment below to create an instance of `XmlSignatureModel`
        """
        model = XmlSignatureModel()
        if include_optional:
            return XmlSignatureModel(
                type = 'FullXml',
                signed_element = restpki_ng_python_client.models.xml_element_model.XmlElementModel(
                    local_name = '', 
                    attributes = [
                        restpki_ng_python_client.models.xml_attribute_model.XmlAttributeModel(
                            local_name = '', 
                            value = '', 
                            namespace_uri = '', )
                        ], 
                    namespace_uri = '', ),
                signature = restpki_ng_python_client.models.signature_algorithm_and_value_model.SignatureAlgorithmAndValueModel(
                    algorithm_identifier = restpki_ng_python_client.models.signature_algorithm_identifier.SignatureAlgorithmIdentifier(
                        algorithm = 'MD5WithRSA', ), 
                    value = 'YQ==', 
                    hex_value = '', ),
                signature_policy = restpki_ng_python_client.models.signature_policy_identifier_model.SignaturePolicyIdentifierModel(
                    digest = restpki_ng_python_client.models.digest_algorithm_and_value_model.DigestAlgorithmAndValueModel(
                        algorithm = 'MD5', 
                        value = 'YQ==', 
                        hex_value = '', ), 
                    oid = '', 
                    uri = '', ),
                certificate = restpki_ng_python_client.models.certificate_model.CertificateModel(
                    subject_name = restpki_ng_python_client.models.name_model.NameModel(
                        country = '', 
                        organization = '', 
                        organization_unit = '', 
                        dn_qualifier = '', 
                        state_name = '', 
                        common_name = '', 
                        serial_number = '', 
                        locality = '', 
                        title = '', 
                        surname = '', 
                        given_name = '', 
                        initials = '', 
                        pseudonym = '', 
                        generation_qualifier = '', 
                        email_address = '', 
                        all_values = {
                            'key' : [
                                ''
                                ]
                            }, 
                        dn_string = '', ), 
                    issuer_name = restpki_ng_python_client.models.name_model.NameModel(
                        country = '', 
                        organization = '', 
                        organization_unit = '', 
                        dn_qualifier = '', 
                        state_name = '', 
                        common_name = '', 
                        serial_number = '', 
                        locality = '', 
                        title = '', 
                        surname = '', 
                        given_name = '', 
                        initials = '', 
                        pseudonym = '', 
                        generation_qualifier = '', 
                        email_address = '', 
                        dn_string = '', ), 
                    issuer_display_name = '', 
                    serial_number = '', 
                    validity_start = datetime.datetime.strptime('2013-10-20 19:20:30.00', '%Y-%m-%d %H:%M:%S.%f'), 
                    validity_end = datetime.datetime.strptime('2013-10-20 19:20:30.00', '%Y-%m-%d %H:%M:%S.%f'), 
                    issuer = restpki_ng_python_client.models.certificate_model.CertificateModel(
                        issuer_display_name = '', 
                        serial_number = '', 
                        validity_start = datetime.datetime.strptime('2013-10-20 19:20:30.00', '%Y-%m-%d %H:%M:%S.%f'), 
                        validity_end = datetime.datetime.strptime('2013-10-20 19:20:30.00', '%Y-%m-%d %H:%M:%S.%f'), 
                        pki_brazil = restpki_ng_python_client.models.pki_brazil_certificate_model.PkiBrazilCertificateModel(
                            certificate_type = 'Unknown', 
                            cpf = '', 
                            cnpj = '', 
                            responsavel = '', 
                            date_of_birth = '', 
                            company_name = '', 
                            oab_uf = '', 
                            oab_numero = '', 
                            rg_emissor = '', 
                            rg_emissor_uf = '', 
                            rg_numero = '', ), 
                        pki_italy = restpki_ng_python_client.models.pki_italy_certificate_model.PkiItalyCertificateModel(
                            codice_fiscale = '', 
                            id_carta = '', ), 
                        binary_thumbprint_sha256 = 'YQ==', 
                        thumbprint = '', 
                        thumbprint_sha256 = '', 
                        subject_common_name = '', 
                        subject_display_name = '', 
                        subject_identifier = '', 
                        email_address = '', 
                        organization = '', 
                        organization_identifier = '', ), 
                    pki_brazil = restpki_ng_python_client.models.pki_brazil_certificate_model.PkiBrazilCertificateModel(
                        cpf = '', 
                        cnpj = '', 
                        responsavel = '', 
                        date_of_birth = '', 
                        company_name = '', 
                        oab_uf = '', 
                        oab_numero = '', 
                        rg_emissor = '', 
                        rg_emissor_uf = '', 
                        rg_numero = '', ), 
                    pki_italy = restpki_ng_python_client.models.pki_italy_certificate_model.PkiItalyCertificateModel(
                        codice_fiscale = '', 
                        id_carta = '', ), 
                    binary_thumbprint_sha256 = 'YQ==', 
                    thumbprint = '', 
                    thumbprint_sha256 = '', 
                    subject_common_name = '', 
                    subject_display_name = '', 
                    subject_identifier = '', 
                    email_address = '', 
                    organization = '', 
                    organization_identifier = '', ),
                signing_time = datetime.datetime.strptime('2013-10-20 19:20:30.00', '%Y-%m-%d %H:%M:%S.%f'),
                certified_date_reference = datetime.datetime.strptime('2013-10-20 19:20:30.00', '%Y-%m-%d %H:%M:%S.%f'),
                timestamps = [
                    restpki_ng_python_client.models.cades_timestamp_model.CadesTimestampModel(
                        gen_time = datetime.datetime.strptime('2013-10-20 19:20:30.00', '%Y-%m-%d %H:%M:%S.%f'), 
                        serial_number = '', 
                        message_imprint = restpki_ng_python_client.models.digest_algorithm_and_value_model.DigestAlgorithmAndValueModel(
                            algorithm = 'MD5', 
                            value = 'YQ==', 
                            hex_value = '', ), 
                        encapsulated_content_type = 'Data', 
                        has_encapsulated_content = True, 
                        signers = [
                            restpki_ng_python_client.models.cades_signer_model.CadesSignerModel(
                                message_digest = restpki_ng_python_client.models.digest_algorithm_and_value_model.DigestAlgorithmAndValueModel(
                                    value = 'YQ==', 
                                    hex_value = '', ), 
                                signature = restpki_ng_python_client.models.signature_algorithm_and_value_model.SignatureAlgorithmAndValueModel(
                                    algorithm_identifier = restpki_ng_python_client.models.signature_algorithm_identifier.SignatureAlgorithmIdentifier(), 
                                    value = 'YQ==', 
                                    hex_value = '', ), 
                                signature_policy = restpki_ng_python_client.models.signature_policy_identifier_model.SignaturePolicyIdentifierModel(
                                    digest = , 
                                    oid = '', 
                                    uri = '', ), 
                                certificate = restpki_ng_python_client.models.certificate_model.CertificateModel(
                                    subject_name = restpki_ng_python_client.models.name_model.NameModel(
                                        country = '', 
                                        organization = '', 
                                        organization_unit = '', 
                                        dn_qualifier = '', 
                                        state_name = '', 
                                        common_name = '', 
                                        serial_number = '', 
                                        locality = '', 
                                        title = '', 
                                        surname = '', 
                                        given_name = '', 
                                        initials = '', 
                                        pseudonym = '', 
                                        generation_qualifier = '', 
                                        email_address = '', 
                                        all_values = {
                                            'key' : [
                                                ''
                                                ]
                                            }, 
                                        dn_string = '', ), 
                                    issuer_name = restpki_ng_python_client.models.name_model.NameModel(
                                        country = '', 
                                        organization = '', 
                                        organization_unit = '', 
                                        dn_qualifier = '', 
                                        state_name = '', 
                                        common_name = '', 
                                        serial_number = '', 
                                        locality = '', 
                                        title = '', 
                                        surname = '', 
                                        given_name = '', 
                                        initials = '', 
                                        pseudonym = '', 
                                        generation_qualifier = '', 
                                        email_address = '', 
                                        dn_string = '', ), 
                                    issuer_display_name = '', 
                                    serial_number = '', 
                                    validity_start = datetime.datetime.strptime('2013-10-20 19:20:30.00', '%Y-%m-%d %H:%M:%S.%f'), 
                                    validity_end = datetime.datetime.strptime('2013-10-20 19:20:30.00', '%Y-%m-%d %H:%M:%S.%f'), 
                                    issuer = restpki_ng_python_client.models.certificate_model.CertificateModel(
                                        issuer_display_name = '', 
                                        serial_number = '', 
                                        validity_start = datetime.datetime.strptime('2013-10-20 19:20:30.00', '%Y-%m-%d %H:%M:%S.%f'), 
                                        validity_end = datetime.datetime.strptime('2013-10-20 19:20:30.00', '%Y-%m-%d %H:%M:%S.%f'), 
                                        pki_brazil = restpki_ng_python_client.models.pki_brazil_certificate_model.PkiBrazilCertificateModel(
                                            certificate_type = 'Unknown', 
                                            cpf = '', 
                                            cnpj = '', 
                                            responsavel = '', 
                                            date_of_birth = '', 
                                            company_name = '', 
                                            oab_uf = '', 
                                            oab_numero = '', 
                                            rg_emissor = '', 
                                            rg_emissor_uf = '', 
                                            rg_numero = '', ), 
                                        pki_italy = restpki_ng_python_client.models.pki_italy_certificate_model.PkiItalyCertificateModel(
                                            codice_fiscale = '', 
                                            id_carta = '', ), 
                                        binary_thumbprint_sha256 = 'YQ==', 
                                        thumbprint = '', 
                                        thumbprint_sha256 = '', 
                                        subject_common_name = '', 
                                        subject_display_name = '', 
                                        subject_identifier = '', 
                                        email_address = '', 
                                        organization = '', 
                                        organization_identifier = '', ), 
                                    pki_brazil = restpki_ng_python_client.models.pki_brazil_certificate_model.PkiBrazilCertificateModel(
                                        cpf = '', 
                                        cnpj = '', 
                                        responsavel = '', 
                                        date_of_birth = '', 
                                        company_name = '', 
                                        oab_uf = '', 
                                        oab_numero = '', 
                                        rg_emissor = '', 
                                        rg_emissor_uf = '', 
                                        rg_numero = '', ), 
                                    pki_italy = restpki_ng_python_client.models.pki_italy_certificate_model.PkiItalyCertificateModel(
                                        codice_fiscale = '', 
                                        id_carta = '', ), 
                                    binary_thumbprint_sha256 = 'YQ==', 
                                    thumbprint = '', 
                                    thumbprint_sha256 = '', 
                                    subject_common_name = '', 
                                    subject_display_name = '', 
                                    subject_identifier = '', 
                                    email_address = '', 
                                    organization = '', 
                                    organization_identifier = '', ), 
                                signing_time = datetime.datetime.strptime('2013-10-20 19:20:30.00', '%Y-%m-%d %H:%M:%S.%f'), 
                                certified_date_reference = datetime.datetime.strptime('2013-10-20 19:20:30.00', '%Y-%m-%d %H:%M:%S.%f'), 
                                timestamps = [
                                    restpki_ng_python_client.models.cades_timestamp_model.CadesTimestampModel(
                                        gen_time = datetime.datetime.strptime('2013-10-20 19:20:30.00', '%Y-%m-%d %H:%M:%S.%f'), 
                                        serial_number = '', 
                                        has_encapsulated_content = True, 
                                        encapsulated_content = restpki_ng_python_client.models.file_model.FileModel(
                                            mime_type = '', 
                                            content = 'YQ==', 
                                            blob_token = '', 
                                            url = '', ), 
                                        audit_package = restpki_ng_python_client.models.file_model.FileModel(
                                            mime_type = '', 
                                            content = 'YQ==', 
                                            blob_token = '', 
                                            url = '', ), 
                                        b_stamp = restpki_ng_python_client.models.signature_b_stamp_model.SignatureBStampModel(
                                            document_digests = [
                                                
                                                ], 
                                            index_digests = [
                                                
                                                ], 
                                            index_file = , 
                                            blockchain = 'Bitcoin', 
                                            transaction_id = '', 
                                            block_number = 56, 
                                            block_date = datetime.datetime.strptime('2013-10-20 19:20:30.00', '%Y-%m-%d %H:%M:%S.%f'), ), )
                                    ], 
                                validation_results = restpki_ng_python_client.models.validation_results_model.ValidationResultsModel(
                                    passed_checks = [
                                        restpki_ng_python_client.models.validation_item_model.ValidationItemModel(
                                            type = 'Success', 
                                            message = '', 
                                            detail = '', 
                                            inner_validation_results = restpki_ng_python_client.models.validation_results_model.ValidationResultsModel(
                                                errors = [
                                                    restpki_ng_python_client.models.validation_item_model.ValidationItemModel(
                                                        message = '', 
                                                        detail = '', )
                                                    ], 
                                                warnings = [
                                                    
                                                    ], ), )
                                        ], 
                                    errors = [
                                        
                                        ], 
                                    warnings = [
                                        
                                        ], ), 
                                commitment_type = restpki_ng_python_client.models.commitment_type_model.CommitmentTypeModel(
                                    oid = '', 
                                    name = '', ), 
                                b_stamp = restpki_ng_python_client.models.signer_b_stamp_model.SignerBStampModel(
                                    signature_digest = , 
                                    crls_digests = [
                                        
                                        ], 
                                    certificate_digests = [
                                        
                                        ], 
                                    transaction_id = '', 
                                    transaction_date = datetime.datetime.strptime('2013-10-20 19:20:30.00', '%Y-%m-%d %H:%M:%S.%f'), ), )
                            ], 
                        encapsulated_content = , 
                        audit_package = , 
                        b_stamp = restpki_ng_python_client.models.signature_b_stamp_model.SignatureBStampModel(
                            transaction_id = '', 
                            block_number = 56, 
                            block_date = datetime.datetime.strptime('2013-10-20 19:20:30.00', '%Y-%m-%d %H:%M:%S.%f'), ), )
                    ],
                validation_results = restpki_ng_python_client.models.validation_results_model.ValidationResultsModel(
                    passed_checks = [
                        restpki_ng_python_client.models.validation_item_model.ValidationItemModel(
                            type = 'Success', 
                            message = '', 
                            detail = '', 
                            inner_validation_results = restpki_ng_python_client.models.validation_results_model.ValidationResultsModel(
                                errors = [
                                    restpki_ng_python_client.models.validation_item_model.ValidationItemModel(
                                        message = '', 
                                        detail = '', )
                                    ], 
                                warnings = [
                                    
                                    ], ), )
                        ], 
                    errors = [
                        
                        ], 
                    warnings = [
                        
                        ], ),
                b_stamp = restpki_ng_python_client.models.signer_b_stamp_model.SignerBStampModel(
                    signature_digest = restpki_ng_python_client.models.digest_algorithm_and_value_model.DigestAlgorithmAndValueModel(
                        algorithm = 'MD5', 
                        value = 'YQ==', 
                        hex_value = '', ), 
                    crls_digests = [
                        restpki_ng_python_client.models.digest_algorithm_and_value_model.DigestAlgorithmAndValueModel(
                            value = 'YQ==', 
                            hex_value = '', )
                        ], 
                    certificate_digests = [
                        
                        ], 
                    blockchain = 'Bitcoin', 
                    transaction_id = '', 
                    transaction_date = datetime.datetime.strptime('2013-10-20 19:20:30.00', '%Y-%m-%d %H:%M:%S.%f'), )
            )
        else:
            return XmlSignatureModel(
        )
        """

    def testXmlSignatureModel(self):
        """Test XmlSignatureModel"""
        # inst_req_only = self.make_instance(include_optional=False)
        # inst_req_and_optional = self.make_instance(include_optional=True)

if __name__ == '__main__':
    unittest.main()
