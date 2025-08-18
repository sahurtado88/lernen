# What is OpenTelemetry?
A short explanation of what OpenTelemetry is and isn’t.
OpenTelemetry is:

An Observability framework and toolkit designed to create and manage telemetry data such as traces, metrics, and logs.
Vendor- and tool-agnostic, meaning that it can be used with a broad variety of Observability backends, including open source tools like Jaeger and Prometheus, as well as commercial offerings.
Not an observability backend like Jaeger, Prometheus, or other commercial vendors.
Focused on the generation, collection, management, and export of telemetry. A major goal of OpenTelemetry is that you can easily instrument your applications or systems, no matter their language, infrastructure, or runtime environment. The storage and visualization of telemetry is intentionally left to other tools.


# What is observability?
Observability is the ability to understand the internal state of a system by examining its outputs. In the context of software, this means being able to understand the internal state of a system by examining its telemetry data, which includes traces, metrics, and logs.

To make a system observable, it must be instrumented. That is, the code must emit traces, metrics, or logs. The instrumented data must then be sent to an observability backend.

# Why OpenTelemetry?
With the rise of cloud computing, microservices architectures, and increasingly complex business requirements, the need for software and infrastructure observability is greater than ever.

OpenTelemetry satisfies the need for observability while following two key principles:

You own the data that you generate. There’s no vendor lock-in.
You only have to learn a single set of APIs and conventions.
Both principles combined grant teams and organizations the flexibility they need in today’s modern computing world.

If you want to learn more, take a look at OpenTelemetry’s mission, vision, and values.

# Main OpenTelemetry components
OpenTelemetry consists of the following major components:

A specification for all components
A standard protocol that defines the shape of telemetry data
Semantic conventions that define a standard naming scheme for common telemetry data types
APIs that define how to generate telemetry data
Language SDKs that implement the specification, APIs, and export of telemetry data
A library ecosystem that implements instrumentation for common libraries and frameworks
Automatic instrumentation components that generate telemetry data without requiring code changes
The OpenTelemetry Collector, a proxy that receives, processes, and exports telemetry data
Various other tools, such as the OpenTelemetry Operator for Kubernetes, OpenTelemetry Helm Charts, and community assets for FaaS
OpenTelemetry is used by a wide variety of libraries, services and apps that have OpenTelemetry integrated to provide observability by default.

OpenTelemetry is supported by numerous vendors, many of whom provide commercial support for OpenTelemetry and contribute to the project directly.

Extensibi

