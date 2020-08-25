from sys import stderr

from click import Choice as CHOICE, STRING, argument, group, option

from loguru import logger

from notifiers.logging import NotificationHandler

from .api import API as PTP_API, ENDPOINTDEF as PTP_ENDPOINTDEF


@group()
@option('--log-level',
        type=CHOICE(['CRITICAL', 'ERROR', 'WARNING', 'INFO', 'DEBUG', 'SUCCESS', 'TRACE'],
                    case_sensitive=False),
        default='INFO')
@option('--slack-webhook',
        type=STRING,
        envvar='SLACK_WEBHOOK',
        default=None)
@option('--slack-username',
        type=STRING,
        envvar='SLACK_USERNAME',
        default=__name__)
@option('--slack-format',
        type=STRING,
        envvar='SLACK_FORMAT',
        default='{message}')
def cli(log_level, slack_webhook, slack_username, slack_format):
    logger.remove()
    logger.add(stderr, level=log_level)

    if slack_webhook:
        params = {
            "username": slack_username,
            "webhook_url": slack_webhook
        }
        slack = NotificationHandler("slack", defaults=params)
        logger.add(slack, format=slack_format, level="SUCCESS")


@cli.command(name='get-torrent')
@option('--api-user',
        type=STRING,
        required=True)
@option('--api-key',
        type=STRING,
        required=True)
@option('--endpoint',
        type=STRING,
        required=False,
        default=PTP_ENDPOINTDEF)
@argument('hash',
          type=STRING,
          required=True)
def get_torrent(api_user, api_key, endpoint, hash):
    hash = hash.upper()
    logger.info(PTP_API(api_user, api_key, endpoint).get_torrent(hash))


if __name__ == "__main__":
    cli()
