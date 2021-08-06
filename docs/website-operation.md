
## Boost Website Operation

Much of website's functioning can be understood by reviewing [site-tools](site-tools.md) and [boost-tasks](boost-tasks.md).  

However, a few additional features will be covered here.  

## Regression Tests

Example: [https://www.boost.org/development/tests/develop/developer/summary.html](https://www.boost.org/development/tests/develop/developer/summary.html)  
Linked from: [https://www.boost.org/development/testing.html](https://www.boost.org/development/testing.html)  

The test result matrix is generated externally. Downloaded to the RESULTS_DIR on the website.    
```
common/code/boost_config.php:	define('RESULTS_DIR', BOOST_WEBSITE_SHARED_DIR.'/testing');
```
Notice this rewrite rule in development/.htaccess
```
RewriteRule ^tests/(.*)$ testing_results.php/$1 [L]
```

All tests/ pages are handled by testing_results.php.  
testing_results.php calls BoostArchive. Although BoostArchive could be a general class, it's only used by testing_results.php.  BoostArchive serves the zip files directly as web pages. In summary, a cronjob (not yet documented) downloads external test data, and BoostArchive serves that from boost.org.  


