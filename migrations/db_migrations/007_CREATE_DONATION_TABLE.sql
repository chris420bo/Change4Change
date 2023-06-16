CREATE TABLE Donation (
    donation_id int,
    source_wallet_id int,
    destination_charity_id int,
    amount int,

    PRIMARY KEY (donation_id),
    FOREIGN KEY (source_wallet_id) REFERENCES Wallet(wallet_id),
    FOREIGN KEY (destination_charity_id) REFERENCES Charity(user_id)
);