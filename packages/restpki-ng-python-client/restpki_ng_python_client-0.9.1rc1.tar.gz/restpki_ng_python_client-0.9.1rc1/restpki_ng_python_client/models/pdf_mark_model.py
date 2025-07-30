# coding: utf-8

"""
    Rest PKI Core API

    <b><i>Para Português, <a href=\"https://docs.lacunasoftware.com/pt-br/articles/rest-pki/core/integration/get-started\">clique aqui</a></i></b>  <p>   <a href=\"https://docs.lacunasoftware.com/en-us/articles/rest-pki/core/\">Rest PKI Core</a> is an upcoming version of   <a href=\"https://docs.lacunasoftware.com/en-us/articles/rest-pki/\">Rest PKI</a> that will have extended compatibility with environments and databases.  </p>  <p>   In addition to Windows Server (which is already supported by Rest PKI), Rest PKI Core will also run on <b>Linux</b> (Debian- and RedHat-based distributions)   and on <b>Docker</b>. As for database servers, in addition to SQL Server, <b>PostgreSQL</b> will also be supported.  </p>  <p>   <b>Before getting started, see the integration overview on the <a href=\"https://docs.lacunasoftware.com/en-us/articles/rest-pki/core/integration/\">Integration Guide</a></b>  </p>  <p>   For questions regarding the usage of this API, please reach us at <a href=\"https://lacuna.help/\">lacuna.help</a>  </p>    <h2>Parameters</h2>  <p>   You will need the following parameters:  </p>  <ul>   <li><b>Endpoint</b>: address of the Rest PKI Core instance that will be used</li>   <li><b>API Key</b>: authorization key for using the API</li>  </ul>  <p>   The <span class=\"model\">endpoint</span> must be prefixed to all relative URLs mentioned here. As for the <span class=\"model\">API Key</span>, see how to use it below.  </p>    <h2>Authentication</h2>  <p>   The API key must be sent on the <span class=\"model\">X-Api-Key</span> header on each request:  </p>    <!-- unfortunately, class \"example microlight\" doesn't seem to work here -->  <pre style=\"font-size: 12px; padding: 10px; border-radius: 4px; background: #41444e; font-weight: 600; color: #fff;\">  X-Api-Key: yourapp|xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx  </pre>    <h2>HTTP Codes</h2>    <p>   The APIs will return the following HTTP codes:  </p>    <table>   <thead>    <tr>     <th>Code</th>     <th>Description</th>    </tr>   </thead>   <tbody>    <tr>     <td><strong class=\"model-title\">200 (OK)</strong></td>     <td>Request processed successfully. The response is different for each API, please refer to the operation's documentation</td>    </tr>    <tr>     <td><strong class=\"model-title\">400 (Bad Request)</strong></td>     <td>Syntax error. For instance, when a required field was not provided</td>    </tr>    <tr>     <td><strong class=\"model-title\">401 (Unauthorized)</strong></td>     <td>API key not provided or invalid</td>    </tr>    <tr>     <td><strong class=\"model-title\">403 (Forbidden)</strong></td>     <td>API key is valid, but the application has insufficient permissions to complete the requested operation</td>    </tr>    <tr>     <td><strong class=\"model-title\">422 (Unprocessable Entity)</strong></td>     <td>API error. The response body is an <a href=\"#model-ErrorModelV2\" class=\"model\">ErrorModelV2</a>    </tr>    <tr>     <td><strong class=\"model-title\">500 (Internal Server Error)</strong></td>     <td>An unexpected error occurred. The <span class=\"model\">exceptionCode</span> contained on the response body may be of help for our support team during diagnostic.</td>    </tr>   </tbody>  </table>    <h3>Error Codes</h3>    <p>   Some of the error codes returned in the <span class=\"model\">code</span> field of an <a href=\"#model-ErrorModelV2\" class=\"model\">ErrorModelV2</a>   (body of responses with HTTP status code 422) are provided below*:  </p>    <table>   <thead>    <tr>     <th>Code</th>     <th>Description</th>    </tr>   </thead>   <tbody>    <tr>     <td class=\"model\">DocumentNotFound</td>     <td>A referenced document was not found (check the document ID)</td>    </tr>    <tr>     <td class=\"model\">SecurityContextNotFound</td>     <td>A referenced security context was not found (check the security context ID)</td>    </tr>    <tr>     <td class=\"model\">SignatureSessionNotFound</td>     <td>A referenced signature session was not found (check the signature session ID)</td>    </tr>    <tr>     <td class=\"model\">BadSignatureSessionOperation</td>     <td>The operation is invalid for the current signature session or document status. For instance, trying to await the session's completion if it is still <span class=\"model\">Pending</span> results in this error</td>    </tr>    <tr>     <td class=\"model\">BackgroundProcessing</td>     <td>The operation cannot be completed at this time because the resource is being processed in background</td>    </tr>    <tr>     <td class=\"model\">SignatureSessionTokenRequired</td>     <td>The signature session token was not passed on the <span class=\"model\">X-Signature-Session-Token</span> request header</td>    </tr>    <tr>     <td class=\"model\">BadSignatureSessionToken</td>     <td>An invalid signature session token was passed on the <span class=\"model\">X-Signature-Session-Token</span> request header. Check your application for possible corruption of the session token, which may contain characters <span class=\"code\">-</span> (hyphen) and <span class=\"code\">_</span> (underscore)</td>    </tr>    <tr>     <td class=\"model\">ExpiredSignatureSessionToken</td>     <td>An expired signature session token was passed on the <span class=\"model\">X-Signature-Session-Token</span> request header. Signature session tokens are normally valid for 4 hours.</td>    </tr>   </tbody>  </table>    <p style=\"font-size: 0.9em\">   *The codes shown above are the most common error codes. Nonetheless, this list is not comprehensive. New codes may be added anytime without previous warning.  </p>    <h2>Culture / Internationalization (i18n)</h2>  <p>The <span class=\"model\">Accept-Language</span> request header is observed by this API. The following cultures are supported:</p>  <ul>   <li><span class=\"code\">en-US</span> (or simply <span class=\"code\">en</span>)</li>   <li><span class=\"code\">pt-BR</span> (or simply <span class=\"code\">pt</span>)</li>  </ul>  <p><i>Notice: error messages are not affected by this header and therefore should not be displayed to users, being better suited for logging.</i></p>  

    The version of the OpenAPI document: 2.1.2
    Generated by OpenAPI Generator (https://openapi-generator.tech)

    Do not edit the class manually.
"""  # noqa: E501


