from httpinsert.insertion import *
from httpinsert import Request
from httpinsert import find_insertion_points

from urllib.parse import parse_qs, urlencode, urlunparse, quote,urlparse
from xml.etree.ElementTree import ElementTree, fromstring, tostring, Element
from cgi import parse_header, parse_multipart
import json
from io import BytesIO
import requests
import re


import unittest


class TestFindInsertionPoints(unittest.TestCase):
    def test_find_custom(self):
        pass
    def test_find_manual(self):
        pass
    def test_find_method(self):
        pass
    def test_find_path(self):
        pass
    def test_find_query(self):
        """
        class Request:
            def __init__(self, method=None, url=None, headers=None, body=None,host=None,version=None):
        """
        request = Request(method="GET",url="https://ginandjuice.shop/",headers={"User-Agent":"MyUserAgent","Content-Type":"application/x-www-form-urlencoded"},body="SomeBody=test",host="ginandjuice.shop",version="HTTP/1.1")
        insertion_points = find_insertion_points(request,location="query")
        self.assertEqual(len(insertion_points),0)


        request.url="https://ginandjuice.shop/?test=foo&test2=bar&test=et"
        insertion_points = find_insertion_points(request,location="all")
        my_insertion_points = []
        for insertion_point in insertion_points:
            if insertion_point.location.startswith("query"):
                my_insertion_points.append(insertion_point)
        self.assertEqual(len(my_insertion_points), 7)

        self.assertEqual(my_insertion_points[0].location,"query-key")
        self.assertEqual(my_insertion_points[0].key,"test")
        self.assertEqual(my_insertion_points[0].value,"foo")

        self.assertEqual(my_insertion_points[1].location,"query")
        self.assertEqual(my_insertion_points[1].key,"test")
        self.assertEqual(my_insertion_points[1].value,"foo")

        self.assertEqual(my_insertion_points[2].location,"query-key")
        self.assertEqual(my_insertion_points[2].key,"test2")
        self.assertEqual(my_insertion_points[2].value,"bar")

        self.assertEqual(my_insertion_points[3].location,"query")
        self.assertEqual(my_insertion_points[3].key,"test2")
        self.assertEqual(my_insertion_points[3].value,"bar")

        self.assertEqual(my_insertion_points[4].location,"query-key")
        self.assertEqual(my_insertion_points[4].key,"test")
        self.assertEqual(my_insertion_points[4].value,"et")

        self.assertEqual(my_insertion_points[5].location,"query")
        self.assertEqual(my_insertion_points[5].key,"test")
        self.assertEqual(my_insertion_points[5].value,"et")

        self.assertEqual(my_insertion_points[6].location,"query")
        self.assertEqual(my_insertion_points[6].key,"new_param")
        self.assertEqual(my_insertion_points[6].value,"1")



    def test_find_version(self):
        pass

    def test_find_header(self):
        pass

    def test_find_body(self):
        """
        class Request:
            def __init__(self, method=None, url=None, headers=None, body=None,host=None,version=None):
        """
        request = Request(method="GET",url="https://ginandjuice.shop/",headers={"User-Agent":"MyUserAgent","Content-Type":"application/x-www-form-urlencoded"},body="",host="ginandjuice.shop",version="HTTP/1.1")
        insertion_points = find_insertion_points(request,location="body")
        self.assertEqual(len(insertion_points),0)


        request.body="test=foo&test2=bar&test=et"
        insertion_points = find_insertion_points(request,location="all")
        my_insertion_points = []
        for insertion_point in insertion_points:
            if insertion_point.location.startswith("body"):
                my_insertion_points.append(insertion_point)
        self.assertEqual(len(my_insertion_points), 8)

        self.assertEqual(my_insertion_points[0].location,"body-key")
        self.assertEqual(my_insertion_points[0].key,"test")
        self.assertEqual(my_insertion_points[0].value,"foo")

        self.assertEqual(my_insertion_points[1].location,"body")
        self.assertEqual(my_insertion_points[1].key,"test")
        self.assertEqual(my_insertion_points[1].value,"foo")

        self.assertEqual(my_insertion_points[2].location,"body-key")
        self.assertEqual(my_insertion_points[2].key,"test2")
        self.assertEqual(my_insertion_points[2].value,"bar")

        self.assertEqual(my_insertion_points[3].location,"body")
        self.assertEqual(my_insertion_points[3].key,"test2")
        self.assertEqual(my_insertion_points[3].value,"bar")

        self.assertEqual(my_insertion_points[4].location,"body-key")
        self.assertEqual(my_insertion_points[4].key,"test")
        self.assertEqual(my_insertion_points[4].value,"et")

        self.assertEqual(my_insertion_points[5].location,"body")
        self.assertEqual(my_insertion_points[5].key,"test")
        self.assertEqual(my_insertion_points[5].value,"et")

        self.assertEqual(my_insertion_points[6].location,"body")
        self.assertEqual(my_insertion_points[6].key,"new_param")
        self.assertEqual(my_insertion_points[6].value,"1")

        self.assertEqual(my_insertion_points[7].location,"body")
        self.assertEqual(my_insertion_points[7].key,"full")
        self.assertEqual(my_insertion_points[7].value,"test=foo&test2=bar&test=et")


    def test_find_body_json(self):
        """
        class Request:
            def __init__(self, method=None, url=None, headers=None, body=None,host=None,version=None):
        """
        request = Request(method="GET",url="https://ginandjuice.shop/",headers={"User-Agent":"MyUserAgent","Content-Type":"application/json"},body="",host="ginandjuice.shop",version="HTTP/1.1")
        insertion_points = find_insertion_points(request,location="body")
        self.assertEqual(len(insertion_points),0)


        request.body = '"test"'

        insertion_points = find_insertion_points(request,location="all")
        my_insertion_points = []
        for insertion_point in insertion_points:
            if insertion_point.location.startswith("body-json"):
                my_insertion_points.append(insertion_point)

        self.assertEqual(len(my_insertion_points), 1)
        self.assertEqual(my_insertion_points[0].location, "body-json")
        self.assertEqual(my_insertion_points[0].key, "<class 'str'>")
        self.assertEqual(my_insertion_points[0].value, "test")




        request.body='{"test":1,"test2":{"test3":[1,2,3]},"test4":0}'
        insertion_points = find_insertion_points(request,location="all")
        my_insertion_points = []
        for insertion_point in insertion_points:
            if insertion_point.location.startswith("body-json"):
                my_insertion_points.append(insertion_point)
        self.assertEqual(len(my_insertion_points), 11)

        self.assertEqual(my_insertion_points[0].location,"body-json-key")
        self.assertEqual(my_insertion_points[0].key,"test")
        self.assertEqual(my_insertion_points[0].value,1)

        self.assertEqual(my_insertion_points[1].location,"body-json")
        self.assertEqual(my_insertion_points[1].key,"test")
        self.assertEqual(my_insertion_points[1].value,1)

        self.assertEqual(my_insertion_points[2].location,"body-json-key")
        self.assertEqual(my_insertion_points[2].key,"test2")
        self.assertEqual(my_insertion_points[2].value,{'test3': [1, 2, 3]})

        self.assertEqual(my_insertion_points[3].location,"body-json-key")
        self.assertEqual(my_insertion_points[3].key,"test2.test3")
        self.assertEqual(my_insertion_points[3].value,[1,2,3])
        
        self.assertEqual(my_insertion_points[4].location,"body-json")
        self.assertEqual(my_insertion_points[4].key,"test2.test3[0]")
        self.assertEqual(my_insertion_points[4].value,1)

        self.assertEqual(my_insertion_points[5].location,"body-json")
        self.assertEqual(my_insertion_points[5].key,"test2.test3[1]")
        self.assertEqual(my_insertion_points[5].value,2)

        self.assertEqual(my_insertion_points[6].location,"body-json")
        self.assertEqual(my_insertion_points[6].key,"test2.test3[2]")
        self.assertEqual(my_insertion_points[6].value,3)

        self.assertEqual(my_insertion_points[7].location,"body-json")
        self.assertEqual(my_insertion_points[7].key,"test2.new_param")
        self.assertEqual(my_insertion_points[7].value,"1")

        self.assertEqual(my_insertion_points[8].location,"body-json-key")
        self.assertEqual(my_insertion_points[8].key,"test4")
        self.assertEqual(my_insertion_points[8].value,0)


        self.assertEqual(my_insertion_points[9].location,"body-json")
        self.assertEqual(my_insertion_points[9].key,"test4")
        self.assertEqual(my_insertion_points[9].value,0)

        self.assertEqual(my_insertion_points[10].location,"body-json")
        self.assertEqual(my_insertion_points[10].key,"new_param")
        self.assertEqual(my_insertion_points[10].value,"1")




    def test_find_body_multipart(self):
        """
        class Request:
            def __init__(self, method=None, url=None, headers=None, body=None,host=None,version=None):
        """
        request = Request(method="POST",url="https://ginandjuice.shop/",headers={"User-Agent":"MyUserAgent","Content-Type":"multipart/form-data; boundary=---------------------------9051914041544843365972754266"},body="",host="ginandjuice.shop",version="HTTP/1.1")
        insertion_points = find_insertion_points(request,location="body")
        self.assertEqual(len(insertion_points),0)
        request.body = """-----------------------------9051914041544843365972754266
Content-Disposition: form-data; name="text"

text default
-----------------------------9051914041544843365972754266
Content-Disposition: form-data; name="file1"; filename="a.txt"
Content-Type: text/plain

Content of a.txt.

-----------------------------9051914041544843365972754266
Content-Disposition: form-data; name="file2"; filename="a.html"
Content-Type: text/html

<!DOCTYPE html><title>Content of a.html.</title>

-----------------------------9051914041544843365972754266--

        """.replace("\n","\r\n")
        insertion_points = find_insertion_points(request,location="all")
        my_insertion_points = []
        for insertion_point in insertion_points:
            if insertion_point.location.startswith("body-multipart"):
                my_insertion_points.append(insertion_point)

        self.assertEqual(len(my_insertion_points),26)

        self.assertEqual(my_insertion_points[0].location,"body-multipart-header-key")
        self.assertEqual(my_insertion_points[0].key,"Content-Disposition")
        self.assertEqual(my_insertion_points[0].value,'form-data; name="text"')

        self.assertEqual(my_insertion_points[1].location,"body-multipart-attr-key")
        self.assertEqual(my_insertion_points[1].key,"Content-Disposition;name")
        self.assertEqual(my_insertion_points[1].value,'text')

        self.assertEqual(my_insertion_points[2].location,"body-multipart-attr")
        self.assertEqual(my_insertion_points[2].key,"Content-Disposition;name")
        self.assertEqual(my_insertion_points[2].value,'text')

        self.assertEqual(my_insertion_points[3].location,"body-multipart-header")
        self.assertEqual(my_insertion_points[3].key,"Content-Disposition")
        self.assertEqual(my_insertion_points[3].value,'form-data; name="text"')

        self.assertEqual(my_insertion_points[4].location,"body-multipart-part-key")
        self.assertEqual(my_insertion_points[4].key,"text")
        self.assertEqual(my_insertion_points[4].value,"text default")

        self.assertEqual(my_insertion_points[5].location,"body-multipart-part")
        self.assertEqual(my_insertion_points[5].key,"text")
        self.assertEqual(my_insertion_points[5].value,"text default")

        self.assertEqual(my_insertion_points[6].location,"body-multipart-header-key")
        self.assertEqual(my_insertion_points[6].key,"Content-Disposition")
        self.assertEqual(my_insertion_points[6].value,'form-data; name="file1"; filename="a.txt"')

        self.assertEqual(my_insertion_points[7].location,"body-multipart-attr-key")
        self.assertEqual(my_insertion_points[7].key,"Content-Disposition;name")
        self.assertEqual(my_insertion_points[7].value,'file1')

        self.assertEqual(my_insertion_points[8].location,"body-multipart-attr")
        self.assertEqual(my_insertion_points[8].key,"Content-Disposition;name")
        self.assertEqual(my_insertion_points[8].value,'file1')

        self.assertEqual(my_insertion_points[9].location,"body-multipart-attr-key")
        self.assertEqual(my_insertion_points[9].key,"Content-Disposition;filename")
        self.assertEqual(my_insertion_points[9].value,'a.txt')

        self.assertEqual(my_insertion_points[10].location,"body-multipart-attr")
        self.assertEqual(my_insertion_points[10].key,"Content-Disposition;filename")
        self.assertEqual(my_insertion_points[10].value,'a.txt')

        self.assertEqual(my_insertion_points[11].location,"body-multipart-header")
        self.assertEqual(my_insertion_points[11].key,"Content-Disposition")
        self.assertEqual(my_insertion_points[11].value,'form-data; name="file1"; filename="a.txt"')

        self.assertEqual(my_insertion_points[12].location,"body-multipart-header-key")
        self.assertEqual(my_insertion_points[12].key,"Content-Type")
        self.assertEqual(my_insertion_points[12].value,"text/plain")

        self.assertEqual(my_insertion_points[13].location,"body-multipart-header")
        self.assertEqual(my_insertion_points[13].key,"Content-Type")
        self.assertEqual(my_insertion_points[13].value,"text/plain")

        self.assertEqual(my_insertion_points[14].location,"body-multipart-part-key")
        self.assertEqual(my_insertion_points[14].key,"file1")
        self.assertEqual(my_insertion_points[14].value,"Content of a.txt.\r\n")

        self.assertEqual(my_insertion_points[15].location,"body-multipart-part")
        self.assertEqual(my_insertion_points[15].key,"file1")
        self.assertEqual(my_insertion_points[15].value,'Content of a.txt.\r\n')

        self.assertEqual(my_insertion_points[16].location,"body-multipart-header-key")
        self.assertEqual(my_insertion_points[16].key,"Content-Disposition")
        self.assertEqual(my_insertion_points[16].value,'form-data; name="file2"; filename="a.html"')

        self.assertEqual(my_insertion_points[17].location,"body-multipart-attr-key")
        self.assertEqual(my_insertion_points[17].key,"Content-Disposition;name")
        self.assertEqual(my_insertion_points[17].value,"file2")

        self.assertEqual(my_insertion_points[18].location,"body-multipart-attr")
        self.assertEqual(my_insertion_points[18].key,"Content-Disposition;name")
        self.assertEqual(my_insertion_points[18].value,"file2")

        self.assertEqual(my_insertion_points[19].location,"body-multipart-attr-key")
        self.assertEqual(my_insertion_points[19].key,"Content-Disposition;filename")
        self.assertEqual(my_insertion_points[19].value,"a.html")

        self.assertEqual(my_insertion_points[20].location,"body-multipart-attr")
        self.assertEqual(my_insertion_points[20].key,"Content-Disposition;filename")
        self.assertEqual(my_insertion_points[20].value,"a.html")

        self.assertEqual(my_insertion_points[21].location,"body-multipart-header")
        self.assertEqual(my_insertion_points[21].key,"Content-Disposition")
        self.assertEqual(my_insertion_points[21].value,'form-data; name="file2"; filename="a.html"')

        self.assertEqual(my_insertion_points[22].location,"body-multipart-header-key")
        self.assertEqual(my_insertion_points[22].key,"Content-Type")
        self.assertEqual(my_insertion_points[22].value,"text/html")

        self.assertEqual(my_insertion_points[23].location,"body-multipart-header")
        self.assertEqual(my_insertion_points[23].key,"Content-Type")
        self.assertEqual(my_insertion_points[23].value,"text/html")

        self.assertEqual(my_insertion_points[24].location,"body-multipart-part-key")
        self.assertEqual(my_insertion_points[24].key,"file2")
        self.assertEqual(my_insertion_points[24].value,'<!DOCTYPE html><title>Content of a.html.</title>\r\n')

        self.assertEqual(my_insertion_points[25].location,"body-multipart-part")
        self.assertEqual(my_insertion_points[25].key,"file2")
        self.assertEqual(my_insertion_points[25].value,'<!DOCTYPE html><title>Content of a.html.</title>\r\n')

    def test_find_body_xml(self):
        """
        class Request:
            def __init__(self, method=None, url=None, headers=None, body=None,host=None,version=None):
        """
        request = Request(method="GET",url="https://ginandjuice.shop/",headers={"User-Agent":"MyUserAgent","Content-Type":"application/xml"},body="",host="ginandjuice.shop",version="HTTP/1.1")
        insertion_points = find_insertion_points(request,location="body")
        self.assertEqual(len(insertion_points),0)

        request.body = """<?xml version="1.0" encoding="UTF-8"?><!DOCTYPE foo [ <!ENTITY xxe SYSTEM "file:///etc/passwd"> ]><test><testing>test2data</testing></test>"""
        insertion_points = find_insertion_points(request,location="all")
        my_insertion_points = []
        for insertion_point in insertion_points:
            if insertion_point.location.startswith("body-xml"):
                my_insertion_points.append(insertion_point)

        self.assertEqual(len(my_insertion_points), 8)


        self.assertEqual(my_insertion_points[0].location, "body-xml-version")
        self.assertEqual(my_insertion_points[0].key, "version")
        self.assertEqual(my_insertion_points[0].value,'<?xml version="1.0" encoding="UTF-8"?>')

        self.assertEqual(my_insertion_points[1].location, "body-xml-doctype")
        self.assertEqual(my_insertion_points[1].key, "DOCTYPE")
        self.assertEqual(my_insertion_points[1].value,'<!DOCTYPE foo [ <!ENTITY xxe SYSTEM "file:///etc/passwd"> ]>') 

        self.assertEqual(my_insertion_points[2].location, "body-xml-key")
        self.assertEqual(my_insertion_points[2].key, "test")
        self.assertEqual(my_insertion_points[2].value,"")

        self.assertEqual(my_insertion_points[3].location, "body-xml")
        self.assertEqual(my_insertion_points[3].key, "test")
        self.assertEqual(my_insertion_points[3].value,"")

        self.assertEqual(my_insertion_points[4].location, "body-xml")
        self.assertEqual(my_insertion_points[4].key, "test.new_tag")
        self.assertEqual(my_insertion_points[4].value,"1")

        self.assertEqual(my_insertion_points[5].location, "body-xml-key")
        self.assertEqual(my_insertion_points[5].key, "testing")
        self.assertEqual(my_insertion_points[5].value,"test2data")

        self.assertEqual(my_insertion_points[6].location, "body-xml")
        self.assertEqual(my_insertion_points[6].key, "testing")
        self.assertEqual(my_insertion_points[6].value,"test2data")

        self.assertEqual(my_insertion_points[7].location, "body-xml")
        self.assertEqual(my_insertion_points[7].key, "testing.new_tag")
        self.assertEqual(my_insertion_points[7].value,"1")



if __name__ == "__main__":
    unittest.main()
