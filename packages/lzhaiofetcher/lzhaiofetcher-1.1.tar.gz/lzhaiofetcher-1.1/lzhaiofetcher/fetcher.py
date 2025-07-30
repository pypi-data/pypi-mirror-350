import aiohttp
import asyncio
import random
import logging
from lzhgetlogger import get_logger

logger = get_logger(level=logging.INFO)

class AioFetcher:
    """
    将 aiohttp 的异步 get 封装了 3 个函数。包含失败重试、串行任务、并行任务、随机延迟、任务并发数控制等特性
    ##### 示例
    - 单个任务
    ```python
    import asyncio
    from lzhaiofetcher import AioFetcher

    async def main():
        fetcher = AioFetcher()
        html = await fetcher.fetch('http://example.com')
        if html:
            print(html[:200])
        await fetcher.close()

    asyncio.run(main())
    ```
    - 多个任务，顺序做
    ```python
    import asyncio
    from lzhaiofetcher import AioFetcher

    async def main():
        fetcher = AioFetcher()
        urls = ["https://example.com", "https://another.com"]
        results = await fetcher.fetch_all(urls)
        await fetcher.close()

    asyncio.run(main())
    ```
    - 多个任务，同时做
    ```python
    import asyncio
    from lzhaiofetcher import AioFetcher

    async def main():
        fetcher = AioFetcher(max_connections=20, concurrent_tasks=5)
        urls = ["https://example.com", "https://another.com", "https://something.com"]
        results = await fetcher.fetch_all_concurrent(urls)
        await fetcher.close()

    asyncio.run(main())
    ```
    """
    def __init__(
            self, 
            timeout=30, 
            max_connections=100, 
            max_retries=2, 
            min_delay=0.5, 
            max_delay=1.5, 
            concurrent_tasks=3):
        """
        - `min_delay` 任务间随机延迟最小值，单位秒
        - `max_delay` 任务间随机延迟最大值，单位秒
        - `concurrent_tasks` 任务并发数
        """
        self._timeout = aiohttp.ClientTimeout(total=timeout)
        self._connector = aiohttp.TCPConnector(limit=max_connections, ssl=True)
        self._session = None
        self._max_retries = max_retries
        self._min_delay = min_delay
        self._max_delay = max_delay
        self._concurrent_tasks = concurrent_tasks

    async def _ensure_session(self):
        if self._session is None or self._session.closed:
            self._session = aiohttp.ClientSession(
                timeout=self._timeout,
                connector=self._connector,
                headers={
                    "User-Agent": self._random_user_agent()
                }
            )

    def _random_user_agent(self):
        agents = [
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Safari/605.1.15",
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
        ]
        return random.choice(agents)

    async def fetch(self, url:str):
        """单个任务，失败重试"""
        await self._ensure_session()
        attempt = 0
        while attempt < self._max_retries:
            try:
                async with self._session.get(url) as response:
                    raw_data = await response.read()
                    html = raw_data.decode('utf-8')
                    logger.info(f"[Success] {url}")
                    return html

            except Exception as e:
                logger.info(f"[Retry {attempt + 1}] {url} failed: {e}")
                attempt += 1
                await asyncio.sleep(1)

        logger.info(f"[Error] Giving up on {url} after {self._max_retries} retries.")
        return None

    async def fetch_all(self, urls:list[str]):
        """
        多个任务，顺序执行，任务间有随机延迟
        - `urls`网址列表
        """
        await self._ensure_session()

        results = []
        result = await self.fetch(url)
        results.append(result)
        for url in urls[1:]:
            delay = random.uniform(self._min_delay, self._max_delay)
            await asyncio.sleep(delay)
            result = await self.fetch(url)
            results.append(result)
        return results

    async def fetch_all_concurrent(self, urls:list[str]):
        """
        多个任务，并发执行，任务开启间有随机延迟
        - `urls`网址列表
        """
        await self._ensure_session()

        semaphore = asyncio.Semaphore(self._concurrent_tasks)

        async def sem_fetch(url):
            async with semaphore:
                delay = random.uniform(self._min_delay, self._max_delay)
                await asyncio.sleep(delay)
                return await self.fetch(url)

        tasks = [asyncio.create_task(sem_fetch(url)) for url in urls]
        results = await asyncio.gather(*tasks)
        return results

    async def close(self):
        if self._session and not self._session.closed:
            await self._session.close()
