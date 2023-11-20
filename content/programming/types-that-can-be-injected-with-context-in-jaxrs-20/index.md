---
title: Types that can be injected with @Context in JAX-RS 2.0
date: 2016-03-08
tags:
- java
- jax-rs
summary: A summary of all types that can be injected with @Context in JAX-RS resources and providers.
aliases:
- /2016/03/08/types-that-can-be-injected-with-context-in-jaxrs-20/
---

The [`@Context`][1] annotation allows you to inject request/response context details into JAX-RS provider and resource classes. Injection can be performed into a class field, a bean property or a method parameter.

The following list summarizes all the types that can be injected using the [`@Context`][1] annotation, according to the [JAX-RS 2.0 specification][2]:

- [`javax.ws.rs.core.Application`][3]
- [`javax.ws.rs.core.HttpHeaders`][4]
- [`javax.ws.rs.core.Request`][5]
- [`javax.ws.rs.core.SecurityContext`][6]
- [`javax.ws.rs.core.UriInfo`][7]
- [`javax.ws.rs.core.Configuration`][8]
- [`javax.ws.rs.container.ResourceContext`][9]
- [`javax.ws.rs.ext.Providers`][10]

Except for [`Configuration`][8] and [`Providers`][10], which
are injectable in both client and server-side providers, all the other types are server-side only.

The following types are available *only* when the application is deployed in a servlet container:

- [`javax.servlet.HttpServletRequest`][11]
- [`javax.servlet.HttpServletResponse`][12]
- [`javax.servlet.ServletConfig`][13]
- [`javax.servlet.ServletContext`][14]

[JAX-RS 2.1][15] introduced other types that can be injected with [`@Context`][1]:

- [`javax.ws.rs.sse.Sse`][16]
- [`javax.ws.rs.sse.SseEventSink`][17]

Besides the standard types listed above, JAX-RS implementations, such as [Jersey][18], [RESTEasy][19] and [Apache CXF][20], might define their own types that can be injected using [`@Context`][1].

---

Find below a quick description of each JAX-RS type available for injection:

- **Application:** The instance of the application-supplied [`Application`][3] subclass can be injected into a class field or method parameter. Access to the [`Application`][3] subclass instance allows configuration information to be centralized in that class.

- **URIs and URI templates:** [`UriInfo`][7] provides both static and dynamic, per-request information, about the components of a request URI.

- **Headers:** [`HttpHeaders`][4] provides access to request header information either in map form or via strongly typed convenience methods. Response headers may be provided using the [`Response`][21] class.

- **Content negotiation and preconditions:** The methods of [`Request`][5] allow a caller to determine the best matching representation variant and to evaluate whether the current state of the resource matches any preconditions in the request.

- **Security context:** The [`SecurityContext`][6] interface provides access to information about the security context of the current request. The methods of [`SecurityContext`][6] provide access to the current user principal, information about roles assumed by the requester, whether the request arrived over a secure channel and the authentication scheme used.

- **Providers:** The [`Providers`][10] interface allows for lookup of provider instances based on a set of search criteria. This interface is expected to be primarily of interest to provider authors wishing to use other providers functionality. It is injectable in both client and server providers.

- **Resource context:** The [`ResourceContext`][9] interface provides access to instantiation and initialization of resource or subresource classes in the default per-request scope. It can be injected to help with creation and initialization, or just initialization, of instances created by an application.

- **Configuration:** Both the client and the server runtime [`Configuration`][8]s are available for injection in providers (client or server) and resource classes (server only).

- **SSE events:** [`SseEventSink`][17] represents the incoming SSE connection and provides methods to send events. [`Sse`][16] provides factory methods for events and broadcasters.


  [1]: https://javaee.github.io/javaee-spec/javadocs/javax/ws/rs/core/Context.html
  [2]: http://download.oracle.com/otn-pub/jcp/jaxrs-2_0-fr-eval-spec/jsr339-jaxrs-2.0-final-spec.pdf
  [3]: https://javaee.github.io/javaee-spec/javadocs/javax/ws/rs/core/Application.html
  [4]: https://javaee.github.io/javaee-spec/javadocs/javax/ws/rs/core/HttpHeaders.html
  [5]: https://javaee.github.io/javaee-spec/javadocs/javax/ws/rs/core/Request.html
  [6]: https://javaee.github.io/javaee-spec/javadocs/javax/ws/rs/core/SecurityContext.html
  [7]: https://javaee.github.io/javaee-spec/javadocs/javax/ws/rs/core/UriInfo.html
  [8]: https://javaee.github.io/javaee-spec/javadocs/javax/ws/rs/core/Configuration.html
  [9]: https://javaee.github.io/javaee-spec/javadocs/javax/ws/rs/container/ResourceContext.html
  [10]: https://javaee.github.io/javaee-spec/javadocs/javax/ws/rs/ext/Providers.html
  [11]: https://javaee.github.io/javaee-spec/javadocs/javax/servlet/http/HttpServletRequest.html
  [12]: https://javaee.github.io/javaee-spec/javadocs/javax/servlet/http/HttpServletResponse.html
  [13]: https://javaee.github.io/javaee-spec/javadocs/javax/servlet/ServletConfig.html
  [14]: https://javaee.github.io/javaee-spec/javadocs/javax/servlet/ServletContext.html
  [15]: http://download.oracle.com/otn-pub/jcp/jaxrs-2_1-pfd-spec/jaxrs-2_1-pfd-spec.pdf
  [16]: https://javaee.github.io/javaee-spec/javadocs/javax/ws/rs/sse/Sse.html
  [17]: https://javaee.github.io/javaee-spec/javadocs/javax/ws/rs/sse/SseEventSink.html
  [18]: https://jersey.github.io/
  [19]: http://resteasy.jboss.org/
  [20]: https://cxf.apache.org/
  [21]: https://javaee.github.io/javaee-spec/javadocs/javax/ws/rs/core/Response.html
