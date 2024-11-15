import datetime
import hashlib
import io

from .. import arc

#def test_init_arc_header():
#    "Make sure Header can be initialise only with expected fields"
#    with pytest.raises(TypeError):
#        arc.ARCHeader(test="1234")

def test_arc_header_attributes():
    "Make sure that ARC1 header fields are accessible as attributes. Double check for attributes that are converted for convenience (e.g. date and length)"
    header = arc.ARCHeader(url ="https://archive.org",
                           ip_address = "127.0.0.1",
                           date = "20120301093000",
                           content_type = "text/html",
                           length = "500",
                           result_code = "200",
                           checksum = "a123456",
                           location ="https://www.archive.org",
                           offset = "300",
                           filename = "sample.arc.gz")

    assert header.url == "https://archive.org"
    assert header.ip_address == "127.0.0.1"
    assert header.date == datetime.datetime.strptime("20120301093000", "%Y%m%d%H%M%S")
    assert header['date'] == "20120301093000"
    assert header.content_type == "text/html"
    assert header.length == 500
    assert header['length'] == "500"
    assert header.result_code == "200"
    assert header.checksum == "a123456"
    assert header.location == "https://www.archive.org"
    assert header.offset == 300
    assert header.filename == "sample.arc.gz"

def test_arc_v1_header_creation():
    "Validate ARC V1 header creation"
    header = arc.ARCHeader(url ="https://archive.org",
                           ip_address = "127.0.0.1",
                           date = "20120301093000",
                           content_type = "text/html",
                           length = "500",
                           result_code = "200",
                           checksum = "a123456",
                           location ="https://www.archive.org",
                           offset = "300",
                           filename = "sample.arc.gz")
    f = io.StringIO()
    header.write_to(f, 1)
    header_v1_string = f.getvalue()
    assert header_v1_string == "https://archive.org 127.0.0.1 20120301093000 text/html 500"


def test_arc_v2_header_creation():
    "Validate ARC V2 header creation"
    header = arc.ARCHeader(url ="https://archive.org",
                           ip_address = "127.0.0.1",
                           date = "20120301093000",
                           content_type = "text/html",
                           length = "500",
                           result_code = "200",
                           checksum = "a123456",
                           location = "https://www.archive.org",
                           offset = "300",
                           filename = "sample.arc.gz")
    f = io.StringIO()
    header.write_to(f)
    header_v2_string = f.getvalue()
    assert header_v2_string == "https://archive.org 127.0.0.1 20120301093000 text/html 200 a123456 https://www.archive.org 300 sample.arc.gz 500"


def test_arc_v1_record_creation():
    "Validate ARC V1 record creation"
    header = arc.ARCHeader(url = "https://archive.org",
                           ip_address = "127.0.0.1",
                           date = "20120301093000",
                           content_type = "text/html",
                           length = "500",
                           result_code = "200",
                           checksum = "a123456",
                           location = "https://www.archive.org",
                           offset = "300",
                           filename = "sample.arc.gz")
    record_v1 = arc.ARCRecord(header, "BlahBlah")
    f = io.StringIO()
    record_v1.write_to(f, 1)
    record_v1_string = f.getvalue()
    assert record_v1_string == "https://archive.org 127.0.0.1 20120301093000 text/html 500\nBlahBlah\n"

def test_arc_v2_record_creation():
    "Validate ARC V1 record creation"
    header = dict(url = "https://archive.org",
                  ip_address = "127.0.0.1",
                  date = "20120301093000",
                  content_type = "text/html",
                  length = "500",
                  result_code = "200",
                  checksum = "a123456",
                  location = "https://www.archive.org",
                  offset = "300",
                  filename = "sample.arc.gz")
    record_v2 = arc.ARCRecord(payload = "BlahBlah", headers = header)
    f = io.StringIO()
    record_v2.write_to(f)
    record_v2_string = f.getvalue()
    assert record_v2_string == "https://archive.org 127.0.0.1 20120301093000 text/html 200 a123456 https://www.archive.org 300 sample.arc.gz 500\nBlahBlah\n"