from __future__ import annotations
import pprint
import re  # noqa: F401
import json


from typing import Any, ClassVar, Dict, List, Optional, Union
from pydantic import BaseModel, StrictFloat, StrictInt
from pydantic import Field
from restpki_ng_python_client.models.color_model import ColorModel
from restpki_ng_python_client.models.pades_visual_rectangle_model import PadesVisualRectangleModel
from restpki_ng_python_client.models.pdf_mark_element_model import PdfMarkElementModel
from restpki_ng_python_client.models.pdf_mark_page_options import PdfMarkPageOptions
try:
    from typing import Self
except ImportError:
    from typing_extensions import Self

class PdfMarkModel(BaseModel):
    """
    PdfMarkModel
    """ # noqa: E501
    container: PadesVisualRectangleModel
    border_width: Optional[Union[StrictFloat, StrictInt]] = Field(default=None, alias="borderWidth")
    border_color: Optional[ColorModel] = Field(default=None, alias="borderColor")
    background_color: Optional[ColorModel] = Field(default=None, alias="backgroundColor")
    elements: List[PdfMarkElementModel]
    page_option: Optional[PdfMarkPageOptions] = Field(default=None, alias="pageOption")
    page_option_number: Optional[StrictInt] = Field(default=None, alias="pageOptionNumber")
    __properties: ClassVar[List[str]] = ["container", "borderWidth", "borderColor", "backgroundColor", "elements", "pageOption", "pageOptionNumber"]

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
        """Create an instance of PdfMarkModel from a JSON string"""
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
        # override the default output from pydantic by calling `to_dict()` of container
        if self.container:
            _dict['container'] = self.container.to_dict()
        # override the default output from pydantic by calling `to_dict()` of border_color
        if self.border_color:
            _dict['borderColor'] = self.border_color.to_dict()
        # override the default output from pydantic by calling `to_dict()` of background_color
        if self.background_color:
            _dict['backgroundColor'] = self.background_color.to_dict()
        # override the default output from pydantic by calling `to_dict()` of each item in elements (list)
        _items = []
        if self.elements:
            for _item in self.elements:
                if _item:
                    _items.append(_item.to_dict())
            _dict['elements'] = _items
        # set to None if page_option_number (nullable) is None
        # and model_fields_set contains the field
        if self.page_option_number is None and "page_option_number" in self.model_fields_set:
            _dict['pageOptionNumber'] = None

        return _dict

    @classmethod
    def from_dict(cls, obj: Dict) -> Self:
        """Create an instance of PdfMarkModel from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return cls.model_validate(obj)

        _obj = cls.model_validate({
            "container": PadesVisualRectangleModel.from_dict(obj.get("container")) if obj.get("container") is not None else None,
            "borderWidth": obj.get("borderWidth"),
            "borderColor": ColorModel.from_dict(obj.get("borderColor")) if obj.get("borderColor") is not None else None,
            "backgroundColor": ColorModel.from_dict(obj.get("backgroundColor")) if obj.get("backgroundColor") is not None else None,
            "elements": [PdfMarkElementModel.from_dict(_item) for _item in obj.get("elements")] if obj.get("elements") is not None else None,
            "pageOption": obj.get("pageOption"),
            "pageOptionNumber": obj.get("pageOptionNumber")
        })
        return _obj
    
    
    # region Fluent API

    def on_container(self, container):
        self.container = container
        return self

    def with_border_width(self, border_width):
        self.border_width = border_width
        return self

    def on_all_pages(self):
        self.page_option = PdfMarkPageOptions.ALLPAGES
        return self

    def on_new_page(self):
        self.page_option = PdfMarkPageOptions.NEWPAGE
        return self

    def on_single_page(self, page_number):
        self.page_option = PdfMarkPageOptions.SINGLEPAGE
        self.page_option_number = page_number
        return self

    def on_single_page_from_end(self, page_number):
        self.page_option = PdfMarkPageOptions.SINGLEPAGEFROMEND
        self.page_option_number = page_number
        return self

    def add_element(self, element):
        self.elements.append(element)
        return self

    def with_border_color(self, border_color):
        self.border_color = border_color
        return self

    def with_background_color(self, background_color):
        self.background_color = background_color
        return self

    # endregion


