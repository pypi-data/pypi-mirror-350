# coding: utf-8

"""
    Rest PKI Core API

    <b><i>Para Português, <a href=\"https://docs.lacunasoftware.com/pt-br/articles/rest-pki/core/integration/get-started\">clique aqui</a></i></b>  <p>   <a href=\"https://docs.lacunasoftware.com/en-us/articles/rest-pki/core/\">Rest PKI Core</a> is an upcoming version of   <a href=\"https://docs.lacunasoftware.com/en-us/articles/rest-pki/\">Rest PKI</a> that will have extended compatibility with environments and databases.  </p>  <p>   In addition to Windows Server (which is already supported by Rest PKI), Rest PKI Core will also run on <b>Linux</b> (Debian- and RedHat-based distributions)   and on <b>Docker</b>. As for database servers, in addition to SQL Server, <b>PostgreSQL</b> will also be supported.  </p>  <p>   <b>Before getting started, see the integration overview on the <a href=\"https://docs.lacunasoftware.com/en-us/articles/rest-pki/core/integration/\">Integration Guide</a></b>  </p>  <p>   For questions regarding the usage of this API, please reach us at <a href=\"https://lacuna.help/\">lacuna.help</a>  </p>    <h2>Parameters</h2>  <p>   You will need the following parameters:  </p>  <ul>   <li><b>Endpoint</b>: address of the Rest PKI Core instance that will be used</li>   <li><b>API Key</b>: authorization key for using the API</li>  </ul>  <p>   The <span class=\"model\">endpoint</span> must be prefixed to all relative URLs mentioned here. As for the <span class=\"model\">API Key</span>, see how to use it below.  </p>    <h2>Authentication</h2>  <p>   The API key must be sent on the <span class=\"model\">X-Api-Key</span> header on each request:  </p>    <!-- unfortunately, class \"example microlight\" doesn't seem to work here -->  <pre style=\"font-size: 12px; padding: 10px; border-radius: 4px; background: #41444e; font-weight: 600; color: #fff;\">  X-Api-Key: yourapp|xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx  </pre>    <h2>HTTP Codes</h2>    <p>   The APIs will return the following HTTP codes:  </p>    <table>   <thead>    <tr>     <th>Code</th>     <th>Description</th>    </tr>   </thead>   <tbody>    <tr>     <td><strong class=\"model-title\">200 (OK)</strong></td>     <td>Request processed successfully. The response is different for each API, please refer to the operation's documentation</td>    </tr>    <tr>     <td><strong class=\"model-title\">400 (Bad Request)</strong></td>     <td>Syntax error. For instance, when a required field was not provided</td>    </tr>    <tr>     <td><strong class=\"model-title\">401 (Unauthorized)</strong></td>     <td>API key not provided or invalid</td>    </tr>    <tr>     <td><strong class=\"model-title\">403 (Forbidden)</strong></td>     <td>API key is valid, but the application has insufficient permissions to complete the requested operation</td>    </tr>    <tr>     <td><strong class=\"model-title\">422 (Unprocessable Entity)</strong></td>     <td>API error. The response body is an <a href=\"#model-ErrorModelV2\" class=\"model\">ErrorModelV2</a>    </tr>    <tr>     <td><strong class=\"model-title\">500 (Internal Server Error)</strong></td>     <td>An unexpected error occurred. The <span class=\"model\">exceptionCode</span> contained on the response body may be of help for our support team during diagnostic.</td>    </tr>   </tbody>  </table>    <h3>Error Codes</h3>    <p>   Some of the error codes returned in the <span class=\"model\">code</span> field of an <a href=\"#model-ErrorModelV2\" class=\"model\">ErrorModelV2</a>   (body of responses with HTTP status code 422) are provided below*:  </p>    <table>   <thead>    <tr>     <th>Code</th>     <th>Description</th>    </tr>   </thead>   <tbody>    <tr>     <td class=\"model\">DocumentNotFound</td>     <td>A referenced document was not found (check the document ID)</td>    </tr>    <tr>     <td class=\"model\">SecurityContextNotFound</td>     <td>A referenced security context was not found (check the security context ID)</td>    </tr>    <tr>     <td class=\"model\">SignatureSessionNotFound</td>     <td>A referenced signature session was not found (check the signature session ID)</td>    </tr>    <tr>     <td class=\"model\">BadSignatureSessionOperation</td>     <td>The operation is invalid for the current signature session or document status. For instance, trying to await the session's completion if it is still <span class=\"model\">Pending</span> results in this error</td>    </tr>    <tr>     <td class=\"model\">BackgroundProcessing</td>     <td>The operation cannot be completed at this time because the resource is being processed in background</td>    </tr>    <tr>     <td class=\"model\">SignatureSessionTokenRequired</td>     <td>The signature session token was not passed on the <span class=\"model\">X-Signature-Session-Token</span> request header</td>    </tr>    <tr>     <td class=\"model\">BadSignatureSessionToken</td>     <td>An invalid signature session token was passed on the <span class=\"model\">X-Signature-Session-Token</span> request header. Check your application for possible corruption of the session token, which may contain characters <span class=\"code\">-</span> (hyphen) and <span class=\"code\">_</span> (underscore)</td>    </tr>    <tr>     <td class=\"model\">ExpiredSignatureSessionToken</td>     <td>An expired signature session token was passed on the <span class=\"model\">X-Signature-Session-Token</span> request header. Signature session tokens are normally valid for 4 hours.</td>    </tr>   </tbody>  </table>    <p style=\"font-size: 0.9em\">   *The codes shown above are the most common error codes. Nonetheless, this list is not comprehensive. New codes may be added anytime without previous warning.  </p>    <h2>Culture / Internationalization (i18n)</h2>  <p>The <span class=\"model\">Accept-Language</span> request header is observed by this API. The following cultures are supported:</p>  <ul>   <li><span class=\"code\">en-US</span> (or simply <span class=\"code\">en</span>)</li>   <li><span class=\"code\">pt-BR</span> (or simply <span class=\"code\">pt</span>)</li>  </ul>  <p><i>Notice: error messages are not affected by this header and therefore should not be displayed to users, being better suited for logging.</i></p>  

    The version of the OpenAPI document: 2.2.2
    Generated by OpenAPI Generator (https://openapi-generator.tech)

    Do not edit the class manually.
"""  # noqa: E501


