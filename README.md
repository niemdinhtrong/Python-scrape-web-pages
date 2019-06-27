Sử dung BeautifulSoup để thực hiện get dữ liệu HTML từ một trang web. Sau đó dữ liệu lấy về sẽ được lưu vào MySQL. Nếu khi có một comment mới thì nó sẽ được gửi về telegram để tiện theo dõi.

Chương trình thực hiện lấy các comment tại các bài viết của Nhân Hòa tại trang `https://canhme.com/`. Các thông tin lấy được bao gồm:
 * Địa chỉ của từng bài viết
 * Title của bài viết
 * Các comment trong mỗi bài viết
 * Tên của người comment
 * Thời gian của comment

## Chuẩn bị

### Một số thư viện yêu cầu:

**requests**

```
pip install requests
```

**BeautifulSoup**

```
pip install beautifulsoup4
```

**lxml**

```
pip install lxml
```

**pymsql**

```
pip install PyMySQL
```

### Tạo một database trên mysql

```
mysql -u root -p

create database DB_html;

grant all privileges on DB_html.* to 'html'@'%' identified by "html123@";

use DB_html;

create table user (iduser int not null auto_increment, username text CHARSET utf8 not null, primary key (iduser));

create table site (idsite int not null auto_increment, links text not null, tieude text CHARSET utf8, primary key (idsite));

create table comment (idcomment varchar(20) not null, idsite int not null, iduser int not null, nd_comment text CHARSET utf8, times datetime,\
primary key (idcomment), foreign key (iduser) references user (iduser), foreign key (idsite) references site (idsite));
```

## Khai báo thông tin trong code

```
# info mysql
hostname = '10.10.10.168'
username = 'html'
password = 'Admin123@'
database = 'DB_html'

# info telegram
token = "your tele-bot's token"
chat_id = "your telegram's chat_id"
```

Ta cần khai báo thông tin của mysql để tiến hành lưu dữ liệu vào thông tin về telegam để gửi được tin nhắn.

Trong đó:
 * `hostname`: địa chỉ IP của máy cài MySQL
 * `username`: user mysql sử dụng để thao tác báo DB
 * `password`: Password để login vào mysql
 * `database`: Tên database để ghi dữ liệu vào
 * `token`: Token của telegram bot
 * `chat_id`: Chat_id telegram mà bạn muốn gửi tin nhắn đến.

Để tạo telegram bot hoặc lấy chat_id của telegram của bạn tham khảo [tại đây](https://blog.cloud365.vn/monitor/zabbix4-thiet-lap-canh-bao-qua-telegram/)

