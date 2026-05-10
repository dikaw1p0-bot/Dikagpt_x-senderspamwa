#!/usr/bin/env python3
"""
DIKAGPT-X - Modular High-Rate WhatsApp Load Tester (Termux)
"""

import asyncio
import argparse
import sys
import signal
from config import DEFAULT_MESSAGE_TEMPLATE, DEFAULT_RATE, DEFAULT_COUNT, KILLSWITCH_PATH
from rate_limiter import RateLimiter
from killswitch import is_killswitch_active
from sender import WhatsAppSender

def signal_handler(sig, frame):
    print("\n[!] Interrupted. Exiting.")
    sys.exit(0)

async def worker(sender, message_template, idx, rate_limiter):
    """Send a single message with rate limiting and killswitch check."""
    if is_killswitch_active():
        return False
    await rate_limiter.acquire()
    msg = message_template.replace("@COUNT@", str(idx)).replace("@TIMESTAMP@", str(asyncio.get_event_loop().time()))
    await sender.send_message(msg)
    return True

async def burst(phone: str, message_template: str, total_msgs: int, rate_per_sec: int):
    sender = WhatsAppSender()
    sender.connect()
    await sender.open_chat(phone)
    
    print(f"[*] Sending {total_msgs} messages at {rate_per_sec} msg/sec")
    rate_limiter = RateLimiter(rate_per_sec)
    tasks = []
    for i in range(1, total_msgs + 1):
        if is_killswitch_active():
            print("[!] Killswitch detected. Stopping.")
            break
        tasks.append(asyncio.create_task(worker(sender, message_template, i, rate_limiter)))
    await asyncio.gather(*tasks, return_exceptions=True)
    
    await sender.close()
    print("[*] Burst finished.")

def main():
    parser = argparse.ArgumentParser(description="DIKAGPT-X - Modular WhatsApp Load Tester")
    parser.add_argument("--phone", required=True, help="Your own phone number (e.g., 628123456789)")
    parser.add_argument("--message", default=DEFAULT_MESSAGE_TEMPLATE, help="Message template")
    parser.add_argument("--count", type=int, default=DEFAULT_COUNT, help="Total messages to send")
    parser.add_argument("--rate", type=int, default=DEFAULT_RATE, help="Messages per second (default 20)")
    args = parser.parse_args()
    
    if args.rate > 30:
        print("[!] Rate >30 msg/sec extremely risky. Continue? (y/N)")
        if input().lower() != 'y':
            return
    
    signal.signal(signal.SIGINT, signal_handler)
    asyncio.run(burst(args.phone, args.message, args.count, args.rate))

if __name__ == "__main__":
    main()
