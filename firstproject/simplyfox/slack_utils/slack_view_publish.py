from .slack_blocks import slack_block

def view_publish(client, user_id, block_id, updated_data=None):
    return client.views_publish(
        user_id = user_id,
        view = slack_block(block_id, updated_data)
    )