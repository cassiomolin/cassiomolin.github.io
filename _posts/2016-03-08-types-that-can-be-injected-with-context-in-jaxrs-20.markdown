---
title: Types that can be injected with @Context in JAX-RS 2.0
date: 2016-03-08 13:25:08 Z
tags:
- java
- jax-rs
layout: post
author: Cássio Mazzochi Molin
excerpt: A summary of all types that can be injected with @Context in JAX-RS resources
  and providers.
image: "/images/types-that-can-be-injected-with-context-in-jaxrs-20.jpg"
imageSource: https://unsplash.com/photos/kDppwO0MUQA
---

The following list summarizes all the types that can be injected using the [`@Context`][1] annotation, according to the [JAX-RS 2.0 specification][2]:

- [`javax.ws.rs.container.ResourceContext`][4]
- [`javax.ws.rs.core.Application`][5]
- [`javax.ws.rs.core.HttpHeaders`][6]
- [`javax.ws.rs.core.Request`][7]
- [`javax.ws.rs.core.SecurityContext`][8]
- [`javax.ws.rs.core.UriInfo`][9]
- [`javax.ws.rs.core.Configuration`][10]
- [`javax.ws.rs.ext.Providers`][11]

The following types are available *only* when the application is deployed in a servlet container:

- [`javax.servlet.HttpServletRequest`][12]
- [`javax.servlet.HttpServletResponse`][13]
- [`javax.servlet.ServletConfig`][14]
- [`javax.servlet.ServletContext`][15]

[JAX-RS 2.1][16] introduced other types that can be injected with [`@Context`][1]:

- [`javax.ws.rs.sse.Sse`][17]
- [`javax.ws.rs.sse.SseEventSink`][19]

---

Besides the standard types listed above, JAX-RS implementations, such as [Jersey][21], [RESTEasy][22] and [Apache CXF][23], might define their own types that can be injected using [`@Context`][1].


  [1]: https://javaee.github.io/javaee-spec/javadocs/javax/ws/rs/core/Context.html
  [2]: http://download.oracle.com/otn-pub/jcp/jaxrs-2_0-fr-eval-spec/jsr339-jaxrs-2.0-final-spec.pdf
  [3]: https://javaee.github.io/javaee-spec/javadocs/javax/ws/rs/container/ContainerRequestContext.html
  [4]: https://javaee.github.io/javaee-spec/javadocs/javax/ws/rs/container/ResourceContext.html
  [5]: https://javaee.github.io/javaee-spec/javadocs/javax/ws/rs/core/Application.html
  [6]: https://javaee.github.io/javaee-spec/javadocs/javax/ws/rs/core/HttpHeaders.html
  [7]: https://javaee.github.io/javaee-spec/javadocs/javax/ws/rs/core/Request.html
  [8]: https://javaee.github.io/javaee-spec/javadocs/javax/ws/rs/core/SecurityContext.html
  [9]: https://javaee.github.io/javaee-spec/javadocs/javax/ws/rs/core/UriInfo.html
  [10]: https://javaee.github.io/javaee-spec/javadocs/javax/ws/rs/core/Configuration.html
  [11]: https://javaee.github.io/javaee-spec/javadocs/javax/ws/rs/ext/Providers.html
  [12]: https://javaee.github.io/javaee-spec/javadocs/javax/servlet/http/HttpServletRequest.html
  [13]: https://javaee.github.io/javaee-spec/javadocs/javax/servlet/http/HttpServletResponse.html
  [14]: https://javaee.github.io/javaee-spec/javadocs/javax/servlet/ServletConfig.html
  [15]: https://javaee.github.io/javaee-spec/javadocs/javax/servlet/ServletContext.html
  [16]: http://download.oracle.com/otn-pub/jcp/jaxrs-2_1-pfd-spec/jaxrs-2_1-pfd-spec.pdf
  [17]: https://javaee.github.io/javaee-spec/javadocs/javax/ws/rs/sse/Sse.html
  [19]: https://javaee.github.io/javaee-spec/javadocs/javax/ws/rs/sse/SseEventSink.html
  [20]: https://github.com/jax-rs/api/blob/master/jaxrs-api/src/main/java/javax/ws/rs/sse/SseEventSink.java
  [21]: https://jersey.github.io/
  [22]: http://resteasy.jboss.org/
  [23]: https://cxf.apache.org/