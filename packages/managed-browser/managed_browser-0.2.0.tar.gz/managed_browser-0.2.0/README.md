# Managed Browser

A minimal wrapper to seamlessly integrate [browser-use](https://github.com/browser-use/browser-use/tree/main/browser_use) agents into your existing Playwright (Python) workflows.

---

## Motivation
Browser agents powered by LLMs can think creatively—click links by intent, extract arbitrary data, and navigate dynamic UIs—but they remain **inherently non-deterministic**. They may:

- Misinterpret a button label or page layout  
- Click the wrong element when the UI changes  
- Drift off-task if given an open-ended prompt  

Meanwhile, your Playwright scripts are **rock-solid and repeatable**, but rigid for anything beyond well-defined interactions.

**managed-browser** bridges the gap:

1. **Drop-in Agent Segments**  
   Invoke an LLM-driven agent exactly where you need it, without refactoring your existing Playwright logic.

2. **Seamless Control Transfer**  
   Hand off to the agent, then regain the _exact same_ `Page`—with cookies, localStorage, DOM state, and session intact—so you can resume deterministic flows.

3. **Best of Both Worlds**  
   Let Playwright handle the mechanical, repeatable steps; delegate the fuzzy, creative extraction to your agent, then pick up where you left off.

4. **Full Visibility & Audit**  
   Wrap every agent run in a Playwright trace ZIP for step-by-step replay, screenshots, network logs, and DOM snapshots.

---

## Installation

Requires **Python 3.11+**.

```bash
pip install managed-browser
```

---

## Quick Example

```python
import asyncio
from browser_use import BrowserConfig
from langchain_openai import ChatOpenAI
from managed_browser import BrowserManager

async def main():
    bm = BrowserManager(browser_config=BrowserConfig(headless=True))
    llm = ChatOpenAI(model="gpt-4o")

    async with bm.managed_context(use_tracing=True, tracing_output_path=...) as session:
        page = await session.browser_context.new_page()
        await page.goto("https://example.com/product/42")

        # 1) Agentic handoff: extract product info into JSON
        agent = session.make_agent(
            start_page=page,
            llm=llm,
            task="Return JSON: {\"title\": <product title>, \"price\": <price as number>}."
        )
        product_info, page = await agent.run()
        print("Extracted:", product_info)

        # 2) Hand control back to Playwright for a follow-up action
        await page.click("button#add-to-cart")
        await page.wait_for_selector(".cart-count")
        print("Added to cart, cart count:", await page.inner_text(".cart-count"))

    await bm.shutdown()

asyncio.run(main())
```

---

## Core API

### `BrowserManager(browser_config, *, autostart=True)`

- **`.managed_context(use_tracing=False, tracing_output_path=None, randomize_user_agent=True, context_kwargs=None)`**  
  Async context manager yielding a `ManagedSession`.
- **`.shutdown()`**  
  Gracefully close the browser.

### `ManagedSession`

- **`.browser_context`** → Playwright `BrowserContext`  
- **`.make_agent(start_page: Page, llm: BaseChatModel, **agent_kwargs)`**  
  Returns an `AgentWithControlTransfer` whose `.run()` yields `(output, final_page)`.

---

## License
MIT © Amrit Baveja
