CREATE TABLE Bank (
    account_id int,
    bank_name varchar(20),
    username varchar(10),
    password varchar(20),
    connection_status bool,
    withdrawal_status bool,
    user_id int,

    PRIMARY KEY (account_id),
    FOREIGN KEY (user_id) REFERENCES Users(user_id)
);