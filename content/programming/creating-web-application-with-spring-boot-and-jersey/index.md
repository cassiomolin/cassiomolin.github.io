---
title: Creating web application with Spring Boot and Jersey
date: 2016-10-07
tags:
- java
- jersey
- spring-boot
summary: Example of how to create a standalone application with Jersey with Spring Boot.
aliases:
- /2016/10/07/creating-web-application-with-spring-boot-and-jersey/
---

Spring Boot helps you accelerate the application development and makes it easy to create standalone applications that you can "_just run_". Spring Boot embeds a web server, such as Tomcat or Jetty, in the application. So there's no need to deploy a WAR file. It's packed as a JAR and, to run it, you just need `java -jar`.

Jersey is the reference implementation of the JAX-RS 2.0 specification and provides a solid API for creating and consuming web services in Java.

In this post, let's create a sample application with Spring Boot and Jersey.

Ensure your `pom.xml` file declares `spring-boot-starter-parent` as the parent project and declares all the dependencies and plugins shown below:

```xml
<project xmlns="http://maven.apache.org/POM/4.0.0" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
    xsi:schemaLocation="http://maven.apache.org/POM/4.0.0 http://maven.apache.org/xsd/maven-4.0.0.xsd">
    <modelVersion>4.0.0</modelVersion>
    <groupId>com.cassiomolin</groupId>
    <artifactId>spring-jersey</artifactId>
    <version>1.0-SNAPSHOT</version>

    <parent>
        <groupId>org.springframework.boot</groupId>
        <artifactId>spring-boot-starter-parent</artifactId>
        <version>1.4.0.RELEASE</version>
    </parent>

    <properties>
        <project.build.sourceEncoding>UTF-8</project.build.sourceEncoding>
        <java.version>1.8</java.version>
    </properties>

    <dependencies>
        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter-web</artifactId>
        </dependency>
        <dependency>
            <groupId>org.glassfish.jersey.ext</groupId>
            <artifactId>jersey-spring3</artifactId>
        </dependency>
        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter-test</artifactId>
            <scope>test</scope>
        </dependency>
        <dependency>
            <groupId>junit</groupId>
            <artifactId>junit</artifactId>
            <scope>test</scope>
        </dependency>
    </dependencies>

    <build>
        <plugins>
            <plugin>
                <groupId>org.springframework.boot</groupId>
                <artifactId>spring-boot-maven-plugin</artifactId>
            </plugin>
        </plugins>
    </build>

</project>
```

The Spring Boot Maven plugin collects all the JARs on the classpath and builds a single, runnable _uber JAR_, which makes it more convenient to execute and transport the application. Besides it, the plugin searches for the `public static void main()` method to flag as a runnable class.

Create a Jersey resource class annotated with [`@Path`][4] and define a resource method to handle `GET` requests, producing `text/plain`:

```java
@Path("/greetings")
public class GreetingResource {

    @GET
    @Produces(MediaType.TEXT_PLAIN)
    public Response getGreeting() {
        return Response.ok("Hello, World!").build();
    }
}
```

Create a class that extends [`ResourceConfig`][2] or [`Application`][3] to register the Jersey resources:

```java
@Component
@ApplicationPath("api")
public class JerseyConfig extends ResourceConfig {

    @PostConstruct
    private void init() {
        registerClasses(GreetingResource.class);
    }
}
```

And finally create a Spring Boot class to execute the application:

```java
@SpringBootApplication
public class Application {

    public static void main(String[] args) {
        SpringApplication.run(Application.class, args);
    }
}
```

To test this web service, we can use the [JAX-RS Client API][5]:

```java
@RunWith(SpringRunner.class)
@SpringBootTest(webEnvironment = SpringBootTest.WebEnvironment.RANDOM_PORT)
public class GreetingResourceTest {

    @LocalServerPort
    private int port;

    private URI uri;

    @Before
    public void setUp() throws Exception {
        this.uri = new URI("http://localhost:" + port);
    }

    @Test
    public void testGreeting() {

        Client client = ClientBuilder.newClient();
        Response response = client.target(uri).path("api").path("greetings")
                                  .request(MediaType.TEXT_PLAIN).get();

        String entity = response.readEntity(String.class);
        assertEquals("Hello, World!", entity);
    }
}
```

To compile and run the application, follow these steps:

- Open a command line window or terminal.
- Navigate to the root directory of the project, where the `pom.xml` resides.
- Compile the project: `mvn clean compile`.
- Package the application: `mvn package`.
- Look in the `target` directory. You should see a file with the following or a similar name: `spring-jersey-1.0-SNAPSHOT.jar`.
- Change into the `target` directory.
- Execute the JAR: `java -jar spring-jersey-1.0-SNAPSHOT.jar`.
- The application should be available at `http://localhost:8080/api/greetings`.

---

This example is available on [GitHub][1].

[1]: https://github.com/cassiomolin/jersey-springboot
[2]: https://jersey.java.net/apidocs/2.23/jersey/org/glassfish/jersey/server/ResourceConfig.html
[3]: https://jersey.java.net/apidocs/2.23/jersey/javax/ws/rs/core/Application.html
[4]: https://jersey.java.net/apidocs/2.23/jersey/javax/ws/rs/Path.html
[5]: https://jersey.java.net/apidocs/2.23/jersey/javax/ws/rs/client/package-summary.html
