---
title: Combining the Jackson Streaming API with ObjectMapper for parsing JSON
date: 2019-08-19 17:00:00 Z
tags:
- java
- jackson
- json
layout: post
author: Cassio Mazzochi Molin
excerpt: This post demonstrates how to combine Jackson Streaming API and the data binding capabilities provided by ObjectMapper to parse JSON content.
featured_image: "/assets/images/posts/river.jpg"
featured_image_thumbnail: "/assets/images/posts/river_small.jpg"
featured: false
hidden: false
redirect_from:
  - /2019/08/19/parsing-json-with-jackson-streaming-api-and-objectmapper/
  - /combining-jackson-streaming-api-with-objectmapper-for-parsing-json/
---



The _Jackson Streaming API_ allows us to parse huge JSON documents without loading their whole content in memory at once. It _is the most efficient way_ to process JSON content and has the lowest memory and processing overhead, but it comes with a cost: _is not the most convenient_ way to process JSON content.

In this post we'll see how to take advantage of the Jackson Streaming API without losing the powerful capabilities of data binding provided by [`ObjectMapper`][com.fasterxml.jackson.databind.ObjectMapper].

This post in heavy on examples and the code is available on [GitHub][repo].



<!--more-->



##### Table of contents 
{:.no_toc}

* TOC 
{:toc}




## Introduction

For demonstration purposes, let's consider we want to parse the JSON array where each element represents a contact:

```json
[
  {
    "id": 1,
    "firstName": "John",
    "lastName": "Doe",
    "emails": [
      "john.doe@mail.com"
    ],
    "createdDateTime": "2019-08-19T20:30:00Z"
  },
  {
    "id": 2,
    "firstName": "Jane",
    "lastName": "Poe",
    "emails": [
      "jane.poe@mail.com",
      "janep@mail.com"
    ],
    "createdDateTime": "2019-08-19T20:45:00Z"
  }
]
```

Each contact can be mapped to an instance of `Contact`, which is defined as follows:

```java
@Data
public class Contact {
    private Integer id;
    private String firstName;
    private String lastName;
    private List<String> emails;
    private OffsetDateTime createdDateTime;
}
```

In most of applications, we can take advantage of the data binding capabilities provided by [`ObjectMapper`][com.fasterxml.jackson.databind.ObjectMapper] and parse the array with the following code:

```java
ObjectMapper mapper = new ObjectMapper();
mapper.registerModule(new JavaTimeModule());
List<Contact> contacts = mapper.readValue(json, new TypeReference<List<Contact>>() {});
```

However, in situations where we may have a couple of millions of elements in the array, we may not be able to hold all data in memory. So we need to fallback to the Jackson Streaming API.

The Jackson Streaming API was inspired in [StAX][stax], an event-based API for processing XML documents. Unlike StAX, it uses the term _token_ instead of _event_, which better reflects the JSON structure.

The main types of the Jackson Streaming API are:

| Type | Description |
|------|-------------|
| [`JsonParser`][com.fasterxml.jackson.core.JsonParser] | Logical cursor for iterating over tokens, providing low level JSON reader capabilities |
| [`JsonGenerator`][com.fasterxml.jackson.core.JsonGenerator] | Low level JSON writer |
| [`JsonFactory`][com.fasterxml.jackson.core.JsonFactory] | Factory for creating instances of [`JsonParser`][com.fasterxml.jackson.core.JsonParser] and [`JsonGenerator`][com.fasterxml.jackson.core.JsonGenerator] |

When using streaming, the content to read (and write) has to be processed in the _exact same order_ as input comes in (or output is to go out). having said that, it's important to mention that  _random access_ is only provided by [data binding][com.fasterxml.jackson.databind.ObjectMapper] and [tree model][com.fasterxml.jackson.core.TreeNode] APIs, which both actually use the streaming API under the hood for reading and writing JSON documents.




## `JsonParser`

[`JsonParser`][com.fasterxml.jackson.core.JsonParser] is used to parse JSON content into tokens along with its associated data. It is the lowest level of read access to JSON content in Jackson.

To iterate the stream of tokens, the application advances the cursor by calling the [`nextToken()`][com.fasterxml.jackson.core.JsonParser.nextToken] method. And to access data and properties of the token cursor points to, the application calls one of accessors which will refer to property of the currently pointed-to token.

The [`JsonParser`][com.fasterxml.jackson.core.JsonParser] only keeps track of the data that the cursor currently points to (and just a little bit of context information for nesting, input line numbers and such).



### Parsing JSON with `JsonParser`

Let's see how to parse the JSON document shown above with [`JsonParser`][com.fasterxml.jackson.core.JsonParser]:

