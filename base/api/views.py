import hashlib
import random
import secrets

from mnemonic import Mnemonic
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView

from .client import qrng


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token["username"] = user.username
        token["email"] = user.email
        return token


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


def _positive_int(value, field, maximum):
    try:
        parsed = int(value)
    except (TypeError, ValueError):
        raise ValueError(f"{field} must be an integer")
    if parsed <= 0 or parsed > maximum:
        raise ValueError(f"{field} must be between 1 and {maximum}")
    return parsed


@api_view(["GET", "POST"])
def getQrng(request):
    key = random.randint(100000000000, 99999999999999)
    data = hashlib.sha256(str(key).encode("utf-8")).hexdigest()
    return Response({"type": "hex16", "data": data, "success": True})


@api_view(["POST"])
def getqrng_DecimalArray(request):
    try:
        length = _positive_int(request.data.get("length"), "length", 20)
    except ValueError as exc:
        return Response(
            {"type": "uint8", "message": str(exc), "success": False},
            status=status.HTTP_400_BAD_REQUEST,
        )

    if request.data.get("method") == "qrng":
        try:
            data = qrng("127.0.0.1", 1721).getQrngArray(length)
            return Response({"type": "uint8", "data": data, "success": True})
        except (OSError, ValueError, ConnectionError):
            pass

    data = [secrets.randbelow(256) for _ in range(length)]
    return Response({"type": "uint8", "data": data, "success": True})


@api_view(["GET", "POST"])
def getQrngDecimalinrandom(request):
    if request.method == "POST" and request.data.get("method") == "qrng":
        try:
            data = qrng("127.0.0.1", 1721).getQrngDecimal(3)
            return Response({"type": "uint8", "data": data, "success": True})
        except (OSError, ValueError, ConnectionError):
            pass

    key = random.randint(100000000000, 99999999999999)
    digest = hashlib.sha256(str(key).encode("utf-8")).hexdigest()
    return Response({"type": "decimal", "data": int(digest, 16), "success": True})


@api_view(["GET"])
def get_mnemonic_details(request):
    words = Mnemonic("english").generate(strength=256).split()
    return Response({"mnemonic_words": words, "success": True})


@api_view(["POST"])
def getQrngHexArrayinrandom(request):
    try:
        length = _positive_int(request.data.get("length"), "length", 20)
        size = _positive_int(request.data.get("size"), "size", 9)
    except ValueError as exc:
        return Response(
            {"type": "hex16", "message": str(exc), "success": False},
            status=status.HTTP_400_BAD_REQUEST,
        )

    if request.data.get("method") == "qrng":
        try:
            data = qrng("127.0.0.1", 1721).getQrngHexArray(length, size)
            return Response({"type": "hex16", "data": data, "success": True})
        except (OSError, ValueError, ConnectionError):
            pass

    required_chars = length * size
    text = secrets.token_hex((required_chars + 1) // 2)[:required_chars]
    data = [text[index : index + size] for index in range(0, required_chars, size)]
    return Response({"type": "hex16", "data": data, "success": True})


@api_view(["GET"])
def health(request):
    return Response({"status": "ok"})