def test_arc_v1_writer():
    "Try writing records to an ARC V1 file. This is what API will feel like to a user of the library"
    now = "20120302193210"
    file_headers = dict(ip_address = "127.0.0.1",
                        date = now,
                        org = "Internet Archive")

    opfile = io.StringIO()
    opfile.name = "sample.arc" # Necessary since only file objects in Python have names.

    f = arc.ARCFile(fileobj = opfile, version = 1, file_headers = file_headers)
    for payload in "Payload1 Payload2".split():
        header = dict(url = "https://www.archive.org",
                      ip_address = "127.0.0.1",
                      date = now,
                      content_type = "text/html",
                      length = len(payload))
        r = arc.ARCRecord(headers = header, payload = payload)
        f.write(r)
    expected_value = "filedesc://sample.arc 127.0.0.1 20120302193210 text/plain 76\n1 0 Internet Archive\nURL IP-address Archive-date Content-type Archive-length\n\nhttps://www.archive.org 127.0.0.1 20120302193210 text/html 8\nPayload1\n\nhttps://www.archive.org 127.0.0.1 20120302193210 text/html 8\nPayload2\n\n"
    assert opfile.getvalue() == expected_value
    f.close()

def test_arc1_v1_writer_default_headers():
    "This is similar to the previous test but validates the default values for all the header fields except time"
    now = datetime.datetime(year = 2012, month = 3, day = 2, hour = 19, minute = 32, second = 10)
    file_headers = dict(date = now)

    opfile = io.StringIO()
    opfile.name = "sample.arc" # Necessary since only file objects in Python have names.

    f = arc.ARCFile(fileobj = opfile, version = 1, file_headers = file_headers)
    for payload in "Payload1 Payload2".split():
        header = dict(url = "https://www.archive.org",
                      ip_address = "127.0.0.1",
                      date = now,
                      content_type = "text/html",
                      length = len(payload))
        r = arc.ARCRecord(headers = header, payload = payload)
        f.write(r)
    expected_value = "filedesc://sample.arc 127.0.0.1 20120302193210 text/plain 67\n1 0 Unknown\nURL IP-address Archive-date Content-type Archive-length\n\nhttps://www.archive.org 127.0.0.1 20120302193210 text/html 8\nPayload1\n\nhttps://www.archive.org 127.0.0.1 20120302193210 text/html 8\nPayload2\n\n"
    assert opfile.getvalue() == expected_value
    f.close()

def test_arc_v2_writer():
    "Try writing records to an ARC V2 file. This is what API will feel like to a user of the library"
    now = "20120302193210"
    file_headers = dict(ip_address = "127.0.0.1",
                        date = now,
                        org = "Internet Archive")

    opfile = io.StringIO()
    opfile.name = "sample.arc" # Necessary since only file objects in Python have names.

    f = arc.ARCFile(fileobj = opfile, file_headers = file_headers)
    for payload in "Payload1 Payload2".split():
        header = arc.ARCHeader(url = "https://archive.org",
                               ip_address = "127.0.0.1",
                               date = "20120301093000",
                               content_type = "text/html",
                               length = "500",
                               result_code = "200",
                               checksum = "a123456",
                               location = "https://www.archive.org",
                               offset = "300",
                               filename = "sample.arc.gz")
        r = arc.ARCRecord(headers = header, payload = payload)
        f.write(r)
    assert opfile.getvalue() == "filedesc://sample.arc 127.0.0.1 20120302193210 text/plain 200 - - 0 sample.arc 113\n2 0 Internet Archive\nURL IP-address Archive-date Content-type Result-code Checksum Location Offset Filename Archive-length\n\nhttps://archive.org 127.0.0.1 20120301093000 text/html 200 a123456 https://www.archive.org 300 sample.arc.gz 500\nPayload1\n\nhttps://archive.org 127.0.0.1 20120301093000 text/html 200 a123456 https://www.archive.org 300 sample.arc.gz 500\nPayload2\n\n"
    f.close()

