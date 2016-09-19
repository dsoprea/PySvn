__author__ = 'tusharmakkar08'

diff_summary = [{'item': 'modified',
                 'kind': 'file',
                 'path': 'http://svn.apache.org/repos/asf/sling/trunk/pom.xml'},
                {'item': 'added',
                 'kind': 'file',
                 'path': 'http://svn.apache.org/repos/asf/sling/trunk/bundles/extensions/models/pom.xml'}]
diff = [{'path': 'http://svn.apache.org/repos/asf/sling/trunk/pom.xml', 'kind': 'file',
         'diff': '--- sling/trunk/pom.xml\t(revision 1760022)\n+++ sling/trunk/pom.xml\t'
                 '(revision 1760023)\n@@ -182,9 +182,7 @@\n         '
                 '<module>bundles/extensions/healthcheck</module>\n        '
                 ' <module>bundles/resourceaccesssecurity/core</module>\n         '
                 '<module>bundles/resourceaccesssecurity/it</module>\n-        '
                 '<module>bundles/extensions/models/api</module>\n-        '
                 '<module>bundles/extensions/models/impl</module>\n-       '
                 ' <module>bundles/extensions/models/integration-tests</module>\n+        '
                 '<module>bundles/extensions/models</module>\n        '
                 ' <module>bundles/extensions/i18n</module>\n         '
                 '<module>bundles/extensions/xss</module>\n        '
                 ' <module>bundles/extensions/resourcebuilder</module>\n@@ -224,7 +222,6 @@\n      '
                 '       </activation>\n             <modules>\n            '
                 '     <module>bundles/extensions/validation</module>\n-               '
                 ' <module>bundles/extensions/models/validation-impl</module>\n    '
                 '         </modules>\n         </profile>\n         <profile>',
         'item': 'modified'},
        {'path': 'http://svn.apache.org/repos/asf/sling/trunk/bundles/extensions/models/pom.xml', 'kind': 'file',
         'diff': '--- sling/trunk/bundles/extensions/models/pom.xml\t(revision 0)\n+++ '
                 'sling/trunk/bundles/extensions/models/pom.xml\t(revision 1760023)\n@@ -'
                 '0,0 +1,61 @@\n+<?xml version="1.0" encoding="UTF-8"?>\n+<!--\n+  '
                 'Licensed to the Apache Software Foundation (ASF) under one\n+  '
                 'or more contributor license agreements.  See the NOTICE file\n+  '
                 'distributed with this work for additional information\n+  '
                 'regarding copyright ownership.  The ASF licenses this file\n+  '
                 'to you under the Apache License, Version 2.0 (the\n+  "License"); '
                 'you may not use this file except in compliance\n+  with the License.  '
                 'You may obtain a copy of the License at\n+\n+   '
                 'http://www.apache.org/licenses/LICENSE-2.0\n+\n+  '
                 'Unless required by applicable law or agreed to in writing,\n+  '
                 'software distributed under the License is distributed on an\n+  '
                 '"AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY\n+  KIND, '
                 'either express or implied.  See the License for the\n+ '
                 ' specific language governing permissions and limitations\n+  '
                 'under the License.\n+-->\n+<project xmlns="http://maven.apache.org/POM/4.0.0"'
                 ' xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation='
                 '"http://maven.apache.org/POM/4.0.0 https://maven.apache.org/xsd/maven-4.0.0.xsd">\n+'
                 '    <modelVersion>4.0.0</modelVersion>\n+\n+    <parent>\n+      '
                 '  <groupId>org.apache.sling</groupId>\n+        <artifactId>sling</artifactId>\n+  '
                 '      <version>28</version>\n+        <relativePath/>\n+    </parent>\n+  \n+  '
                 '  <artifactId>org.apache.sling.models.reactor</artifactId>\n+    <packaging>pom</packaging>\n+'
                 '    <version>0.0.1-SNAPSHOT</version>\n+    <name>Apache Sling Models Reactor</name>\n+   '
                 ' <description>Apache Sling Models</description>\n+  \n+    <scm>\n+       '
                 ' <connection>scm:svn:https://svn.apache.org/repos/asf/sling/trunk/bundles/'
                 'extensions/models</connection>\n+        '
                 '<developerConnection>scm:svn:https://svn.apache.org/repos/asf/sling/trunk/bundles/'
                 'extensions/models</developerConnection>\n+        '
                 '<url>https://svn.apache.org/repos/asf/sling/trunk/bundles/extensions/models</url>\n+    '
                 '</scm>\n+    \n+    <modules>\n+        <module>api</module>\n+        <module>impl</module>\n+  '
                 '      <module>integration-tests</module>\n+    </modules>\n+\n+    <profiles>\n+       '
                 ' <profile>\n+            <!-- build modules depending on Java 8 also -->\n+         '
                 '   <id>java8</id>\n+            <activation>\n+                <jdk>[1.8,)</jdk>\n+   '
                 '         </activation>\n+            <modules>\n+             '
                 '   <module>validation-impl</module>\n+            </modules>\n+     '
                 '   </profile>\n+    </profiles>\n+\n+</project>\n\nProperty changes on: '
                 'sling/trunk/bundles/extensions/models/pom.xml\n__________________________________'
                 '_________________________________\nAdded: svn:mime-type\n## -0,0 +1 ##\n+text/plain\n\\ '
                 'No newline at end of property\nAdded: svn:keywords\n## -0,0 +1 ##\n+LastChangedDate '
                 'LastChangedRevision LastChangedBy HeadURL Id Author\n\\ No newline at end of property\nAdded: '
                 'svn:eol-style\n## -0,0 +1 ##\n+native\n\\ No newline at end of property',
         'item': 'added'}]
cat = """This is an as-yet incomplete update for Abdera. All of the base dependencies
have been updated and a broad range of significant changes have been made to
the overall code structure, many of the apis and implementation detail. """