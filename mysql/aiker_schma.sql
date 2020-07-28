USE aiker;

-- user정보
CREATE TABLE user( 
	idx int(11) not null AUTO_INCREMENT,
    ID varchar(10) not null,
    password varchar(15) not null,
    username varchar(10) not null,
    created_at datetime not null default current_timestamp on update current_timestamp,
    updated_at datetime not null default current_timestamp on update current_timestamp,
    PRIMARY KEY(idx)
);

-- docker container에 관한 정보
CREATE TABLE docker( 
	idx int(11) not null AUTO_INCREMENT,
    name varchar(100) not null,
    image varchar(100) not null,
    label_idx varchar(10) not null,
    created_at datetime not null default current_timestamp on update current_timestamp,
    updated_at datetime not null default current_timestamp on update current_timestamp,
    PRIMARY KEY(idx)
);


-- 라벨의 정보(우리가 직접 넣어야 함, 웹에서 x)
CREATE TABLE label(
	idx int (11) not null AUTO_INCREMENT,
	name varchar(100) not null,
    created_at datetime not null default current_timestamp on update current_timestamp,
    updated_at datetime not null default current_timestamp on update current_timestamp,
    PRIMARY KEY(idx)
);

-- docker container의 배포기록
CREATE TABLE docker_log(
    idx int(11) not null AUTO_INCREMENT,
    docker_idx int(11) not null,
    docker_name varchar(100) not null,
    docker_image varchar(100) not null,
    user_idx int(11) not null,
    created_at datetime not null default current_timestamp on update current_timestamp,
    PRIMARY KEY(idx)
);






