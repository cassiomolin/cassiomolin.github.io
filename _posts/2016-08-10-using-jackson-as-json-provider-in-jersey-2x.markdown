---
title: Using Jackson as JSON provider in Jersey 2.x
date: 2016-08-10 12:58:15 Z
tags:
- jackson
- java
- jersey
- json
layout: post
author: Cassio Mazzochi Molin
excerpt: Using Jackson, a popular JSON parser for Java, in Jersey applications.
featured_image: null
featured_image_thumbnail: null
---

When producing and consuming JSON in a Jersey application, will need a JSON provider, otherwise you'll see an error like this:

```nocode
A message body writer for Java class ... and MIME media type application/json was not found
```

At time of writing, Jersey 2.x integrates with the following modules to provide JSON support:

- [MOXy][1]
- [Java API for JSON Processing (JSON-P)][2]
- [Jackson][3]
- [Jettison][4]

Among the options mentioned above, I would say Jackson is the one which offers more features when parsing JSON.

## Using Jackson

See below the steps to use Jackson, a popular Java parser for Java, as a JSON provider in Jersey 2.x:

### Adding Jackson module dependencies

To use Jackson 2.x as your JSON provider you need to add [`jersey-media-json-jackson`][5] module to the `pom.xml` file:

```xml
<dependency>
    <groupId>org.glassfish.jersey.media</groupId>
    <artifactId>jersey-media-json-jackson</artifactId>
    <version>2.23.1</version>
</dependency>
```

To use Jackson 1.x, add the [`jersey-media-json-jackson1`][5] artifact to the `pom.xml` file:

```xml
<dependency>
    <groupId>org.glassfish.jersey.media</groupId>
    <artifactId>jersey-media-json-jackson1</artifactId>
    <version>2.23.1</version>
</dependency>
```

### Registering Jackson module

Besides adding the dependency mentioned above, you need to register [`JacksonFeature`][6] (or [`Jackson1Feature`][7] for Jackson 1.x) in your [`Application`][8] / [`ResourceConfig`][9] sub-class:

```java
@ApplicationPath("/api")
public class MyApplication extends Application {

    @Override
    public Set<Class<?>> getClasses() {
        Set<Class<?>> classes = new HashSet<Class<?>>();
        classes.add(JacksonFeature.class);
        return classes;
    }
}
```

```java
@ApplicationPath("/api")
public class MyApplication extends ResourceConfig {

    public MyApplication() {
        register(JacksonFeature.class);
    }
}
```

If you don't have an [`Application`][8] / [`ResourceConfig`][9] sub-class, you can register the [`JacksonFeature`][6] in your `web.xml` deployment descriptor by adding the feature fully-qualified class name to the [`jersey.config.server.provider.classnames`][10] initialization parameter:

```xml
<init-param>
    <param-name>jersey.config.server.provider.classnames</param-name>
    <param-value>org.glassfish.jersey.jackson.JacksonFeature</param-value>
</init-param>
```

If you need to register other features, resources or providers, separate their fully-qualified class names with comma (`,`).

Just in case you are interested in having a look at the implementation, the [`MessageBodyWriter`][11] provided by Jackson is [`JacksonJsonProvider`][12].

---

For more details, check the Jersey [documentation][13] about support for common media type representations.

[1]: https://jersey.java.net/documentation/latest/media.html#json.moxy
[10]: https://jersey.java.net/project-info/2.23.1/jersey/project/jersey-media-json-jackson1/dependencies.html
[11]: http://docs.oracle.com/javaee/7/api/javax/ws/rs/ext/MessageBodyWriter.html
[12]: http://fasterxml.github.io/jackson-jaxrs-providers/javadoc/2.8/com/fasterxml/jackson/jaxrs/json/JacksonJsonProvider.html
[13]: https://jersey.github.io/documentation/latest/media.html
[2]: https://jersey.github.io/documentation/latest/media.html#json.json-p
[3]: https://jersey.github.io/documentation/latest/media.html#json.jackson
[4]: https://jersey.github.io/documentation/latest/media.html#json.jettison
[5]: https://jersey.github.io/project-info/2.23.1/jersey/project/jersey-media-json-jackson/dependencies.html
[6]: https://jersey.github.io/apidocs/2.23.1/jersey/org/glassfish/jersey/jackson/JacksonFeature.html
[7]: https://jersey.github.io/apidocs/2.23.1/jersey/org/glassfish/jersey/jackson1/Jackson1Feature.html
[8]: https://jersey.github.io/apidocs/2.23.1/jersey/javax/ws/rs/core/Application.html
[9]: https://jersey.github.io/apidocs/2.23.1/jersey/org/glassfish/jersey/server/ResourceConfig.html
