

def prettify_tracker_log_dict(dict):

    pretty_status = {
                    "count_showup":"You showed up!",
                    "count_value":"Still working on it..",
                    "boolean_showup": "You showed up!",
                    "boolean_success": "Great success!!",
                    "fail_or_no_submit":"Did not complete",}

    if dict['tracker'].metric_tracker_type == "boolean":
        if dict['boolean_status'] != None:
            status = pretty_status[dict['boolean_status']]
        else:
            status = "awaiting progress"
        dict_status_pretty = {  "tracker type": "Yes or no",
                                "period starts": dict["period_log_start"],
                                "period ends": dict['period_log_end'],
                                "period status": status,
                                }
    else:
        if dict["tracker"].metric_tracker_type == "maximize":
            tracker_type = "counting up"
        else:
            tracker_type = "counting down"

        if dict['count_status'] != None:
            status = pretty_status[dict['count_status']]
        else:
            status = "awaiting progress"
        dict_status_pretty = {  "tracker type": tracker_type,
                                "period starts": dict["period_log_start"],
                                "period ends": dict['period_log_end'],
                                "period status": status,
                                "logs in period": dict['count_quantity'],
                                "total count": dict['count_status'],
                                }

    return dict_status_pretty
