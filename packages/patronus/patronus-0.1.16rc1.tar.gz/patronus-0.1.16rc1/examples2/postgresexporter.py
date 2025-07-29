import threading

import random

import time
from opentelemetry.trace import get_current_span, SpanContext

import patronus
from patronus import traced

result: SpanContext = None


@traced()
def run_in_thread():
    global result
    ctx = get_current_span()
    time.sleep(1)
    result = ctx.get_span_context()
    return None


@patronus.traced()
def raiser():
    time.sleep(random.random() / 20)
    span = get_current_span()

    t = threading.Thread(target=run_in_thread)
    t.start()
    t.join()

    span.add_link(result, {"key": "value"})

    span.add_event("We crash soon", {"foo": "bar"})
    raise RuntimeError("Hello")


@patronus.traced()
def workflow():
    time.sleep(random.random() / 20)
    patronus.get_logger().info("Hello!")
    raiser()


def main():
    patronus.init()
    workflow()


if __name__ == "__main__":
    main()
