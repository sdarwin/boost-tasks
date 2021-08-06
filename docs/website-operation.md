
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

## Releases  

How do releases work?  

Divide the list of boost-tasks into multiple categories: release scripts, cron jobs, administrative.  And then, focus on only a boost release. What is an ordered list of release steps? Which web pages are updated during releases, (and from cronjobs). To a certain extent, this is a repeat of other docs.  

mirror  
release-from-artifactory	RELEASE SCRIPT  
update-doc-list  
update-explicit-failures  
update-pull-request-report  
update-super-project  
update-website-documentation  
upload-inspect-report  
upload-this-to-server		MISC ADMINISTRATIVE  
  
git-prep-beta.sh  
list-test-compilers.php  
load-release.data.php  
new-libraries.php  
refresh-pages.php  
scan-documentation.php  
set-release-status.php		RELEASE SCRIPT, major release (called from r-f-a)  
update-doc-list.php		RELEASE (called from r-f-a)  
update-pages.php		RELEASE (called from r-f-a)  
update-repo.php  

Release steps:
- At the start of a release cycle (months before publishing). Follow the steps covered here: https://github.com/boostorg/wiki/wiki/Releases%3A-Checklists  
  - manually update boost version numbers in different repositories.  
  - place new template at location such as feed/history/boost_1_60_0.qbk  
- When publishing (beta rc, beta, rc, or official). Instructions continuing on same wiki page.  
  - run release-tools/publish_release.py (supercedes download_snaphot.sh). This will "convert" a -snapshot into a release, and upload that to artifactory.  
  - run release-from-artifactory    
  - beta, release candidates: tag git. run set-release-status.php  
  
   


