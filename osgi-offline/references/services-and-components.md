# Services, Declarative Services, and configuration

## Prefer explicit service dynamics

The registry is dynamic: a service can arrive, change properties, or depart while its consumer remains active. Avoid storing a raw service or `BundleContext` in static state. Code must respect the acquisition mechanism's lifecycle and must not use a service after it has been released or unbound.

Use Declarative Services (DS) when it is already supported by the project. Use manual registration, trackers, or activators only when their control is actually needed. Do not mix multiple ownership mechanisms for the same dependency.

## Diagnose DS from runtime state

Separate the component description from its runtime configurations. Capture:

- whether the description is enabled and why a configuration is unsatisfied or failed;
- each reference's interface, target filter, cardinality, policy, policy option, and matching services;
- configuration policy and the effective properties/PID;
- the activation exception and its root cause;
- the DS specification level implemented by the deployed runtime.

Generated XML is authoritative at runtime. Confirm that annotations were processed, `Service-Component` points to packaged descriptors, and annotation features are supported by the actual DS implementation.

## Choose reference behavior deliberately

- Cardinality expresses whether a reference is optional/mandatory and unary/multiple.
- Static policy normally reactivates a component when a bound service must change; dynamic policy calls bind/update/unbind while the component remains active.
- Reluctant policy option keeps a suitable binding where allowed; greedy can rebind to a more preferred candidate. Do not switch these settings solely to hide ordering bugs.
- Target filters are part of the contract. Validate LDAP filter syntax and the types/values of service properties.

Dynamic callbacks can race with application work. Publish state safely, make callbacks small, and avoid calling unknown service code while holding internal locks. Multiple-cardinality collections must match the supported DS injection semantics; do not assume they are ordinary mutable lists.

Activation should validate inputs and acquire only component-owned resources. Deactivation must tolerate partial activation and release those resources. Avoid expensive blocking I/O on the framework or SCR event thread.

## Config Admin

Distinguish component properties from Configuration Admin data and framework properties. Confirm the expected PID or factory PID, configuration policy, property types, and whether an update causes modification or component recreation. Treat secrets in configuration and diagnostics as sensitive; do not print complete configuration dictionaries.

Test at least service arrival, service departure, configuration update/removal, activation failure, and clean shutdown when those transitions are relevant.
