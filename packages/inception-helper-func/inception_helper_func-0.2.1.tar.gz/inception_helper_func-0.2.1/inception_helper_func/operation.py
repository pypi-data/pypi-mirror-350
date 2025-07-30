import aiohttp
from fastapi import HTTPException


async def post_data(
    payload: dict, url: str, authorization: str, extra_headers: dict = {}
):
    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(
                url,
                json=payload,
                headers={
                    "Content-Type": "application/json",
                    "Authorization": authorization,
                    **extra_headers,
                },
            ) as response:
                if response.status in (200, 201):
                    return await response.json()

                error_detail = await response.text()
                raise HTTPException(
                    status_code=response.status,
                    detail=f"Failed to save data: {error_detail}",
                )
    except aiohttp.ClientError as e:
        raise HTTPException(
            status_code=500, detail=f"Network error occurred on {url}: {str(e)}"
        )
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Unexpected error occurred on {url}: {str(e)}"
        )


async def get_data(url: str, authorization: str, extra_headers: dict = {}):
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(
                url,
                headers={
                    "Content-Type": "application/json",
                    "Authorization": authorization,
                    **extra_headers,
                },
            ) as response:
                if response.status in (200, 201):
                    return await response.json()

                error_detail = await response.text()
                raise HTTPException(
                    status_code=response.status,
                    detail=f"Failed to retrieve data: {error_detail}",
                )
    except aiohttp.ClientError as e:
        raise HTTPException(
            status_code=500, detail=f"Network error occurred on {url}: {str(e)}"
        )
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Unexpected error occurred on {url}: {str(e)}"
        )


async def put_data(
    payload: dict, url: str, authorization: str, extra_headers: dict = {}
):
    try:
        async with aiohttp.ClientSession() as session:
            async with session.put(
                url,
                json=payload,
                headers={
                    "Content-Type": "application/json",
                    "Authorization": authorization,
                    **extra_headers,
                },
            ) as response:
                if response.status in (200, 201):
                    return await response.json()

                error_detail = await response.text()
                raise HTTPException(
                    status_code=response.status,
                    detail=f"Failed to update data: {error_detail}",
                )
    except aiohttp.ClientError as e:
        raise HTTPException(
            status_code=500, detail=f"Network error occurred on {url}: {str(e)}"
        )
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Unexpected error occurred on {url}: {str(e)}"
        )


async def delete_data(url: str, authorization: str, extra_headers: dict = {}):
    try:
        async with aiohttp.ClientSession() as session:
            async with session.delete(
                url,
                headers={
                    "Content-Type": "application/json",
                    "Authorization": authorization,
                    **extra_headers,
                },
            ) as response:
                if response.status in (200, 201):
                    return await response.json()

                error_detail = await response.text()
                raise HTTPException(
                    status_code=response.status,
                    detail=f"Failed to delete data: {error_detail}",
                )
    except aiohttp.ClientError as e:
        raise HTTPException(
            status_code=500, detail=f"Network error occurred on {url}: {str(e)}"
        )
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Unexpected error occurred on {url}: {str(e)}"
        )


async def patch_data(
    payload: dict, url: str, authorization: str, extra_headers: dict = {}
):
    try:
        async with aiohttp.ClientSession() as session:
            async with session.patch(
                url,
                json=payload,
                headers={
                    "Content-Type": "application/json",
                    "Authorization": authorization,
                    **extra_headers,
                },
            ) as response:
                if response.status in (200, 201):
                    return await response.json()

                error_detail = await response.text()
                raise HTTPException(
                    status_code=response.status,
                    detail=f"Failed to patch data: {error_detail}",
                )
    except aiohttp.ClientError as e:
        raise HTTPException(
            status_code=500, detail=f"Network error occurred on {url}: {str(e)}"
        )
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Unexpected error occurred on {url}: {str(e)}"
        )
