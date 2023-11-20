---
title: Adding Maven dependencies to Arquillian test
date: 2015-06-07
tags:
- java
- test
- arquillian
summary: Using ShrinkWrap resolvers to add Maven dependencies to Arquillian tests.
aliases:
- /2015/06/07/adding-maven-dependencies-to-arquillian-test/
---

By default, Arquillian won't pack the Maven dependencies into the micro deployment files.

If the classes your are testing depend on external dependencies managed by Maven, follow the steps described below to ensure the Maven dependencies will be packed into the Arquillian micro deployments, avoiding [`ClassNotFoundException`][3]s:

## Adding Arquillian dependencies

Add Arquillian dependencies to your `pom.xml`:

```xml
<dependencyManagement>
    <dependencies>
        <dependency>
            <groupId>org.jboss.arquillian</groupId>
            <artifactId>arquillian-bom</artifactId>
            <version>1.1.8.Final</version>
            <scope>import</scope>
            <type>pom</type>
        </dependency>
    </dependencies>
</dependencyManagement>
```

Add the ShrinkWrap resolver (Maven implementation) to your `pom.xml`:

```xml
<dependency>
    <groupId>org.jboss.shrinkwrap.resolver</groupId>
    <artifactId>shrinkwrap-resolver-impl-maven</artifactId>
    <scope>test</scope>
</dependency>
```

If you are using JUnit, add the Arquillian JUnit container to your `pom.xml`:

```xml
<dependency>
    <groupId>org.jboss.arquillian.junit</groupId>
    <artifactId>arquillian-junit-container</artifactId>
    <scope>test</scope>
</dependency>
```

## Importing Maven dependencies

In your test class, within the method annotated with `@Deployment`, import the runtime dependencies with the following line:

```java
File[] files = Maven.resolver().loadPomFromFile("pom.xml")
        .importRuntimeDependencies().resolve().withTransitivity().asFile();
```

And then add the dependencies to your deploy using the `addAsLibraries(files)` method:

```java
ShrinkWrap.create(WebArchive.class)
          .addClass(MyClass1.class)
          .addClass(MyClass2.class)
          .addClass(MyClass3.class)
          .addAsLibraries(files);
```

This is how your test class will look like if you are using JUnit:

```java
import java.io.File;

import org.jboss.arquillian.container.test.api.Deployment;
import org.jboss.arquillian.junit.Arquillian;
import org.jboss.shrinkwrap.api.ShrinkWrap;
import org.jboss.shrinkwrap.api.asset.EmptyAsset;
import org.jboss.shrinkwrap.api.spec.WebArchive;
import org.jboss.shrinkwrap.resolver.api.maven.Maven;
import org.junit.Test;
import org.junit.runner.RunWith;
import static org.junit.Assert.*;

@RunWith(Arquillian.class)
public class MyTestClassWithMavenDependencies {

    @Deployment
    public static WebArchive createDeployment() {

        // Import Maven runtime dependencies
        File[] files = Maven.resolver().loadPomFromFile("pom.xml")
                .importRuntimeDependencies().resolve().withTransitivity().asFile();

        // Create deploy file
        WebArchive war = ShrinkWrap.create(WebArchive.class)
                .addClass(MyClass1.class)
                .addClass(MyClass2.class)
                .addClass(MyClass3.class)
                .addAsLibraries(files);

        // Show the deploy structure
        System.out.println(war.toString(true));

        return war;
    }

    // Create your tests here
}
```

---

**Note 1:** The above solution was tested with Arquillian `1.1.8.Final`. Check the most recent version of Arquillian artifacts on the [documentation][1].

**Note 2:** For more details on how to resolve dependencies, have a look at the [ShrinkWrap Resolvers documentation][2].

[1]: http://arquillian.org/modules/core-platform/#artifacts
[2]: https://github.com/shrinkwrap/resolver#resolving-dependencies
[3]: https://docs.oracle.com/javase/8/docs/api/java/lang/ClassNotFoundException.html
