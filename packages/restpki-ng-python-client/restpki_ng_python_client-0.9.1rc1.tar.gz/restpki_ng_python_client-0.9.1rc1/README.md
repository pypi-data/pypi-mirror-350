# restpki_ng_python_client
<b><i>Para Português, <a href=\"https://docs.lacunasoftware.com/pt-br/articles/rest-pki/core/integration/get-started\">clique aqui</a></i></b>
<p>
 <a href=\"https://docs.lacunasoftware.com/en-us/articles/rest-pki/core/\">Rest PKI Core</a> is an upcoming version of
 <a href=\"https://docs.lacunasoftware.com/en-us/articles/rest-pki/\">Rest PKI</a> that will have extended compatibility with environments and databases.
</p>
<p>
 In addition to Windows Server (which is already supported by Rest PKI), Rest PKI Core will also run on <b>Linux</b> (Debian- and RedHat-based distributions)
 and on <b>Docker</b>. As for database servers, in addition to SQL Server, <b>PostgreSQL</b> will also be supported.
</p>
<p>
 <b>Before getting started, see the integration overview on the <a href=\"https://docs.lacunasoftware.com/en-us/articles/rest-pki/core/integration/\">Integration Guide</a></b>
</p>
<p>
 For questions regarding the usage of this API, please reach us at <a href=\"https://lacuna.help/\">lacuna.help</a>
</p>

<h2>Parameters</h2>
<p>
 You will need the following parameters:
</p>
<ul>
 <li><b>Endpoint</b>: address of the Rest PKI Core instance that will be used</li>
 <li><b>API Key</b>: authorization key for using the API</li>
</ul>
<p>
 The <span class=\"model\">endpoint</span> must be prefixed to all relative URLs mentioned here. As for the <span class=\"model\">API Key</span>, see how to use it below.
</p>

<h2>Authentication</h2>
<p>
 The API key must be sent on the <span class=\"model\">X-Api-Key</span> header on each request:
</p>

<!-- unfortunately, class \"example microlight\" doesn't seem to work here -->
<pre style=\"font-size: 12px; padding: 10px; border-radius: 4px; background: #41444e; font-weight: 600; color: #fff;\">
X-Api-Key: yourapp|xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
</pre>

<h2>HTTP Codes</h2>

<p>
 The APIs will return the following HTTP codes:
</p>

<table>
 <thead>
  <tr>
   <th>Code</th>
   <th>Description</th>
  </tr>
 </thead>
 <tbody>
  <tr>
   <td><strong class=\"model-title\">200 (OK)</strong></td>
   <td>Request processed successfully. The response is different for each API, please refer to the operation's documentation</td>
  </tr>
  <tr>
   <td><strong class=\"model-title\">400 (Bad Request)</strong></td>
   <td>Syntax error. For instance, when a required field was not provided</td>
  </tr>
  <tr>
   <td><strong class=\"model-title\">401 (Unauthorized)</strong></td>
   <td>API key not provided or invalid</td>
  </tr>
  <tr>
   <td><strong class=\"model-title\">403 (Forbidden)</strong></td>
   <td>API key is valid, but the application has insufficient permissions to complete the requested operation</td>
  </tr>
  <tr>
   <td><strong class=\"model-title\">422 (Unprocessable Entity)</strong></td>
   <td>API error. The response body is an <a href=\"#model-ErrorModelV2\" class=\"model\">ErrorModelV2</a>
  </tr>
  <tr>
   <td><strong class=\"model-title\">500 (Internal Server Error)</strong></td>
   <td>An unexpected error occurred. The <span class=\"model\">exceptionCode</span> contained on the response body may be of help for our support team during diagnostic.</td>
  </tr>
 </tbody>
</table>

<h3>Error Codes</h3>

<p>
 Some of the error codes returned in the <span class=\"model\">code</span> field of an <a href=\"#model-ErrorModelV2\" class=\"model\">ErrorModelV2</a>
 (body of responses with HTTP status code 422) are provided below*:
