import time
from collections.abc import Callable
from typing import Any, ClassVar

import grpc

from archipy.configs.base_config import BaseConfig
from archipy.helpers.interceptors.grpc.base.server_interceptor import BaseGrpcServerInterceptor
from archipy.helpers.utils.base_utils import BaseUtils


class GrpcServerMetricInterceptor(BaseGrpcServerInterceptor):
    """A gRPC server interceptor for collecting and reporting metrics using Prometheus.

    This interceptor measures the response time of gRPC methods and records it in a Prometheus histogram.
    It also captures errors and logs them for monitoring purposes.
    """

    from prometheus_client import Histogram

    "Buckets for measuring response times between 0 and 1 second."
    ZERO_TO_ONE_SECONDS_BUCKETS: ClassVar[list[float]] = [i / 1000 for i in range(0, 1000, 5)]

    "Buckets for measuring response times between 1 and 5 seconds."
    ONE_TO_FIVE_SECONDS_BUCKETS: ClassVar[list[float]] = [i / 100 for i in range(100, 500, 20)]

    "Buckets for measuring response times between 5 and 30 seconds."
    FIVE_TO_THIRTY_SECONDS_BUCKETS: ClassVar[list[float]] = [i / 100 for i in range(500, 3000, 50)]

    "Combined buckets for measuring response times from 0 to 30 seconds and beyond."
    TOTAL_BUCKETS = (
        ZERO_TO_ONE_SECONDS_BUCKETS + ONE_TO_FIVE_SECONDS_BUCKETS + FIVE_TO_THIRTY_SECONDS_BUCKETS + [float("inf")]
    )

    "Prometheus histogram for tracking response times of gRPC methods."
    RESPONSE_TIME_SECONDS = Histogram(
        "response_time_seconds",
        "Time spent processing request",
        labelnames=("package", "service", "method", "status_code"),
        buckets=TOTAL_BUCKETS,
    )

    def intercept(self, method: Callable, request: Any, context: grpc.ServicerContext):
        """Intercepts a gRPC server call to measure response time and capture errors.

        Args:
            method (Callable): The gRPC method being intercepted.
            request (Any): The request object passed to the method.
            context (grpc.ServicerContext): The context of the gRPC call.

        Returns:
            Any: The result of the intercepted gRPC method.

        Raises:
            Exception: If an exception occurs during the method execution, it is captured and logged.
        """
        try:
            # Skip metric collection if Prometheus is disabled
            if not BaseConfig.global_config().PROMETHEUS.IS_ENABLED:
                return method(request, context)

            method_name_model = context.method_name_model

            # Measure the start time
            start_time = time.time()

            # Execute the gRPC method
            result = method(request, context)

            # Record the response time in the Prometheus histogram
            self.RESPONSE_TIME_SECONDS.labels(
                package=method_name_model.package,
                service=method_name_model.service,
                method=method_name_model.method,
                status_code=context.code().name if context.code() else "OK",
            ).observe(time.time() - start_time)

            return result

        except Exception as exception:
            BaseUtils.capture_exception(exception)
