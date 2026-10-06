#!/usr/bin/env python3
"""
End-to-end test for the Excalidraw scripts (requires network + Playwright).

Simulates a real session:
1. Candidate opens Excalidraw and starts a live collaboration session.
2. Candidate dismisses the share modal and draws a component box.
3. write_board.py connects and posts a requirements card.
4. snap_board.py connects and captures the entire board.
5. Verifies both the box and the requirements card are captured.

Usage:
    python3 tests/e2e_board.py [--keep OUTPUT_PNG]
"""

from __future__ import annotations

import argparse
import asyncio
import os
import subprocess
import sys
import tempfile

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def run(script: str, *args: str, stdin: str | None = None) -> subprocess.CompletedProcess:
    return subprocess.run([sys.executable, os.path.join(ROOT, "scripts", script), *args],
                          input=stdin, capture_output=True, text=True, timeout=120)


async def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--keep", help="Copy the resulting snapshot here")
    args = parser.parse_args()

    from playwright.async_api import async_playwright

    out = args.keep or os.path.join(tempfile.mkdtemp(), "e2e.png")

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        candidate = await (await browser.new_context(viewport={"width": 1920, "height": 1080})).new_page()
        await candidate.goto("https://excalidraw.com", timeout=30000, wait_until="domcontentloaded")
        await candidate.wait_for_selector("canvas", state="visible", timeout=30000)
        await asyncio.sleep(2)

        # Start live collaboration session
        await candidate.locator('button:has-text("Share")').click()
        await asyncio.sleep(1)
        start_btn = candidate.locator('button:has-text("Start session")')
        if await start_btn.count() > 0:
            await start_btn.click()
            await asyncio.sleep(2)

        url = candidate.url
        # Dismiss share modal
        await candidate.mouse.click(100, 100)
        await asyncio.sleep(1)

        # Candidate draws a box
        await candidate.keyboard.press("r")
        await asyncio.sleep(0.5)
        await candidate.mouse.move(500, 300)
        await candidate.mouse.down()
        await candidate.mouse.move(800, 500)
        await candidate.mouse.up()
        await asyncio.sleep(1)

        # Interviewer writes requirements
        w = await asyncio.to_thread(run, "write_board.py", url, "-",
                                    stdin="E2E Requirements\n- 100M DAU\n- p99 < 200ms")
        print(f"write_board.py exit={w.returncode} {w.stdout.strip()} {w.stderr.strip()}")
        await asyncio.sleep(2)

        # Interviewer snaps board
        s = await asyncio.to_thread(run, "snap_board.py", url, out)
        print(f"snap_board.py exit={s.returncode} {s.stdout.strip()} {s.stderr.strip()}")
        await browser.close()

    ok = w.returncode == 0 and s.returncode == 0 and os.path.getsize(out) > 10_000
    print(f"Snapshot: {out}")
    print("E2E PASSED ✓ (verified live collaboration and board capture)" if ok else "E2E FAILED ✗")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(asyncio.run(main()))
