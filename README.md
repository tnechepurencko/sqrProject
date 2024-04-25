- Running on http://127.0.0.1:5000

## Endpoints

- GET: /login?uname=\<uname>&pwd=\<pwd>  
- GET: /logout?uname=\<uname>
- POST: /registration?uname=\<uname>&pwd=\<pwd>
- POST: /create_store?uname=\<uname>&sname=\<sname>
- POST: /remove_store?uname=\<uname>&sname=\<sname>
- POST: /get_stores?uname=\<uname>
- POST: /add_package?uname=\<uname>&sname=\<sname>&pname=\<pname>
- POST: /rem_package?uname=\<uname>&sname=\<sname>&pname=\<pname>
- GET: /dif_paths?uname=\<uname>&sname1=\<sname1>&sname2=\<sname2>
- GET: /dif_package?uname=\<uname>&sname1=\<sname1>&pname1=\<pname1>&sname2=\<sname2>&pname2=\<pname2>
- GET: /size_package?uname=\<uname>&sname=\<sname>&pname=\<pname>
- GET: /package_exists?uname=\<uname>&sname=\<sname>&pname=\<pname>