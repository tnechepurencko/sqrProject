- Running on http://127.0.0.1:5000

## Endpoints

- GET: /login?uname=\<uname>&pwd=\<pwd>  
- GET: /logout?uname=\<uname>
- POST: /registration?uname=\<uname>&pwd=\<pwd>
- POST: /create_store?uname=\<uname>&sname=\<sname>
- POST: /remove_store?uname=\<uname>&sname=\<sname>
- POST: /track_store?sname=\<sname>
- POST: /add_package?pname=\<pname>&sname=\<sname>
- POST: /rem_package?pname=\<pname>&sname=\<sname>
- GET: /dif_paths?sname1=\<sname1>&sname2=\<sname2>
- GET: /dif_package?package1=\<package1>&package2=\<package2>
- GET: /size_package?package=\<package>
- GET: /package_exists?package=\<package>