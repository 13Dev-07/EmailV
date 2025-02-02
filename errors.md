app/smtp_connection_pool.py Line: 227 
The is operator performs an identity comparison that uses the built-in is() method to test if the compared items are the same object or not. It should be used with only singletons, such as None. We recommend that you use the == or != equality operators to determine if two objects are equal.

Learn more 

Confusion between equality ==, != and identity is in conditional expressions can lead to unintended behavior.

Source
CodeGuru
Was this helpful?


app/utils/dns_resolver.py Line: 112 
It appears that you are generically passing an Exception object without performing any other operation on it. This may hide error conditions that can otherwise be quickly detected and addressed. We recommend that you catch a more specific exception. If the code must broadly catch all exceptions, consider logging the stack trace using the logging.exception()  API. For example,

try:
    x = 1 / 0
except ZeroDivisionError as e:
    logging.exception('ZeroDivisionError: %s', e)

Similar issue at line number 118.

Do not pass generic exception.

Source
CodeGuru
Was this helpful?


app/dns_resolver.py Line: 87 
The naive datetime objects are treated by many datetime methods as local times, it is preferred to use aware datetimes to represent times in UTC. The recommended way to create an aware datetime object representing a specific timestamp in UTC is by passing tzinfo as an argument to the method.

Learn more 

Naive datetime objects are treated by many datetime methods as local times and might cause time zone related issues.

Source
CodeGuru
Was this helpful?


app/utils/smtp_verifier.py Line: 119 
It appears that you are generically passing an Exception object without performing any other operation on it. This may hide error conditions that can otherwise be quickly detected and addressed. We recommend that you catch a more specific exception. If the code must broadly catch all exceptions, consider logging the stack trace using the logging.exception()  API. For example,

try:
    x = 1 / 0
except ZeroDivisionError as e:
    logging.exception('ZeroDivisionError: %s', e)

Similar issue at line number 126.

Do not pass generic exception.

Source
CodeGuru
Was this helpful?


app/caching/redis_client.py Line: 147 
The naive datetime objects are treated by many datetime methods as local times, it is preferred to use aware datetimes to represent times in UTC. The recommended way to create an aware datetime object representing a specific timestamp in UTC is by passing tzinfo as an argument to the method.

Learn more 

Naive datetime objects are treated by many datetime methods as local times and might cause time zone related issues.

Source
CodeGuru
Was this helpful?


app/smtp_connection_pool.py Line: 92 
It appears that you are generically passing an Exception object without performing any other operation on it. This may hide error conditions that can otherwise be quickly detected and addressed. We recommend that you catch a more specific exception. If the code must broadly catch all exceptions, consider logging the stack trace using the logging.exception()  API. For example,

try:
    x = 1 / 0
except ZeroDivisionError as e:
    logging.exception('ZeroDivisionError: %s', e)

Do not pass generic exception.

Source
CodeGuru
Was this helpful?


app/smtp_connection_pool.py Line: 221 
It appears that you are generically passing an Exception object without performing any other operation on it. This may hide error conditions that can otherwise be quickly detected and addressed. We recommend that you catch a more specific exception. If the code must broadly catch all exceptions, consider logging the stack trace using the logging.exception()  API. For example,

try:
    x = 1 / 0
except ZeroDivisionError as e:
    logging.exception('ZeroDivisionError: %s', e)

Do not pass generic exception.

Source
CodeGuru
Was this helpful?


app/batching/batch_processor.py Line: 115 
Modifying object.__dict__ directly or writing to an instance of a class __dict__ attribute directly is not recommended. Inside every module is a __dict__ object.dict  attribute which contains its symbol table. If you modify object.__dict__, then the symbol table is changed. Also, direct assignment to the __dict__ attribute is not possible.

Learn more 

Modifying object.__dict__ directly or writing to an instance of a class __dict__ attribute directly is not recommended. Inside every module is a __dict__ attribute which contains its symbol table. If you modify object.__dict__, then the symbol table is changed. Also, direct assignment to the __dict__ attribute is not possible.

Source
CodeGuru
Was this helpful?