```java
private void parseJson(InputStream is) throws IOException {

    // Create a factory for creating a JsonParser instance
    JsonFactory jsonFactory = new JsonFactory();

    // Create a JsonParser instance
    try (JsonParser jsonParser = jsonFactory.createParser(is)) {

        // Check the first token
        if (jsonParser.nextToken() != JsonToken.START_ARRAY) {
            throw new IllegalStateException("Expected content to be an array");
        }

        // Iterate over the tokens until the end of the array
        while (jsonParser.nextToken() != JsonToken.END_ARRAY) {

            // Read a contact and do something with it
            Contact contact = readContact(jsonParser);
            doSomethingWithContact(contact);
        }
    }
}
```

```java
private Contact readContact(JsonParser jsonParser) throws IOException {

    // Check the first token
    if (jsonParser.currentToken() != JsonToken.START_OBJECT) {
        throw new IllegalStateException("Expected content to be an object");
    }

    Contact contact = new Contact();

    // Iterate over the properties of the object
    while (jsonParser.nextToken() != JsonToken.END_OBJECT) {

        // Get the current property name
        String property = jsonParser.getCurrentName();

        // Move to the corresponding value
        jsonParser.nextToken();

        // Evaluate each property name and extract the value
        switch (property) {
            case "id":
                contact.setId(jsonParser.getIntValue());
                break;
            case "firstName":
                contact.setFirstName(jsonParser.getText());
                break;
            case "lastName":
                contact.setLastName(jsonParser.getText());
                break;
            case "emails":
                List<String> emails = readEmails(jsonParser);
                contact.setEmails(emails);
                break;
            case "createdDateTime":
                contact.setCreatedDateTime(OffsetDateTime.parse(jsonParser.getText()));
                break;
            // Unknown properties are ignored
        }
    }

    return contact;
}
```

```java
private List<String> readEmails(JsonParser jsonParser) throws IOException {

    // Check the first token
    if (jsonParser.currentToken() != JsonToken.START_ARRAY) {
        throw new IllegalStateException("Expected content to be an object");
    }

    List<String> emails = new ArrayList<>();

    // Iterate over the tokens until the end of the array
    while (jsonParser.nextToken() != JsonToken.END_ARRAY) {

        // Add each element of the array to the list of emails
        emails.add(jsonParser.getText());
    }

    return emails;
}
```

Well, it's an _efficient_ way to parse JSON content in terms of memory consumption and processing overhead. But, as we can see, it's not _conveninent_: it's verbose, repetitive and tedious to write.

We will see below how to combine streaming with data binding to reduce the verbosity of our code.



### Parsing JSON with `JsonParser` and `ObjectMapper`

This example shows how to take advantage of the data binding capabilities of [`ObjectMapper`][com.fasterxml.jackson.databind.ObjectMapper] while streaming the content of a file:

```java
private void parseJson(InputStream is) throws IOException {

    // Create and configure an ObjectMapper instance
    ObjectMapper mapper = new ObjectMapper();
    mapper.registerModule(new JavaTimeModule());
    mapper.disable(DeserializationFeature.FAIL_ON_UNKNOWN_PROPERTIES);

    // Create a JsonParser instance
    try (JsonParser jsonParser = mapper.getFactory().createParser(is)) {

        // Check the first token
        if (jsonParser.nextToken() != JsonToken.START_ARRAY) {
            throw new IllegalStateException("Expected content to be an array");
        }

        // Iterate over the tokens until the end of the array
        while (jsonParser.nextToken() != JsonToken.END_ARRAY) {

            // Read a contact instance using ObjectMapper and do something with it
            Contact contact = mapper.readValue(jsonParser, Contact.class);
            doSomethingWithContact(contact);
        }
    }
}
```

[`ObjectMapper`][com.fasterxml.jackson.databind.ObjectMapper] can read a value directly from [`JsonParser`][com.fasterxml.jackson.core.JsonParser], so we can mix streaming with data binding, taking full advantage of the [`ObjectMapper`][com.fasterxml.jackson.databind.ObjectMapper] configuration, such as modules, deserialization features and custom deserializers.



## `JsonGenerator`

[`JsonGenerator`][com.fasterxml.jackson.core.JsonGenerator] allows to construct JSON content based on a sequence of calls to output JSON tokens. It is the lowest level of write access to JSON content in Jackson.



### Generating JSON with `JsonGenerator`

Let’s see how to generate a JSON document using [`JsonGenerator`][com.fasterxml.jackson.core.JsonGenerator]:

