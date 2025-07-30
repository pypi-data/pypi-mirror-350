""" 
User defined, this is not included in the openAPI generation package
This client intends to center all requests and provide a better name for some of the operations
To help the user to make a more informed decision
it is a facade class, which hides all the apis and other implementation problems
"""

import hashlib
from io import BufferedReader, BytesIO
import io
import os
import ssl
from typing import Dict, List, Union
from restpki_ng_python_client.rest import RESTResponse
from restpki_ng_python_client.configuration import Configuration
from restpki_ng_python_client.api_client import ApiClient
from restpki_ng_python_client.api import *
from restpki_ng_python_client.models import *
from restpki_ng_python_client.utils import Utils


class RestPkiClient:
    
    def __init__(self, endpoint: str, api_key: str):
        self.endpoint = endpoint
        self.api_key = api_key

        self._config = Configuration(
            host=self.endpoint,
            api_key=self.api_key,
            username=None,
            api_key_prefix=None,
            password=None,
            server_variables=None,
            server_index=None,
            server_operation_index=None,
            server_operation_variables=None,
            ssl_ca_cert=None)
        self._config.verify_ssl = False

        # api_key_dict = {'x-api-key': f'Bearer {self.api_key}'}

        self._apiClient = ApiClient(configuration=self._config)
        self._apiClient.user_agent = 'RestPkiClient/Python/Lib/Beta'
        
        self._apiClient.default_headers['Authorization'] = "Bearer " + self.api_key
        self._apiClient.default_headers['x-api-key'] = "Bearer " + self.api_key
        
        # Upload stuff
        self.__multipart_upload_threshold = 5 * 1024 * 1024  # 5 MB

        # Todo: create one client with the endpoint and apikey for each of the routes
        # AppKeys29 API
        # self._app_keys_29_api = ApplicationKeysController29Api(api_client=self._apiClient)
        # Applications API
        # self._apps_api = ApplicationsApi(api_client=self._apiClient)
        # Applications Controller 29 API
        # self._app_ctrl_29_api = ApplicationsController29Api(api_client=self._apiClient)
        # Authentication API
        self._auth_api = AuthenticationApi(api_client=self._apiClient)
        # Cades Signature API
        self._cades_sig_api = CadesSignatureApi(api_client=self._apiClient)
        # Certificates API
        # self._certs_api = CertificatesApi(api_client=self._apiClient)
        # DocumentKeys API
        self._doc_keys_api = DocumentKeysApi(api_client=self._apiClient)
        # Documents API
        self._docs_api = DocumentsApi(api_client=self._apiClient)
        # Pades Signature API
        self._pades_sig_api = PadesSignatureApi(api_client=self._apiClient)
        # Pades visual positioning presets API
        self._pades_visual_pos_pres_api = PadesVisualPositioningPresetsApi(
            api_client=self._apiClient)
        # PDF API
        self._pdf_api = PdfApi(api_client=self._apiClient)
        # Pending Signatures API
        # self._pending_sigs_api = PendingSignaturesApi(api_client=self._apiClient)
        # Signature API
        self._sig_api = SignatureApi(api_client=self._apiClient)
        # Signature Inspection API
        self._sig_insp_api = SignatureInspectionApi(api_client=self._apiClient)
        # Signature Sessions API
        self._sig_ses_api = SignatureSessionsApi(api_client=self._apiClient)
        # Timestamp API
        self._ts_api = TimestampApi(api_client=self._apiClient)
        # Upload API
        self._upload_api = UploadApi(api_client=self._apiClient)
        # XML Signature API
        self._xml_sig_api = XmlSignatureApi(api_client=self._apiClient)

    # # ApplicationsController`29 Manage applications
    # def get_application_controller(self, q, limit, offset, cursor, order, name) -> SubscriptionAccessModelRolesRootRolesApplicationModelPaginatedSearchResponse:
    #     self._app_ctrl_29_api.api_applications_get(q, limit, offset, cursor, order, name)

    # def create_application_controller(self, request: AuthorizationDataRootAuthorizationDataRolesRootRolesApplicationData) -> SubscriptionAccessModelRolesRootRolesApplicationModel:
    #     self._app_ctrl_29_api.api_applications_post(request)

    # def get_application_controller_by_id(self, id) -> SubscriptionAccessModelRolesRootRolesApplicationModel:
    #     self._app_ctrl_29_api.api_applications_id_get(id)

    # def delete_application_controller_by_id(self, id):
    #     self._app_ctrl_29_api.api_applications_id_delete(id)

    # def check_for_application_name_availability(self, name) -> bool:
    #     self._app_ctrl_29_api.api_applications_name_availability_get(name)

    # ApplicationKeysController`29

    # def create_application_keys(self, app_id, request: CreateApplicationApiKeyRequest) -> CreateApplicationApiKeyResponse:
    #     self._app_keys_29_api.api_applications_app_id_api_keys_post(app_id, request)

    # Applications

    # Configures a set of metadata values to be added to each document created by the application

    def add_document_metadata_set(self, id, request: Dict[str, List]) -> Dict[str, List[str]]:
        return self._apps_api.api_applications_id_default_document_metadata_put(id, request)

    # Returns the set of metadata values that is currently added for documents created by a given application
    def document_metadata_get(self, id) -> Dict[str, List[str]]:
        return self._apps_api.api_applications_id_default_document_metadata_get(id)

    # Applications

    # Prepares for a certificate authentication
    def start_authentication_v2(self, request: PrepareAuthenticationRequest) -> PrepareAuthenticationResponse:
        return self._auth_api.api_v2_authentication_post(prepare_authentication_request=request)

    # Completes a certificate authentication
    def complete_authentication_v2(self, request: CompleteAuthenticationRequest) -> CompleteAuthenticationResponse:
        return self._auth_api.api_v2_authentication_completion_post(complete_authentication_request=request)

    def create_authentications(self, request: AuthenticationsPostRequest) -> AuthenticationsPostResponse:
        return self._auth_api.api_authentications_post(authentications_post_request=request)

    def finalize_authentication_token(self, token) -> AuthenticationPostResponse:
        return self._auth_api.api_authentications_token_finalize_post(token=token)

    def finalize_authentication_token(self, request: AuthenticationsPostSignedBytesRequest) -> AuthenticationsPostSignedBytesResponse:
        return self._auth_api.api_authentications_token_signed_bytes_post(authentications_post_signed_bytes_request=request)

    def authentication_get_nonce(self) -> AuthenticationGetResponse:
        return self._auth_api.api_authentication_get()

    def start_authentication(self, request: AuthenticationsPostRequest) -> AuthenticationPostResponse:
        return self._auth_api.api_authentication_post(authentication_post_request=request)

    # CadesSignature

    def create_cades_signature_v2(self, request: CadesSignaturePostRequestV1) -> CadesSignaturePostResponse:
        return self._cades_sig_api.api_cades_signatures_post(cades_signature_post_request_v1=request)

    def create_cades_signature_v2(self, request: CadesSignaturePostRequestV2) -> CadesSignaturePostResponse:
        return self._cades_sig_api.api_v2_cades_signatures_post(cades_signature_post_request_v2=request)

    def create_cades_signature_v3(self, request: CadesSignaturePostRequestV3) -> CadesSignaturePostResponse:
        return self._cades_sig_api.api_v3_cades_signatures_post(cades_signature_post_request_v3=request)

    def create_cades_signatures_with_token_signed_bytes_v1(self, token, request: CadesSignaturePostSignedBytesRequest) -> CadesSignaturePostSignedBytesResponse:
        return self._cades_sig_api.api_cades_signatures_token_signed_bytes_post(token=token, cades_signature_post_signed_bytes_request=request)

    def finish_cades_signatures_with_token(self, token,) -> CadesSignaturePostSignedBytesResponse:
        return self._cades_sig_api.api_cades_signatures_token_finalize_post(token=token)

    def create_cades_signatures_with_token_signed_bytes_v2(self, token, request: CompleteSignatureRequest) -> SignatureResultModel:
        return self._cades_sig_api.api_v2_cades_signatures_token_signed_bytes_post(token=token, complete_signature_request=request)

    def create_cades_signature_required_hashes(self, request: FileModel) -> List[DigestAlgorithms]:
        return self._cades_sig_api.api_cades_signatures_required_hashes_post(file_model=request)

    def open_cades_signature(self, request: OpenCadesSignatureRequestModel) -> CadesSignatureModel:
        return self._cades_sig_api.api_cades_signatures_open_post(open_cades_signature_request_model=request)

    # Certificates

    # Retrieves information about a X.509 certificate previously used to sign some document
    # def retrieve_certificate_info(self, certificate_thumbprint_sha256: str, fill_pem_encoded: bool, fill_encoded: bool) -> CertificateFullModel:
    #     self._certs_api.api_certificates_thumbprint_sha256_get(certificate_thumbprint_sha256, fill_pem_encoded, fill_encoded)

    # Document Keys

    # Allocates a document key to be used later on a document signature
    def allocate_document_key(self, request: AllocateDocumentKeyRequest) -> DocumentKeyModel:
        return self._doc_keys_api.api_document_keys_post(allocate_document_key_request=request)

    # Allocates a batch of document keys to be used later on document signatures
    def allocate_batch_document_keys(self, request: AllocateDocumentKeyBatchRequest) -> List[DocumentKeyModel]:
        return self._doc_keys_api.api_document_keys_batch_post(allocate_document_key_batch_request=request)

    # Queries documents by key
    def query_documents_by_key(self, key: str) -> DocumentKeyQueryResponse:
        return self._doc_keys_api.api_document_keys_key_get(key=key)

    # Queries unused document keys
    def query_unused_document_keys(self, metadata_name: str, metadata_value: str) -> List[DocumentKeySummary]:
        return self._doc_keys_api.api_document_keys_unused_get(metadata_name=metadata_name, metadata_value=metadata_value)

    # Documents

    # Retrieves document details
    def retrieve_document_by_id(self, id: str) -> DocumentModel:
        return self._docs_api.api_documents_id_get(id=id)

    # Retrieves the full information about each of a document's signers
    def retrieve_signers_info_in_document_by_id(self, id: str) -> List[SignerModel]:
        return self._docs_api.api_documents_id_signers_get(id=id)

    # Retrieves the full information about each of a document's signers
    def retrieve_document_details_by_key(self, key: str) -> DocumentQueryResponse:
        return self._docs_api.api_documents_keys_key_get(key=key)

    # PadesSignature

    def start_pades_signature(self, request: PadesSignaturePostRequestV1) -> PadesSignaturePostResponse:
        return self._pades_sig_api.api_pades_signatures_post(pades_signature_post_request_v1=request)

    def start_pades_signature_v2(self, request: PadesSignaturePostRequestV2) -> PadesSignaturePostResponse:
        return self._pades_sig_api.api_v2_pades_signatures_post(pades_signature_post_request_v2=request)

    def complete_pades_signature_with_token_and_signed_bytes(self, token: str, request: PadesSignaturePostSignedBytesRequest) -> PadesSignaturePostSignedBytesResponse:
        return self._pades_sig_api.api_pades_signatures_token_signed_bytes_post(token=token, pades_signature_post_signed_bytes_request=request)

    def complete_pades_signature_with_token(self, token) -> PadesSignaturePostSignedBytesResponse:
        return self._pades_sig_api.api_pades_signatures_token_finalize_post(token=token)

    def complete_pades_signature_with_token_and_signed_bytes_v2(self, token, request: CompleteSignatureRequest) -> SignatureResultModel:
        return self._pades_sig_api.api_v2_pades_signatures_token_signed_bytes_post(complete_signature_request=request, token=token)

    def open_pades_signature(self, request: OpenSignatureRequestModel) -> PadesSignatureModel:
        return self._pades_sig_api.api_pades_signatures_open_post(open_signature_request_model=request)

    # PadesVisualPositioningPresets

    def get_footnotes_pades_visual_positioning_presets(self, page_number, rows) -> PadesVisualPositioningModel:
        return self._pades_visual_pos_pres_api.api_pades_visual_positioning_presets_footnote_get(page_number=page_number, rows=rows)

    def get_footnotes_pades_visual_positioning_presets_bottom_up(self, page_number, rows) -> PadesVisualPositioningModel:
        return self._pades_visual_pos_pres_api.api_pades_visual_positioning_presets_footnote_bottom_up_get(page_number=page_number, rows=rows)

    def get_footnotes_pades_visual_positioning_presets_new_page(self) -> PadesVisualPositioningModel:
        return self._pades_visual_pos_pres_api.api_pades_visual_positioning_presets_new_page_get()

    # Pdf

    def pdf_add_marks(self, request: PdfAddMarksRequest) -> PdfAddMarksResponse:
        return self._pdf_api.api_pdf_add_marks_post(pdf_add_marks_request=request)

    # Signature

    def start_signature(self, request: PrepareSignatureRequest) -> PrepareSignatureResponse:
        return self._sig_api.api_signature_post(prepare_signature_request=request)

    def complete_signature(self, request: CompleteSignatureRequestV2) -> DocumentModel:
        return self._sig_api.api_signature_completion_post(complete_signature_request_v2=request)

    # Signature Inspection

    # Inspects a signed file, returning information about its signers and metadata about the corresponding document (if signed on this instance)
    def inspect_signed_file(self, request: InspectSignatureRequest) -> InspectSignatureResponse:
        return self._sig_insp_api.api_signature_inspection_put(inspect_signature_request=request)

    # SignatureSessions

    # Retrieves a signature session's details
    def retrieve_signature_session_details_by_id(self, id) -> SignatureSessionModel:
        return self._sig_ses_api.api_signature_sessions_id_get(id=id)

    # Creates a signature session
    def create_signature_session(self, request: CreateSignatureSessionRequest) -> CreateSignatureSessionResponse:
        return self._sig_ses_api.api_signature_sessions_post(create_signature_session_request=request)

    # Waits for the completion of a signature session
    def wait_for_completion_signature_session_by_id(self, id):
        return self._sig_ses_api.api_signature_sessions_id_when_completed_get(id=id)

    # Timestamp

    def issue_timestamp_plan_with_identifier(self, identifier, request: DigestAlgorithmAndValueModel) -> TimestampIssueResponse:
        return self._ts_api.api_timestamp_plans_identifier_issue_post(identifier=identifier, digest_algorithm_and_value_model=request)

    def create_timestamp_plan_with_identifier(self, identifier, request: DigestAlgorithmAndValueModel) -> TimestampIssueResponse:
        return self._ts_api.api_timestamp_plans_identifier_issue_post(identifier=identifier, digest_algorithm_and_value_model=request)

    # Upload

    # public methods
    def upload_file_multipart(self, file_desc: Union[BufferedReader,BytesIO,str]):
        if not isinstance(file_desc, BufferedReader) or not isinstance(file_desc, BytesIO) or not isinstance(file_desc, str):
            raise TypeError("File is not a valid type, it must be a instance of BufferedReader, BytesIO or string")

        blob_token = self._upload_multipart(file_desc)
        return blob_token
    
    def upload_file_plain(self, file_path: str, file_desc: Union[BufferedReader,BytesIO,str]):
        if not isinstance(file_desc, BufferedReader) or not isinstance(file_desc, BytesIO) or not isinstance(file_desc, str):
            raise TypeError("File is not a valid type, it must be a instance of BufferedReader, BytesIO or string")

        blob_token = self._perform_plain_uploads(file_path, file_desc)
        return blob_token

    def upload_file_from_path(self, path):
        # Check if the file exists
        if not os.path.exists(path):
            print(f"Error: File not found at {path}")
            return False
        else:
            with open(path, 'rb') as file_desc:
                isMultipart = self._isBiggerThanThreshold(file_desc)
                if isMultipart:
                    return self.upload_file_multipart(file_desc)
                else:
                    return self.upload_file_plain(path, file_desc)


    def upload_file_from_raw(self, content_raw):
        stream = BytesIO()
        stream.write(content_raw)
        stream.seek(0, 0)
        
        isMultipart = self._isBiggerThanThreshold(content_raw)
        if isMultipart:
            return self.upload_file_multipart(content_raw)
        else:
            return self.upload_file_plain(content_raw)
        
    def get_file_from_url(self, url: str) -> RESTResponse:
        return self._apiClient.rest_client.request('GET', url, self._apiClient.default_headers)
        
    # END public methods

    # private methods
    def _upload_multipart(self, file_desc):

        # Begin the upload
        response = self._perform_multipart_uploads()
        blob_token = response.blob_token
        part_size = response.part_size

        # begin_url = self.__endpoint_url + 'Api/MultipartUploads'
        # begin_response = requests.post(begin_url,
        #                                headers=self.get_request_headers())
        # self._check_response('GET', begin_url, begin_response)

        # blob_token = begin_response.json().get('blobToken')
        # blob_uri = "Api/MultipartUploads/%s" % blob_token
        # part_size = begin_response.json().get('partSize')

        # Read the file part by part

        part_e_tags = []
        part_number = 0

        # Return to the start of the stream.
        file_desc.seek(0, 0)
        while True:
            buffer = file_desc.read(part_size)
            if buffer is None or len(buffer) == 0:
                # Reached end-of-file.
                break
            part_hash = hashlib.md5(buffer)
            part_digest = Utils._base64_url_safe_encode_string(part_hash.digest())
            # self._apiClient.default_headers['Content-MD5'] = Utils.encodeBase64(part_hash.digest())
            # self._apiClient.default_headers['Content-Type'] = 'application/octet-stream'
            # part_url = '%s/%s' % (blob_uri, part_number)
            # response = requests.post(self.__endpoint_url + part_url,
            #                          data=buffer,
            #                          headers=headers)
            response = self._perform_multipart_uploads_with_token_and_part_number(blob_token, part_number, part_digest)
            # self._check_response('POST', part_url, response)
            e_tag = response.headers['ETag']
            part_e_tags.append(e_tag)
            part_number += 1

        # Finish upload

        # end_request = {
        #     'partETags': part_e_tags,
        #     'completeMD5': None
        # }
            
        end_request = MultipartUploadEndRequest(
            part_e_tags=part_e_tags,
            complete_md5=None
        )

        if self.__multipart_upload_double_check:
            file_desc.seek(0, 0)
            md5 = hashlib.md5(file_desc.read())
            digest = md5.digest()
            end_request.complete_md5 = Utils._base64_encode_string(digest)
        
        # finish_url = self.__endpoint_url + blob_uri
        # finish_response = requests.post(finish_url,
        #                                 data=json.dumps(end_request),
        #                                 headers=self.get_request_headers())
        response = self._perform_multipart_uploads_with_token(blob_token)
        # self._check_response('POST', finish_url, finish_response)

        return response

    def _perform_plain_uploads(self, file_path, file) -> FileReferenceModel:
        return self._upload_api.api_plain_uploads_post(file_path, file)

    def _perform_multipart_uploads(self) -> MultipartUploadBeginResponse:
        return self._upload_api.api_multipart_uploads_post()

    def _perform_multipart_uploads_with_token_and_part_number(self, token, part_number, part_digest):
        return self._upload_api.api_multipart_uploads_token_part_number_post(token, part_number, part_digest)

    def _perform_multipart_uploads_with_token(self, token):
        return self._upload_api.api_multipart_uploads_token_post(token=token)
    
    def _isBiggerThanThreshold(self, file) -> bool:
        if isinstance(file, str):  # Check if file is a file path
            return self._checkSizeForFilePath(file)
        elif isinstance(file, io.BufferedReader):  # Check if file is a ReadableBuffer
            return self._checkSizeForRawContent(file)
        else: 
            print(f"Error: Unsupported input type ({type(file)}).")
    
    def _checkSizeForFilePath(self, file_path) -> bool:
        # Get the file size in bytes
        file_size_bytes = os.path.getsize(file_path)

        # Check if the file size is below the limit
        if file_size_bytes <= self.__multipart_upload_threshold:
            return False
        else:
            return True
    
    def _checkSizeForRawContent(self, buffer) -> bool:
        # Get the file size in bytes
        buffer.seek(0, io.SEEK_END)
        content_size_bytes = buffer.tell()
        buffer.seek(0, io.SEEK_SET)

        # Check if the file size is below the limit
        if content_size_bytes <= self.__multipart_upload_threshold:
            return False
        else:
            return True

    # END private methods

    # END Upload
    # XMLSignature

    def create_full_xml_signature(self, request: FullXmlSignaturePostRequest) -> XmlSignaturePostResponse:
        return self._xml_sig_api.api_xml_signatures_full_xml_signature_post(full_xml_signature_post_request=request)

    def create_element_xml_signature(self, request: XmlElementSignaturePostRequest) -> XmlSignatureResponseModel:
        return self._xml_sig_api.api_xml_signatures_xml_element_signature_post(xml_element_signature_post_request=request)

    def complete_xml_signature_with_token_and_signed_bytes(self, token, request: XmlSignaturePostSignedBytesRequest) -> XmlSignaturePostSignedBytesResponse:
        return self._xml_sig_api.api_xml_signatures_token_signed_bytes_post(token=token, xml_signature_post_signed_bytes_request=request)

    def complete_xml_signature_with_token(self, token) -> XmlSignaturePostSignedBytesResponse:
        return self._xml_sig_api.api_xml_signatures_token_finalize_post(token=token)

    def open_xml_signature(self, request: OpenXmlSignatureRequestModel) -> List[XmlSignatureModel]:
        return self._xml_sig_api.api_xml_signatures_open_post(open_xml_signature_request_model=request)

    def open_xml_signature_v2(self, request: OpenXmlSignatureRequestModel) -> XmlSignatureResponseModel:
        return self._xml_sig_api.api_v2_xml_signatures_open_post(open_xml_signature_request_model=request)