app/api/key_management.py Line: 32 
Naive datetime objects are treated by many datetime methods as local times, We recommend that you create aware timestamps with the now or fromtimestamp functions using the tzinfo to attribute to represent times in UTC. Do not use the datetime.utcnow()  because it returns only a naive datetime object.

Learn more 

Naive datetime objects are treated by many datetime methods as local times and might cause time zone related issues.

Source
CodeGuru
Was this helpful?


app/utils/smtp_verifier.py Line: 136 
It appears that you are generically passing an Exception object without performing any other operation on it. This may hide error conditions that can otherwise be quickly detected and addressed. We recommend that you catch a more specific exception. If the code must broadly catch all exceptions, consider logging the stack trace using the logging.exception()  API. For example,

try:
    x = 1 / 0
except ZeroDivisionError as e:
    logging.exception('ZeroDivisionError: %s', e)

Do not pass generic exception.

Source
CodeGuru


app/utils/dns_resolver.py Line: 194 
It appears that you are generically passing an Exception object without performing any other operation on it. This may hide error conditions that can otherwise be quickly detected and addressed. We recommend that you catch a more specific exception. If the code must broadly catch all exceptions, consider logging the stack trace using the logging.exception()  API. For example,

try:
    x = 1 / 0
except ZeroDivisionError as e:
    logging.exception('ZeroDivisionError: %s', e)

Similar issue at line numbers 201, 208, and 219.

Do not pass generic exception.

Source
CodeGuru
Was this helpful?


app/monitoring/reporting.py Line: 25 
The naive datetime objects are treated by many datetime methods as local times, it is preferred to use aware datetimes to represent times in UTC. The recommended way to create an aware datetime object representing a specific timestamp in UTC is by passing tzinfo as an argument to the method.

Learn more 

Naive datetime objects are treated by many datetime methods as local times and might cause time zone related issues.

Source
CodeGuru
Was this helpful?


app/utils/dns_resolver.py Line: 162 
It appears that you are generically passing an Exception object without performing any other operation on it. This may hide error conditions that can otherwise be quickly detected and addressed. We recommend that you catch a more specific exception. If the code must broadly catch all exceptions, consider logging the stack trace using the logging.exception()  API. For example,

try:
    x = 1 / 0
except ZeroDivisionError as e:
    logging.exception('ZeroDivisionError: %s', e)

Do not pass generic exception.

Source
CodeGuru
Was this helpful?


app/utils/catch_all_detector.py Line: 34 
This function contains 41 lines of code, not including blank lines or lines with only comments, Python punctuation characters, identifiers, or literals. By comparison, 98% of the functions in the CodeGuru reference dataset contain fewer lines of code. Large functions might be difficult to read and have logic that is hard to understand and test.

We recommend that you simplify this function or break it into multiple functions. For example, consider extracting the code block on lines 34-69 into a separate function.

Large functions might be difficult to read, and have logic that is hard to understand and test. Large functions should be simplified or broken into multiple smaller functions. The size of a function is computed as the number of lines of code, not including blank lines or lines with only comments, Python punctuation characters, identifiers, or literals.

Source
CodeGuru
Was this helpful?


app/monitoring.py Line: 47 
Naive datetime objects are treated by many datetime methods as local times, We recommend that you create aware timestamps with the now or fromtimestamp functions using the tzinfo to attribute to represent times in UTC. Do not use the datetime.utcnow()  because it returns only a naive datetime object.

Learn more 

Naive datetime objects are treated by many datetime methods as local times and might cause time zone related issues.

Source
CodeGuru
Was this helpful?


app/api/audit_logger.py Line: 51 
Naive datetime objects are treated by many datetime methods as local times, We recommend that you create aware timestamps with the now or fromtimestamp functions using the tzinfo to attribute to represent times in UTC. Do not use the datetime.utcnow()  because it returns only a naive datetime object.

Learn more 

Naive datetime objects are treated by many datetime methods as local times and might cause time zone related issues.

Source
CodeGuru
Was this helpful?


app/smtp_connection_pool.py Line: 71 
It appears that you are generically passing an Exception object without performing any other operation on it. This may hide error conditions that can otherwise be quickly detected and addressed. We recommend that you catch a more specific exception. If the code must broadly catch all exceptions, consider logging the stack trace using the logging.exception()  API. For example,

try:
    x = 1 / 0
