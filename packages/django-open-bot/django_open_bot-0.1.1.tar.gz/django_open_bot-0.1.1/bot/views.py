import json
import logging
import requests
from django.http import JsonResponse
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt


from .utils import get_bot_model


logger = logging.getLogger(__name__)

@csrf_exempt
def telegram_webhook(request, pk):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            bot = get_bot_model()
            bot = bot.objects.get(pk=pk)
            bot.dp.updater(data)
            return JsonResponse({"status": "success"}, status=200)
        except Exception as e:
            logger.error(f"Error in webhook: {str(e)}")
            return JsonResponse({"status": "failed", "message": str(e)}, status=400)
    return JsonResponse({"status": "ok"}, status=200)


def get_webhook(request):
    bot = get_bot_model()
    bots = bot.objects.all()
    ws = []
    for bot in bots:
        webhook_url = f"{bot.base_api}bot{bot.token}/setWebhook?url={f'{request.build_absolute_uri()}{bot.id}/'}"
        response = requests.get(webhook_url)
        ws.append({f'{request.build_absolute_uri()}{bot.id}/': response.json()})
    return JsonResponse({"status": "ok", "webhooks": ws}, status=200)