</p>

<table>
 <thead>
  <tr>
   <th>Code</th>
   <th>Description</th>
  </tr>
 </thead>
 <tbody>
  <tr>
   <td class=\"model\">DocumentNotFound</td>
   <td>A referenced document was not found (check the document ID)</td>
  </tr>
  <tr>
   <td class=\"model\">SecurityContextNotFound</td>
   <td>A referenced security context was not found (check the security context ID)</td>
  </tr>
  <tr>
   <td class=\"model\">SignatureSessionNotFound</td>
   <td>A referenced signature session was not found (check the signature session ID)</td>
  </tr>
  <tr>
   <td class=\"model\">BadSignatureSessionOperation</td>
   <td>The operation is invalid for the current signature session or document status. For instance, trying to await the session's completion if it is still <span class=\"model\">Pending</span> results in this error</td>
  </tr>
  <tr>
   <td class=\"model\">BackgroundProcessing</td>
   <td>The operation cannot be completed at this time because the resource is being processed in background</td>
  </tr>
  <tr>
   <td class=\"model\">SignatureSessionTokenRequired</td>
   <td>The signature session token was not passed on the <span class=\"model\">X-Signature-Session-Token</span> request header</td>
  </tr>
  <tr>
   <td class=\"model\">BadSignatureSessionToken</td>
   <td>An invalid signature session token was passed on the <span class=\"model\">X-Signature-Session-Token</span> request header. Check your application for possible corruption of the session token, which may contain characters <span class=\"code\">-</span> (hyphen) and <span class=\"code\">_</span> (underscore)</td>
  </tr>
  <tr>
   <td class=\"model\">ExpiredSignatureSessionToken</td>
   <td>An expired signature session token was passed on the <span class=\"model\">X-Signature-Session-Token</span> request header. Signature session tokens are normally valid for 4 hours.</td>
  </tr>
 </tbody>
</table>

<p style=\"font-size: 0.9em\">
 *The codes shown above are the most common error codes. Nonetheless, this list is not comprehensive. New codes may be added anytime without previous warning.
</p>

<h2>Culture / Internationalization (i18n)</h2>
<p>The <span class=\"model\">Accept-Language</span> request header is observed by this API. The following cultures are supported:</p>
<ul>
 <li><span class=\"code\">en-US</span> (or simply <span class=\"code\">en</span>)</li>
 <li><span class=\"code\">pt-BR</span> (or simply <span class=\"code\">pt</span>)</li>
</ul>
<p><i>Notice: error messages are not affected by this header and therefore should not be displayed to users, being better suited for logging.</i></p>