except ZeroDivisionError as e:
    logging.exception('ZeroDivisionError: %s', e)

Do not pass generic exception.

Source
CodeGuru
Was this helpful?


app/database_setup.py Line: 32 
Using Exception and BaseException can make your code prone to errors and difficult to maintain. Instead, we recommend using one of the Built-in Exceptions  or creating a custom exception class that is derived from Exception or one of its subclasses.

Throwing a base or generic exception might cause important error information to be lost. This can make your code difficult to maintain. We recommend using built-in exceptions or creating a custom exception class that is derived from Exception or one of its subclasses.

Source
CodeGuru
Was this helpful?


app/api/key_management.py Line: 73 
Naive datetime objects are treated by many datetime methods as local times, We recommend that you create aware timestamps with the now or fromtimestamp functions using the tzinfo to attribute to represent times in UTC. Do not use the datetime.utcnow()  because it returns only a naive datetime object.

Learn more 

Naive datetime objects are treated by many datetime methods as local times and might cause time zone related issues.

Source
CodeGuru
Was this helpful?


app/monitoring/reporting.py Line: 144 
The naive datetime objects are treated by many datetime methods as local times, it is preferred to use aware datetimes to represent times in UTC. The recommended way to create an aware datetime object representing a specific timestamp in UTC is by passing tzinfo as an argument to the method.

Learn more 

Naive datetime objects are treated by many datetime methods as local times and might cause time zone related issues.

Source
CodeGuru



app/smtp_connection_pool.py Line: 264 
It appears that you are generically passing an Exception object without performing any other operation on it. This may hide error conditions that can otherwise be quickly detected and addressed. We recommend that you catch a more specific exception. If the code must broadly catch all exceptions, consider logging the stack trace using the logging.exception()  API. For example,

try:
    x = 1 / 0
except ZeroDivisionError as e:
    logging.exception('ZeroDivisionError: %s', e)

Do not pass generic exception.

Source
CodeGuru
Was this helpful?


appspec.yml Line: 2 
Security
Resource not properly configured

Making sure the basic CloudFormation resources are properly configured.

Source
CodeGuru
Was this helpful?


app/smtp_connection_pool.py Line: 173 
Security
We detected a URL in your code that uses an unencrypted ftp, telnet, http or smtp connection. These protocols are not secure and introduce the risk of exposing sensitive data to third parties. To secure your connection, we recommend using ssh instead of telnet, sftp, ftps or scp instead of ftp, https instead of http and tls over smtp (smtps). For more information, see CWE-200  and CWE-319 .

Connections that use insecure protocols transmit data in cleartext. This introduces a risk of exposing sensitive data to third parties.

Source
CodeGuru
Was this helpful?


app/smtp_connection_pool.py Line: 55 
Security
We detected a URL in your code that uses an unencrypted ftp, telnet, http or smtp connection. These protocols are not secure and introduce the risk of exposing sensitive data to third parties. To secure your connection, we recommend using ssh instead of telnet, sftp, ftps or scp instead of ftp, https instead of http and tls over smtp (smtps). For more information, see CWE-200  and CWE-319 .

Connections that use insecure protocols transmit data in cleartext. This introduces a risk of exposing sensitive data to third parties.

Source
CodeGuru
Was this helpful?


appspec.yml Line: 1 
Security
Top level template section version is not valid

Making sure the basic CloudFormation template components are properly configured.

Source
CodeGuru
Was this helpful?


app/monitoring/reporting.py Line: 97 
Security
HTML templating engines have an autoescape mechanism that protects web applications from the most common cross-site-scripting (XSS) vulnerabilities. To increase the security of your code, set the autoescape attribute to True.

User-controllable input must be sanitized before it's included in output used to dynamically generate a web page. Unsanitized user input can introduce cross-side scripting (XSS) vulnerabilities that can lead to inadvertedly running malicious code in a trusted context.

Source
CodeGuru
Was this helpful?


app/dns_resolver.py Line: 203 
Security
Problem This line of code might contain a resource leak. Resource leaks can cause your system to slow down or crash.

Fix Consider closing the following resource: loop. The resource is allocated by call asyncio.get_event_loop. Execution paths that do not contain closure statements were detected. Close loop in a try-finally block to prevent the resource leak.

