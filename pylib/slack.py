from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError


def slack_message(message):
    token = 'xoxb-139838512128-6238539024723-IzEnQAAPyosDUaDWlB2HAUfQ'
    channel_id = "C067CS5ED4Z"
    client = WebClient(token=token)
    try:
        blocks = [
            {
                "type": "header",
                "text": {
                    "type": "plain_text",
                    "text": "Test Results"
                }
            }
        ]

        attachments = [
            {
                "color": "#ff0000",
                "blocks": [
                    {
                        "type": "section",
                        "text": {
                            "type": "mrkdwn",
                            "text": message
                        }
                    }
                ]
            }
        ]

        response = client.chat_postMessage(channel=channel_id, text='Test Results', blocks=blocks, attachments=attachments)
        # print(response)
    except SlackApiError as e:
        if not e.response['ok']:
            print(f'slack message send error')
            print(e.response)


if __name__ == '__main__':
    message = "It's a testing message."
    slack_message(message)
