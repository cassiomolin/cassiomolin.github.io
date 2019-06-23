---
title: Customizing ObjectMapper in a JAX-RS application
date: 2017-11-21 13:15:59 Z
tags:
- java
- jackson
- json
- jax-rs
layout: post
author: Cassio Mazzochi Molin
excerpt: Using Jackson with JAX-RS? See how to define a ContextResolver for ObjectMapper to customize serialization and deserialization.
featured_image: "/assets/images/posts/abstract_2.jpg"
featured_image_thumbnail: "/assets/images/posts/abstract_2_small.jpg"
---

If you use Jackson as the JSON provider in your JAX-RS application, you may want to redefine the default Jackson behaviour or even fine-tune the serializarion and deserialization processes. 

It can be achieved with a [`ContextResolver`][ContextResolver] for [`ObjectMapper`][ObjectMapper]:

```java
@Provider
public class ObjectMapperContextResolver implements ContextResolver<ObjectMapper> {

    private final ObjectMapper mapper;

    public ObjectMapperContextResolver() {
        this.mapper = createObjectMapper();
    }

    @Override
    public ObjectMapper getContext(Class<?> type) {
        return mapper;
    }

    private ObjectMapper createObjectMapper() {
        ObjectMapper mapper = new ObjectMapper();
        mapper.disable(DeserializationFeature.FAIL_ON_UNKNOWN_PROPERTIES);
        return mapper;
    }
}
```

Under the hood, the [`ObjectMapper`][ObjectMapper] instance created above will be picked by the [`JacksonJsonProvider`][JacksonJsonProvider] class, the Jackson implementation for [`MessageBodyReader`][MessageBodyReader] and [`MessageBodyWriter`][MessageBodyWriter] that binds JSON content to and from Java objects in JAX-RS.

---

If, for some reason, you need to access the [`ObjectMapper`][ObjectMapper] directly, use the [`@Context`][Context] annotation to inject [`Providers`][Providers] in your JAX-RS resource or provider classes:

```java
@Context
private Providers providers;
```

Then look up the [`ContextResolver`][ContextResolver] to get the [`ObjectMapper`][ObjectMapper] instance:

```java
ContextResolver<ObjectMapper> resolver = 
        providers.getContextResolver(ObjectMapper.class, MediaType.WILDCARD_TYPE);
ObjectMapper mapper = resolver.getContext(ObjectMapper.class);
```

---

I usually use the following serialization and deserialization settings:

```java
mapper.enable(SerializationFeature.INDENT_OUTPUT);
mapper.enable(DeserializationFeature.ACCEPT_EMPTY_STRING_AS_NULL_OBJECT);
mapper.disable(SerializationFeature.FAIL_ON_EMPTY_BEANS);
mapper.disable(SerializationFeature.WRITE_DATES_AS_TIMESTAMPS);
mapper.disable(DeserializationFeature.FAIL_ON_UNKNOWN_PROPERTIES);
```

For applications with Java 8 or above, I also register the following modules:

```java
mapper.registerModule(new Jdk8Module());
mapper.registerModule(new JavaTimeModule());
mapper.registerModule(new ParameterNamesModule());
```

Don't forget to add the following dependencies to your project:

```xml
<dependency>
    <groupId>com.fasterxml.jackson.module</groupId>
    <artifactId>jackson-module-parameter-names</artifactId>
    <version>${jackson.version}</version>
</dependency>
<dependency>
    <groupId>com.fasterxml.jackson.datatype</groupId>
    <artifactId>jackson-datatype-jdk8</artifactId>
    <version>${jackson.version}</version>
</dependency>
<dependency>
    <groupId>com.fasterxml.jackson.datatype</groupId>
    <artifactId>jackson-datatype-jsr310</artifactId>
    <version>${jackson.version}</version>
</dependency>
```


  [ObjectMapper]: https://fasterxml.github.io/jackson-databind/javadoc/2.9/com/fasterxml/jackson/databind/ObjectMapper.html
  [Providers]: https://javaee.github.io/javaee-spec/javadocs/javax/ws/rs/ext/Providers.html
  [Context]: https://javaee.github.io/javaee-spec/javadocs/javax/ws/rs/core/Context.html
  [ContextResolver]: https://javaee.github.io/javaee-spec/javadocs/javax/ws/rs/ext/ContextResolver.html
  [JacksonJsonProvider]: http://fasterxml.github.io/jackson-jaxrs-providers/javadoc/2.9/com/fasterxml/jackson/jaxrs/json/JacksonJsonProvider.html
  [MessageBodyReader]: https://javaee.github.io/javaee-spec/javadocs/javax/ws/rs/ext/MessageBodyReader.html
  [MessageBodyWriter]: https://javaee.github.io/javaee-spec/javadocs/javax/ws/rs/ext/MessageBodyWriter.html