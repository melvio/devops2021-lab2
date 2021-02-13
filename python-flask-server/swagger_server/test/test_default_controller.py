# coding: utf-8

from __future__ import absolute_import

from flask import json

from swagger_server.models.student import Student  # noqa: E501
from swagger_server.test import BaseTestCase
import names


class TestDefaultController(BaseTestCase):
    """DefaultController integration test stubs"""

    def test_add_student(self):
        """Test case for add_student
        Add a new student
        """
        body = Student()
        body.first_name = names.get_first_name()
        body.last_name = names.get_last_name()
        body.grades = {'math': 8, 'history': 9}
        response = self.client.open(
            '/service-api/student',
            method='POST',
            data=json.dumps(body),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))
        self.assertTrue(response.is_json)
        self.assertIsInstance(response.json, int)

    def test_delete_student(self):
        """Test case for delete_student
        """
        body = Student()
        body.first_name = names.get_first_name()
        body.last_name = names.get_last_name()
        body.grades = {'math': 8, 'history': 9}
        response = self.client.open(
            '/service-api/student',
            method='POST',
            data=json.dumps(body),
            content_type='application/json')
        student_id = (response.json)
        # response = self.client.open(
        #     '/service-api/student/{student_id}'.format(student_id=student_id),
        #     method='DELETE')
        # self.assert200(response,
        #                'Response body is : ' + response.data.decode('utf-8'))
        #
        # response = self.client.open(
        #     '/service-api/student/{student_id}'.format(student_id=-1),
        #     method='DELETE')
        # self.assert404(response,
        #                'Response body is : ' + response.data.decode('utf-8'))

    def test_get_student_by_id(self):
        """Test case for get_student_by_id

        Find student by ID
        """
        body = Student()
        body.first_name = names.get_first_name()
        body.last_name = names.get_last_name()
        body.grades = {'math': 8, 'history': 9}
        response = self.client.open(
            '/service-api/student',
            method='POST',
            data=json.dumps(body),
            content_type='application/json')
        student_id = (response.json)

        query_string = [('math', 9)]
        response = self.client.open(
            '/service-api/student/{student_id}'.format(student_id=student_id),
            method='GET',
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))
        self.assertTrue(response.is_json)
        self.assertIsInstance(response.json, dict)


if __name__ == '__main__':
    import unittest

    unittest.main()
