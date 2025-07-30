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

from datetime import datetime
from typing import Any, ClassVar, Dict, List, Optional
from pydantic import BaseModel, StrictBool, StrictStr
from pydantic import Field
from restpki_ng_python_client.models.attribute_certificate_model import AttributeCertificateModel
from restpki_ng_python_client.models.cades_timestamp_model import CadesTimestampModel
from restpki_ng_python_client.models.certificate_model import CertificateModel
from restpki_ng_python_client.models.digest_algorithm_and_value_model import DigestAlgorithmAndValueModel
from restpki_ng_python_client.models.signature_algorithm_and_value_model import SignatureAlgorithmAndValueModel
from restpki_ng_python_client.models.signature_policy_identifier_model import SignaturePolicyIdentifierModel
from restpki_ng_python_client.models.validation_results_model import ValidationResultsModel
from restpki_ng_python_client.models.xml_element_model import XmlElementModel
from restpki_ng_python_client.models.xml_signed_entity_types import XmlSignedEntityTypes
try:
    from typing import Self
except ImportError:
    from typing_extensions import Self

class SignerModel(BaseModel):
    """
    SignerModel
    """ # noqa: E501
    message_digest: Optional[DigestAlgorithmAndValueModel] = Field(default=None, alias="messageDigest")
    signature: Optional[SignatureAlgorithmAndValueModel] = None
    signature_policy: Optional[SignaturePolicyIdentifierModel] = Field(default=None, alias="signaturePolicy")
    signing_time: Optional[datetime] = Field(default=None, alias="signingTime")
    certified_date_reference: Optional[datetime] = Field(default=None, alias="certifiedDateReference")
    timestamps: Optional[List[CadesTimestampModel]] = None
    is_document_timestamp: Optional[StrictBool] = Field(default=None, alias="isDocumentTimestamp")
    signature_field_name: Optional[StrictStr] = Field(default=None, alias="signatureFieldName")
    validation_results: Optional[ValidationResultsModel] = Field(default=None, alias="validationResults")
    has_ltv: Optional[StrictBool] = Field(default=None, alias="hasLtv")
    xml_signed_entity_type: Optional[XmlSignedEntityTypes] = Field(default=None, alias="xmlSignedEntityType")
    xml_signed_element: Optional[XmlElementModel] = Field(default=None, alias="xmlSignedElement")
    attribute_certificates: Optional[List[AttributeCertificateModel]] = Field(default=None, alias="attributeCertificates")
    certificate: Optional[CertificateModel] = None
    var_date: Optional[datetime] = Field(default=None, alias="date")
    __properties: ClassVar[List[str]] = ["messageDigest", "signature", "signaturePolicy", "signingTime", "certifiedDateReference", "timestamps", "isDocumentTimestamp", "signatureFieldName", "validationResults", "hasLtv", "xmlSignedEntityType", "xmlSignedElement", "attributeCertificates", "certificate", "date"]

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
        """Create an instance of SignerModel from a JSON string"""
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
        # override the default output from pydantic by calling `to_dict()` of message_digest
        if self.message_digest:
            _dict['messageDigest'] = self.message_digest.to_dict()
        # override the default output from pydantic by calling `to_dict()` of signature
        if self.signature:
            _dict['signature'] = self.signature.to_dict()
        # override the default output from pydantic by calling `to_dict()` of signature_policy
        if self.signature_policy:
            _dict['signaturePolicy'] = self.signature_policy.to_dict()
        # override the default output from pydantic by calling `to_dict()` of each item in timestamps (list)
        _items = []
        if self.timestamps:
            for _item in self.timestamps:
                if _item:
                    _items.append(_item.to_dict())
            _dict['timestamps'] = _items
        # override the default output from pydantic by calling `to_dict()` of validation_results
        if self.validation_results:
            _dict['validationResults'] = self.validation_results.to_dict()
        # override the default output from pydantic by calling `to_dict()` of xml_signed_element
        if self.xml_signed_element:
            _dict['xmlSignedElement'] = self.xml_signed_element.to_dict()
        # override the default output from pydantic by calling `to_dict()` of each item in attribute_certificates (list)
        _items = []
        if self.attribute_certificates:
            for _item in self.attribute_certificates:
                if _item:
                    _items.append(_item.to_dict())
            _dict['attributeCertificates'] = _items
        # override the default output from pydantic by calling `to_dict()` of certificate
        if self.certificate:
            _dict['certificate'] = self.certificate.to_dict()
        # set to None if signing_time (nullable) is None
        # and model_fields_set contains the field
        if self.signing_time is None and "signing_time" in self.model_fields_set:
            _dict['signingTime'] = None

        # set to None if certified_date_reference (nullable) is None
        # and model_fields_set contains the field
        if self.certified_date_reference is None and "certified_date_reference" in self.model_fields_set:
            _dict['certifiedDateReference'] = None

        # set to None if timestamps (nullable) is None
        # and model_fields_set contains the field
        if self.timestamps is None and "timestamps" in self.model_fields_set:
            _dict['timestamps'] = None

        # set to None if signature_field_name (nullable) is None
        # and model_fields_set contains the field
        if self.signature_field_name is None and "signature_field_name" in self.model_fields_set:
            _dict['signatureFieldName'] = None

        # set to None if has_ltv (nullable) is None
        # and model_fields_set contains the field
        if self.has_ltv is None and "has_ltv" in self.model_fields_set:
            _dict['hasLtv'] = None

        # set to None if attribute_certificates (nullable) is None
        # and model_fields_set contains the field
        if self.attribute_certificates is None and "attribute_certificates" in self.model_fields_set:
            _dict['attributeCertificates'] = None

        return _dict

    @classmethod
    def from_dict(cls, obj: Dict) -> Self:
        """Create an instance of SignerModel from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return cls.model_validate(obj)

        _obj = cls.model_validate({
            "messageDigest": DigestAlgorithmAndValueModel.from_dict(obj.get("messageDigest")) if obj.get("messageDigest") is not None else None,
            "signature": SignatureAlgorithmAndValueModel.from_dict(obj.get("signature")) if obj.get("signature") is not None else None,
            "signaturePolicy": SignaturePolicyIdentifierModel.from_dict(obj.get("signaturePolicy")) if obj.get("signaturePolicy") is not None else None,
            "signingTime": obj.get("signingTime"),
            "certifiedDateReference": obj.get("certifiedDateReference"),
            "timestamps": [CadesTimestampModel.from_dict(_item) for _item in obj.get("timestamps")] if obj.get("timestamps") is not None else None,
            "isDocumentTimestamp": obj.get("isDocumentTimestamp"),
            "signatureFieldName": obj.get("signatureFieldName"),
            "validationResults": ValidationResultsModel.from_dict(obj.get("validationResults")) if obj.get("validationResults") is not None else None,
            "hasLtv": obj.get("hasLtv"),
            "xmlSignedEntityType": obj.get("xmlSignedEntityType"),
            "xmlSignedElement": XmlElementModel.from_dict(obj.get("xmlSignedElement")) if obj.get("xmlSignedElement") is not None else None,
            "attributeCertificates": [AttributeCertificateModel.from_dict(_item) for _item in obj.get("attributeCertificates")] if obj.get("attributeCertificates") is not None else None,
            "certificate": CertificateModel.from_dict(obj.get("certificate")) if obj.get("certificate") is not None else None,
            "date": obj.get("date")
        })
        return _obj


