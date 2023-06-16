CREATE TABLE CheckingAccount (
    account_number varchar(20),
    account_id int,
    balance int,

    PRIMARY KEY (account_number),
    FOREIGN KEY (account_id) REFERENCES Bank(account_id)
);