Allocated resources are not released properly. This can slow down or crash your system. They must be closed along all paths to prevent a resource leak.

Source
CodeGuru
Was this helpful?


app/utils/smtp_verifier.py Line: 119 
Security
Try, Except, Pass detected. https://bandit.readthedocs.io/en/latest/plugins/b110_try_except_pass.html

Improper error handling can enable attacks and lead to unwanted behavior. Parts of the system may receive unintended input, which may result in altered control flow, arbitrary control of a resource, or arbitrary code execution.

Source
Bandit 1.6
Was this helpful?


app/utils/dns_resolver.py Line: 208 
Security
Try, Except, Pass detected. https://bandit.readthedocs.io/en/latest/plugins/b110_try_except_pass.html

Improper error handling can enable attacks and lead to unwanted behavior. Parts of the system may receive unintended input, which may result in altered control flow, arbitrary control of a resource, or arbitrary code execution.

Source
Bandit 1.6
Was this helpful?


app/utils/dns_resolver.py Line: 219 
Security
Try, Except, Pass detected. https://bandit.readthedocs.io/en/latest/plugins/b110_try_except_pass.html

Improper error handling can enable attacks and lead to unwanted behavior. Parts of the system may receive unintended input, which may result in altered control flow, arbitrary control of a resource, or arbitrary code execution.

Source

app/utils/dns_resolver.py Line: 118 
Security
Try, Except, Pass detected. https://bandit.readthedocs.io/en/latest/plugins/b110_try_except_pass.html

Improper error handling can enable attacks and lead to unwanted behavior. Parts of the system may receive unintended input, which may result in altered control flow, arbitrary control of a resource, or arbitrary code execution.

Source
Bandit 1.6
Was this helpful?


app/smtp_connection_pool.py Line: 264 
Security
Try, Except, Pass detected. https://bandit.readthedocs.io/en/latest/plugins/b110_try_except_pass.html

Improper error handling can enable attacks and lead to unwanted behavior. Parts of the system may receive unintended input, which may result in altered control flow, arbitrary control of a resource, or arbitrary code execution.

Source
Bandit 1.6
Was this helpful?


app/dns_resolver_new.py Line: 67 
Security
Try, Except, Continue detected. https://bandit.readthedocs.io/en/latest/plugins/b112_try_except_continue.html

Improper error handling can enable attacks and lead to unwanted behavior. Parts of the system may receive unintended input, which may result in altered control flow, arbitrary control of a resource, or arbitrary code execution.

Source
Bandit 1.6
Was this helpful?


app/utils/dns_resolver.py Line: 162 
Security
Try, Except, Pass detected. https://bandit.readthedocs.io/en/latest/plugins/b110_try_except_pass.html

Improper error handling can enable attacks and lead to unwanted behavior. Parts of the system may receive unintended input, which may result in altered control flow, arbitrary control of a resource, or arbitrary code execution.

Source
Bandit 1.6
Was this helpful?


app/smtp_connection_pool.py Line: 71 
Security
Try, Except, Pass detected. https://bandit.readthedocs.io/en/latest/plugins/b110_try_except_pass.html

Improper error handling can enable attacks and lead to unwanted behavior. Parts of the system may receive unintended input, which may result in altered control flow, arbitrary control of a resource, or arbitrary code execution.

Source
Bandit 1.6
Was this helpful?


app/utils/dns_resolver.py Line: 112 
Security
Try, Except, Pass detected. https://bandit.readthedocs.io/en/latest/plugins/b110_try_except_pass.html

Improper error handling can enable attacks and lead to unwanted behavior. Parts of the system may receive unintended input, which may result in altered control flow, arbitrary control of a resource, or arbitrary code execution.

Source
Bandit 1.6
Was this helpful?


app/smtp_connection_pool.py Line: 221 
Security
Try, Except, Pass detected. https://bandit.readthedocs.io/en/latest/plugins/b110_try_except_pass.html

Improper error handling can enable attacks and lead to unwanted behavior. Parts of the system may receive unintended input, which may result in altered control flow, arbitrary control of a resource, or arbitrary code execution.

Source
Bandit 1.6
Was this helpful?


