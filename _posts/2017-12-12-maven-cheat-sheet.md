---
title: Maven cheat sheet
date: 2017-12-12 13:27:30 Z
tags:
- java
- maven
layout: post
author: Cassio Mazzochi Molin
excerpt: A compilation of some Maven commands for quick reference.
image: "/assets/images/posts/2017-12-12-maven-cheat-sheet/cover.jpg"
image_source: https://unsplash.com/photos/VviFtDJakYk
---

I've put together some Maven commands, properties and command line options.

Creating a project (jar):

```bash
mvn archetype:generate \
    -DgroupId=com.example.project \
    -DartifactId=application
```

Creating a project (war):

```bash
mvn archetype:generate \
    -DgroupId=com.example.project \
    -DartifactId=application \
    -DarchetypeArtifactId=maven-archetype-webapp
```

Setting the source code encoding:

```xml
<properties>
    <project.build.sourceEncoding>UTF-8</project.build.sourceEncoding>
</properties>
```

Setting the Java version:

```xml
<properties>
    <maven.compiler.source>1.8</maven.compiler.source>
    <maven.compiler.target>1.8</maven.compiler.target>
</properties>
```

## Default lifecycle

The `default` lifecycle consist of the following phases:

| Phase      | Description                                                                                      |
| ---------- | ------------------------------------------------------------------------------------------------ |
| `validate` | Validate the project, checking if everything is correct.                                         |
| `compile`  | Compile source code of the project and store classes in `target/classes`.                        |
| `test`     | Run the tests.                                                                                   |
| `package`  | Take the compiled code and package it in its distributable format, sucg as JAR or WAR.           |
| `verify`   | Run any checks to verify the package is valid and meets quality criteria.                        |
| `install`  | Install the package into the local repository, or use as a dependency in other projects locally. |
| `deploy`   | Copies the final package to the remote repository.                                               |

Use `mvn <phase name>` to execute a phase.

## Useful command line options

| Command line option                          | Description                                                              |
| -------------------------------------------- | ------------------------------------------------------------------------ |
| `-DskipTests`                                | Compile the tests but don't run them                                     |
| `-Dmaven.test.skip=true`                     | Don't compile the tests and don't run them                               |
| `-X` or `--debug`                            | Enable debug output                                                      |
| `-U` or `--update-snapshots`                 | Forces a check for updated releases and snapshots on remote repositories |
| `-o` or `--offline`                          | Work offline (run as if no network connection is available)              |
| `-l <file path>` or `--log-file <file path>` | Writes the build output to a file                                        |
| `-v` or `--version`                          | Display Maven version                                                    |

## Useful properties

### Project properties

| Property                               | Description                                                         |
| -------------------------------------- | ------------------------------------------------------------------- |
| `${project.groupId}`                   | Project's group id                                                  |
| `${project.artifactId}`                | Project's artifact id                                               |
| `${project.version}`                   | Project's version                                                   |
| `${project.name}`                      | Project's name                                                      |
| `${project.description}`               | Project's description                                               |
| `${project.basedir}`                   | Directory containing the `pom.xml` file                             |
| `${project.baseUri}`                   | Directory containing the `pom.xml` file as URI                      |
| `${project.build.sourceDirectory}`     | Project source directory                                            |
| `${project.build.testSourceDirectory}` | Project test source directory                                       |
| `${project.build.outputDirectory}`     | Project output directory                                            |
| `${project.build.testOutputDirectory}` | Project test output directory                                       |
| `${project.build.directory}`           | Directory which contains all of these output directories (`target`) |
| `${project.build.finalName}`           | Final name of the file created when the built project is packaged   |

### Build time properties

| Property                          | Description                                                                    |
| --------------------------------- | ------------------------------------------------------------------------------ |
| `${maven.build.timestamp}`        | The UTC timestamp of build start, in `yyyy-MM-dd'T'HH:mm:ss'Z'` default format |
| `${build.timestamp}`              | Same as `${maven.build.timestamp}`                                             |
| `${maven.build.timestamp.format}` | Can be used to override the default format for the build timestamp             |

### Java system properties

| Property             | Description                      |
| -------------------- | -------------------------------- |
| `${java.class.path}` | Java class path                  |
| `${java.home}`       | Java installation directory      |
| `${java.vendor}`     | Java Runtime Environment vendor  |
| `${java.version}`    | Java Runtime Environment version |
| `${line.separator}`  | Line separator                   |
| `${file.separator}`  | File separator                   |
| `${os.name}`         | Operating system name            |
| `${os.arch}`         | Operating system architecture    |
| `${os.version}`      | Operating system version         |
| `${user.name}`       | User’s account name              |
| `${user.dir}`        | User’s current working directory |
| `${user.home}`       | User’s home directory            |

## Useful plugins

- [**Dependency plugin**][Dependency plugin]: Provides the capability to manipulate artifacts.
  - `mvn dependency:tree`: Show dependency tree.
  - `mvn dependency:resolve`: Resolve dependencies.
  - `mvn dependency:resolve-plugins`: Resolve plugins.

- [**Versions plugin**][Versions plugin]: Manage the versions of artifacts in a project's POM.
  - `mvn versions:set -DgenerateBackupPoms=false -DnewVersion=[new version]`: Set a new project version.

- [**Assembly plugin**][Assembly plugin]: Aggregate the project output along with its dependencies, modules and other files into a single distributable archive.

- [**Release plugin**][Release plugin]: Plugin used to release a project.

- [**Shade plugin**][Shade plugin]: Package the artifact in an uber-jar, including its dependencies.

- [**Javadoc plugin**][Javadoc plugin]: Generate javadocs for a project.
  - `mvn javadoc:javadoc`: Output javadocs HTML files in `target/site/apidocs`.

## Resources

- [Maven: The Complete Reference][Maven: The Complete Reference]
- [Introduction to the Build Lifecycle][Lifecycle]


  [Lifecycle]: https://maven.apache.org/guides/introduction/introduction-to-the-lifecycle.html
  [Versions plugin]: http://www.mojohaus.org/versions-maven-plugin/
  [Dependency plugin]: http://maven.apache.org/plugins/maven-dependency-plugin/
  [Release plugin]: http://maven.apache.org/maven-release/maven-release-plugin/
  [Shade plugin]: https://maven.apache.org/plugins/maven-shade-plugin/
  [Javadoc plugin]: http://maven.apache.org/plugins/maven-javadoc-plugin/
  [Assembly plugin]: http://maven.apache.org/plugins/maven-assembly-plugin/
  [Maven: The Complete Reference]: http://books.sonatype.com/mvnref-book/reference/index.html