def update_for_days_selected(block, channels_list, days_selected):
    for block_item in block["blocks"]:
        if (
            block_item.get("type") == "input"
            and block_item["element"].get("type") == "multi_channels_select"
        ):
            block_item["element"]["initial_channels"] = channels_list

    for block_item in block["blocks"]:
        if (
            block_item.get("type") == "section"
            and block_item["accessory"].get("type") == "static_select"
        ):
            block_item["accessory"]["initial_option"] = {
                "text": {
                    "type": "plain_text",
                    "text": str(days_selected),
                },
                "value": str(days_selected),
            }

    new_block = {
        "type": "section",
        "text": {"type": "mrkdwn", "text": " "},
        "accessory": {
            "type": "button",
            "text": {"type": "plain_text", "text": "Get Summary!"},
            "style": "primary",
            "value": "click_me_123",
            "action_id": "buttonGetSummary",
        },
    }

    if not block_exists(block["blocks"], new_block):
        block["blocks"].append(new_block)

    return block


def update_for_summaryBox(block):
    new_block = {
        "type": "actions",
        "elements": [
            {
                "type": "button",
                "text": {"type": "plain_text", "text": "📩   Save me"},
                "style": "primary",
                "value": "saveSummary",
                "action_id": "saveSummary",
            },
            {
                "type": "button",
                "text": {"type": "plain_text", "text": "📨   Mail me"},
                "style": "danger",
                "value": "mailSummary",
                "action_id": "mailSummary",
            },
        ],
    }

    if not block_exists(block["blocks"], new_block):
        block["blocks"].append(new_block)

    new_block = {
        "dispatch_action": True,
        "type": "input",
        "element": {
            "type": "plain_text_input",
            "action_id": "questionAskedTextBox",
            "placeholder": {"type": "plain_text", "text": "(Optional)"},
        },
        "label": {"type": "plain_text", "text": "Any specific thing wanna find out?"},
    }

    if not block_exists(block["blocks"], new_block):
        block["blocks"].append(new_block)

    return block


def update_for_query_answers(blocks, query_answer):
    new_query_answer_block = {
        "type": "section",
        "text": {"type": "mrkdwn", "text": query_answer},
    }
    blocks[-1] = new_query_answer_block
    divider_block = {"type": "divider"}
    blocks.append(divider_block)
    new_block = {
        "dispatch_action": True,
        "type": "input",
        "element": {
            "type": "plain_text_input",
            "action_id": "questionAskedTextBox",
            "placeholder": {"type": "plain_text", "text": "(Optional)"},
        },
        "label": {"type": "plain_text", "text": "Any specific thing wanna find out?"},
    }

    if not block_exists(blocks, new_block):
        blocks.append(new_block)
    return blocks


def replace_last_block_with_loading(blocks):
    loading_block = {
        "type": "context",
        "elements": [
            {
                "type": "image",
                "image_url": "https://media.tenor.com/dHAJxtIpUCoAAAAi/loading-animation.gif",
                "alt_text": "Loading...",
            },
            {"type": "plain_text", "text": "Answer for your query is on the way!"},
        ],
    }
    blocks[-1] = loading_block
    return blocks


def block_exists(blocks, new_block):
    return any(block == new_block for block in blocks)


def remove_save_me_and_text_input_block(blocks):
    filtered_blocks = []

    for block in blocks:
        if block.get("type") == "actions":
            elements = block.get("elements", [])
            if any(
                el.get("type") == "button"
                and el.get("value") in ["saveSummary", "mailSummary"]
                for el in elements
            ):
                continue

        if block.get("type") == "input":
            element = block.get("element", {})
            if element.get("type") == "plain_text_input":
                continue

        filtered_blocks.append(block)

    return filtered_blocks