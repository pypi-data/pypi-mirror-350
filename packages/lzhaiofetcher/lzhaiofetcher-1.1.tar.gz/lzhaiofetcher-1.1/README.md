# aiofetcher
将 aiohttp 的异步 get 封装了 3 个函数。包含失败重试、串行任务、并行任务、随机延迟、任务并发数控制等特性
## 示例
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

## 安装 - [PyPI](https://pypi.org/project/lzhaiofetcher/)
```bash
pip install lzhaiofetcher
```
## API
[Document](https://zhhtdm.github.io/aio-fetcher/)
