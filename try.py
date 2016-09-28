from collections import namedtuple

log_data = """1.1.2014 12:01,111-222-333,454-333-222,COMPLETED
1.1.2014 13:01,111-222-333,111-333,FAILED
1.1.2014 13:04,111-222-333,454-333-222,FAILED
1.1.2014 13:05,111-222-333,454-333-222,COMPLETED
2.1.2014 13:01,111-333,111-222-333,FAILED
"""

expected_result = {
    "111-222-333": "40.00%",
    "454-333-222": "66.67%",
    "111-333" : "0.00%"
}

Call = namedtuple('Call', ['date', 'caller', 'callee', 'status'])


def compute_success_ratio(logdata):
    log_data_dict = {}
    result = {}
    for line in logdata.split('\n'):
        if line:
            call = Call(*line.split(','))

            if call.caller not in log_data_dict:
                log_data_dict[call.caller] = {'total':0, 'success': 0}

            if call.callee not in log_data_dict:
                log_data_dict[call.callee] = {'total': 0, 'success': 0}

            log_data_dict[call.caller]['total'] += 1
            log_data_dict[call.callee]['total'] += 1

            if call.status == 'COMPLETED':
                log_data_dict[call.caller]['success'] += 1
                log_data_dict[call.callee]['success'] += 1

        for phone_number, call_info in log_data_dict.items():
            result[phone_number] = '{:.2f}%'.format(call_info['success'] * 100 / call_info['total'])

    return result


if __name__ == "__main__":
    assert(compute_success_ratio(log_data) == expected_result)