import psutil
import os
import socket

from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.metrics import MeterProvider
from opentelemetry.sdk.metrics.export import PeriodicExportingMetricReader
from opentelemetry.exporter.otlp.proto.http.metric_exporter import OTLPMetricExporter
from opentelemetry.metrics import set_meter_provider, get_meter, Observation

process = psutil.Process(os.getpid())

# Recurso da aplicação
resource = Resource.create({
    "service.name": "auth",
    "service.instance.id": socket.gethostname(),
    "service.version": "1.0.0"
})

# Exportador OTLP
reader = PeriodicExportingMetricReader(
    OTLPMetricExporter(endpoint="http://otel:4318/v1/metrics")
)

# Provedor de métricas
provider = MeterProvider(resource=resource, metric_readers=[reader])
set_meter_provider(provider)

# Coletor de métricas
meter = get_meter("auth.metrics")

# Callback de CPU
def cpu_usage_callback(options):
    return [Observation(
        value=process.cpu_percent(interval=None) / psutil.cpu_count(),
        attributes={}
    )]

meter.create_observable_gauge(
    name="custom.cpu.percent",
    callbacks=[cpu_usage_callback],
    unit="%",
    description="CPU usage percent"
)

# Callback de memória
def memory_usage_callback(options):
    # mem = psutil.virtual_memory()
    # return [Observation(value=mem.percent, attributes={})]

    return [Observation(
        value=process.memory_percent(),
        attributes={}
    )]

meter.create_observable_gauge(
    name="custom.memory.percent",
    callbacks=[memory_usage_callback],
    unit="%",
    description="Used memory in percent"
)
