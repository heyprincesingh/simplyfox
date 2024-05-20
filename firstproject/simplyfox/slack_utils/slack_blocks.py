from simplyfox.slack_utils.slack_block_functions import replace_last_block_with_loading, update_for_days_selected, update_for_query_answers, update_for_summaryBox


def slack_block(block_id, updated_data=None):
    block = slack_blocks_list[block_id]
    if block_id == "app_home_days_selected":
        return update_for_days_selected(block, updated_data[0], updated_data[1])
    elif block_id == "app_home_get_summary":
        block["blocks"] = updated_data
        return update_for_summaryBox(block)
    elif block_id == "app_home_query_answers":
        block["blocks"] = update_for_query_answers(blocks=updated_data[0], query_answer=updated_data[1])
    elif block_id == "replace_last_block_with_loading":
        block["blocks"] = replace_last_block_with_loading(blocks=updated_data)
    return block 


slack_blocks_list = {
    "app_home_opened": {
        "type": "home",
        "blocks": [
            {
                "type": "header",
                "text": {
                    "type": "plain_text",
                    "text": "Get your conversations simplified!",
                },
            },
            {
                "type": "input",
                "element": {
                    "type": "multi_channels_select",
                    "placeholder": {
                        "type": "plain_text",
                        "text": "Select channel",
                    },
                    "action_id": "channelsList",
                },
                "label": {
                    "type": "plain_text",
                    "text": "Which channels do you want me to summarize?",
                },
            },
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": "Summarize these many days of conversation",
                },
                "accessory": {
                    "type": "static_select",
                    "placeholder": {
                        "type": "plain_text",
                        "text": "Select days",
                    },
                    "options": [
                        {
                            "text": {"type": "plain_text", "text": "1"},
                            "value": "1",
                        },
                        {
                            "text": {"type": "plain_text", "text": "2"},
                            "value": "2",
                        },
                        {
                            "text": {"type": "plain_text", "text": "3"},
                            "value": "3",
                        },
                        {
                            "text": {"type": "plain_text", "text": "4"},
                            "value": "4",
                        },
                        {
                            "text": {"type": "plain_text", "text": "5"},
                            "value": "5",
                        },
                    ],
                    "action_id": "daysSelect",
                },
            },
        ],
    },
    "app_home_days_selected": {
        "type": "home",
        "blocks": [
            {
                "type": "header",
                "text": {
                    "type": "plain_text",
                    "text": "Get your conversations simplified!",
                },
            },
            {
                "type": "input",
                "element": {
                    "type": "multi_channels_select",
                    "placeholder": {"type": "plain_text", "text": "Select channel"},
                    "action_id": "channelsList",
                },
                "label": {
                    "type": "plain_text",
                    "text": "Which channels do you want me to summarize?",
                },
            },
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": "Summarize these many days of conversation",
                },
                "accessory": {
                    "type": "static_select",
                    "placeholder": {"type": "plain_text", "text": "Select days"},
                    "options": [
                        {"text": {"type": "plain_text", "text": "1"}, "value": "1"},
                        {"text": {"type": "plain_text", "text": "2"}, "value": "2"},
                        {"text": {"type": "plain_text", "text": "3"}, "value": "3"},
                        {"text": {"type": "plain_text", "text": "4"}, "value": "4"},
                        {"text": {"type": "plain_text", "text": "5"}, "value": "5"},
                    ],
                    "action_id": "daysSelect",
                },
            },
        ],
    },
    "app_home_get_summary": {
        "type": "home",
    },
    "app_home_summary_loading": {
        "type": "home",
        "blocks": [
            {
                "type": "context",
                "elements": [
                    {
                        "type": "image",
                        "image_url": "https://media.tenor.com/dHAJxtIpUCoAAAAi/loading-animation.gif",
                        "alt_text": "Loading...",
                    },
                    {
                        "type": "plain_text",
                        "text": "You're summarization is on the way!"
                    },
                ],
            }
        ],
    },
    "app_home_query_answers": {
        "type": "home",
    },
    "replace_last_block_with_loading": {
        "type": "home",
    },
}