```java
private void generateJson(List<Contact> contacts, OutputStream os) throws IOException {

    // Create a factory which will be used for creating a JsonGenerator instance
    JsonFactory jsonFactory = new JsonFactory();

    // Create a JsonGenerator instance
    try (JsonGenerator jsonGenerator = jsonFactory.createGenerator(os)) {

        // Configure the JsonGenerator to pretty print the output
        jsonGenerator.useDefaultPrettyPrinter();

        // Write the start array token
        jsonGenerator.writeStartArray();

        // Iterate over the contacts and write each contact as a JSON object
        for (Contact contact : contacts) {
            writeContact(jsonGenerator, contact);
        }

        // Write the end array token
        jsonGenerator.writeEndArray();
    }
}
```

```java
private void writeContact(JsonGenerator jsonGenerator, Contact contact) throws IOException {

    // Write the start object token
    jsonGenerator.writeStartObject();

    // Write each field of the contact instance as a property/value pair
    jsonGenerator.writeNumberField("id", contact.getId());
    jsonGenerator.writeStringField("firstName", contact.getFirstName());
    jsonGenerator.writeStringField("lastName", contact.getLastName());
    jsonGenerator.writeFieldName("emails");
    writeEmails(jsonGenerator, contact.getEmails());
    jsonGenerator.writeStringField("createDateTime", contact.getCreatedDateTime().format(DateTimeFormatter.ISO_OFFSET_DATE_TIME));

    // Write the end object token
    jsonGenerator.writeEndObject();
}
```

```java
private void writeEmails(JsonGenerator jsonGenerator, List<String> emails) throws IOException {

    // Write the start array token
    jsonGenerator.writeStartArray();

    // Iterate over the emails and write each emails as a string
    for (String email: emails) {
        jsonGenerator.writeString(email);
    }

    // Write the end array token
    jsonGenerator.writeEndArray();
}
```

Like the code for parsing the JSON document, it is _efficient_ in terms of memory consumption and processing overhead. But it's verbose and repetitive.

So let's see how to combine the Jackson Streaming API with data binding for generating JSON documents.



### Generating JSON with `JsonGenerator` and `ObjectMapper`

To wrap up, let's see how to generate JSON content combining [`JsonGenerator`][com.fasterxml.jackson.core.JsonGenerator] and [`ObjectMapper`][com.fasterxml.jackson.databind.ObjectMapper]:

```java
private void generateJson(List<Contact> contacts, OutputStream os) throws IOException {

    // Create and configure an ObjectMapper instance
    ObjectMapper mapper = new ObjectMapper();
    mapper.registerModule(new JavaTimeModule());
    mapper.disable(SerializationFeature.WRITE_DATES_AS_TIMESTAMPS);
    mapper.enable(SerializationFeature.INDENT_OUTPUT);

    // Create a JsonGenerator instance
    try (JsonGenerator jsonGenerator = mapper.getFactory().createGenerator(os)) {

        // Write the start array token
        jsonGenerator.writeStartArray();

        // Iterate over the contacts and write each contact as a JSON object
        for (Contact contact : contacts) {
            
             // Write a contact instance as JSON using ObjectMapper
             mapper.writeValue(jsonGenerator, contact);
        }

        // Write the end array token
        jsonGenerator.writeEndArray();
    }
}
```

[`ObjectMapper`][com.fasterxml.jackson.databind.ObjectMapper] can write a value directly to [`JsonGenerator`][com.fasterxml.jackson.core.JsonGenerator], allowing us to combine streaming with data binding to significantly reduce the amount of code we need to write. This approach takes advantage of modules, serialization features and custom serializers defined in the [`ObjectMapper`][com.fasterxml.jackson.databind.ObjectMapper].



  [com.fasterxml.jackson.core.JsonFactory]: https://fasterxml.github.io/jackson-core/javadoc/2.9/com/fasterxml/jackson/core/JsonFactory.html
  [com.fasterxml.jackson.core.JsonParser]: https://fasterxml.github.io/jackson-core/javadoc/2.9/com/fasterxml/jackson/core/JsonParser.html
  [com.fasterxml.jackson.core.JsonParser.nextToken]: https://fasterxml.github.io/jackson-core/javadoc/2.9/com/fasterxml/jackson/core/JsonParser.html#nextToken--
  [com.fasterxml.jackson.core.JsonGenerator]: https://fasterxml.github.io/jackson-core/javadoc/2.9/com/fasterxml/jackson/core/JsonGenerator.html
  [com.fasterxml.jackson.databind.ObjectMapper]: https://fasterxml.github.io/jackson-databind/javadoc/2.9/com/fasterxml/jackson/databind/ObjectMapper.html
  [com.fasterxml.jackson.core.TreeNode]: https://fasterxml.github.io/jackson-core/javadoc/2.9/com/fasterxml/jackson/core/TreeNode.html
  
  [repo]: https://github.com/cassiomolin/using-jackson-streaming-api-with-objectmapper.git
  
  [stax]: https://docs.oracle.com/javase/tutorial/jaxp/stax/api.html
  
