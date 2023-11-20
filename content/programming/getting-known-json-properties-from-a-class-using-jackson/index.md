---
title: Getting known JSON properties from a class using Jackson
date: 2017-08-23
tags:
- java
- jackson
- json
summary: Using the Jackson API to introspect a Java class and extract the available JSON properties from it.
aliases:
- /2017/08/23/getting-known-json-properties-from-a-class-using-jackson/
---

[Jackson][7] is a (or probably the most) popular framework for parsing JSON in Java. The Jackson API makes it easy to [introspect an arbitrary class][1] to get the available JSON properties:

```java
// Construct a Jackson JavaType for your class
JavaType javaType = mapper.getTypeFactory().constructType(MyDto.class);

// Introspect the given type
BeanDescription beanDescription = mapper.getSerializationConfig().introspect(javaType);

// Find properties
List<BeanPropertyDefinition> properties = beanDescription.findProperties();
```

The [`BeanPropertyDefinition`][2] list should give you the details you need regarding the JSON properties.

---

The [`@JsonIgnoreProperties`][3] class level annotation is not taken into account with the above mentioned approach. But you can use an [`AnnotationIntrospector`][4] to get the properties ignored on class level:

```java
// Get class level ignored properties
Set<String> ignoredProperties = mapper.getSerializationConfig().getAnnotationIntrospector()
        .findPropertyIgnorals(beanDescription.getClassInfo()).getIgnored();
```

Then filter `properties` removing the properties which are present in `ignoredProperties`:

```java
// Filter properties removing the class level ignored ones
List<BeanPropertyDefinition> availableProperties = properties.stream()
        .filter(property -> !ignoredProperties.contains(property.getName()))
        .collect(Collectors.toList());
```

This approach works even if you have mix-ins defined for your class.

---

The [`AnnotationIntrospector#findPropertyIgnorals(Annotated)`][5] method was introduced in Jackson 2.8. The [`AnnotationIntrospector#findPropertiesToIgnore(Annotated, boolean)`][6] method can be used for older versions (but it's deprecated since Jackson 2.8).


  [1]: https://stackoverflow.com/a/44266188/1426227
  [2]: https://fasterxml.github.io/jackson-databind/javadoc/2.8/com/fasterxml/jackson/databind/introspect/BeanPropertyDefinition.html
  [3]: https://fasterxml.github.io/jackson-annotations/javadoc/2.8/com/fasterxml/jackson/annotation/JsonIgnoreProperties.html
  [4]: https://fasterxml.github.io/jackson-databind/javadoc/2.8/com/fasterxml/jackson/databind/AnnotationIntrospector.html
  [5]: https://fasterxml.github.io/jackson-databind/javadoc/2.8/com/fasterxml/jackson/databind/AnnotationIntrospector.html#findPropertyIgnorals(com.fasterxml.jackson.databind.introspect.Annotated)
  [6]: https://fasterxml.github.io/jackson-databind/javadoc/2.8/com/fasterxml/jackson/databind/AnnotationIntrospector.html#findPropertiesToIgnore(com.fasterxml.jackson.databind.introspect.Annotated,%20boolean)
  [7]: https://github.com/FasterXML/jackson