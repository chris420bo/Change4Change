CREATE TABLE Wallet (
    wallet_id int,
    balance int,
    user_id int,

    PRIMARY KEY (wallet_id),
    FOREIGN KEY (user_id) REFERENCES Users(user_id)
);