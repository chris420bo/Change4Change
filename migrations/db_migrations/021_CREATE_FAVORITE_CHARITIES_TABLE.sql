CREATE TABLE Favorite_Charities (
	user_id		int,
	name		varchar(20),

	PRIMARY KEY (user_id, name),
    FOREIGN KEY (user_id) REFERENCES Users(user_id),
	FOREIGN KEY (name) REFERENCES Charity(name)
)