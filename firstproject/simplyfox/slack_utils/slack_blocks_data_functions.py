from simplyfox.slack_utils.slack_get_functions import get_channel_info

def format_data_into_blocks(data):
    summary_update_blocks = [
        {
            "type": "header",
            "text": {
                "type": "plain_text",
                "text": "📩 Here's your Summary! 🔻",
            },
        },
        {"type": "divider"},
    ]
    
    for channel_id, summary in data.items():
        summary_chunks = split_text(summary)
        for i, chunk in enumerate(summary_chunks):
            if i == 0:
                summary_update_blocks.extend(
                    [
                        {
                            "type": "section",
                            "text": {
                                "type": "mrkdwn",
                                "text": f"💬 In *<#{channel_id}>* channel, you had these conversations:",
                            },
                        },
                        {
                            "type": "section",
                            "text": {"type": "mrkdwn", "text": chunk},
                        },
                    ]
                )
            else:
                summary_update_blocks.extend(
                    [
                        {
                            "type": "section",
                            "text": {"type": "mrkdwn", "text": chunk},
                        },
                    ]
                )
        summary_update_blocks.append({"type": "divider"})
    
    return summary_update_blocks


def format_blocks_into_data(block_data, client):
    if 'view' not in block_data or 'blocks' not in block_data['view']:
        return ""

    blocks = block_data['view']['blocks']
    texts = []

    symbol_mapping = {
        ":envelope_with_arrow:": "📩",
        ":small_red_triangle_down:": "🔻",
        ":speech_balloon:": "💬",
        ":incoming_envelope:": "📨"
    }

    for block in blocks:
        if block['type'] == 'divider':
            texts.append('---')
        elif 'text' in block:
            text_data = block['text']
            if isinstance(text_data, dict) and 'text' in text_data:
                text = text_data['text']
                if block['type'] == 'header':
                    text = f"*{text}*"
                
                text = replace_channel_id_with_name(text, client)

                for symbol_name, symbol in symbol_mapping.items():
                    text = text.replace(symbol_name, symbol)
                texts.append(text)

    return '\n\n'.join(texts).replace("*", "**").replace("**Ans:","\n**Ans:")

def replace_channel_id_with_name(text, client):
    import re

    channel_pattern = re.compile(r"<#(C\w+)>")
    matches = channel_pattern.findall(text)

    for channel_id in matches:
        channel_info = get_channel_info(client, channel_id)
        if channel_info["ok"]:
            if channel_name := channel_info["channel"]["name"]:
                text = text.replace(f"<#{channel_id}>", f"#{channel_name}")
    return text

def split_text(text, max_length=2900):
    chunks = []
    while len(text) > max_length:
        split_at = text.rfind('\n', 0, max_length)
        if split_at == -1:
            split_at = max_length
        chunks.append(text[:split_at])
        text = text[split_at:].lstrip()
    chunks.append(text)
    return chunks