# Code obtained from
# https://github.com/vllm-project/vllm/blob/40253bab443ad0cdd22ff33bd8f777d2f289cfc4/vllm/engine/metrics.py

from enum import Enum, auto
from itertools import pairwise
from logging import Logger
import re
import time
from typing import List, Optional

from prometheus_client import (
    Counter,
    Gauge,
    GCCollector,
    Histogram,
    PlatformCollector,
    ProcessCollector,
    disable_created_metrics,
    make_asgi_app,
)
from prometheus_client.registry import CollectorRegistry
from starlette.routing import Mount

logger = Logger(__name__)


class _Metrics:

    def __init__(self):
        labelnames = ["model_name"]

        # First sets of metrics to support.
        self.gauge_scheduler_running = Gauge(
            name="furiosa_llm:num_requests_running",
            documentation="Number of requests currently running on RNGD.",
            labelnames=labelnames,
            registry=_REGISTRY,
        )
        self.gauge_scheduler_waiting = Gauge(
            name="furiosa_llm:num_requests_waiting",
            documentation="Number of requests waiting to be processed.",
            labelnames=labelnames,
            registry=_REGISTRY,
        )
        self.counter_request_received = Counter(
            name="furiosa_llm:request_received_total",
            documentation="Count of requests.",
            labelnames=labelnames,
            registry=_REGISTRY,
        )
        self.counter_request_success = Counter(
            name="furiosa_llm:request_success_total",
            documentation="Count of successfully processed requests.",
            labelnames=labelnames,
            registry=_REGISTRY,
        )
        self.counter_request_failure = Counter(
            name="furiosa_llm:request_failure_total",
            documentation="Count of request process failures.",
            labelnames=labelnames,
            registry=_REGISTRY,
        )

        self.counter_prompt_tokens = Counter(
            name="furiosa_llm:prompt_tokens_total",
            documentation="Number of prefill tokens processed.",
            labelnames=labelnames,
            registry=_REGISTRY,
        )
        self.counter_generation_tokens = Counter(
            name="furiosa_llm:generation_tokens_total",
            documentation="Number of generation tokens processed.",
            labelnames=labelnames,
            registry=_REGISTRY,
        )

        self.histogram_time_to_first_token = Histogram(
            name="furiosa_llm:time_to_first_token_seconds",
            documentation="Histogram of time to first token in seconds.",
            labelnames=labelnames,
            buckets=[
                0.001,
                0.005,
                0.01,
                0.02,
                0.04,
                0.06,
                0.08,
                0.1,
                0.25,
                0.5,
                0.75,
                1.0,
                2.5,
                5.0,
                7.5,
                10.0,
            ],
            registry=_REGISTRY,
        )
        self.histogram_time_per_output_token = Histogram(
            name="furiosa_llm:time_per_output_token_seconds",
            documentation="Histogram of time per output token in seconds.",
            labelnames=labelnames,
            buckets=[0.01, 0.025, 0.05, 0.075, 0.1, 0.15, 0.2, 0.3, 0.4, 0.5, 0.75, 1.0, 2.5],
            registry=_REGISTRY,
        )

        # Request stats
        #   Latency
        request_latency_buckets = [
            0.3,
            0.5,
            0.8,
            1.0,
            1.5,
            2.0,
            2.5,
            5.0,
            10.0,
            15.0,
            20.0,
            30.0,
            40.0,
            50.0,
            60.0,
        ]
        self.histogram_e2e_time_request = Histogram(
            name="furiosa_llm:e2e_request_latency_seconds",
            documentation="Histogram of end to end request latency in seconds.",
            labelnames=labelnames,
            buckets=request_latency_buckets,
            registry=_REGISTRY,
        )
        #   Metadata
        self.histogram_num_prompt_tokens_request = Histogram(
            name="furiosa_llm:request_prompt_tokens",
            documentation="Number of prefill tokens processed.",
            labelnames=labelnames,
            buckets=_build_buckets([1, 2, 5], _MAX_MODEL_LEN),
            registry=_REGISTRY,
        )
        self.histogram_num_generation_tokens_request = Histogram(
            name="furiosa_llm:request_generation_tokens",
            documentation="Number of generation tokens processed.",
            labelnames=labelnames,
            buckets=_build_buckets([1, 2, 5], _MAX_MODEL_LEN),
            registry=_REGISTRY,
        )
        self.histogram_max_tokens_request = Histogram(
            name="furiosa_llm:request_params_max_tokens",
            documentation="Histogram of the max_tokens request parameter.",
            labelnames=labelnames,
            buckets=_build_buckets([1, 2, 5], _MAX_MODEL_LEN),
            registry=_REGISTRY,
        )


