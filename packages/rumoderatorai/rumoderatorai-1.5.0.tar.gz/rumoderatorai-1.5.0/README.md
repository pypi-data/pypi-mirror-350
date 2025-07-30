# RuModeratorAI

Библиотека для использования Omni Antispam API (https://moderator.omni-devel.ru), в прошлом - RuModeratorAI API.

## Установка

```bash
pip install rumoderatorai
```

## Пример использования
```python
from rumoderatorai import Client, Context, ChatContext

import asyncio

from PIL import Image

import os


async def main():
    async with Client(
        api_key=os.getenv("RUMODERATORAI_API_KEY")
    ) as client:
        context = Context(
            chat_context=ChatContext(
                title="Test group",
                topic_title="Test topic"
            ),
            allowed_rules=[
                "mutual subscriptions",
                "job offers",
                "cars selling"
            ]
        )

        text_response = await client.get_text_class("Hello, world!", context=context)
        print(text_response)

        profile_response = await client.get_profile_class(
            username="test",
            first_name="test",
            last_name="test",
            description="test",
            is_premium=False,
        )
        print(profile_response)

        image = Image.open("tests/image.png")
        image_response = await client.get_image_class(image)
        print(image_response)

        ocr_response = await client.get_ocr(image)
        print(ocr_response)

        multimodal_text_response = await client.get_multimodal_text_class(
            text="Всем привет!",
            images=[
                "tests/image_spam.png", "tests/image_not_spam.png", "tests/image_spam_2.png"
            ],
            context=context
        )
        print(multimodal_text_response)

        stats_response = await client.get_stats()
        print(stats_response)

        key_info_response = await client.get_key_info()
        print(key_info_response)

        prediction_response = await client.get_prediction(unique_id=text_response.unique_id)
        print(prediction_response)

        ips_response = await client.get_ips()
        print(ips_response)

        prices_response = await client.get_prices()
        print(prices_response)


asyncio.run(main())
```

Или можно использовать без async with:
```python
from rumoderatorai import Client, Context, ChatContext

import asyncio

from PIL import Image

import os


async def main():
    client = Client(
        api_key=os.getenv("RUMODERATORAI_API_KEY"),
    )
    await client.init()

    context = Context(
        chat_context=ChatContext(
            title="Test group",
            topic_title="Test topic"
        ),
        allowed_rules=[
            "job offers",
            "cars selling"
        ]
    )

    text_response = await client.get_text_class("Hello, world!", context=context)
    print(text_response)

    profile_response = await client.get_profile_class(
        username="test",
        first_name="test",
        last_name="test",
        description="test",
        is_premium=False,
    )
    print(profile_response)

    image = Image.open("tests/image.png")
    image_response = await client.get_image_class(image)
    print(image_response)

    ocr_response = await client.get_ocr(image)
    print(ocr_response)

    multimodal_text_response = await client.get_multimodal_text_class(
        text="Всем привет!",
        images=[
            "tests/image_spam.png", "tests/image_not_spam.png", "tests/image_spam_2.png"
        ],
        context=context
    )
    print(multimodal_text_response)

    stats_response = await client.get_stats()
    print(stats_response)

    key_info_response = await client.get_key_info()
    print(key_info_response)

    prediction_response = await client.get_prediction(unique_id=text_response.unique_id)
    print(prediction_response)

    ips_response = await client.get_ips()
    print(ips_response)

    prices_response = await client.get_prices()
    print(prices_response)

    await client.close()


asyncio.run(main())
```

**Примечание:** Не забудьте установить переменную окружения `RUMODERATORAI_API_KEY` перед запуском кода.
