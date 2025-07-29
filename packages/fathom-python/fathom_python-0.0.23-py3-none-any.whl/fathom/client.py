from .base_client import BaseClient, AsyncBaseClient
from svix.webhooks import Webhook


class FathomApi(BaseClient):
  def verify_webhook(
    self,
    webhook_secret: str,
    headers: dict,
    payload: str
  ):
    wh = Webhook(webhook_secret)
    return wh.verify(payload, headers)



class AsyncFathomApi(AsyncBaseClient):
  def verify_webhook(
    self,
    webhook_secret: str,
    headers: dict,
    payload: str
  ):
    wh = Webhook(webhook_secret)
    return wh.verify(payload, headers)
