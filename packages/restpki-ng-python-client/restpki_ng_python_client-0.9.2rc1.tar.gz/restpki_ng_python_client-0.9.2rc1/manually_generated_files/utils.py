import base64
import binascii
from io import BytesIO, FileIO

from restpki_ng_python_client.models.file_model import FileModel

class Utils:
    def _base64_encode_string(value):
        """

        This method is just a wrapper that handle the incompatibility between the
        standard_b64encode() method on versions 2 and 3 of Python. On Python 2, a
        string is returned, but on Python 3, a bytes-class instance is returned.

        """
        value_base64 = base64.standard_b64encode(value)
        if type(value_base64) is str:
            return value_base64
        elif type(value_base64) is bytes or type(value_base64) is bytearray:
            return value_base64.decode('ascii')
        return None
    def _base64_url_safe_encode_string(value):
        """

        This method is just a wrapper that handle the incompatibility between the
        standard_b64encode() method on versions 2 and 3 of Python. On Python 2, a
        string is returned, but on Python 3, a bytes-class instance is returned.

        """
        value_base64 = base64.urlsafe_b64encode(value)
        if type(value_base64) is str:
            return value_base64
        elif type(value_base64) is bytes or type(value_base64) is bytearray:
            return value_base64.decode('ascii')
        return None


    def _base64_decode(value):
        if value is None:
            raise Exception('The provided value is not valid')
        try:
            raw = base64.standard_b64decode(value)
        except (TypeError, binascii.Error):
            raise Exception('The provided certificate is not Base64-encoded')
        return raw


    def _copy_stream(src, dst, offset=0, from_where=0, buff_size=4096):
        # Position source ont he required position.
        dst.seek(offset, from_where)
        while True:
            buff = src.read(buff_size)
            if not buff:
                break
            dst.write(buff)


    def _get_raw_stream(content):
        stream = BytesIO(content)
        stream.seek(0, 0)
        return stream
    
    def write_to_file(file: FileModel, path: str,
        client = None, offset=0, from_where=0, 
        buff_size=4096):
        content_base64 = file.content if file.content != None else None
        content_raw = Utils._base64_decode(content_base64)\
            if content_base64 is not None else None
        with open(path, 'wb') as f_out:
            if content_raw is not None:
                f_in = BytesIO(content_raw)
                Utils._copy_stream(f_in, f_out, offset, from_where, buff_size)
                f_in.close()
            else:
                if file.url != None or file.url != '' or client != None or client.endpoint != '':
                    req_url = '%s%s' % (client.endpoint, file.url)
                    res = client.get_file_from_url(req_url)
                    for chunk in res.data\
                            .iter_content(buff_size):
                        f_out.write(chunk)