_MAX_MODEL_LEN: int
_METRICS: _Metrics
_MODEL: str
_REGISTRY: CollectorRegistry


def initialize_metrics(model: str, max_model_len: int) -> None:
    global _MAX_MODEL_LEN, _METRICS, _MODEL, _REGISTRY
    _REGISTRY = CollectorRegistry()
    GCCollector(registry=_REGISTRY)
    ProcessCollector(registry=_REGISTRY)
    PlatformCollector(registry=_REGISTRY)

    _MAX_MODEL_LEN = max_model_len
    _MODEL = model
    _METRICS = _Metrics()

    disable_created_metrics()


def get_metrics_mount() -> Mount:
    metrics_route = Mount("/metrics", make_asgi_app(registry=_REGISTRY))
    # Workaround for 307 Redirect for /metrics
    metrics_route.path_regex = re.compile("^/metrics(?P<path>.*)$")
    return metrics_route


def _build_buckets(mantissa_lst: List[int], max_value: int) -> List[int]:
    """
    Builds a list of buckets with increasing powers of 10 multiplied by
    mantissa values until the value exceeds the specified maximum.
    """
    exponent = 0
    buckets: List[int] = []
    mantissa_lst = sorted(mantissa_lst)
    while True:
        for m in mantissa_lst:
            value = m * 10**exponent
            if value <= max_value:
                buckets.append(value)
            else:
                return buckets
        exponent += 1


class RequestStatus(Enum):
    WAITING = auto()
    RUNNING = auto()


class RequestMetrics:
    def __init__(self) -> None:
        self.request_created: float = time.monotonic()
        self.request_status: RequestStatus = RequestStatus.WAITING
        self.request_completed: Optional[float] = None
        self.max_tokens_request: Optional[int] = None
        self.request_success: bool = True
        self.token_generation_time: List[float] = []
        self.prompt_tokens: int = 0
        self.generation_tokens: int = 0
        _METRICS.counter_request_received.labels(_MODEL).inc()
        _METRICS.gauge_scheduler_waiting.labels(_MODEL).inc()

    def is_running(self) -> bool:
        return self.request_status == RequestStatus.RUNNING

    def set_running(self) -> None:
        if self.is_running():
            logger.warning("Trying to set status of request that is already running.")
        else:
            self.request_status = RequestStatus.RUNNING
            _METRICS.gauge_scheduler_waiting.labels(_MODEL).dec()
            _METRICS.gauge_scheduler_running.labels(_MODEL).inc()

    def __del__(self) -> None:
        if self.request_success:
            _METRICS.counter_request_success.labels(_MODEL).inc()
        else:
            _METRICS.counter_request_failure.labels(_MODEL).inc()

        if self.request_status == RequestStatus.WAITING:
            _METRICS.gauge_scheduler_waiting.labels(_MODEL).dec()
        elif self.request_status == RequestStatus.RUNNING:
            _METRICS.gauge_scheduler_running.labels(_MODEL).dec()

        if self.request_completed is not None:
            _METRICS.histogram_e2e_time_request.labels(_MODEL).observe(
                self.request_completed - self.request_created
            )
        if self.max_tokens_request is None:
            _METRICS.histogram_max_tokens_request.labels(_MODEL).observe(
                _MAX_MODEL_LEN - self.prompt_tokens
            )
        else:
            _METRICS.histogram_max_tokens_request.labels(_MODEL).observe(self.max_tokens_request)

        if self.token_generation_time:
            _METRICS.histogram_time_to_first_token.labels(_MODEL).observe(
                self.token_generation_time[0] - self.request_created
            )
        for start, end in pairwise(self.token_generation_time):
            _METRICS.histogram_time_per_output_token.labels(_MODEL).observe(end - start)

        _METRICS.counter_prompt_tokens.labels(_MODEL).inc(self.prompt_tokens)
        _METRICS.counter_generation_tokens.labels(_MODEL).inc(self.generation_tokens)
        _METRICS.histogram_num_prompt_tokens_request.labels(_MODEL).observe(self.prompt_tokens)
        _METRICS.histogram_num_generation_tokens_request.labels(_MODEL).observe(
            self.generation_tokens
        )