This Python package is automatically generated by the [OpenAPI Generator](https://openapi-generator.tech) project:

- API version: 2.2.2
- Package version: 0.9.1-rc1
- Build package: org.openapitools.codegen.languages.PythonClientCodegen

## Requirements.

Python 3.7+

## Installation & Usage
### pip install

If the python package is hosted on a repository, you can install directly using:

```sh
pip install git+https://github.com/GIT_USER_ID/GIT_REPO_ID.git
```
(you may need to run `pip` with root permission: `sudo pip install git+https://github.com/GIT_USER_ID/GIT_REPO_ID.git`)

Then import the package:
```python
import restpki_ng_python_client
```

### Setuptools

Install via [Setuptools](http://pypi.python.org/pypi/setuptools).

```sh
python setup.py install --user
```
(or `sudo python setup.py install` to install the package for all users)

Then import the package:
```python
import restpki_ng_python_client
```

### Tests

Execute `pytest` to run the tests.

## Getting Started

Please follow the [installation procedure](#installation--usage) and then run the following:

```python

import time
import restpki_ng_python_client
from restpki_ng_python_client.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = restpki_ng_python_client.Configuration(
    host = "http://localhost"
)



# Enter a context with an instance of the API client
with restpki_ng_python_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = restpki_ng_python_client.AuthenticationApi(api_client)

    try:
        api_response = api_instance.api_authentication_get()
        print("The response of AuthenticationApi->api_authentication_get:\n")
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling AuthenticationApi->api_authentication_get: %s\n" % e)

```

## Documentation for API Endpoints

All URIs are relative to *http://localhost*

Class | Method | HTTP request | Description
------------ | ------------- | ------------- | -------------
*AuthenticationApi* | [**api_authentication_get**](docs/AuthenticationApi.md#api_authentication_get) | **GET** /Api/Authentication | 
*AuthenticationApi* | [**api_authentication_post**](docs/AuthenticationApi.md#api_authentication_post) | **POST** /Api/Authentication | 
*AuthenticationApi* | [**api_authentications_post**](docs/AuthenticationApi.md#api_authentications_post) | **POST** /Api/Authentications | 
*AuthenticationApi* | [**api_authentications_token_finalize_post**](docs/AuthenticationApi.md#api_authentications_token_finalize_post) | **POST** /Api/Authentications/{token}/Finalize | 
*AuthenticationApi* | [**api_authentications_token_signed_bytes_post**](docs/AuthenticationApi.md#api_authentications_token_signed_bytes_post) | **POST** /Api/Authentications/{token}/SignedBytes | 
*AuthenticationApi* | [**api_v2_authentication_completion_post**](docs/AuthenticationApi.md#api_v2_authentication_completion_post) | **POST** /api/v2/authentication/completion | Completes a certificate authentication
*AuthenticationApi* | [**api_v2_authentication_post**](docs/AuthenticationApi.md#api_v2_authentication_post) | **POST** /api/v2/authentication | Prepares for a certificate authentication
*CadesSignatureApi* | [**api_cades_signatures_open_post**](docs/CadesSignatureApi.md#api_cades_signatures_open_post) | **POST** /Api/CadesSignatures/Open | 
*CadesSignatureApi* | [**api_cades_signatures_post**](docs/CadesSignatureApi.md#api_cades_signatures_post) | **POST** /Api/CadesSignatures | 
*CadesSignatureApi* | [**api_cades_signatures_required_hashes_post**](docs/CadesSignatureApi.md#api_cades_signatures_required_hashes_post) | **POST** /Api/CadesSignatures/RequiredHashes | 
*CadesSignatureApi* | [**api_cades_signatures_token_finalize_post**](docs/CadesSignatureApi.md#api_cades_signatures_token_finalize_post) | **POST** /Api/CadesSignatures/{token}/Finalize | 
*CadesSignatureApi* | [**api_cades_signatures_token_signed_bytes_post**](docs/CadesSignatureApi.md#api_cades_signatures_token_signed_bytes_post) | **POST** /Api/CadesSignatures/{token}/SignedBytes | 
*CadesSignatureApi* | [**api_v2_cades_signatures_post**](docs/CadesSignatureApi.md#api_v2_cades_signatures_post) | **POST** /Api/v2/CadesSignatures | 
*CadesSignatureApi* | [**api_v2_cades_signatures_token_signed_bytes_post**](docs/CadesSignatureApi.md#api_v2_cades_signatures_token_signed_bytes_post) | **POST** /Api/v2/CadesSignatures/{token}/SignedBytes | 
*CadesSignatureApi* | [**api_v3_cades_signatures_post**](docs/CadesSignatureApi.md#api_v3_cades_signatures_post) | **POST** /Api/v3/CadesSignatures | 
*DocumentKeysApi* | [**api_document_keys_batch_post**](docs/DocumentKeysApi.md#api_document_keys_batch_post) | **POST** /api/document-keys/batch | Allocates a batch of document keys to be used later on document signatures
*DocumentKeysApi* | [**api_document_keys_key_get**](docs/DocumentKeysApi.md#api_document_keys_key_get) | **GET** /api/document-keys/{key} | Queries documents by key
*DocumentKeysApi* | [**api_document_keys_post**](docs/DocumentKeysApi.md#api_document_keys_post) | **POST** /api/document-keys | Allocates a document key to be used later on a document signature
*DocumentKeysApi* | [**api_document_keys_unused_get**](docs/DocumentKeysApi.md#api_document_keys_unused_get) | **GET** /api/document-keys/unused | Queries unused document keys
*DocumentsApi* | [**api_documents_id_get**](docs/DocumentsApi.md#api_documents_id_get) | **GET** /api/documents/{id} | Retrieves a document&#39;s details
*DocumentsApi* | [**api_documents_id_signers_get**](docs/DocumentsApi.md#api_documents_id_signers_get) | **GET** /api/documents/{id}/signers | Retrieves the full information about each of a document&#39;s signers
*DocumentsApi* | [**api_documents_keys_key_get**](docs/DocumentsApi.md#api_documents_keys_key_get) | **GET** /api/documents/keys/{key} | Finds a document&#39;s details by its key
*PadesSignatureApi* | [**api_pades_signatures_open_post**](docs/PadesSignatureApi.md#api_pades_signatures_open_post) | **POST** /Api/PadesSignatures/Open | 
*PadesSignatureApi* | [**api_pades_signatures_post**](docs/PadesSignatureApi.md#api_pades_signatures_post) | **POST** /Api/PadesSignatures | 
*PadesSignatureApi* | [**api_pades_signatures_token_finalize_post**](docs/PadesSignatureApi.md#api_pades_signatures_token_finalize_post) | **POST** /Api/PadesSignatures/{token}/Finalize | 
*PadesSignatureApi* | [**api_pades_signatures_token_signed_bytes_post**](docs/PadesSignatureApi.md#api_pades_signatures_token_signed_bytes_post) | **POST** /Api/PadesSignatures/{token}/SignedBytes | 
*PadesSignatureApi* | [**api_v2_pades_signatures_post**](docs/PadesSignatureApi.md#api_v2_pades_signatures_post) | **POST** /Api/v2/PadesSignatures | 
*PadesSignatureApi* | [**api_v2_pades_signatures_token_signed_bytes_post**](docs/PadesSignatureApi.md#api_v2_pades_signatures_token_signed_bytes_post) | **POST** /Api/v2/PadesSignatures/{token}/SignedBytes | 
*PadesVisualPositioningPresetsApi* | [**api_pades_visual_positioning_presets_footnote_bottom_up_get**](docs/PadesVisualPositioningPresetsApi.md#api_pades_visual_positioning_presets_footnote_bottom_up_get) | **GET** /Api/PadesVisualPositioningPresets/FootnoteBottomUp | 
*PadesVisualPositioningPresetsApi* | [**api_pades_visual_positioning_presets_footnote_get**](docs/PadesVisualPositioningPresetsApi.md#api_pades_visual_positioning_presets_footnote_get) | **GET** /Api/PadesVisualPositioningPresets/Footnote | 
*PadesVisualPositioningPresetsApi* | [**api_pades_visual_positioning_presets_new_page_get**](docs/PadesVisualPositioningPresetsApi.md#api_pades_visual_positioning_presets_new_page_get) | **GET** /Api/PadesVisualPositioningPresets/NewPage | 
*PdfApi* | [**api_pdf_add_marks_post**](docs/PdfApi.md#api_pdf_add_marks_post) | **POST** /Api/Pdf/AddMarks | 
*PdfApi* | [**api_pdf_stamp_post**](docs/PdfApi.md#api_pdf_stamp_post) | **POST** /api/pdf/stamp | 
*SignatureApi* | [**api_signature_completion_post**](docs/SignatureApi.md#api_signature_completion_post) | **POST** /api/signature/completion | 
*SignatureApi* | [**api_signature_post**](docs/SignatureApi.md#api_signature_post) | **POST** /api/signature | 
*SignatureInspectionApi* | [**api_signature_inspection_put**](docs/SignatureInspectionApi.md#api_signature_inspection_put) | **PUT** /api/signature-inspection | Inspects a signed file, returning information about its signers and metadata about the corresponding document (if signed on this instance)
*SignatureSessionsApi* | [**api_signature_sessions_id_get**](docs/SignatureSessionsApi.md#api_signature_sessions_id_get) | **GET** /api/signature-sessions/{id} | Retrieves a signature session&#39;s details
*SignatureSessionsApi* | [**api_signature_sessions_id_when_completed_get**](docs/SignatureSessionsApi.md#api_signature_sessions_id_when_completed_get) | **GET** /api/signature-sessions/{id}/when-completed | Waits for the completion of a signature session
*SignatureSessionsApi* | [**api_signature_sessions_post**](docs/SignatureSessionsApi.md#api_signature_sessions_post) | **POST** /api/signature-sessions | Creates a signature session
*TimestampApi* | [**api_timestamp_plans_identifier_issue_post**](docs/TimestampApi.md#api_timestamp_plans_identifier_issue_post) | **POST** /Api/TimestampPlans/{identifier}/Issue | 
*TimestampApi* | [**api_tsp_identifier_post**](docs/TimestampApi.md#api_tsp_identifier_post) | **POST** /api/tsp/{identifier} | 
*UploadApi* | [**api_multipart_uploads_post**](docs/UploadApi.md#api_multipart_uploads_post) | **POST** /Api/MultipartUploads | 
*UploadApi* | [**api_multipart_uploads_token_part_number_post**](docs/UploadApi.md#api_multipart_uploads_token_part_number_post) | **POST** /Api/MultipartUploads/{token}/{partNumber} | 
*UploadApi* | [**api_multipart_uploads_token_post**](docs/UploadApi.md#api_multipart_uploads_token_post) | **POST** /Api/MultipartUploads/{token} | 
*UploadApi* | [**api_plain_uploads_post**](docs/UploadApi.md#api_plain_uploads_post) | **POST** /api/plain-uploads | 
*XmlSignatureApi* | [**api_v2_xml_signatures_open_post**](docs/XmlSignatureApi.md#api_v2_xml_signatures_open_post) | **POST** /Api/v2/XmlSignatures/Open | 
*XmlSignatureApi* | [**api_xml_signatures_full_xml_signature_post**](docs/XmlSignatureApi.md#api_xml_signatures_full_xml_signature_post) | **POST** /Api/XmlSignatures/FullXmlSignature | 
*XmlSignatureApi* | [**api_xml_signatures_open_post**](docs/XmlSignatureApi.md#api_xml_signatures_open_post) | **POST** /Api/XmlSignatures/Open | 
*XmlSignatureApi* | [**api_xml_signatures_token_finalize_post**](docs/XmlSignatureApi.md#api_xml_signatures_token_finalize_post) | **POST** /Api/XmlSignatures/{token}/Finalize | 
*XmlSignatureApi* | [**api_xml_signatures_token_signed_bytes_post**](docs/XmlSignatureApi.md#api_xml_signatures_token_signed_bytes_post) | **POST** /Api/XmlSignatures/{token}/SignedBytes | 
*XmlSignatureApi* | [**api_xml_signatures_xml_element_signature_post**](docs/XmlSignatureApi.md#api_xml_signatures_xml_element_signature_post) | **POST** /Api/XmlSignatures/XmlElementSignature | 


## Documentation For Models

 - [AllocateDocumentKeyBatchRequest](docs/AllocateDocumentKeyBatchRequest.md)
 - [AllocateDocumentKeyRequest](docs/AllocateDocumentKeyRequest.md)
 - [AttributeCertificateModel](docs/AttributeCertificateModel.md)
 - [AuditPackageOptions](docs/AuditPackageOptions.md)
 - [AuthenticationFailures](docs/AuthenticationFailures.md)
 - [AuthenticationGetResponse](docs/AuthenticationGetResponse.md)
 - [AuthenticationPostRequest](docs/AuthenticationPostRequest.md)
 - [AuthenticationPostResponse](docs/AuthenticationPostResponse.md)
 - [AuthenticationsPostRequest](docs/AuthenticationsPostRequest.md)
 - [AuthenticationsPostResponse](docs/AuthenticationsPostResponse.md)
 - [AuthenticationsPostSignedBytesRequest](docs/AuthenticationsPostSignedBytesRequest.md)
 - [AuthenticationsPostSignedBytesResponse](docs/AuthenticationsPostSignedBytesResponse.md)
 - [AutoPositioningHorizontalDirections](docs/AutoPositioningHorizontalDirections.md)
 - [AutoPositioningVerticalDirections](docs/AutoPositioningVerticalDirections.md)
 - [Blockchains](docs/Blockchains.md)
 - [CadesSignatureModel](docs/CadesSignatureModel.md)
 - [CadesSignaturePostRequestV1](docs/CadesSignaturePostRequestV1.md)
 - [CadesSignaturePostRequestV2](docs/CadesSignaturePostRequestV2.md)
 - [CadesSignaturePostRequestV3](docs/CadesSignaturePostRequestV3.md)
 - [CadesSignaturePostResponse](docs/CadesSignaturePostResponse.md)
 - [CadesSignaturePostSignedBytesRequest](docs/CadesSignaturePostSignedBytesRequest.md)
 - [CadesSignaturePostSignedBytesResponse](docs/CadesSignaturePostSignedBytesResponse.md)
 - [CadesSignerModel](docs/CadesSignerModel.md)
 - [CadesTimestampModel](docs/CadesTimestampModel.md)
 - [CertificateModel](docs/CertificateModel.md)
 - [CertificateReferenceModel](docs/CertificateReferenceModel.md)
 - [CertificateRequirement](docs/CertificateRequirement.md)
 - [CertificateRequirementTypes](docs/CertificateRequirementTypes.md)
 - [CertificateSummary](docs/CertificateSummary.md)
 - [CertifiedAttributeModel](docs/CertifiedAttributeModel.md)
 - [CertifiedAttributeTypes](docs/CertifiedAttributeTypes.md)
 - [CmsContentTypes](docs/CmsContentTypes.md)
 - [CmsSignatureOptions](docs/CmsSignatureOptions.md)
 - [ColorModel](docs/ColorModel.md)
 - [CommitmentTypeModel](docs/CommitmentTypeModel.md)
 - [CompleteAuthenticationRequest](docs/CompleteAuthenticationRequest.md)
 - [CompleteAuthenticationResponse](docs/CompleteAuthenticationResponse.md)
 - [CompleteSignatureRequest](docs/CompleteSignatureRequest.md)
 - [CompleteSignatureRequestV2](docs/CompleteSignatureRequestV2.md)
 - [CreateSignatureSessionRequest](docs/CreateSignatureSessionRequest.md)
 - [CreateSignatureSessionResponse](docs/CreateSignatureSessionResponse.md)
 - [DigestAlgorithmAndValueModel](docs/DigestAlgorithmAndValueModel.md)
 - [DigestAlgorithms](docs/DigestAlgorithms.md)
 - [DocumentFileModel](docs/DocumentFileModel.md)
 - [DocumentKeyModel](docs/DocumentKeyModel.md)
 - [DocumentKeyQueryResponse](docs/DocumentKeyQueryResponse.md)
 - [DocumentKeySummary](docs/DocumentKeySummary.md)
 - [DocumentModel](docs/DocumentModel.md)
 - [DocumentQueryResponse](docs/DocumentQueryResponse.md)
 - [DocumentStatus](docs/DocumentStatus.md)
 - [DocumentSummary](docs/DocumentSummary.md)
 - [ErrorModelV2](docs/ErrorModelV2.md)
 - [FileModel](docs/FileModel.md)
 - [FileReferenceModel](docs/FileReferenceModel.md)
 - [FullXmlSignaturePostRequest](docs/FullXmlSignaturePostRequest.md)
 - [GeneralNameChoices](docs/GeneralNameChoices.md)
 - [GeneralNameModel](docs/GeneralNameModel.md)
 - [HolderTypes](docs/HolderTypes.md)
 - [InspectSignatureFailures](docs/InspectSignatureFailures.md)
 - [InspectSignatureRequest](docs/InspectSignatureRequest.md)
 - [InspectSignatureResponse](docs/InspectSignatureResponse.md)
 - [MultipartUploadBeginResponse](docs/MultipartUploadBeginResponse.md)
 - [MultipartUploadEndRequest](docs/MultipartUploadEndRequest.md)
 - [NameModel](docs/NameModel.md)
 - [NamespaceModel](docs/NamespaceModel.md)
 - [OpenCadesSignatureRequestModel](docs/OpenCadesSignatureRequestModel.md)
 - [OpenSignatureRequestModel](docs/OpenSignatureRequestModel.md)
 - [OpenXmlSignatureRequestModel](docs/OpenXmlSignatureRequestModel.md)
 - [OtherNameModel](docs/OtherNameModel.md)
 - [PadesCertificationLevel](docs/PadesCertificationLevel.md)
 - [PadesHorizontalAlign](docs/PadesHorizontalAlign.md)
 - [PadesMeasurementUnits](docs/PadesMeasurementUnits.md)
 - [PadesPageOptimizationModel](docs/PadesPageOptimizationModel.md)
 - [PadesSignatureModel](docs/PadesSignatureModel.md)
 - [PadesSignaturePostRequestV1](docs/PadesSignaturePostRequestV1.md)
 - [PadesSignaturePostRequestV2](docs/PadesSignaturePostRequestV2.md)
 - [PadesSignaturePostResponse](docs/PadesSignaturePostResponse.md)
 - [PadesSignaturePostSignedBytesRequest](docs/PadesSignaturePostSignedBytesRequest.md)
 - [PadesSignaturePostSignedBytesResponse](docs/PadesSignaturePostSignedBytesResponse.md)
 - [PadesSignerModel](docs/PadesSignerModel.md)
 - [PadesSizeModel](docs/PadesSizeModel.md)
 - [PadesTextHorizontalAlign](docs/PadesTextHorizontalAlign.md)
 - [PadesVerticalAlign](docs/PadesVerticalAlign.md)
 - [PadesVisualAutoPositioningModel](docs/PadesVisualAutoPositioningModel.md)
 - [PadesVisualImageModel](docs/PadesVisualImageModel.md)
 - [PadesVisualPositioningModel](docs/PadesVisualPositioningModel.md)
 - [PadesVisualRectangleModel](docs/PadesVisualRectangleModel.md)
 - [PadesVisualRepresentationModel](docs/PadesVisualRepresentationModel.md)
 - [PadesVisualTextModel](docs/PadesVisualTextModel.md)
 - [PageOrientations](docs/PageOrientations.md)
 - [PaperSizes](docs/PaperSizes.md)
 - [PdfAddMarksRequest](docs/PdfAddMarksRequest.md)
 - [PdfAddMarksResponse](docs/PdfAddMarksResponse.md)
 - [PdfMarkElementModel](docs/PdfMarkElementModel.md)
 - [PdfMarkElementType](docs/PdfMarkElementType.md)
 - [PdfMarkImageModel](docs/PdfMarkImageModel.md)
 - [PdfMarkModel](docs/PdfMarkModel.md)
 - [PdfMarkPageOptions](docs/PdfMarkPageOptions.md)
 - [PdfSignatureOptions](docs/PdfSignatureOptions.md)
 - [PdfTextSectionModel](docs/PdfTextSectionModel.md)
 - [PdfTextStyle](docs/PdfTextStyle.md)
 - [PkiBrazilCertificateModel](docs/PkiBrazilCertificateModel.md)
 - [PkiBrazilCertificateTypes](docs/PkiBrazilCertificateTypes.md)
 - [PkiItalyCertificateModel](docs/PkiItalyCertificateModel.md)
 - [PkiItalyCertificateTypes](docs/PkiItalyCertificateTypes.md)
 - [PrepareAuthenticationRequest](docs/PrepareAuthenticationRequest.md)
 - [PrepareAuthenticationResponse](docs/PrepareAuthenticationResponse.md)
 - [PrepareSignatureFailures](docs/PrepareSignatureFailures.md)
 - [PrepareSignatureRequest](docs/PrepareSignatureRequest.md)
 - [PrepareSignatureResponse](docs/PrepareSignatureResponse.md)
 - [ResourceContentOrReference](docs/ResourceContentOrReference.md)
 - [RoleAttributeModel](docs/RoleAttributeModel.md)
 - [SessionCompletionStatus](docs/SessionCompletionStatus.md)
 - [SignatureAlgorithmAndValueModel](docs/SignatureAlgorithmAndValueModel.md)
 - [SignatureAlgorithmIdentifier](docs/SignatureAlgorithmIdentifier.md)
 - [SignatureAlgorithms](docs/SignatureAlgorithms.md)
 - [SignatureBStampModel](docs/SignatureBStampModel.md)
 - [SignaturePolicyIdentifierModel](docs/SignaturePolicyIdentifierModel.md)
 - [SignatureResultModel](docs/SignatureResultModel.md)
 - [SignatureSessionDocumentData](docs/SignatureSessionDocumentData.md)
 - [SignatureSessionDocumentSummary](docs/SignatureSessionDocumentSummary.md)
 - [SignatureSessionModel](docs/SignatureSessionModel.md)
 - [SignatureSessionStatus](docs/SignatureSessionStatus.md)
 - [SignatureTypes](docs/SignatureTypes.md)
 - [SignerBStampModel](docs/SignerBStampModel.md)
 - [SignerModel](docs/SignerModel.md)
 - [SignerSummary](docs/SignerSummary.md)
 - [StampPdfRequest](docs/StampPdfRequest.md)
 - [StampPdfResponse](docs/StampPdfResponse.md)
 - [TimestampIssueResponse](docs/TimestampIssueResponse.md)
 - [ValidationItemModel](docs/ValidationItemModel.md)
 - [ValidationItemTypes](docs/ValidationItemTypes.md)
 - [ValidationResultsModel](docs/ValidationResultsModel.md)
 - [WebhookEventModel](docs/WebhookEventModel.md)
 - [WebhookEventTypes](docs/WebhookEventTypes.md)
 - [XmlAttributeModel](docs/XmlAttributeModel.md)
 - [XmlElementLocationModel](docs/XmlElementLocationModel.md)
 - [XmlElementModel](docs/XmlElementModel.md)
 - [XmlElementSignaturePostRequest](docs/XmlElementSignaturePostRequest.md)
 - [XmlIdAttributeModel](docs/XmlIdAttributeModel.md)
 - [XmlIdResolutionTableModel](docs/XmlIdResolutionTableModel.md)
 - [XmlInsertionOptions](docs/XmlInsertionOptions.md)
 - [XmlNodeNameModel](docs/XmlNodeNameModel.md)
 - [XmlSignatureModel](docs/XmlSignatureModel.md)
 - [XmlSignatureOptions](docs/XmlSignatureOptions.md)
 - [XmlSignaturePostResponse](docs/XmlSignaturePostResponse.md)
 - [XmlSignaturePostSignedBytesRequest](docs/XmlSignaturePostSignedBytesRequest.md)
 - [XmlSignaturePostSignedBytesResponse](docs/XmlSignaturePostSignedBytesResponse.md)
 - [XmlSignatureResponseModel](docs/XmlSignatureResponseModel.md)
 - [XmlSignatureTypes](docs/XmlSignatureTypes.md)
 - [XmlSignedEntityTypes](docs/XmlSignedEntityTypes.md)


<a id="documentation-for-authorization"></a>
## Documentation For Authorization

Endpoints do not require authorization.


## Author




