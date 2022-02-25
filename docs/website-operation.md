
## Boost Website Operation

Much of website's functioning can be understood by reviewing [site-tools](site-tools.md) and [boost-tasks](boost-tasks.md).  

However, a few additional features will be covered here.  

## Regression Tests

Covered in [regression-tests.md](regression-tests.md)

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
  
   


