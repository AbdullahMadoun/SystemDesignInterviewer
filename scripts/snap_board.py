#!/usr/bin/env python3
"""
Capture a zoom-to-fit snapshot of a live Excalidraw collaboration room.

Joins the room in a headless Chromium browser, waits for the scene to sync,
presses Shift+1 (zoom to fit all elements), and saves a PNG screenshot that
an agent can inspect.

Usage:
    snap_board.py <excalidraw_room_url> <output_png> [--settle SECONDS] [--timeout SECONDS]

Exit codes:
    0  success
    1  runtime failure (navigation, canvas not found, screenshot failed)
    2  invalid arguments
    3  Playwright not installed

Privacy: the room URL fragment contains the room's encryption key. This script
never prints or logs the URL.
"""

import argparse
import asyncio
import os
import re
import sys

ROOM_URL_RE = re.compile(r"^https://(www\.)?excalidraw\.com/#room=[A-Za-z0-9]+,[A-Za-z0-9_-]+$")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Snapshot a live Excalidraw room to PNG.")
    parser.add_argument("room_url", help="https://excalidraw.com/#room=<id>,<key>")
    parser.add_argument("output_path", help="Destination .png path")
    parser.add_argument("--settle", type=float, default=5.0,
                        help="Seconds to wait after the canvas appears for collaborators' elements to sync (default: 5)")
    parser.add_argument("--timeout", type=float, default=30.0,
                        help="Navigation / canvas-ready timeout in seconds (default: 30)")
    args = parser.parse_args()

    if not ROOM_URL_RE.match(args.room_url):
        parser.error("room_url must look like https://excalidraw.com/#room=<id>,<key>")
    if not args.output_path.lower().endswith(".png"):
        parser.error("output_path must end with .png")
    if args.settle < 0 or args.timeout <= 0:
        parser.error("--settle must be >= 0 and --timeout must be > 0")
    return args


async def snap(room_url: str, output_path: str, settle: float, timeout: float) -> None:
    from playwright.async_api import async_playwright

    timeout_ms = int(timeout * 1000)
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        try:
            context = await browser.new_context(viewport={"width": 1920, "height": 1080})
            page = await context.new_page()
            await page.goto(room_url, timeout=timeout_ms, wait_until="domcontentloaded")
            await page.wait_for_selector("canvas", state="visible", timeout=timeout_ms)

            # Give the collaboration socket time to deliver existing elements.
            await asyncio.sleep(settle)

            # Focus the canvas without drawing anything, then zoom to fit.
            await page.keyboard.press("Escape")
            await page.keyboard.press("Shift+Digit1")
            await asyncio.sleep(1)

            os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)
            await page.screenshot(path=output_path, full_page=False)
        finally:
            await browser.close()


def main() -> int:
    args = parse_args()
    try:
        import playwright  # noqa: F401
    except ImportError:
        print("Error: Playwright is not installed. Run:\n"
              "  pip install -r requirements.txt && python3 -m playwright install chromium",
              file=sys.stderr)
        return 3

    try:
        asyncio.run(snap(args.room_url, args.output_path, args.settle, args.timeout))
    except Exception as exc:  # report a single clean line to the agent
        print(f"Error: snapshot failed: {type(exc).__name__}: {str(exc).splitlines()[0] if str(exc) else ''}",
              file=sys.stderr)
        return 1

    print(f"Snapshot saved to {os.path.abspath(args.output_path)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