def test_arc_reader_guess_version():
    "Make sure that the ARCFile object automatically detects the file version"
    v1 = io.StringIO("filedesc://sample.arc 127.0.0.1 20120302193210 text/plain 68\n1 0 Unknown\nURL IP-address Archive-date Content-type Archive-length\n\n\nhttps://www.archive.org 127.0.0.1 20120302193210 text/html 8\n\nPayload1\nhttps://www.archive.org 127.0.0.1 20120302193210 text/html 8\n\nPayload2")
    v2 = io.StringIO("filedesc://sample.arc 127.0.0.1 20120302193210 text/plain 200 - - 0 sample.arc 114\n2 0 Internet Archive\nURL IP-address Archive-date Content-type Result-code Checksum Location Offset Filename Archive-length\n\n\nhttps://archive.org 127.0.0.1 20120301093000 text/html 200 a123456 https://www.archive.org 300 sample.arc.gz 500\n\nPayload1\nhttps://archive.org 127.0.0.1 20120301093000 text/html 200 a123456 https://www.archive.org 300 sample.arc.gz 500\n\nPayload2")

    arc_v1 = arc.ARCFile(fileobj = v1)
    arc_v2 = arc.ARCFile(fileobj = v2)

    arc_v1.read()
    arc_v2.read()

    assert arc_v1.version == 1
    assert arc_v2.version == 2

def test_arc_reader_read_file_headers():
    "Make sure that the parser is reading file headers properly"
    ip = io.StringIO("filedesc://sample.arc 127.0.0.1 20120302193210 text/plain 200 - - 0 sample.arc 114\n2 0 Internet Archive\nURL IP-address Archive-date Content-type Result-code Checksum Location Offset Filename Archive-length\n\n\nhttps://archive.org 127.0.0.1 20120301093000 text/html 200 a123456 https://www.archive.org 300 sample.arc.gz 500\n\nPayload1\nhttps://archive.org 127.0.0.1 20120301093000 text/html 200 a123456 https://www.archive.org 300 sample.arc.gz 500\n\nPayload2")
    arc_file = arc.ARCFile(fileobj = ip)
    arc_file.read()
    arc_file.file_headers['ip_address'] == "127.0.0.1"
    arc_file.file_headers['date'] == "20120301093000"
    arc_file.file_headers['org'] == "Internet Archive"


def test_arc_reader_v1():
    "Make sure that the parser reads out V1 ARC records. (Also tests iterator behaviour)"
    v1 = io.StringIO("filedesc://sample.arc 127.0.0.1 20120302193210 text/plain 68\n1 0 Unknown\nURL IP-address Archive-date Content-type Archive-length\n\n\nhttps://www.archive.org 127.0.0.1 20120302193210 text/html 8\nPayload1\nhttps://archive.org 127.0.0.1 20120302193211 text/plain 8\nPayload2")
    arc_file = arc.ARCFile(fileobj = v1)

    r1  = arc_file.read()
    r2  = arc_file.read()

    assert r1['url'] == "https://www.archive.org"
    assert r1['ip_address'] == "127.0.0.1"
    assert r1['date'] == "20120302193210"
    assert r1['content_type'] == "text/html"
    assert r1['length'] == "8"
    assert r1.payload == "Payload1"

    assert r2['url'] == "https://archive.org"
    assert r2['ip_address'] == "127.0.0.1"
    assert r2['date'] == "20120302193211"
    assert r2['content_type'] == "text/plain"
    assert r2['length'] == "8"
    assert r2.payload == "Payload2"


