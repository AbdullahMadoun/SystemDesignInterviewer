#!/usr/bin/env python3
"""
Write a multi-line text card onto a live Excalidraw collaboration room.

Used by the interviewer (at most once per session) to post the requirements
the candidate agreed on. Joins the room headlessly, moves the pointer to
(x, y) in viewport coordinates, and dispatches a native paste event carrying
the text. Excalidraw turns pasted plain text into a single text element at the
pointer and broadcasts it to all collaborators. (Pasting is far more reliable
headlessly than driving the text tool via toolbar clicks or shortcuts.)

Usage:
    write_board.py <excalidraw_room_url> <text> [--x PX] [--y PX] [--settle SECONDS] [--timeout SECONDS]
    write_board.py <excalidraw_room_url> -          # read text from stdin

Exit codes:
    0  success
    1  runtime failure
    2  invalid arguments
    3  Playwright not installed

Privacy: the room URL fragment contains the room's encryption key. This script
never prints or logs the URL.
"""

import argparse
import asyncio
import re
import sys

ROOM_URL_RE = re.compile(r"^https://(www\.)?excalidraw\.com/#room=[A-Za-z0-9]+,[A-Za-z0-9_-]+$")
MAX_CHARS = 2000
VIEWPORT = {"width": 1920, "height": 1080}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Write a text card onto a live Excalidraw room.")
    parser.add_argument("room_url", help="https://excalidraw.com/#room=<id>,<key>")
    parser.add_argument("text", help="Text to write (use '-' to read from stdin). Newlines are preserved.")
    parser.add_argument("--x", type=int, default=200, help="Viewport x coordinate (default: 200)")
    parser.add_argument("--y", type=int, default=150, help="Viewport y coordinate (default: 150)")
    parser.add_argument("--settle", type=float, default=3.0,
                        help="Seconds to wait after the canvas appears before writing (default: 3)")
    parser.add_argument("--timeout", type=float, default=30.0,
                        help="Navigation / canvas-ready timeout in seconds (default: 30)")
    args = parser.parse_args()

    if not ROOM_URL_RE.match(args.room_url):
        parser.error("room_url must look like https://excalidraw.com/#room=<id>,<key>")
    if args.text == "-":
        args.text = sys.stdin.read()
    args.text = args.text.replace("\r\n", "\n").strip("\n")
    if not args.text.strip():
        parser.error("text must not be empty")
    if len(args.text) > MAX_CHARS:
        parser.error(f"text is longer than {MAX_CHARS} characters; keep the card concise")
    if not (0 <= args.x < VIEWPORT["width"] - 50 and 0 <= args.y < VIEWPORT["height"] - 50):
        parser.error(f"--x/--y must be inside the {VIEWPORT['width']}x{VIEWPORT['height']} viewport")
    return args


async def write_text(room_url: str, text: str, x: int, y: int, settle: float, timeout: float) -> None:
    from playwright.async_api import async_playwright

    timeout_ms = int(timeout * 1000)
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        try:
            context = await browser.new_context(viewport=VIEWPORT)
            page = await context.new_page()
            await page.goto(room_url, timeout=timeout_ms, wait_until="domcontentloaded")
            await page.wait_for_selector("canvas", state="visible", timeout=timeout_ms)
            await asyncio.sleep(settle)

            # Paste lands at the last known pointer position.
            await page.mouse.move(x, y)
            await page.evaluate(
                """(t) => {
                    const dt = new DataTransfer();
                    dt.setData('text/plain', t);
                    document.dispatchEvent(new ClipboardEvent('paste', {clipboardData: dt, bubbles: true, cancelable: true}));
                }""",
                text,
            )

            # Verify: a fresh session has an empty undo stack, so the Undo button
            # becomes enabled only if the text element was actually created.
            undo = page.locator('[data-testid="button-undo"]')
            if await undo.count():
                await page.wait_for_function(
                    "() => !document.querySelector('[data-testid=\"button-undo\"]').disabled",
                    timeout=5000,
                )

            # Leave time for the change to broadcast to collaborators before disconnecting.
            await asyncio.sleep(2)
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
        asyncio.run(write_text(args.room_url, args.text, args.x, args.y, args.settle, args.timeout))
    except Exception as exc:
        print(f"Error: write failed: {type(exc).__name__}: {str(exc).splitlines()[0] if str(exc) else ''}",
              file=sys.stderr)
        return 1

    print("Text written to the Excalidraw board.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
