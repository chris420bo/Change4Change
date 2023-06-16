CREATE TABLE Users (
    user_id int,
    username varchar(10),
    password varchar(20),
    first_name varchar(10),
    last_name varchar(20),
    birthday date,
    street_address varchar(30),
    city varchar(20),
    state varchar(2),
    zipcode int,

    PRIMARY KEY (user_id)
);