def test_arc_reader_v2():
    "Make sure that the parser reads out V2 ARC records. (Also tests iterator behaviour)"
    v2 = io.StringIO("filedesc://sample.arc 127.0.0.1 20120302193210 text/plain 200 - - 0 sample.arc 114\n2 0 Internet Archive\nURL IP-address Archive-date Content-type Result-code Checksum Location Offset Filename Archive-length\n\n\nhttps://archive.org 127.0.0.1 20120301093000 text/html 200 a123456 https://www.archive.org 300 sample.arc.gz 8\nPayload1\nhttps://archive.org 127.0.0.1 20120301093000 text/html 200 a123456 https://www.archive.org 300 sample.arc.gz 8\nPayload2")
    arc_file = arc.ARCFile(fileobj = v2)
    r1, r2 = list(arc_file)

    assert r1['url'] == "https://archive.org"
    assert r1['ip_address'] == "127.0.0.1"
    assert r1['date'] == "20120301093000"
    assert r1['content_type'] == "text/html"
    assert r1['checksum'] == "a123456"
    assert r1['location'] == "https://www.archive.org"
    assert r1['offset'] == "300"
    assert r1['filename'] == "sample.arc.gz"
    assert r1['length'] == "8"
    assert r1.payload == "Payload1"

def test_arc_v1_record_from_string():
    "Validate ARC V1 record creation from string"
    record_v1_string = "https://www.archive.org 127.0.0.1 20120301093000 text/html 500\nBlahBlah"
    record = arc.ARCRecord.from_string(record_v1_string, 1)

    assert record['url'] == "https://www.archive.org"
    assert record['ip_address'] == "127.0.0.1"
    assert record['date'] == "20120301093000"
    assert record['content_type'] == "text/html"
    assert record['length'] == "500"
    assert record.payload == "BlahBlah"


def test_arc_v2_record_from_string():
    "Validate ARC V2 record creation from string"
    record_v2_string = "https://archive.org 127.0.0.1 20120301093000 text/html 200 a123456 https://www.archive.org 300 sample.arc.gz 500\nBlahBlah"
    record = arc.ARCRecord.from_string(record_v2_string, 2)

    assert record['url'] == "https://archive.org"
    assert record['ip_address'] == "127.0.0.1"
    assert record['date'] == "20120301093000"
    assert record['content_type'] == "text/html"
    assert record['checksum'] == "a123456"
    assert record['location'] == "https://www.archive.org"
    assert record['offset'] == "300"
    assert record['filename'] == "sample.arc.gz"
    assert record['length'] == "500"
    assert record.payload == "BlahBlah"

def test_arc_record_versions():
    "Check initialising an ARCRecord with a version to see if it outputs stuff properly"
    header = dict(url = "https://archive.org",
                  ip_address = "127.0.0.1",
                  date = "20120301093000",
                  content_type = "text/html",
                  length = "500",
                  result_code = "200",
                  checksum = "a123456",
                  location = "https://www.archive.org",
                  offset = "300",
                  filename = "sample.arc.gz")
    record_1 = arc.ARCRecord(payload = "BlahBlah", headers = header, version = 1)
    record_2 = arc.ARCRecord(payload = "BlahBlah", headers = header, version = 2)
    f = io.StringIO()
    record_1.write_to(f)
    record_string = f.getvalue()
    assert record_string == "https://archive.org 127.0.0.1 20120301093000 text/html 500\nBlahBlah\n"

    f = io.StringIO()
    record_2.write_to(f)
    record_string = f.getvalue()
    assert record_string == "https://archive.org 127.0.0.1 20120301093000 text/html 200 a123456 https://www.archive.org 300 sample.arc.gz 500\nBlahBlah\n"


class TestARCFile:
    def test_write_headers(self):
        """Test to make sure header is written just once.
        """
        f = io.StringIO()
        f.name = "sample.arc"
        afile = arc.ARCFile(fileobj=f, version=1)
        afile._write_header()

        # Make sure header is written only once
        assert f.getvalue().count("filedesc://") == 1

    def test_filename(self):
        """If filename is specified as argument to ARCFile, it should be used."""
        f = io.StringIO()
        afile = arc.ARCFile(fileobj=f, filename="sample.arc", version=1)
        afile._write_header()
        assert "sample.arc" in f.getvalue()

    def test_no_filename(self):
        """should be able to write ARCFile even if there is no filename."""
        f = io.StringIO()
        afile = arc.ARCFile(fileobj=f, version=1)
        afile._write_header()
        # filename should be empty
        assert f.getvalue().startswith("filedesc:// ")

