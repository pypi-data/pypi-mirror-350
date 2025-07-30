# coding: utf-8

"""
    Rest PKI Core API

    <b><i>Para Português, <a href=\"https://docs.lacunasoftware.com/pt-br/articles/rest-pki/core/integration/get-started\">clique aqui</a></i></b>  <p>   <a href=\"https://docs.lacunasoftware.com/en-us/articles/rest-pki/core/\">Rest PKI Core</a> is an upcoming version of   <a href=\"https://docs.lacunasoftware.com/en-us/articles/rest-pki/\">Rest PKI</a> that will have extended compatibility with environments and databases.  </p>  <p>   In addition to Windows Server (which is already supported by Rest PKI), Rest PKI Core will also run on <b>Linux</b> (Debian- and RedHat-based distributions)   and on <b>Docker</b>. As for database servers, in addition to SQL Server, <b>PostgreSQL</b> will also be supported.  </p>  <p>   <b>Before getting started, see the integration overview on the <a href=\"https://docs.lacunasoftware.com/en-us/articles/rest-pki/core/integration/\">Integration Guide</a></b>  </p>  <p>   For questions regarding the usage of this API, please reach us at <a href=\"https://lacuna.help/\">lacuna.help</a>  </p>    <h2>Parameters</h2>  <p>   You will need the following parameters:  </p>  <ul>   <li><b>Endpoint</b>: address of the Rest PKI Core instance that will be used</li>   <li><b>API Key</b>: authorization key for using the API</li>  </ul>  <p>   The <span class=\"model\">endpoint</span> must be prefixed to all relative URLs mentioned here. As for the <span class=\"model\">API Key</span>, see how to use it below.  </p>    <h2>Authentication</h2>  <p>   The API key must be sent on the <span class=\"model\">X-Api-Key</span> header on each request:  </p>    <!-- unfortunately, class \"example microlight\" doesn't seem to work here -->  <pre style=\"font-size: 12px; padding: 10px; border-radius: 4px; background: #41444e; font-weight: 600; color: #fff;\">  X-Api-Key: yourapp|xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx  </pre>    <h2>HTTP Codes</h2>    <p>   The APIs will return the following HTTP codes:  </p>    <table>   <thead>    <tr>     <th>Code</th>     <th>Description</th>    </tr>   </thead>   <tbody>    <tr>     <td><strong class=\"model-title\">200 (OK)</strong></td>     <td>Request processed successfully. The response is different for each API, please refer to the operation's documentation</td>    </tr>    <tr>     <td><strong class=\"model-title\">400 (Bad Request)</strong></td>     <td>Syntax error. For instance, when a required field was not provided</td>    </tr>    <tr>     <td><strong class=\"model-title\">401 (Unauthorized)</strong></td>     <td>API key not provided or invalid</td>    </tr>    <tr>     <td><strong class=\"model-title\">403 (Forbidden)</strong></td>     <td>API key is valid, but the application has insufficient permissions to complete the requested operation</td>    </tr>    <tr>     <td><strong class=\"model-title\">422 (Unprocessable Entity)</strong></td>     <td>API error. The response body is an <a href=\"#model-ErrorModelV2\" class=\"model\">ErrorModelV2</a>    </tr>    <tr>     <td><strong class=\"model-title\">500 (Internal Server Error)</strong></td>     <td>An unexpected error occurred. The <span class=\"model\">exceptionCode</span> contained on the response body may be of help for our support team during diagnostic.</td>    </tr>   </tbody>  </table>    <h3>Error Codes</h3>    <p>   Some of the error codes returned in the <span class=\"model\">code</span> field of an <a href=\"#model-ErrorModelV2\" class=\"model\">ErrorModelV2</a>   (body of responses with HTTP status code 422) are provided below*:  </p>    <table>   <thead>    <tr>     <th>Code</th>     <th>Description</th>    </tr>   </thead>   <tbody>    <tr>     <td class=\"model\">DocumentNotFound</td>     <td>A referenced document was not found (check the document ID)</td>    </tr>    <tr>     <td class=\"model\">SecurityContextNotFound</td>     <td>A referenced security context was not found (check the security context ID)</td>    </tr>    <tr>     <td class=\"model\">SignatureSessionNotFound</td>     <td>A referenced signature session was not found (check the signature session ID)</td>    </tr>    <tr>     <td class=\"model\">BadSignatureSessionOperation</td>     <td>The operation is invalid for the current signature session or document status. For instance, trying to await the session's completion if it is still <span class=\"model\">Pending</span> results in this error</td>    </tr>    <tr>     <td class=\"model\">BackgroundProcessing</td>     <td>The operation cannot be completed at this time because the resource is being processed in background</td>    </tr>    <tr>     <td class=\"model\">SignatureSessionTokenRequired</td>     <td>The signature session token was not passed on the <span class=\"model\">X-Signature-Session-Token</span> request header</td>    </tr>    <tr>     <td class=\"model\">BadSignatureSessionToken</td>     <td>An invalid signature session token was passed on the <span class=\"model\">X-Signature-Session-Token</span> request header. Check your application for possible corruption of the session token, which may contain characters <span class=\"code\">-</span> (hyphen) and <span class=\"code\">_</span> (underscore)</td>    </tr>    <tr>     <td class=\"model\">ExpiredSignatureSessionToken</td>     <td>An expired signature session token was passed on the <span class=\"model\">X-Signature-Session-Token</span> request header. Signature session tokens are normally valid for 4 hours.</td>    </tr>   </tbody>  </table>    <p style=\"font-size: 0.9em\">   *The codes shown above are the most common error codes. Nonetheless, this list is not comprehensive. New codes may be added anytime without previous warning.  </p>    <h2>Culture / Internationalization (i18n)</h2>  <p>The <span class=\"model\">Accept-Language</span> request header is observed by this API. The following cultures are supported:</p>  <ul>   <li><span class=\"code\">en-US</span> (or simply <span class=\"code\">en</span>)</li>   <li><span class=\"code\">pt-BR</span> (or simply <span class=\"code\">pt</span>)</li>  </ul>  <p><i>Notice: error messages are not affected by this header and therefore should not be displayed to users, being better suited for logging.</i></p>  

    The version of the OpenAPI document: 2.2.2
    Generated by OpenAPI Generator (https://openapi-generator.tech)

    Do not edit the class manually.
"""  # noqa: E501


