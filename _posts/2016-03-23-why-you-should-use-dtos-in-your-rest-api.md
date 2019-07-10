---
title: Why you should use DTOs in your REST API
date: 2016-03-23 10:16:45 Z
tags:
- rest
- java
- dto
layout: post
author: Cassio Mazzochi Molin
excerpt: Why you should consider using Data Transfer Objects instead of persistence models in your REST API.
featured_image: null
featured_image_thumbnail: null
redirect_from:
  - /why-you-should-use-dtos-in-your-rest-api/
---

**DTO** stands for [**D**ata **T**ransfer **O**bject][1]. 

This pattern was created with a very well defined purpose: **transfer data to _remote interfaces_**, just like *web services*. This pattern fits very well in a REST API and DTOs will give you more *flexibility* in the long run.

The models that represent the _domain_ of your application and the models that represent the _data handled by your API_ are (or at least should be) _different concerns_ and should be __decoupled__ from each other. You don’t want to break your API clients when you add, remove or rename a field from the application domain model.

While your service layer operates over the domain/persistence models, your API controllers should operate over a different set of models. As your domain/persistence models evolve to support new business requirements, for example, you may want to create new versions of the API models to support these changes. You also may want to deprecate the old versions of your API as new versions are released. And it’s perfectly possible to achieve when the things are decoupled.

---

Just to mention a few benefits of exposing DTOs instead of persistence models: 

- _Decouple_ persistence models from API models.

- DTOs can be *tailored* to your needs and they are great when exposing only a set of attributes of your persistence entities. You won't need annotations such as [`@XmlTransient`][2] and [`@JsonIgnore`][3] to avoid the serialization of some attributes.

- By using DTOs, you will avoid a *hell of annotations* in your persistence entities, that is, your persistence entities won't be bloated with non persistence related annotations.

- You will have *full control* over the attributes you are receiving when creating or updating a resource.

- If you are using [Swagger][4], you can use [`@ApiModel`][5] and [`@ApiModelProperty`][6] annotations to document your API models without messing your persistence entities.

- You can have different DTOs for each version of your API.

- You'll have more flexibility when mapping relationships.

- You can have different DTOs for different media types.

- Your DTOs can have a list of links for [HATEOAS][7]. That's the kind of thing that shouldn't be added to persistence objects. When using [Spring HATEOAS][8], you can make your DTO classes extend [`ResourceSupport`][9] or wrap them with [`Resource<T>`][10].

## Dealing with the boilerplate code

You won't need to map your persistence entities to DTOs and vice versa *mannually*. There are [many mapping frameworks][11] you can use to do it. For instance, have a look at [MapStruct][12], which is annotation based and works as a Maven Annotation Processor. It works well in both CDI and Spring-based applications.

You also may want to consider [Lombok][13] to generate getters, setters, `equals()`, `hashcode()` and `toString()` methods for you.

---

<sup>**Related:** To give better names to your DTO classes, refer to this [post][14] or to this [answer][15] on Stack Overflow.</sup>


  [1]: https://en.wikipedia.org/wiki/Data_transfer_object
  [2]: http://docs.oracle.com/javaee/7/api/javax/xml/bind/annotation/XmlTransient.html
  [3]: https://fasterxml.github.io/jackson-annotations/javadoc/2.7/com/fasterxml/jackson/annotation/JsonIgnore.html
  [4]: https://github.com/swagger-api/swagger-core
  [5]: https://github.com/swagger-api/swagger-core/wiki/Annotations-1.5.X#apimodel
  [6]: https://github.com/swagger-api/swagger-core/wiki/Annotations-1.5.X#apimodelproperty
  [7]: https://en.wikipedia.org/wiki/HATEOAS
  [8]: https://spring.io/projects/spring-hateoas
  [9]: https://docs.spring.io/spring-hateoas/docs/0.18.0.RELEASE/api/org/springframework/hateoas/ResourceSupport.html
  [10]: https://docs.spring.io/spring-hateoas/docs/0.18.0.RELEASE/api/org/springframework/hateoas/Resource.html
  [11]: https://stackoverflow.com/a/1432956/1426227
  [12]: http://mapstruct.org/
  [13]: https://projectlombok.org/
  [14]: https://cassiomolin.com/2016/02/11/give-better-names-to-your-dtos/
  [15]: https://stackoverflow.com/a/35341664/1426227