from __future__ import annotations
import pprint
import re  # noqa: F401
import json


from typing import Any, ClassVar, Dict, List, Optional, Union
from pydantic import BaseModel, StrictBool, StrictBytes, StrictStr
from pydantic import Field
from restpki_ng_python_client.models.pades_certification_level import PadesCertificationLevel
from restpki_ng_python_client.models.pades_measurement_units import PadesMeasurementUnits
from restpki_ng_python_client.models.pades_page_optimization_model import PadesPageOptimizationModel
from restpki_ng_python_client.models.pades_visual_representation_model import PadesVisualRepresentationModel
from restpki_ng_python_client.models.pdf_mark_model import PdfMarkModel
try:
    from typing import Self
except ImportError:
    from typing_extensions import Self

class PadesSignaturePostRequestV1(BaseModel):
    """
    PadesSignaturePostRequestV1
    """ # noqa: E501
    pdf_to_sign: Union[StrictBytes, StrictStr] = Field(alias="pdfToSign")
    visual_representation: Optional[PadesVisualRepresentationModel] = Field(default=None, alias="visualRepresentation")
    pdf_marks: Optional[List[PdfMarkModel]] = Field(default=None, alias="pdfMarks")
    bypass_marks_if_signed: Optional[StrictBool] = Field(default=None, alias="bypassMarksIfSigned")
    measurement_units: Optional[PadesMeasurementUnits] = Field(default=None, alias="measurementUnits")
    page_optimization: Optional[PadesPageOptimizationModel] = Field(default=None, alias="pageOptimization")
    custom_signature_field_name: Optional[StrictStr] = Field(default=None, alias="customSignatureFieldName")
    certification_level: Optional[PadesCertificationLevel] = Field(default=None, alias="certificationLevel")
    reason: Optional[StrictStr] = None
    certificate: Optional[Union[StrictBytes, StrictStr]] = None
    signature_policy_id: Optional[StrictStr] = Field(default=None, alias="signaturePolicyId")
    security_context_id: Optional[StrictStr] = Field(default=None, alias="securityContextId")
    callback_argument: Optional[StrictStr] = Field(default=None, alias="callbackArgument")
    ignore_revocation_status_unknown: Optional[StrictBool] = Field(default=None, alias="ignoreRevocationStatusUnknown")
    __properties: ClassVar[List[str]] = ["pdfToSign", "visualRepresentation", "pdfMarks", "bypassMarksIfSigned", "measurementUnits", "pageOptimization", "customSignatureFieldName", "certificationLevel", "reason", "certificate", "signaturePolicyId", "securityContextId", "callbackArgument", "ignoreRevocationStatusUnknown"]

    model_config = {
        "populate_by_name": True,
        "validate_assignment": True
    }


    def to_str(self) -> str:
        """Returns the string representation of the model using alias"""
        return pprint.pformat(self.model_dump(by_alias=True))

    def to_json(self) -> str:
        """Returns the JSON representation of the model using alias"""
        # TODO: pydantic v2: use .model_dump_json(by_alias=True, exclude_unset=True) instead
        return json.dumps(self.to_dict())

    @classmethod
    def from_json(cls, json_str: str) -> Self:
        """Create an instance of PadesSignaturePostRequestV1 from a JSON string"""
        return cls.from_dict(json.loads(json_str))

    def to_dict(self) -> Dict[str, Any]:
        """Return the dictionary representation of the model using alias.

        This has the following differences from calling pydantic's
        `self.model_dump(by_alias=True)`:

        * `None` is only added to the output dict for nullable fields that
          were set at model initialization. Other fields with value `None`
          are ignored.
        """
        _dict = self.model_dump(
            by_alias=True,
            exclude={
            },
            exclude_none=True,
        )
        # override the default output from pydantic by calling `to_dict()` of visual_representation
        if self.visual_representation:
            _dict['visualRepresentation'] = self.visual_representation.to_dict()
        # override the default output from pydantic by calling `to_dict()` of each item in pdf_marks (list)
        _items = []
        if self.pdf_marks:
            for _item in self.pdf_marks:
                if _item:
                    _items.append(_item.to_dict())
            _dict['pdfMarks'] = _items
        # override the default output from pydantic by calling `to_dict()` of page_optimization
        if self.page_optimization:
            _dict['pageOptimization'] = self.page_optimization.to_dict()
        # set to None if pdf_marks (nullable) is None
        # and model_fields_set contains the field
        if self.pdf_marks is None and "pdf_marks" in self.model_fields_set:
            _dict['pdfMarks'] = None

        # set to None if custom_signature_field_name (nullable) is None
        # and model_fields_set contains the field
        if self.custom_signature_field_name is None and "custom_signature_field_name" in self.model_fields_set:
            _dict['customSignatureFieldName'] = None

        # set to None if reason (nullable) is None
        # and model_fields_set contains the field
        if self.reason is None and "reason" in self.model_fields_set:
            _dict['reason'] = None

        # set to None if certificate (nullable) is None
        # and model_fields_set contains the field
        if self.certificate is None and "certificate" in self.model_fields_set:
            _dict['certificate'] = None

        # set to None if security_context_id (nullable) is None
        # and model_fields_set contains the field
        if self.security_context_id is None and "security_context_id" in self.model_fields_set:
            _dict['securityContextId'] = None

        # set to None if callback_argument (nullable) is None
        # and model_fields_set contains the field
        if self.callback_argument is None and "callback_argument" in self.model_fields_set:
            _dict['callbackArgument'] = None

        # set to None if ignore_revocation_status_unknown (nullable) is None
        # and model_fields_set contains the field
        if self.ignore_revocation_status_unknown is None and "ignore_revocation_status_unknown" in self.model_fields_set:
            _dict['ignoreRevocationStatusUnknown'] = None

        return _dict

    @classmethod
    def from_dict(cls, obj: Dict) -> Self:
        """Create an instance of PadesSignaturePostRequestV1 from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return cls.model_validate(obj)

        _obj = cls.model_validate({
            "pdfToSign": obj.get("pdfToSign"),
            "visualRepresentation": PadesVisualRepresentationModel.from_dict(obj.get("visualRepresentation")) if obj.get("visualRepresentation") is not None else None,
            "pdfMarks": [PdfMarkModel.from_dict(_item) for _item in obj.get("pdfMarks")] if obj.get("pdfMarks") is not None else None,
            "bypassMarksIfSigned": obj.get("bypassMarksIfSigned"),
            "measurementUnits": obj.get("measurementUnits"),
            "pageOptimization": PadesPageOptimizationModel.from_dict(obj.get("pageOptimization")) if obj.get("pageOptimization") is not None else None,
            "customSignatureFieldName": obj.get("customSignatureFieldName"),
            "certificationLevel": obj.get("certificationLevel"),
            "reason": obj.get("reason"),
            "certificate": obj.get("certificate"),
            "signaturePolicyId": obj.get("signaturePolicyId"),
            "securityContextId": obj.get("securityContextId"),
            "callbackArgument": obj.get("callbackArgument"),
            "ignoreRevocationStatusUnknown": obj.get("ignoreRevocationStatusUnknown")
        })
        return _obj


