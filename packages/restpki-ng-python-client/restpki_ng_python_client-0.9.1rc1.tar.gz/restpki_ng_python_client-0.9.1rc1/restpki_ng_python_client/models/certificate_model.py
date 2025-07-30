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
from typing import Any, ClassVar, Dict, List, Optional, Union
from pydantic import BaseModel, StrictBytes, StrictStr
from pydantic import Field
from restpki_ng_python_client.models.name_model import NameModel
from restpki_ng_python_client.models.pki_brazil_certificate_model import PkiBrazilCertificateModel
from restpki_ng_python_client.models.pki_italy_certificate_model import PkiItalyCertificateModel
try:
    from typing import Self
except ImportError:
    from typing_extensions import Self

class CertificateModel(BaseModel):
    """
    CertificateModel
    """ # noqa: E501
    subject_name: Optional[NameModel] = Field(default=None, alias="subjectName")
    issuer_name: Optional[NameModel] = Field(default=None, alias="issuerName")
    issuer_display_name: Optional[StrictStr] = Field(default=None, alias="issuerDisplayName")
    serial_number: Optional[StrictStr] = Field(default=None, alias="serialNumber")
    validity_start: Optional[datetime] = Field(default=None, alias="validityStart")
    validity_end: Optional[datetime] = Field(default=None, alias="validityEnd")
    issuer: Optional[CertificateModel] = None
    pki_brazil: Optional[PkiBrazilCertificateModel] = Field(default=None, alias="pkiBrazil")
    pki_italy: Optional[PkiItalyCertificateModel] = Field(default=None, alias="pkiItaly")
    binary_thumbprint_sha256: Optional[Union[StrictBytes, StrictStr]] = Field(default=None, alias="binaryThumbprintSHA256")
    thumbprint: Optional[StrictStr] = None
    thumbprint_sha256: Optional[StrictStr] = Field(default=None, alias="thumbprintSHA256")
    subject_common_name: Optional[StrictStr] = Field(default=None, alias="subjectCommonName")
    subject_display_name: Optional[StrictStr] = Field(default=None, alias="subjectDisplayName")
    subject_identifier: Optional[StrictStr] = Field(default=None, alias="subjectIdentifier")
    email_address: Optional[StrictStr] = Field(default=None, alias="emailAddress")
    organization: Optional[StrictStr] = None
    organization_identifier: Optional[StrictStr] = Field(default=None, alias="organizationIdentifier")
    __properties: ClassVar[List[str]] = ["subjectName", "issuerName", "issuerDisplayName", "serialNumber", "validityStart", "validityEnd", "issuer", "pkiBrazil", "pkiItaly", "binaryThumbprintSHA256", "thumbprint", "thumbprintSHA256", "subjectCommonName", "subjectDisplayName", "subjectIdentifier", "emailAddress", "organization", "organizationIdentifier"]

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
        """Create an instance of CertificateModel from a JSON string"""
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
        # override the default output from pydantic by calling `to_dict()` of subject_name
        if self.subject_name:
            _dict['subjectName'] = self.subject_name.to_dict()
        # override the default output from pydantic by calling `to_dict()` of issuer_name
        if self.issuer_name:
            _dict['issuerName'] = self.issuer_name.to_dict()
        # override the default output from pydantic by calling `to_dict()` of issuer
        if self.issuer:
            _dict['issuer'] = self.issuer.to_dict()
        # override the default output from pydantic by calling `to_dict()` of pki_brazil
        if self.pki_brazil:
            _dict['pkiBrazil'] = self.pki_brazil.to_dict()
        # override the default output from pydantic by calling `to_dict()` of pki_italy
        if self.pki_italy:
            _dict['pkiItaly'] = self.pki_italy.to_dict()
        # set to None if issuer_display_name (nullable) is None
        # and model_fields_set contains the field
        if self.issuer_display_name is None and "issuer_display_name" in self.model_fields_set:
            _dict['issuerDisplayName'] = None

        # set to None if serial_number (nullable) is None
        # and model_fields_set contains the field
        if self.serial_number is None and "serial_number" in self.model_fields_set:
            _dict['serialNumber'] = None

        # set to None if binary_thumbprint_sha256 (nullable) is None
        # and model_fields_set contains the field
        if self.binary_thumbprint_sha256 is None and "binary_thumbprint_sha256" in self.model_fields_set:
            _dict['binaryThumbprintSHA256'] = None

        # set to None if thumbprint (nullable) is None
        # and model_fields_set contains the field
        if self.thumbprint is None and "thumbprint" in self.model_fields_set:
            _dict['thumbprint'] = None

        # set to None if thumbprint_sha256 (nullable) is None
        # and model_fields_set contains the field
        if self.thumbprint_sha256 is None and "thumbprint_sha256" in self.model_fields_set:
            _dict['thumbprintSHA256'] = None

        # set to None if subject_common_name (nullable) is None
        # and model_fields_set contains the field
        if self.subject_common_name is None and "subject_common_name" in self.model_fields_set:
            _dict['subjectCommonName'] = None

        # set to None if subject_display_name (nullable) is None
        # and model_fields_set contains the field
        if self.subject_display_name is None and "subject_display_name" in self.model_fields_set:
            _dict['subjectDisplayName'] = None

        # set to None if subject_identifier (nullable) is None
        # and model_fields_set contains the field
        if self.subject_identifier is None and "subject_identifier" in self.model_fields_set:
            _dict['subjectIdentifier'] = None

        # set to None if email_address (nullable) is None
        # and model_fields_set contains the field
        if self.email_address is None and "email_address" in self.model_fields_set:
            _dict['emailAddress'] = None

        # set to None if organization (nullable) is None
        # and model_fields_set contains the field
        if self.organization is None and "organization" in self.model_fields_set:
            _dict['organization'] = None

        # set to None if organization_identifier (nullable) is None
        # and model_fields_set contains the field
        if self.organization_identifier is None and "organization_identifier" in self.model_fields_set:
            _dict['organizationIdentifier'] = None

        return _dict

    @classmethod
    def from_dict(cls, obj: Dict) -> Self:
        """Create an instance of CertificateModel from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return cls.model_validate(obj)

        _obj = cls.model_validate({
            "subjectName": NameModel.from_dict(obj.get("subjectName")) if obj.get("subjectName") is not None else None,
            "issuerName": NameModel.from_dict(obj.get("issuerName")) if obj.get("issuerName") is not None else None,
            "issuerDisplayName": obj.get("issuerDisplayName"),
            "serialNumber": obj.get("serialNumber"),
            "validityStart": obj.get("validityStart"),
            "validityEnd": obj.get("validityEnd"),
            "issuer": CertificateModel.from_dict(obj.get("issuer")) if obj.get("issuer") is not None else None,
            "pkiBrazil": PkiBrazilCertificateModel.from_dict(obj.get("pkiBrazil")) if obj.get("pkiBrazil") is not None else None,
            "pkiItaly": PkiItalyCertificateModel.from_dict(obj.get("pkiItaly")) if obj.get("pkiItaly") is not None else None,
            "binaryThumbprintSHA256": obj.get("binaryThumbprintSHA256"),
            "thumbprint": obj.get("thumbprint"),
            "thumbprintSHA256": obj.get("thumbprintSHA256"),
            "subjectCommonName": obj.get("subjectCommonName"),
            "subjectDisplayName": obj.get("subjectDisplayName"),
            "subjectIdentifier": obj.get("subjectIdentifier"),
            "emailAddress": obj.get("emailAddress"),
            "organization": obj.get("organization"),
            "organizationIdentifier": obj.get("organizationIdentifier")
        })
        return _obj

# TODO: Rewrite to not use raise_errors
CertificateModel.model_rebuild(raise_errors=False)

