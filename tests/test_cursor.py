#
#  Copyright (c) 2022, salesforce.com, inc.
#  All rights reserved.
#  SPDX-License-Identifier: BSD-3-Clause
#  For full license text, see the LICENSE file in the repo root or https://opensource.org/licenses/BSD-3-Clause
#

import unittest
from unittest.mock import patch

from salesforcecdpconnector.connection import SalesforceCDPConnection
from salesforcecdpconnector.query_submitter import QuerySubmitter


class MyTestCase(unittest.TestCase):

    call1 = {
        "data": [
            [
                "Andy",
                "2021-09-16T16:26:36.000+00:00"
            ],
            [
                "Jon",
                "2021-09-16T16:26:36.000+00:00"
            ],
            [
                "Sarah",
                "2021-09-16T16:26:36.000+00:00"
            ]
        ],
        "startTime": "2022-03-07T19:57:19.374525Z",
        "endTime": "2022-03-07T19:57:20.063372Z",
        "rowCount": 3,
        "queryId": "20220307_195719_00109_5frjj",
        "nextBatchId": "fa489494-ff42-45ce-afd6-b838854b5a99",
        "done": False,
        "metadata": {
            "ssot__FirstName__c": {
                "type": "VARCHAR",
                "placeInOrder": 0,
                "typeCode": 12
            },
            "ssot__LastModifiedDate__c": {
                "type": "TIMESTAMP",
                "placeInOrder": 1,
                "typeCode": 93
            }
        }
    }

    call2 = {
        "data": [
            [
                "Andy",
                "2021-09-16T16:26:36.000+00:00"
            ],
            [
                "Jon",
                "2021-09-16T16:26:36.000+00:00"
            ],
            [
                "Sarah",
                "2021-09-16T16:26:36.000+00:00"
            ]
        ],
        "startTime": "2022-03-07T19:57:19.374525Z",
        "endTime": "2022-03-07T19:57:20.063372Z",
        "rowCount": 3,
        "queryId": "20220307_195719_00109_5frjj",
        "nextBatchId": "fa489494-ff42-45ce-afd6-b838854b5a99",
        "done": True,
        "metadata": {
            "ssot__FirstName__c": {
                "type": "VARCHAR",
                "placeInOrder": 0,
                "typeCode": 12
            },
            "ssot__LastModifiedDate__c": {
                "type": "TIMESTAMP",
                "placeInOrder": 1,
                "typeCode": 93
            }
        }
    }

    empty_batch_intermediate = {
        "data": [
        ],
        "startTime": "2022-03-07T19:57:19.374525Z",
        "endTime": "2022-03-07T19:57:20.063372Z",
        "rowCount": 3,
        "queryId": "20220307_195719_00109_5frjj",
        "nextBatchId": "fa489494-ff42-45ce-afd6-b838854b5a99",
        "done": False,
        "metadata": {
            "ssot__FirstName__c": {
                "type": "VARCHAR",
                "placeInOrder": 0,
                "typeCode": 12
            },
            "ssot__LastModifiedDate__c": {
                "type": "TIMESTAMP",
                "placeInOrder": 1,
                "typeCode": 93
            }
        }
    }

    empty_batch_last = {
        "data": [
        ],
        "startTime": "2022-03-07T19:57:19.374525Z",
        "endTime": "2022-03-07T19:57:20.063372Z",
        "rowCount": 3,
        "queryId": "20220307_195719_00109_5frjj",
        "nextBatchId": "fa489494-ff42-45ce-afd6-b838854b5a99",
        "done": True,
        "metadata": {
            "ssot__FirstName__c": {
                "type": "VARCHAR",
                "placeInOrder": 0,
                "typeCode": 12
            },
            "ssot__LastModifiedDate__c": {
                "type": "TIMESTAMP",
                "placeInOrder": 1,
                "typeCode": 93
            }
        }
    }

    @patch.object(QuerySubmitter, 'get_next_batch', return_value=call2)
    @patch.object(QuerySubmitter, 'execute', return_value=call1)
    def test_execute(self, mock1, mock2):
        connection = SalesforceCDPConnection('login_url', 'username', 'password', 'client_id', 'client_secret')
        cursor = connection.cursor()
        cursor.execute("select * from UnifiedIndividuals__dlm")
        self.assertEqual(len(cursor.data), 3)
        cursor.fetchall()
        self.assertEqual(len(cursor.data), 6)
        cursor.close()

    @patch.object(QuerySubmitter, 'get_next_batch', return_value=empty_batch_last)
    @patch.object(QuerySubmitter, 'execute', return_value=call1)
    def test_fetchoneendingwithemptybatch(self, mock1, mock2):
        connection = SalesforceCDPConnection('login_url', 'username', 'password', 'client_id', 'client_secret')
        cursor = connection.cursor()
        cursor.execute("select * from UnifiedIndividuals__dlm")
        all_records = []
        record = cursor.fetchone()
        while record is not None:
            all_records.append(record)
            record = cursor.fetchone()
        self.assertEqual(len(all_records), 3)
        cursor.close()

    def test_params_fail(self):
        connection = SalesforceCDPConnection('login_url', 'username', 'password', 'client_id', 'client_secret')
        cursor = connection.cursor()
        with self.assertRaises(Exception) as context:
            cursor.execute("select * from UnifiedIndividuals__dlm where col__c = ?", ['test'])
        self.assertTrue("Parameters are not supported" in context.exception.args)

if __name__ == '__main__':
    unittest.main()
