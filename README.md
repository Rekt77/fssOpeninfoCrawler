# fssOpeninfoCrawler
금융감독원 검사결과제제 공시 크롤러

# install docker desktop
link[https://docs.docker.com/desktop/install/windows-install/]

# docker Mysql 설정
1. docker pull mysql
2. docker run --name fss-mysql-container -e MYSQL_ROOT_PASSWORD=test -d -p 3306:3306 mysql:latest -character-set-server=utf8 -collation-server=utf8_unicode_ci
3. docker exec -it fss-mysql-container bash
4. mysql -u root -p
5. Enter password:test