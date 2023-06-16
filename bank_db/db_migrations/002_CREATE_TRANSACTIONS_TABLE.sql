CREATE TABLE Transactions (
    transaction_id int,
    source_account_number varchar(20),
    destination_account_number varchar(20),
    description varchar(50),
    amount int,

    PRIMARY KEY (transaction_id),
    FOREIGN KEY (source_account_number) REFERENCES CheckingAccount(account_number),
    FOREIGN KEY (destination_account_number) REFERENCES CheckingAccount(account_number)
);