app/utils/dns_resolver.py Line: 194 
Security
Try, Except, Pass detected. https://bandit.readthedocs.io/en/latest/plugins/b110_try_except_pass.html

Improper error handling can enable attacks and lead to unwanted behavior. Parts of the system may receive unintended input, which may result in altered control flow, arbitrary control of a resource, or arbitrary code execution.

Source
Bandit 1.6
Was this helpful?


app/utils/smtp_verifier.py Line: 136 
Security
Try, Except, Pass detected. https://bandit.readthedocs.io/en/latest/plugins/b110_try_except_pass.html

Improper error handling can enable attacks and lead to unwanted behavior. Parts of the system may receive unintended input, which may result in altered control flow, arbitrary control of a resource, or arbitrary code execution.

Source
Bandit 1.6
Was this helpful?


app/utils/dns_resolver.py Line: 201 
Security
Try, Except, Pass detected. https://bandit.readthedocs.io/en/latest/plugins/b110_try_except_pass.html

Improper error handling can enable attacks and lead to unwanted behavior. Parts of the system may receive unintended input, which may result in altered control flow, arbitrary control of a resource, or arbitrary code execution.

Source


app/smtp_connection_pool.py Line: 92 
Security
Try, Except, Pass detected. https://bandit.readthedocs.io/en/latest/plugins/b110_try_except_pass.html

Improper error handling can enable attacks and lead to unwanted behavior. Parts of the system may receive unintended input, which may result in altered control flow, arbitrary control of a resource, or arbitrary code execution.

Source
Bandit 1.6
Was this helpful?


app/utils/smtp_verifier.py Line: 126 
Security
Try, Except, Pass detected. https://bandit.readthedocs.io/en/latest/plugins/b110_try_except_pass.html

Improper error handling can enable attacks and lead to unwanted behavior. Parts of the system may receive unintended input, which may result in altered control flow, arbitrary control of a resource, or arbitrary code execution.

Source
Bandit 1.6
Was this helpful?


app/utils/catch_all_detector.py Line: 86 
Security
We detected a URL in your code that uses an unencrypted ftp, telnet, http or smtp connection. These protocols are not secure and introduce the risk of exposing sensitive data to third parties. To secure your connection, we recommend using ssh instead of telnet, sftp, ftps or scp instead of ftp, https instead of http and tls over smtp (smtps). For more information, see CWE-200  and CWE-319 .

Connections that use insecure protocols transmit data in cleartext. This introduces a risk of exposing sensitive data to third parties.

Source
CodeGuru
Was this helpful?


app/api/router.py Line: 125 
Security
You have a log statement that might use unsanitized input originating from HTTP requests or AWS Lambda sources. Depending on the context, this could result in:

A log injection attack that breaks log integrity, forges log entries, or bypasses monitors that use the logs. To increase the security of your code, sanitize your inputs before logging them. Learn more 

A sensitive information leak that exposes users' credentials, private information, or identifying information to an attacker. To preserve privacy in your code, redact sensitive user information before logging it. Learn more 

User-provided inputs must be sanitized before they are logged. An attacker can use unsanitized input to break a log's integrity, forge log entries, or bypass log monitors.

Source
CodeGuru
Was this helpful?


app/smtp_validator.py Line: 70 
Security
Problem This line of code might contain a resource leak. Resource leaks can cause your system to slow down or crash.

Fix Consider closing the following resource: loop. The resource is allocated by call asyncio.get_event_loop. Execution paths that do not contain closure statements were detected. Close loop in a try-finally block to prevent the resource leak.

Allocated resources are not released properly. This can slow down or crash your system. They must be closed along all paths to prevent a resource leak.

Source
CodeGuru
Was this helpful?


app/smtp_validator.py Line: 80 
Security
We detected a URL in your code that uses an unencrypted ftp, telnet, http or smtp connection. These protocols are not secure and introduce the risk of exposing sensitive data to third parties. To secure your connection, we recommend using ssh instead of telnet, sftp, ftps or scp instead of ftp, https instead of http and tls over smtp (smtps). For more information, see CWE-200  and CWE-319 .

Connections that use insecure protocols transmit data in cleartext. This introduces a risk of exposing sensitive data to third parties.

Source
CodeGuru