import io
import warnings

from pydantic import validate_call, Field, StrictFloat, StrictStr, StrictInt
from typing import Dict, List, Optional, Tuple, Union, Any

try:
    from typing import Annotated
except ImportError:
    from typing_extensions import Annotated

from typing import Optional

from restpki_ng_python_client.models.inspect_signature_request import InspectSignatureRequest
from restpki_ng_python_client.models.inspect_signature_response import InspectSignatureResponse

from restpki_ng_python_client.api_client import ApiClient
from restpki_ng_python_client.api_response import ApiResponse
from restpki_ng_python_client.rest import RESTResponseType


class SignatureInspectionApi:
    """NOTE: This class is auto generated by OpenAPI Generator
    Ref: https://openapi-generator.tech

    Do not edit the class manually.
    """

    def __init__(self, api_client=None) -> None:
        if api_client is None:
            api_client = ApiClient.get_default()
        self.api_client = api_client


    @validate_call
    def api_signature_inspection_put(
        self,
        inspect_signature_request: Optional[InspectSignatureRequest] = None,
        _request_timeout: Union[
            None,
            Annotated[StrictFloat, Field(gt=0)],
            Tuple[
                Annotated[StrictFloat, Field(gt=0)],
                Annotated[StrictFloat, Field(gt=0)]
            ]
        ] = None,
        _request_auth: Optional[Dict[StrictStr, Any]] = None,
        _content_type: Optional[StrictStr] = None,
        _headers: Optional[Dict[StrictStr, Any]] = None,
        _host_index: Annotated[StrictInt, Field(ge=0, le=0)] = 0,
    ) -> InspectSignatureResponse:
        """Inspects a signed file, returning information about its signers and metadata about the corresponding document (if signed on this instance)

        ## Overview    The simplest usage of this API is by simply passing the `file` to be inspected. If passing a file by its contents, make sure to pass its  `mimeType` so that the API can infer the signature type (PDF/PAdES, CMS/CAdES or XML/XmlDSig) from it.    Information about each signer found is returned on the `signers` property. If the file was signed on this instance, additional information  about the document is returned on the `document` property.    Please note that by default the signatures are not validated. This means that the `validationResults` property of each signer will be `null`  (unless the file was signed on this instance, in which case the property will be filled).    ## Signature validation    By default, the signed file is only inspected, but not validated. To validate the signatures, pass `validate = true`. In this case, you may  optionally specify the `securityContextId` to be used to validate the certificates. If omitted, your default security context will be used.    Please note that validating the signatures may take several seconds or even longer, depending on the number of signers. If more than 10  signers are found, only the first 10 are validated (this limit may be increased on on-demand instances). If your documents can have a large  number of signers per document, please consider using the signer inspection API to validate each user separately on-demand as the user  interacts with the UI.    ## Validating detached CMS/CAdES signatures     When validating detached CMS/CAdES signatures, the detached data file must be specified on the `dataFile` property or its digests must be given  on the `dataHashes` property. If passing `dataHashes`, make sure to pass at least the SHA-256 digest of the data file (other digests may be necessary  depending on the signature algorithm used by the signers). If your data files can be considerably large, passing the `dataHashes` is recommended  since it avoids transmitting the actual data files through the API.    If a CMS/CAdES signature is given with `validate = true` and without the corresponding data file specified, the API returns a 200 (OK) response with  `success = false` and `failure = DataFileRequired`. This allows you to implement a validation form that lets the user submit the signature file and only  requests the data file if necessary.

        :param inspect_signature_request:
        :type inspect_signature_request: InspectSignatureRequest
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :type _request_timeout: int, tuple(int, int), optional
        :param _request_auth: set to override the auth_settings for an a single
                              request; this effectively ignores the
                              authentication in the spec for a single request.
        :type _request_auth: dict, optional
        :param _content_type: force content-type for the request.
        :type _content_type: str, Optional
        :param _headers: set to override the headers for a single
                         request; this effectively ignores the headers
                         in the spec for a single request.
        :type _headers: dict, optional
        :param _host_index: set to override the host_index for a single
                            request; this effectively ignores the host_index
                            in the spec for a single request.
        :type _host_index: int, optional
        :return: Returns the result object.
        """ # noqa: E501

        _param = self._api_signature_inspection_put_serialize(
            inspect_signature_request=inspect_signature_request,
            _request_auth=_request_auth,
            _content_type=_content_type,
            _headers=_headers,
            _host_index=_host_index
        )

        _response_types_map: Dict[str, Optional[str]] = {
            '200': "InspectSignatureResponse",
            '400': None,
            '401': None,
            '403': None,
            '422': None
            
        }
        response_data = self.api_client.call_api(
            *_param,
            _request_timeout=_request_timeout
        )
        response_data.read()
        return self.api_client.response_deserialize(
            response_data=response_data,
            response_types_map=_response_types_map,
        ).data


    @validate_call
    def api_signature_inspection_put_with_http_info(
        self,
        inspect_signature_request: Optional[InspectSignatureRequest] = None,
        _request_timeout: Union[
            None,
            Annotated[StrictFloat, Field(gt=0)],
            Tuple[
                Annotated[StrictFloat, Field(gt=0)],
                Annotated[StrictFloat, Field(gt=0)]
            ]
        ] = None,
        _request_auth: Optional[Dict[StrictStr, Any]] = None,
        _content_type: Optional[StrictStr] = None,
        _headers: Optional[Dict[StrictStr, Any]] = None,
        _host_index: Annotated[StrictInt, Field(ge=0, le=0)] = 0,
    ) -> ApiResponse[InspectSignatureResponse]:
        """Inspects a signed file, returning information about its signers and metadata about the corresponding document (if signed on this instance)

        ## Overview    The simplest usage of this API is by simply passing the `file` to be inspected. If passing a file by its contents, make sure to pass its  `mimeType` so that the API can infer the signature type (PDF/PAdES, CMS/CAdES or XML/XmlDSig) from it.    Information about each signer found is returned on the `signers` property. If the file was signed on this instance, additional information  about the document is returned on the `document` property.    Please note that by default the signatures are not validated. This means that the `validationResults` property of each signer will be `null`  (unless the file was signed on this instance, in which case the property will be filled).    ## Signature validation    By default, the signed file is only inspected, but not validated. To validate the signatures, pass `validate = true`. In this case, you may  optionally specify the `securityContextId` to be used to validate the certificates. If omitted, your default security context will be used.    Please note that validating the signatures may take several seconds or even longer, depending on the number of signers. If more than 10  signers are found, only the first 10 are validated (this limit may be increased on on-demand instances). If your documents can have a large  number of signers per document, please consider using the signer inspection API to validate each user separately on-demand as the user  interacts with the UI.    ## Validating detached CMS/CAdES signatures     When validating detached CMS/CAdES signatures, the detached data file must be specified on the `dataFile` property or its digests must be given  on the `dataHashes` property. If passing `dataHashes`, make sure to pass at least the SHA-256 digest of the data file (other digests may be necessary  depending on the signature algorithm used by the signers). If your data files can be considerably large, passing the `dataHashes` is recommended  since it avoids transmitting the actual data files through the API.    If a CMS/CAdES signature is given with `validate = true` and without the corresponding data file specified, the API returns a 200 (OK) response with  `success = false` and `failure = DataFileRequired`. This allows you to implement a validation form that lets the user submit the signature file and only  requests the data file if necessary.

        :param inspect_signature_request:
        :type inspect_signature_request: InspectSignatureRequest
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :type _request_timeout: int, tuple(int, int), optional
        :param _request_auth: set to override the auth_settings for an a single
                              request; this effectively ignores the
                              authentication in the spec for a single request.
        :type _request_auth: dict, optional
        :param _content_type: force content-type for the request.
        :type _content_type: str, Optional
        :param _headers: set to override the headers for a single
                         request; this effectively ignores the headers
                         in the spec for a single request.
        :type _headers: dict, optional
        :param _host_index: set to override the host_index for a single
                            request; this effectively ignores the host_index
                            in the spec for a single request.
        :type _host_index: int, optional
        :return: Returns the result object.
        """ # noqa: E501

        _param = self._api_signature_inspection_put_serialize(
            inspect_signature_request=inspect_signature_request,
            _request_auth=_request_auth,
            _content_type=_content_type,
            _headers=_headers,
            _host_index=_host_index
        )

        _response_types_map: Dict[str, Optional[str]] = {
            '200': "InspectSignatureResponse",
            '400': None,
            '401': None,
            '403': None,
            '422': None
            
        }
        response_data = self.api_client.call_api(
            *_param,
            _request_timeout=_request_timeout
        )
        response_data.read()
        return self.api_client.response_deserialize(
            response_data=response_data,
            response_types_map=_response_types_map,
        )


    @validate_call
    def api_signature_inspection_put_without_preload_content(
        self,
        inspect_signature_request: Optional[InspectSignatureRequest] = None,
        _request_timeout: Union[
            None,
            Annotated[StrictFloat, Field(gt=0)],
            Tuple[
                Annotated[StrictFloat, Field(gt=0)],
                Annotated[StrictFloat, Field(gt=0)]
            ]
        ] = None,
        _request_auth: Optional[Dict[StrictStr, Any]] = None,
        _content_type: Optional[StrictStr] = None,
        _headers: Optional[Dict[StrictStr, Any]] = None,
        _host_index: Annotated[StrictInt, Field(ge=0, le=0)] = 0,
    ) -> RESTResponseType:
        """Inspects a signed file, returning information about its signers and metadata about the corresponding document (if signed on this instance)

        ## Overview    The simplest usage of this API is by simply passing the `file` to be inspected. If passing a file by its contents, make sure to pass its  `mimeType` so that the API can infer the signature type (PDF/PAdES, CMS/CAdES or XML/XmlDSig) from it.    Information about each signer found is returned on the `signers` property. If the file was signed on this instance, additional information  about the document is returned on the `document` property.    Please note that by default the signatures are not validated. This means that the `validationResults` property of each signer will be `null`  (unless the file was signed on this instance, in which case the property will be filled).    ## Signature validation    By default, the signed file is only inspected, but not validated. To validate the signatures, pass `validate = true`. In this case, you may  optionally specify the `securityContextId` to be used to validate the certificates. If omitted, your default security context will be used.    Please note that validating the signatures may take several seconds or even longer, depending on the number of signers. If more than 10  signers are found, only the first 10 are validated (this limit may be increased on on-demand instances). If your documents can have a large  number of signers per document, please consider using the signer inspection API to validate each user separately on-demand as the user  interacts with the UI.    ## Validating detached CMS/CAdES signatures     When validating detached CMS/CAdES signatures, the detached data file must be specified on the `dataFile` property or its digests must be given  on the `dataHashes` property. If passing `dataHashes`, make sure to pass at least the SHA-256 digest of the data file (other digests may be necessary  depending on the signature algorithm used by the signers). If your data files can be considerably large, passing the `dataHashes` is recommended  since it avoids transmitting the actual data files through the API.    If a CMS/CAdES signature is given with `validate = true` and without the corresponding data file specified, the API returns a 200 (OK) response with  `success = false` and `failure = DataFileRequired`. This allows you to implement a validation form that lets the user submit the signature file and only  requests the data file if necessary.

        :param inspect_signature_request:
        :type inspect_signature_request: InspectSignatureRequest
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :type _request_timeout: int, tuple(int, int), optional
        :param _request_auth: set to override the auth_settings for an a single
                              request; this effectively ignores the
                              authentication in the spec for a single request.
        :type _request_auth: dict, optional
        :param _content_type: force content-type for the request.
        :type _content_type: str, Optional
        :param _headers: set to override the headers for a single
                         request; this effectively ignores the headers
                         in the spec for a single request.
        :type _headers: dict, optional
        :param _host_index: set to override the host_index for a single
                            request; this effectively ignores the host_index
                            in the spec for a single request.
        :type _host_index: int, optional
        :return: Returns the result object.
        """ # noqa: E501

        _param = self._api_signature_inspection_put_serialize(
            inspect_signature_request=inspect_signature_request,
            _request_auth=_request_auth,
            _content_type=_content_type,
            _headers=_headers,
            _host_index=_host_index
        )

        _response_types_map: Dict[str, Optional[str]] = {
            '200': "InspectSignatureResponse",
            '400': None,
            '401': None,
            '403': None,
            '422': None
            
        }
        response_data = self.api_client.call_api(
            *_param,
            _request_timeout=_request_timeout
        )
        return response_data.response


    def _api_signature_inspection_put_serialize(
        self,
        inspect_signature_request,
        _request_auth,
        _content_type,
        _headers,
        _host_index,
    ) -> Tuple:

        _host = None

        _collection_formats: Dict[str, str] = {
            
        }

        _path_params: Dict[str, str] = {}
        _query_params: List[Tuple[str, str]] = []
        _header_params: Dict[str, Optional[str]] = _headers or {}
        _form_params: List[Tuple[str, str]] = []
        _files: Dict[str, str] = {}
        _body_params: Optional[bytes] = None

        # process the path parameters
        # process the query parameters
        # process the header parameters
        # process the form parameters
        # process the body parameter
        if inspect_signature_request is not None:
            _body_params = inspect_signature_request


        # set the HTTP header `Accept`
        _header_params['Accept'] = self.api_client.select_header_accept(
            [
                'application/json', 
                'text/json'
            ]
        )

        # set the HTTP header `Content-Type`
        if _content_type:
            _header_params['Content-Type'] = _content_type
        else:
            _default_content_type = (
                self.api_client.select_header_content_type(
                    [
                        'application/json-patch+json', 
                        'application/json', 
                        'text/json', 
                        'application/*+json'
                    ]
                )
            )
            if _default_content_type is not None:
                _header_params['Content-Type'] = _default_content_type

        # authentication setting
        _auth_settings: List[str] = [
        ]

        return self.api_client.param_serialize(
            method='PUT',
            resource_path='/api/signature-inspection',
            path_params=_path_params,
            query_params=_query_params,
            header_params=_header_params,
            body=_body_params,
            post_params=_form_params,
            files=_files,
            auth_settings=_auth_settings,
            collection_formats=_collection_formats,
            _host=_host,
            _request_auth=_request_auth
        )


